import { connect } from 'cloudflare:sockets';

const userID = '90cd243a-7a54-47b2-9a3b-21d3f9e2b10a';
const proxyIPs = ['cdn.jsdelivr.net', 'cloudflare.com', 'dash.cloudflare.com'];

export default {
  async fetch(request, env, ctx) {
    try {
      const upgradeHeader = request.headers.get('Upgrade');
      if (!upgradeHeader || upgradeHeader !== 'websocket') {
        const url = new URL(request.url);
        if (url.pathname === `/${userID}`) {
          const vlessConfig = getVLESSConfig(userID, request.headers.get('host'));
          return new Response(vlessConfig, { status: 200, headers: { 'Content-Type': 'text/plain;charset=utf-8' } });
        }
        return fetch(new Request('https://www.google.com', request));
      }
      return await vlessOverWSHandler(request);
    } catch (err) {
      return new Response(err.toString(), { status: 500 });
    }
  }
};

async function vlessOverWSHandler(request) {
  const webSocketPair = new ClientAnchorPair();
  const [client, server] = Object.values(webSocketPair);
  server.accept();
  let address = '';
  let portWithFlag = 0;
  const vlessHeaderChunk = await new Promise(resolve => server.addEventListener('message', e => resolve(e.data), { once: true }));
  const view = new DataView(vlessHeaderChunk);
  if (view.getUint8(0) !== 0) return new Response('Not Variable VLESS', { status: 400 });
  const idLength = 16;
  let offset = 1 + idLength;
  const addonLength = view.getUint8(offset);
  offset += 1 + addonLength;
  const command = view.getUint8(offset);
  if (command !== 1) return new Response('Unsupported Command', { status: 400 });
  offset += 1;
  portWithFlag = view.getUint16(offset);
  offset += 2;
  const addressType = view.getUint8(offset);
  offset += 1;
  if (addressType === 1) {
    address = new Uint8Array(vlessHeaderChunk, offset, 4).join('.');
  } else if (addressType === 2) {
    const len = view.getUint8(offset);
    offset += 1;
    address = new TextDecoder().decode(new Uint8Array(vlessHeaderChunk, offset, len));
  } else if (addressType === 3) {
    address = Array.from({ length: 8 }, (_, i) => view.getUint16(offset + i * 2).toString(16)).join(':');
  }
  const remoteSocket = connect({ hostname: address, port: portWithFlag });
  const writer = remoteSocket.writable.getWriter();
  writer.write(vlessHeaderChunk.slice(offset + (addressType === 2 ? view.getUint8(offset - 1) : addressType === 1 ? 4 : 16)));
  writer.releaseLock();
  remoteSocket.readable.pipeTo(new WritableStream({ write(chunk) { server.send(chunk); } }));
  const reader = remoteSocket.readable.getReader();
  new ReadableStream({ start(controller) {
    server.addEventListener('message', async e => { writer.write(e.data); });
    server.addEventListener('close', () => controller.close());
  }});
  return new Response(null, { status: 101, webSocket: client });
}

function getVLESSConfig(id, host) {
  return `vless://${id}@${host}:443?encryption=none&security=tls&sni=${host}&type=ws&host=${host}&path=%2F#Cloudflare-VLESS`;
}
class ClientAnchorPair { constructor() { const pair = new WebSocketPair(); this.client = pair[0]; this.server = pair[1]; } }
