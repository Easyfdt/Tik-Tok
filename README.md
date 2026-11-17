# Mystery Minute – 3D-Kurzfilme für TikTok (Deutsch)

Prozedural erzeugte 3D-Kurzvideos (Three.js) im TikTok-Format **1080×1920, 30 fps**,
mit deutschen Untertiteln und synthetisiertem Ambient-Sound.

## Video rendern

```bash
npm install
node render.js schwarzes-loch --preview   # 4 Vorschaubilder in out/
node render.js schwarzes-loch             # fertiges Video: out/schwarzes-loch.mp4
```

Benötigt: Node 18+, `ffmpeg`, Playwright mit Chromium.

## Neue Folge anlegen

1. `scenes/<name>.js` anlegen – exportiert `duration`, `captions`, `setup(ctx)` und `update(t, ctx)`.
2. Optional `scenes/<name>.audio.txt` – ffmpeg-`aevalsrc`-Ausdruck für den Sound.
3. `node render.js <name>`

Untertitel liegen bei 72 % Bildhöhe – außerhalb der TikTok-Bedienelemente unten und rechts.

## Folgen

| # | Titel | Status |
|---|-------|--------|
| 1 | Was passiert, wenn du in ein Schwarzes Loch fällst? | ✅ `schwarzes-loch` |
| 2 | Wie groß ist die Sonne wirklich? (Größenvergleich) | Idee |
| 3 | Was wäre, wenn der Mond verschwindet? | Idee |
| 4 | Ein Neutronenstern – ein Teelöffel wiegt 1 Mrd. Tonnen | Idee |
| 5 | Wie tief ist der Ozean wirklich? (Tauchfahrt in 3D) | Idee |

## Beitragstext (Vorschlag Folge 1)

> Was passiert, wenn du in ein Schwarzes Loch fällst? 🕳️✨ Bis zum Ende schauen!
> #schwarzesloch #weltall #wissen #3d #lernenmittiktok #fyp #mysteryminute
