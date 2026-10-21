// Zero-dependency static server: clean URLs, 301 redirects, 404 page, caching.
const http = require('http'), fs = require('fs'), path = require('path'), zlib = require('zlib');
const GZ = new Map();  // in-memory gzip cache
const ROOT = __dirname, PORT = process.env.PORT || 3000;
const MIME = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'application/javascript; charset=utf-8','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png','.jpg':'image/jpeg','.xml':'application/xml','.txt':'text/plain; charset=utf-8','.json':'application/json','.ico':'image/x-icon','.woff2':'font/woff2','.mp4':'video/mp4'};
let REDIRECTS = {};  // old www.gujaratbio.com URLs -> new pages; filled from redirects.json at launch
try { REDIRECTS = JSON.parse(fs.readFileSync(path.join(__dirname, 'redirects.json'), 'utf8')); } catch (e) {}
function redirectFor(p) {
  if (REDIRECTS[p]) return REDIRECTS[p];
  const lang = p.match(/^\/(gu|hi)(\/.*)?$/);           // old Gujarati/Hindi copies
  if (lang && Object.keys(REDIRECTS).length) { const rest = lang[2] || '/'; return REDIRECTS[rest] || '/'; }
  return null;
}
function send(res, code, file, extra, req) {
  if (path.extname(file) === '.mp4') {            // videos: stream with byte ranges (needed by iPhone/Safari)
    return fs.stat(file, (e, st) => {
      if (e) { res.writeHead(404); return res.end(); }
      const h = {'Content-Type': 'video/mp4', 'Accept-Ranges': 'bytes', 'Cache-Control': 'public, max-age=31536000, immutable'};
      const m = /bytes=(\d*)-(\d*)/.exec((req && req.headers.range) || '');
      if (m) {
        let start = m[1] ? parseInt(m[1], 10) : 0, end = m[2] ? parseInt(m[2], 10) : st.size - 1;
        if (!m[1] && m[2]) { start = st.size - parseInt(m[2], 10); end = st.size - 1; }
        if (start >= st.size || end >= st.size || start > end) { res.writeHead(416, {'Content-Range': 'bytes */' + st.size}); return res.end(); }
        res.writeHead(206, Object.assign(h, {'Content-Range': `bytes ${start}-${end}/${st.size}`, 'Content-Length': end - start + 1}));
        return fs.createReadStream(file, {start, end}).pipe(res);
      }
      res.writeHead(200, Object.assign(h, {'Content-Length': st.size}));
      fs.createReadStream(file).pipe(res);
    });
  }
  fs.readFile(file, (e, buf) => {
    if (e) { res.writeHead(500); return res.end('Server error'); }
    const ext = path.extname(file);
    const h = Object.assign({'Content-Type': MIME[ext] || 'application/octet-stream', 'X-Content-Type-Options': 'nosniff', 'Vary': 'Accept-Encoding'}, extra || {});
    h['Cache-Control'] = ext === '.html' ? 'public, max-age=300' : (ext === '.css' || ext === '.js') ? 'public, max-age=31536000, immutable' : 'public, max-age=31536000, immutable';
    const textual = /^(\.html|\.css|\.js|\.svg|\.xml|\.txt|\.json)$/.test(ext);
    if (textual && req && /\bgzip\b/.test(req.headers['accept-encoding'] || '')) {
      let z = GZ.get(file);
      if (!z || z.len !== buf.length) { z = {len: buf.length, data: zlib.gzipSync(buf, {level: 9})}; GZ.set(file, z); }
      h['Content-Encoding'] = 'gzip'; res.writeHead(code, h); return res.end(z.data);
    }
    res.writeHead(code, h); res.end(buf);
  });
}
let HOST = {};  // live build only: {"canonical": "...", "redirect_hosts": [...]}
try { HOST = JSON.parse(fs.readFileSync(path.join(__dirname, 'host.json'), 'utf8')); } catch (e) {}
http.createServer((req, res) => {
  const host = (req.headers.host || '').toLowerCase().split(':')[0];
  if (HOST.canonical && (HOST.redirect_hosts || []).includes(host)) { res.writeHead(301, {Location: 'https://' + HOST.canonical + req.url}); return res.end(); }
  let p; try { p = decodeURIComponent(new URL(req.url, 'http://x').pathname); } catch (e) { res.writeHead(400); return res.end('Bad request'); }
  if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
  const to = redirectFor(p); if (to && to !== p) { res.writeHead(301, {Location: to}); return res.end(); }
  const full = path.normalize(path.join(ROOT, p));
  if (!full.startsWith(ROOT) || /(^|\/)\.|server\.js$|package\.json$|\.py$|\.md$|\.gs$|^\/(redirects|host|redirects-at-launch|content_articles)\.json$|\.csv$/.test(p)) return send(res, 404, path.join(ROOT, '404.html'), null, req);
  fs.stat(full, (e, st) => {
    if (!e && st.isFile()) return send(res, 200, full, null, req);
    const idx = path.join(full, 'index.html');
    fs.stat(idx, (e2, st2) => (!e2 && st2.isFile()) ? send(res, 200, idx, null, req) : send(res, 404, path.join(ROOT, '404.html'), null, req));
  });
}).listen(PORT, () => console.log('Listening on ' + PORT));
