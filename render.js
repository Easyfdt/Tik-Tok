// Rendert eine 3D-Szene (scenes/<name>.js) als TikTok-Video (1080x1920, 30fps) nach out/<name>.mp4
// Nutzung: node render.js <szene> [--preview]
const http = require('http'), fs = require('fs'), path = require('path');
const { spawn } = require('child_process');
const { chromium } = require('playwright');

const name = process.argv[2] || 'schwarzes-loch';
const preview = process.argv.includes('--preview');
const root = __dirname;
const types = { '.js': 'text/javascript', '.html': 'text/html', '.json': 'application/json' };

const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(root) || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});

(async () => {
  await new Promise(r => server.listen(0, r));
  const port = server.address().port;
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('console', m => console.log('[page]', m.text()));
  page.on('pageerror', e => console.error('[page error]', e));
  await page.goto(`http://localhost:${port}/render.html?scene=${name}`);
  await page.waitForFunction('window.ready === true', null, { timeout: 60000 });
  const { fps, duration } = await page.evaluate('window.meta');
  fs.mkdirSync(path.join(root, 'out'), { recursive: true });

  if (preview) {
    for (const t of [1, 6, 12, 18]) {
      const b64 = await page.evaluate(i => window.renderFrame(i), Math.round(t * fps));
      fs.writeFileSync(path.join(root, 'out', `${name}-${t}s.jpg`), Buffer.from(b64, 'base64'));
    }
    console.log('Vorschaubilder in out/');
  } else {
    const frames = Math.round(duration * fps);
    const audio = path.join(root, 'scenes', `${name}.audio.txt`);
    const outFile = path.join(root, 'out', `${name}.mp4`);
    const args = ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-'];
    // Atmosphärischer Sound-Teppich, mit ffmpeg synthetisiert
    const expr = fs.existsSync(audio) ? fs.readFileSync(audio, 'utf8').trim() : null;
    if (expr) args.push('-f', 'lavfi', '-t', String(duration), '-i', `aevalsrc=${expr}:s=44100:c=stereo`);
    args.push('-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart');
    if (expr) args.push('-af', `afade=in:d=1,afade=out:st=${duration - 1.5}:d=1.5,volume=0.8`, '-c:a', 'aac', '-b:a', '192k', '-shortest');
    args.push(outFile);
    const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'ignore', 'inherit'] });
    const t0 = Date.now();
    for (let i = 0; i < frames; i++) {
      const b64 = await page.evaluate(i => window.renderFrame(i), i);
      if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 30 === 0) process.stdout.write(`\rFrame ${i}/${frames}  (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    console.log(`\nFertig: ${outFile}`);
  }
  await browser.close(); server.close();
})();
