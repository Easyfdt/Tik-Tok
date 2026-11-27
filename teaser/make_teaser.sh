#!/bin/bash
# Teaser (~10 s) aus einer fertigen Folge: make_teaser.sh <folge.mp4> <ausgabe.mp4> <Serie> <Zeile2> "start dauer" ["start dauer" ...]
# Schnitte aus timeline.json (subs t0/t1) wählen: Spannung aufbauen, vor der Auflösung abbrechen. Endkarte 2 s.
set -e
IN=$1; OUT=$2; SERIE=$3; LINE=$4; shift 4
T=$(mktemp -d); FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf; HERE=$(cd $(dirname $0)/.. && pwd)
i=0; L=$T/l.txt; : > $L
for seg in "$@"; do set -- $seg; i=$((i+1)); E=$(echo "$2-0.12"|bc)
  ffmpeg -v error -y -ss $1 -t $2 -i "$IN" -vf "fade=in:st=0:d=0.12,fade=out:st=$E:d=0.12" -af "afade=in:d=0.05,afade=out:st=$(echo "$2-0.1"|bc):d=0.1" -c:v libx264 -crf 18 -pix_fmt yuv420p -r 24 -c:a aac -ar 48000 -ac 2 $T/c$i.mp4
  echo "file '$T/c$i.mp4'" >> $L; done
ffmpeg -v error -y -f lavfi -i color=c=black:s=1080x1920:r=24:d=2 -f lavfi -i anullsrc=r=48000:cl=stereo -t 2 -vf "drawtext=fontfile=$FONT:text='$SERIE':fontcolor=white:fontsize=100:x=(w-tw)/2:y=820,drawtext=fontfile=$FONT:text='$LINE':fontcolor=0xFFC400:fontsize=64:x=(w-tw)/2:y=960,fade=in:st=0:d=0.25" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -shortest $T/end.mp4
echo "file '$T/end.mp4'" >> $L
ffmpeg -v error -y -f concat -safe 0 -i $L -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -ar 48000 $T/raw.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $T/raw.mp4); H=$(echo "$D-2"|bc)
ffmpeg -v error -y -i $T/raw.mp4 -i $HERE/echo/assets/sfx/hit.mp3 -filter_complex "[1:a]adelay=$(echo "$H*1000/1"|bc)|$(echo "$H*1000/1"|bc),volume=0.7[h];[0:a][h]amix=inputs=2:normalize=0:duration=first[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
rm -rf $T; echo "$OUT $(printf %.1f $D)s"
