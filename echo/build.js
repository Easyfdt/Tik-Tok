// ECHO – baut eine komplette Folge: Stimmen (Piper TTS) -> Timeline -> 3D-Render -> Sounddesign -> MP4
// Nutzung: node echo/build.js 1            (Folge 1)
//          node echo/build.js 1 --preview  (nur Stimmen + Vorschaubilder)
const fs = require('fs'), path = require('path'), http = require('http'), os = require('os');
const { execFileSync, spawn } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const nr = parseInt(process.argv[2] || '1', 10);
const preview = process.argv.includes('--preview');
const id = String(nr).padStart(2, '0');
const ep = JSON.parse(fs.readFileSync(path.join(__dirname, 'folgen', `${id}.json`), 'utf8'));
const FPS = 24;
const WORK = path.join(ROOT, 'out', `echo-${id}`); fs.mkdirSync(WORK, { recursive: true });
const sh = (cmd, args, opt = {}) => execFileSync(cmd, args, { stdio: ['pipe', 'pipe', 'pipe'], maxBuffer: 1 << 26, ...opt });

// ---------- 1. Stimmen ----------
const VOICE_DIR = path.join(os.homedir(), '.cache', 'echo-voices');
const VOICES = { erz: 'de-thorsten-low', uhrmacher: 'de-thorsten-low', lena: 'de-kerstin-low', mats: 'de-pavoque-low' };
function ensureVoices() {
  try { sh('python3', ['-c', 'import piper']); } catch { sh('pip', ['install', '-q', 'piper-tts']); }
  for (const v of new Set(Object.values(VOICES))) {
    const onnx = path.join(VOICE_DIR, v, `${v}.onnx`);
    if (fs.existsSync(onnx)) continue;
    fs.mkdirSync(path.join(VOICE_DIR, v), { recursive: true });
    const tgz = path.join(VOICE_DIR, `${v}.tgz`);
    sh('curl', ['-sSfL', '-o', tgz, `https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-${v}.tar.gz`]);
    sh('tar', ['xzf', tgz, '-C', path.join(VOICE_DIR, v)]); fs.unlinkSync(tgz);
  }
}
// Stimmfarbe pro Figur (ffmpeg-Filter, Ausgabe 44,1 kHz Stereo)
const VOICE_FX = {
  erz: 'aresample=44100,highpass=f=70,equalizer=f=180:t=q:w=1:g=3,aecho=0.8:0.6:45:0.12,volume=1.25',
  lena: 'aresample=44100,highpass=f=120,equalizer=f=3000:t=q:w=1:g=2,aecho=0.8:0.5:30:0.1,volume=1.2',
  mats: 'aresample=44100,highpass=f=90,aecho=0.8:0.5:30:0.1,volume=1.2',
  uhrmacher: 'asetrate=16000*0.8,aresample=44100,atempo=1.12,lowpass=f=5000,aecho=0.8:0.85:70|140:0.35|0.22,volume=1.6',
  radio: 'aresample=44100,highpass=f=400,lowpass=f=3000,acrusher=bits=10:mix=0.35,aecho=0.6:0.4:20:0.2,volume=1.6',
};
const SPEED = { erz: 1.12, lena: 1.0, mats: 0.98, uhrmacher: 1.1 };
function dur(f) { return parseFloat(sh('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString()); }
function voiceLine(line, k) {
  const raw = path.join(WORK, `v${k}.raw.wav`), fin = path.join(WORK, `v${k}.wav`);
  const v = VOICES[line.who]; const model = path.join(VOICE_DIR, v, `${v}.onnx`);
  const text = line.say || line.text; // "say" = Aussprache-Variante (z.B. Zahlen ausgeschrieben)
  sh('python3', ['-m', 'piper', '-m', model, '-f', raw, '--length-scale', String(SPEED[line.who] || 1), '--noise-scale', '0.6', '--sentence-silence', '0.25'], { input: text });
  const fx = line.radio ? VOICE_FX.radio : VOICE_FX[line.who];
  sh('ffmpeg', ['-y', '-v', 'error', '-i', raw, '-af', `${fx},silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,apad=pad_dur=0.05`, '-ac', '2', fin]);
  return { file: fin, d: dur(fin) };
}

// ---------- 2. Timeline ----------
function buildTimeline() {
  let t = 0, k = 0; const shots = [], subs = [], voices = [];
  for (const s of ep.shots) {
    const t0 = t; let cur = t + (s.pre ?? 0.45);
    for (const line of s.lines || []) {
      const v = voiceLine(line, k++);
      voices.push({ file: v.file, at: cur, vol: line.vol ?? 1 });
      subs.push({ t0: cur, t1: cur + v.d + 0.15, who: line.radio ? 'lena' : line.who, text: line.text });
      cur += v.d + (line.gap ?? 0.3);
    }
    const t1 = Math.max(cur + (s.post ?? 0.5), t0 + (s.min ?? 2.2));
    shots.push({ ...s, lines: undefined, t0, t1 });
    t = t1;
  }
  return { nr, titel: ep.titel, fps: FPS, duration: t, shots, subs, voices };
}

// ---------- 3. Sounddesign ----------
const SFX = {
  wind: d => `anoisesrc=c=brown:a=0.5:d=${d},lowpass=f=500,tremolo=f=0.2:d=0.6,volume=0.55`,
  rain: d => `anoisesrc=c=pink:a=0.35:d=${d},highpass=f=800,lowpass=f=7000,volume=0.45`,
  radio: d => `anoisesrc=c=white:a=0.25:d=${d},bandpass=f=2500:w=1800,tremolo=f=7:d=0.7,volume=0.22`,
  clock: d => `aevalsrc='0.45*sin(2*PI*2100*t)*exp(-90*mod(t\\,1))+0.3*sin(2*PI*1400*t)*exp(-90*mod(t+0.5\\,1))':d=${d}:s=44100`,
  heartbeat: d => `aevalsrc='0.9*sin(2*PI*48*t)*(exp(-22*mod(t\\,0.85))+0.7*exp(-22*mod(t+0.6\\,0.85)))':d=${d}:s=44100,lowpass=f=160,volume=1.3`,
  drip: d => `aevalsrc='0.35*sin(2*PI*(900+700*exp(-30*mod(t\\,1.7)))*t)*exp(-25*mod(t\\,1.7))':d=${d}:s=44100,aecho=0.8:0.8:120|260:0.4|0.25`,
  hum: d => `aevalsrc='0.18*sin(2*PI*55*t)+0.08*sin(2*PI*110*t)+0.06*sin(2*PI*165*t)*sin(2*PI*0.4*t)':d=${d}:s=44100`,
  steps: d => `anoisesrc=c=brown:a=0.9:d=${d},lowpass=f=350,volume='exp(-28*mod(t\\,0.55))':eval=frame,volume=1.2`,
  crowd: d => `anoisesrc=c=pink:a=0.2:d=${d},bandpass=f=600:w=500,tremolo=f=1.3:d=0.4,volume=0.4`,
  // Einzel-Effekte (am Shot-Anfang, "riser" endet am Shot-Ende)
  thunder: () => `anoisesrc=c=brown:a=1:d=4.5,lowpass=f=170,volume='min(1\\,t*10)*exp(-1.0*t)':eval=frame,volume=2.4`,
  hit: () => `aevalsrc='(sin(2*PI*42*t)+0.7*sin(2*PI*84*t)+0.3*sin(2*PI*63*t))*exp(-1.8*t)':d=3:s=44100,volume=0.9`,
  whoosh: () => `anoisesrc=c=pink:a=0.7:d=1.1,bandpass=f=1200:w=900,volume='sin(PI*t/1.1)':eval=frame,volume=0.8`,
  static: () => `anoisesrc=c=white:a=0.6:d=0.7,highpass=f=1500,volume='exp(-4*t)':eval=frame,volume=0.7`,
  riser: d => `aevalsrc='0.3*sin(2*PI*(80*t+60*t*t))*(t/${d})*(t/${d})+0.15*sin(2*PI*(160*t+120*t*t))*(t/${d})':d=${d}:s=44100`,
};
const ONE_SHOT = new Set(['thunder', 'hit', 'whoosh', 'static', 'riser']);
// Musik-Teppich: dunkler Drone, der in der zweiten Hälfte anzieht
const musicBed = (D) => `aevalsrc='0.16*sin(2*PI*36.7*t)*(0.7+0.3*sin(2*PI*0.08*t))+0.1*sin(2*PI*55*t+2*sin(2*PI*0.11*t))+0.05*sin(2*PI*82.4*t)*(0.5+0.5*sin(2*PI*0.05*t))+0.04*sin(2*PI*110*t)*min(1\\,t/${D})|0.16*sin(2*PI*36.9*t)*(0.7+0.3*sin(2*PI*0.07*t))+0.1*sin(2*PI*55.3*t+2*sin(2*PI*0.1*t))+0.05*sin(2*PI*82.9*t)*(0.5+0.5*sin(2*PI*0.06*t))+0.04*sin(2*PI*110.4*t)*min(1\\,t/${D})':d=${D}:s=44100:c=stereo`;

function mixAudio(tl) {
  const inputs = [], chains = [], labels = []; let n = 0;
  const D = tl.duration.toFixed(2);
  chains.push(`${musicBed(D)},volume=0.9[m]`); labels.push('[m]');
  for (const s of tl.shots) {
    const d = (s.t1 - s.t0).toFixed(2);
    for (const name of s.sfx || []) {
      if (!SFX[name]) continue;
      const one = ONE_SHOT.has(name);
      const rd = Math.min(4, s.t1 - s.t0).toFixed(2);
      const at = name === 'riser' ? s.t1 - rd : s.t0;
      const src = name === 'riser' ? SFX.riser(rd) : SFX[name](d);
      const L = `s${n++}`;
      chains.push(`${src},aformat=channel_layouts=stereo:sample_rates=44100${one ? '' : `,afade=in:d=0.4,afade=out:st=${Math.max(0, d - 0.4)}:d=0.4`},adelay=${Math.round(at * 1000)}:all=1[${L}]`);
      labels.push(`[${L}]`);
    }
  }
  tl.voices.forEach((v, i) => {
    inputs.push('-i', v.file);
    const L = `v${i}`; chains.push(`[${i}:a]volume=${v.vol},adelay=${Math.round(v.at * 1000)}:all=1[${L}]`); labels.push(`[${L}]`);
  });
  // Stimmen duckt die Effekte leicht: Effekte gesamt leiser, Stimme vorne
  const fx = labels.filter(l => !l.startsWith('[v')), vo = labels.filter(l => l.startsWith('[v'));
  chains.push(`${fx.join('')}amix=inputs=${fx.length}:normalize=0,volume=0.75[fxm]`);
  chains.push(`${vo.join('')}amix=inputs=${vo.length}:normalize=0[vom]`);
  chains.push(`[fxm][vom]amix=inputs=2:normalize=0,atrim=0:${D},afade=out:st=${(tl.duration - 1.2).toFixed(2)}:d=1.2,loudnorm=I=-14:TP=-1.5:LRA=11[a]`);
  const script = path.join(WORK, 'mix.txt'); fs.writeFileSync(script, chains.join(';\n'));
  const outA = path.join(WORK, 'audio.wav');
  sh('ffmpeg', ['-y', '-v', 'error', ...inputs, '-filter_complex_script', script, '-map', '[a]', '-ar', '44100', outA]);
  return outA;
}

// ---------- 4. Rendern ----------
async function render(tl, audio) {
  const { chromium } = require('playwright');
  fs.writeFileSync(path.join(WORK, 'timeline.json'), JSON.stringify(tl));
  const server = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    if (!p.startsWith(ROOT) || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': p.endsWith('.js') ? 'text/javascript' : p.endsWith('.html') ? 'text/html' : 'application/json' });
    fs.createReadStream(p).pipe(res);
  });
  await new Promise(r => server.listen(0, r));
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => console.error('[page error]', e));
  await page.goto(`http://localhost:${server.address().port}/echo/engine.html?tl=/out/echo-${id}/timeline.json`);
  await page.waitForFunction('window.ready === true', null, { timeout: 120000 });
  const frames = Math.round(tl.duration * FPS);
  if (preview) {
    tl.shots.forEach((s, i) => { s._f = Math.round(((s.t0 + s.t1) / 2) * FPS); });
    for (const [i, s] of tl.shots.entries()) {
      const b64 = await page.evaluate(f => window.renderFrame(f), s._f);
      fs.writeFileSync(path.join(WORK, `shot${String(i).padStart(2, '0')}.jpg`), Buffer.from(b64, 'base64'));
    }
  } else {
    const outFile = path.join(ROOT, 'out', `echo-folge-${id}.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', audio,
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '21', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', outFile], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let i = 0; i < frames; i++) {
      const b64 = await page.evaluate(f => window.renderFrame(f), i);
      if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 120 === 0) console.log(`Frame ${i}/${frames} (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    console.log('FERTIG', outFile);
  }
  await browser.close(); server.close();
}

(async () => {
  ensureVoices();
  const tl = buildTimeline();
  console.log(`Folge ${nr} „${ep.titel}“: ${tl.duration.toFixed(1)} s, ${tl.shots.length} Shots`);
  const audio = mixAudio(tl);
  await render(tl, audio);
})().catch(e => { console.error(e.stderr ? e.stderr.toString() : e); process.exit(1); });
