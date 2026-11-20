# Graph Report - echo  (2026-11-20)

## Corpus Check
- Corpus is ~20,241 words - fits in a single context window. You may not need a graph.

## Summary
- 102 nodes · 181 edges · 7 communities (6 shown, 1 thin omitted)
- Extraction: 87% EXTRACTED · 12% INFERRED · 2% AMBIGUOUS · INFERRED: 21 edges (avg confidence: 0.93)
- Token cost: 94,562 input · 0 output

## Community Hubs (Navigation)
- Build-Pipeline Setup
- Uhrmacher und Stollen-Regel
- Folge 1 Sprechtexte (alt)
- Stimmen und Audio-Mix
- Drehbuch-Regeln
- Keller-Familie Folgen 2-4
- Rendern mit Playwright

## God Nodes (most connected - your core abstractions)
1. `ECHO (Mystery-Serie, Staffel 1)` - 24 edges
2. `ECHO Folge 1: Sprechtexte` - 20 edges
3. `sh()` - 10 edges
4. `Der Uhrmacher` - 10 edges
5. `Regeln fuer jedes Drehbuch` - 9 edges
6. `Lena Berger` - 8 edges
7. `Mats Keller` - 8 edges
8. `Der alte Stollen` - 6 edges
9. `Das Funkgeraet` - 6 edges
10. `Folge 1: Die Stunde, die fehlt` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Stimme Rika Sturm (Lena)` --semantically_similar_to--> `Stimme Maya (ElevenLabs)`  [AMBIGUOUS] [semantically similar]
  folgen/01-texte.md → SERIE.md
- `Stimme Daniel - Ruhig und Freundlich (Mats)` --semantically_similar_to--> `Stimme Matthew (ElevenLabs)`  [AMBIGUOUS] [semantically similar]
  folgen/01-texte.md → SERIE.md
- `Stimme Christian Plasa (Erzaehler)` --semantically_similar_to--> `Stimme New MM (ElevenLabs)`  [AMBIGUOUS] [semantically similar]
  folgen/01-texte.md → SERIE.md
- `Stimme Jones - Thriller Audiobook Narrator (Uhrmacher)` --semantically_similar_to--> `Stimme Jones Thriller (ElevenLabs)`  [INFERRED] [semantically similar]
  folgen/01-texte.md → SERIE.md
- `ECHO Folge 1: Sprechtexte` --conceptually_related_to--> `Vorlage folgen/01.json`  [INFERRED]
  folgen/01-texte.md → SERIE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Stimmenbesetzung Folge 1** — echo_folgen_01_texte_stimme_christian_plasa, echo_folgen_01_texte_stimme_rika_sturm, echo_folgen_01_texte_stimme_daniel, echo_folgen_01_texte_stimme_jones_thriller [EXTRACTED 1.00]
- **ECHO Hauptfiguren** — echo_serie_lena_berger, echo_serie_mats_keller, echo_serie_der_uhrmacher [EXTRACTED 1.00]
- **Zeitreise-Mechanik von Grauwald** — echo_serie_die_stunde_die_fehlt, echo_serie_der_alte_stollen, echo_serie_das_funkgeraet, echo_serie_zeitsprung_37_jahre, echo_serie_zeitschleife [INFERRED 0.85]

## Communities (7 total, 1 thin omitted)

### Community 0 - "Build-Pipeline Setup"
Cohesion: 0.06
Nodes (25): clipArg, EL_CACHE, EL_FX, EL_VOICES, ep, { execFileSync, spawn }, fs, http (+17 more)

### Community 1 - "Uhrmacher und Stollen-Regel"
Cohesion: 0.17
Nodes (20): "Die Frage ist: wann", Stimme Jones - Thriller Audiobook Narrator (Uhrmacher), Bergwerksunglueck 1952, Der alte Stollen, Der Uhrmacher, ECHO (Mystery-Serie, Staffel 1), Folge 5: Die Regel, Folge 6: Zweimal Lena (+12 more)

### Community 2 - "Folge 1 Sprechtexte (alt)"
Cohesion: 0.18
Nodes (17): Aufnahmen 01.mp3-25.mp3, ECHO Folge 1: Sprechtexte, Stimme Christian Plasa (Erzaehler), Stimme Daniel - Ruhig und Freundlich (Mats), Stimme Rika Sturm (Lena), Lenas trockener Schal, Das Funkgeraet, Erzaehler (+9 more)

### Community 3 - "Stimmen und Audio-Mix"
Cohesion: 0.26
Nodes (12): buildTimeline(), dur(), elevenLabs(), elKey(), ensureVoices(), envelope(), faceCurves(), mixAudio() (+4 more)

### Community 4 - "Drehbuch-Regeln"
Cohesion: 0.25
Nodes (5): ElevenLabs Modell eleven_v3, Schwarze Endkarte, Vorlage folgen/01.json, Sets, Kameras, FX und SFX, Titelkarte (Shot 2)

### Community 5 - "Keller-Familie Folgen 2-4"
Cohesion: 0.33
Nodes (7): Anderer Name an Mats' Haus (Cliffhanger), Folge 2: Keller, Folge 3: Rauschen, Folge 4: Der Junge von 1989, Foto von 1989, Mats' Grossvater (Keller), Tagebuch des Grossvaters

## Ambiguous Edges - Review These
- `Stimme Maya (ElevenLabs)` → `Stimme Rika Sturm (Lena)`  [AMBIGUOUS]
  folgen/01-texte.md · relation: semantically_similar_to
- `Stimme Matthew (ElevenLabs)` → `Stimme Daniel - Ruhig und Freundlich (Mats)`  [AMBIGUOUS]
  folgen/01-texte.md · relation: semantically_similar_to
- `Stimme New MM (ElevenLabs)` → `Stimme Christian Plasa (Erzaehler)`  [AMBIGUOUS]
  folgen/01-texte.md · relation: semantically_similar_to

## Knowledge Gaps
- **7 isolated node(s):** `Werkstatt des Uhrmachers`, `Tagebuch des Grossvaters`, `Foto von 1989`, `Titelkarte (Shot 2)`, `Schwarze Endkarte` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 39 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ECHO (Mystery-Serie, Staffel 1)` connect `Uhrmacher und Stollen-Regel` to `Folge 1 Sprechtexte (alt)`, `Drehbuch-Regeln`, `Keller-Familie Folgen 2-4`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `ECHO Folge 1: Sprechtexte` (e.g. with `Folge 1: Die Stunde, die fehlt` and `Vorlage folgen/01.json`) actually correct?**
  _`ECHO Folge 1: Sprechtexte` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Werkstatt des Uhrmachers`, `Tagebuch des Grossvaters`, `Foto von 1989` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Build-Pipeline Setup` be split into smaller, more focused modules?**
  _Cohesion score 0.06451612903225806 - nodes in this community are weakly interconnected._
- **Why does `ECHO Folge 1: Sprechtexte` connect `Folge 1 Sprechtexte (alt)` to `Uhrmacher und Stollen-Regel`, `Drehbuch-Regeln`, `Keller-Familie Folgen 2-4`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Stimme Maya (ElevenLabs)` and `Stimme Rika Sturm (Lena)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Stimme Matthew (ElevenLabs)` and `Stimme Daniel - Ruhig und Freundlich (Mats)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._