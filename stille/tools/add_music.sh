#!/bin/bash
# Legt die Serienmusik leise unter ein fertiges Video (nur Tonspur neu, Video wird kopiert).
# Nutzung: add_music.sh <in.mp4> <out.mp4> [musik.mp3] [musik_db]
# Musik ~20 dB unter der Stimme, Ducking per sidechaincompress, Fade-in/out.
set -e
IN="$1"; OUT="$2"; MUS="${3:-$(dirname "$0")/../assets/music/stille-theme.mp3}"; DB="${4:--20}"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
FO=$(python3 -c "print(max(0,$D-1.5))")
ffmpeg -y -v error -i "$IN" -stream_loop -1 -i "$MUS" -filter_complex \
"[0:a]aformat=sample_rates=44100:channel_layouts=stereo,asplit=2[voice][sc];\
[1:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=${DB}dB,atrim=0:$D,afade=t=in:d=1.5,afade=t=out:st=$FO:d=1.5[mus];\
[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400:makeup=1[duck];\
[voice][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart -t "$D" "$OUT"
