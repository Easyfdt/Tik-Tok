# ECHO – Serienbibel (Staffel 1, 15 Folgen)

Eigenständige Mystery-Serie im Stil düsterer deutscher Zeitreise-Thriller.
**Keine** Namen, Orte, Figuren oder Handlungsdetails aus bestehenden Serien übernehmen.

## Welt
- **Grauwald**: Kleinstadt im Wald. Jede Nacht um **23:13** bleiben alle Uhren für eine Minute stehen – „die Stunde, die fehlt“.
- **Der alte Stollen**: stillgelegtes Bergwerk am Waldrand. Um 23:13 leuchtet er blau und öffnet einen Weg **37 Jahre** in die Vergangenheit/Zukunft (2026 ↔ 1989 ↔ 1952).
- **Das Funkgerät**: gehörte Mats' Großvater, empfängt Stimmen aus anderen Zeiten.

## Figuren (genau drei)
| Figur | Stimme (ElevenLabs) | Look | Kern |
|---|---|---|---|
| **Lena Berger (17)** | Rika Sturm `Jpm0FNvrnzdW3k4rnWVH` | rote Jacke, roter Schal, Pferdeschwanz | mutig, stur; steckt 1989 fest |
| **Mats Keller (17)** | Daniel `5rcNUqWNX3O3CWtoa74o` | grüne Jacke, Taschenlampe | loyal, ängstlich, gibt nie auf |
| **Der Uhrmacher** | Jones Thriller `6t8LORFSPwBBPJsBLSYZ` | schwarzer Mantel, Hut, Ziffernblatt statt Gesicht | weiß alles, spricht in Rätseln |
| Erzähler | Vincent Crowe `18X2yBovneA0q06wd8E9` | – | ruhig, unheimlich |

**Großes Geheimnis (erst in Folge 14/15 enthüllen):** Der Uhrmacher ist der alte Mats aus der Zukunft, der seit Jahrzehnten versucht, Lena zu retten – und dabei die Schleife selbst erzeugt.

## Folgenplan
1. **Die Stunde, die fehlt** – Lenas Stimme im kaputten Funkgerät; Mats findet ihren trockenen Schal; Lena erwacht 1989. *Cliff: An Mats' Haus steht ein anderer Name.*
2. **Keller** – Lena 1989: Auf dem Klingelschild steht „Keller“ – Mats' Großvater als Jugendlicher. Mats findet im Funkgerät ein Foto von 1989 – mit Lena darauf. *Cliff: Auf dem Foto steht der Uhrmacher hinter ihr.*
3. **Rauschen** – Mats und Lena sprechen erstmals live über das Funkgerät; jede Minute 23:13 öffnet die Verbindung. *Cliff: Lena: „Hier ist jemand, der genauso aussieht wie du.“*
4. **Der Junge von 1989** – Lena trifft den jungen Großvater, er hält sie für eine Spionin. Mats findet dessen Tagebuch. *Cliff: Letzter Eintrag: „Heute Nacht verschwindet das Mädchen mit dem roten Schal.“*
5. **Die Regel** – Der Uhrmacher erklärt Mats die Regel: Wer durch den Stollen geht, kommt nur mit, wenn jemand anderes zurückbleibt. *Cliff: „Bist du bereit, zu bleiben?“*
6. **Zweimal Lena** – Mats geht durch den Stollen – landet aber 1952. *Cliff: Ein kleines Mädchen mit rotem Schal sagt seinen Namen.*
7. **1952** – Das Bergwerk ist noch in Betrieb; ein Unglück steht bevor. Mats erkennt: das Unglück erzeugte den Riss in der Zeit. *Cliff: Der Uhrmacher – ohne Hut – arbeitet als Bergmann.*
8. **Zahnräder** – Mats findet die Werkstatt des Uhrmachers; jede Uhr zeigt 23:13, eine Uhr trägt Lenas Namen. *Cliff: Die Uhr beginnt rückwärts zu laufen.*
9. **Die andere Seite** – Lena entdeckt 1989, dass sie die Verbindung selbst erzeugt – sie hat 1989 das Funkgerät gebaut. *Cliff: Die Bauanleitung ist in Mats' Handschrift.*
10. **Stille** – Um 23:13 bleibt die Verbindung aus. Mats in 1952 gefangen, Lena allein 1989. *Cliff: Ein Funkspruch aus 2063: „Hier spricht Mats.“*
11. **2063** – Der Zukunfts-Mats warnt: Jede Rettung macht es schlimmer. *Cliff: „Ich habe es 312 Mal versucht.“*
12. **Das Unglück** – Mats versucht in 1952, das Bergwerksunglück zu verhindern. *Cliff: Er löst es selbst aus.*
13. **Rückweg** – Mats und Lena treffen sich endlich – im Stollen zwischen den Zeiten. Nur einer kann zurück. *Cliff: Der Uhrmacher nimmt seinen Hut ab.*
14. **Das Gesicht** – Enthüllung: Der Uhrmacher ist der alte Mats. *Cliff: „Diesmal machen wir es anders, Lena.“*
15. **23:14** – Lena bleibt freiwillig zurück, die Schleife bricht; zum ersten Mal schlägt die Uhr 23:14. Mats wacht auf – das Funkgerät rauscht. *Staffel-Cliff: „Mats … hier ist Lena. Es ist 2089.“*

## Regeln für jedes Drehbuch (`folgen/NN.json`)
- **Länge 80–95 s** (Creator-Programm: über 1 Minute). Ca. 170–210 Wörter Text, 14–17 Shots.
- **Shot 1 = Cold Open-Hook** in den ersten 2 Sekunden (Frage, Schock, Stimme im Dunkeln). Kein langsamer Einstieg.
- **Shot 2 = Titelkarte** `"title": "ECHO", "sub": "FOLGE N · TITEL"` mit `hit` + `clock`.
- **Alle 5–8 Sekunden ein neuer Haken**: neue Frage, Entdeckung, Gefahr, Zeitstempel. Jeder Shot endet offen.
- **Letzter Shot = schwarze Endkarte** `"black": true, "sub": "FOLGE N+1 – MORGEN"` + Frage an die Zuschauer.
- Kurze Sätze. Zahlen für die Stimme in `say` ausschreiben. Stimmen-Modell: **eleven_v3**. `tone` = ElevenLabs-Regieanweisung auf Englisch in eckigen Klammern.
- Sets: `wald`, `hoehle`, `stollen`, `uhrturm`, `zimmer`, `strasse1989`, `leere`. Kameras: `dolly`, `push`, `close`, `extreme`, `orbit`, `crane`, `high`, `low`, `pov`, `wide`.
- FX: `rain`, `fog`, `flicker`, `dark`, `glitch`, `glitch-end`, `lightning`, `dream`. SFX: `wind`, `rain`, `radio`, `clock`, `heartbeat`, `drip`, `hum`, `steps`, `crowd`, `thunder`, `hit`, `whoosh`, `static`, `riser`.
- Figuren: `{ "who": "lena|mats|uhrmacher", "pos": [x, z], "move": [dx, dz], "face": Grad, "pose": "stand|walk|run|look|reach|fear|down" }`.
- Vorlage: `folgen/01.json`.

## Nach Staffel 1
Neue Staffel = neues Thema (z. B. „ECHO – Staffel 2: 2089“ oder eine neue Mini-Serie), wieder 15 Folgen, gleiche Regeln.
