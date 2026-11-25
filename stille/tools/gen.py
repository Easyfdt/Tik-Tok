# WEISSE STILLE – Drehbuch-Generator (Folgen 2–13). Schreibt stille/folgen/NN.json
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'folgen')
def L(who, text, tone, **k): d = {'who': who, 'text': text, 'tone': tone}; d.update(k); return d
def C(who, x, z, face=0, pose='stand', **k): d = {'who': who, 'pos': [x, z], 'face': face, 'pose': pose}; d.update(k); return d
def S(set_, lines, **k):
    d = {'set': set_}; d.update(k); d['lines'] = lines if isinstance(lines, list) else [lines]
    if 'sfx' not in d: d['sfx'] = {'huette': ['room'], 'keller': ['drip', 'hum'], 'aussen': ['wind'], 'schneewald': ['wind'], 'gipfel': ['wind'], 'leere': []}[set_]
    return d
# feste Sitzplätze am Tisch
def SIT(who, seat, **k):
    x, z, f = {'J': (-1.1, -1.15, 0), 'M': (0, -1.15, 0), 'B': (1.1, -1.15, 0), 'L': (-1.1, 0.55, 180), 'T': (0, 0.55, 180), 'X': (1.1, 0.55, 180)}[seat]
    pose = k.pop('pose', 'sit')
    if pose != 'sit': k['sit'] = True
    return C(who, x, z, f, pose, **k)
def END(nr, titel, text, tone='[quiet, ominous]'):
    return S('leere', L('erz', text, tone), black=True, title='WEISSE STILLE', sub=f'FOLGE {nr} · {titel}', cut='hard', pre=0.6, post=0.5)
def OPEN(hook, text, tone='[whispering, ominous]', **k):
    return dict(S(k.pop('set', 'aussen'), L('erz', text, tone), hook=hook, cut='hard', pre=0.5, **k))
E = {}
J, M, B, La, T, X = 'jonas', 'mia', 'ben', 'lara', 'tim', 'sechster'

# ---------- 2 WER FEHLT? ----------
E[2] = ('Wer fehlt?', [
  OPEN('Zähl nicht laut.', 'Als Jonas wieder hinsieht, ist der Stuhl leer.', set='huette', cam='creep', focus='stuhl6', angle=200, d0=6, d1=2.2, fx=['dunkel'], chars=[SIT(J, 'J'), SIT(M, 'M'), SIT(La, 'L'), SIT(T, 'T')], sfx=['heartbeat', 'hum']),
  S('huette', L(B, 'Okay. Das war der Hüttenwirt. Ein Scherz. Ganz sicher.', '[nervous, fast]'), cam='close', focus=B, angle=-20, chars=[SIT(B, 'B')]),
  S('huette', L(M, 'Ein Scherz ohne Gesicht?', '[shaky, angry]'), cam='close', focus=M, angle=15, chars=[SIT(M, 'M', headY=-25), SIT(B, 'B')]),
  S('huette', L(J, 'Wir zählen uns. Jetzt. Laut.', '[firm, scared]'), cam='ots', over=M, focus=J, side=1, chars=[SIT(J, 'J', pose='point'), SIT(M, 'M')]),
  S('huette', L(J, 'Eins. Zwei. Drei. Vier. Fünf …', '[slow, counting, whispering]'), cam='orbit', focus='tisch', angle=40, chars=[SIT(J, 'J', pose='count'), SIT(M, 'M'), SIT(B, 'B'), SIT(La, 'L'), SIT(T, 'T')], sfx=['room', 'clock']),
  S('huette', L(T, 'Sechs.', '[tiny, flat whisper]'), cam='extreme', focus=T, angle=180, cut='hard', chars=[SIT(T, 'T')], sfx=['hit']),
  S('huette', L(La, 'Tim. Wer ist sechs?', '[frozen, whispering]'), cam='close', focus=La, angle=170, chars=[SIT(La, 'L', headY=30), SIT(T, 'T')]),
  S('huette', L(T, 'Der Mann. Er hat mich gezählt.', '[innocent, quiet]'), cam='dutch', focus=T, angle=190, roll=-12, chars=[SIT(T, 'T')], sfx=['hum']),
  S('huette', L('erz', 'Später liegt jeder wach. Niemand schaut zum leeren Stuhl.', '[slow, chilling]'), cam='track', focus='tisch', angle=150, travel=3, dist=4.2, fx=['dunkel'], trans='fade'),
  S('huette', L('erz', 'Auf dem sechsten Teller liegt ein Löffel. Benutzt.', '[very slow, whispering]'), camPos=[1.5, 1.4, 1.6], camTo=[1.25, 1.1, 0.95], look=[1.1, 0.84, 0.05], focus='stuhl6', fx=['dunkel'], sfx=['hum', 'heartbeat']),
  S('huette', L(M, 'Jonas … schau ins Fenster.', '[terrified whisper]'), cam='close', focus=M, angle=60, chars=[C(M, 2.6, 0.9, 120, 'filmen')], sfx=['wind', 'room']),
  S('huette', L('erz', 'Im Glas spiegelt sich der Raum. Fünf Freunde. Und hinter ihnen … einer mehr.', '[slow, ominous]'), cam='creep', focus='fenster', angle=-90, d0=5, d1=1.4, chars=[C(X, 3.3, -1.2, 90, 'stare', alpha=0.55)], sfx=['riser', 'wind']),
  S('huette', L(J, 'Nicht umdrehen. Keiner dreht sich um.', '[barely audible whisper]'), cam='extreme', focus=J, angle=30, cut='hard', chars=[C(J, 2.2, 1.3, 100, 'fear')], sfx=['heartbeat']),
  S('huette', L(X, 'Zu spät.', '[deep, slow, whispering right behind]'), cam='ots', over=X, focus=J, side=-1, chars=[C(J, 2.2, 1.3, 100, 'fear'), C(X, 1.4, 1.6, 70, 'stare')], cut='hard', sfx=['hit'], post=0.5),
  END(3, 'FUSSSPUREN', 'Wer sich umdreht, wird gezählt.')])

# ---------- 3 FUSSSPUREN ----------
E[3] = ('Fußspuren', [
  OPEN('Sie führen nur hin.', 'Am Morgen ist der Sturm kurz still. Und im Schnee sind Spuren.', fx=[], spuren=True, camPos=[0, 6, 14], camTo=[0, 1.2, 6], look=[0, 0.3, 2], focus='weg', sfx=['wind']),
  S('aussen', L(M, 'Barfuß. Wer läuft hier barfuß?', '[shaky, filming]'), cam='close', focus=M, angle=-30, spuren=True, chars=[C(M, -0.9, -1.4, 160, 'filmen', cold=True)]),
  S('aussen', L(J, 'Die Spuren gehen nur zur Hütte. Keine geht weg.', '[slow, realizing]'), cam='track', focus=J, angle=90, spuren=True, chars=[C(J, 0.4, 2, 0, 'down'), C(B, 1.3, 3, 0, 'frieren')]),
  S('aussen', L(B, 'Dann ist er noch drin.', '[whispering, scared]'), cam='ots', over=B, focus='tuer', side=1, spuren=True, chars=[C(B, 1.0, 1.0, 180, 'stand'), C(J, 0.2, 0.6, 180, 'stand')]),
  S('aussen', L('erz', 'Ben folgt den Spuren um die Hütte herum. Bis unter das Fenster, hinter dem sie geschlafen haben.', '[low, tense]'), cam='crane', focus=B, angle=-60, chars=[C(B, 3.8, -2.4, 160, 'walk', move=[0.5, -1])], spuren=True, sfx=['wind', 'steps']),
  S('aussen', L(B, 'Hier ist der Schnee platt. Als hätte jemand die ganze Nacht hier gestanden.', '[horrified whisper]'), cam='close', focus=B, angle=-110, chars=[C(B, 4.3, -3.4, -90, 'down')], sfx=['wind', 'heartbeat']),
  S('aussen', L('erz', 'Und dann hört Ben ein Knirschen. Schritte. Ganz nah.', '[very slow, whispering]'), cam='low', focus=B, angle=-90, chars=[C(B, 4.3, -3.4, -90, 'fear')], sfx=['steps', 'heartbeat']),
  S('aussen', L('erz', 'Neue Abdrücke. Einer nach dem anderen. Direkt auf ihn zu.', '[slow, chilling]'), camPos=[6.5, 1.0, -0.5], camTo=[5.8, 0.6, -1.6], look=[4.3, 0.2, -3.4], focus=B, chars=[C(B, 4.3, -3.4, 60, 'fear')], sfx=['steps', 'riser']),
  S('aussen', L(B, 'Jonas! Da läuft jemand! Ich seh ihn nicht!', '[screaming, panicked]'), cam='dutch', focus=B, angle=40, roll=16, chars=[C(B, 4.3, -3.4, 40, 'run', move=[-1.5, 2])], sfx=['wind', 'hit']),
  S('aussen', L(J, 'Ben! Rein! Sofort!', '[shouting]'), cam='wide', focus=J, angle=20, chars=[C(J, 0.6, -2.5, 120, 'point'), C(M, -0.5, -2.7, 120, 'filmen'), C(B, 2.6, -1.2, -120, 'run', move=[-1.8, -1])]),
  S('huette', L('erz', 'Die Tür knallt zu. Riegel vor. Fünf Herzen, die rasen.', '[fast, tense]'), cam='close', focus='tuer', angle=180, chars=[C(B, 2.4, -2.4, 0, 'fear'), C(J, 1.6, -2.2, 30, 'fear')], cut='hard', sfx=['hit', 'heartbeat']),
  S('huette', L(La, 'Fünf? Wir sind doch …', '[whispering, confused]'), cam='close', focus=La, angle=200, chars=[C(La, -0.4, 1.4, 200, 'stand')]),
  S('huette', L('erz', 'Auf dem Holzboden: nasse Abdrücke. Barfuß. Sie führen ins Zimmer. Und hören mitten im Raum einfach auf.', '[slow, ominous]'), cam='top', focus='main', h=1.9, fx=['dunkel'], sfx=['drip', 'heartbeat']),
  S('huette', L(T, 'Er ist schon drin. Er war nie draußen.', '[calm, creepy, childlike]'), cam='extreme', focus=T, angle=170, cut='hard', chars=[C(T, 0, 1.8, 170, 'stand', tilt=8)], sfx=['hit'], post=0.4),
  END(4, 'DAS FOTO', 'Wer keine Spuren hinterlässt, steht vielleicht direkt neben dir.')])

# ---------- 4 DAS FOTO ----------
E[4] = ('Das Foto', [
  OPEN('Schau genau hin.', 'Mia hat gestern Abend ein Gruppenfoto gemacht. Fünf Freunde am Kamin.', set='huette', cam='close', focus=M, angle=20, chars=[C(M, -1.6, -1.2, 30, 'filmen')], sfx=['room']),
  S('huette', L(M, 'Wir sind sechs auf dem Foto.', '[barely breathing]'), cam='extreme', focus=M, angle=25, chars=[C(M, -1.6, -1.2, 25, 'filmen')], sfx=['hum']),
  S('huette', L('erz', 'Hinter Tim steht ein Mann. Graue Kapuze. Eine Hand auf seiner Schulter. Und wo sein Gesicht sein sollte …', '[slow, chilling whisper]'), cam='creep', focus=X, angle=0, d0=4, d1=1.4, chars=[C(T, -2.2, -1.9, 0, 'stand'), C(X, -2.2, -2.4, 0, 'stare')], fx=['dunkel'], sfx=['riser']),
  S('huette', L(B, 'Lösch das. Lösch das sofort!', '[panicked]'), cam='close', focus=B, angle=-30, chars=[C(B, -0.6, -0.9, -30, 'fear')]),
  S('huette', L(M, 'Da ist noch ein Video. Von heute Nacht. Ich hab nicht gefilmt.', '[terrified whisper]'), cam='ots', over=J, focus=M, side=1, chars=[C(J, -0.6, 0.6, 200, 'stand'), C(M, -1.4, -0.6, 30, 'filmen')]),
  S('huette', L('erz', 'Das Video zeigt Jonas. Er schläft. Die Kamera schwebt über ihm, ganz ruhig.', '[slow, whispering]'), camPos=[1.0, 2.6, 2.2], camTo=[0.6, 2.2, 1.7], look=[0, 0.2, 1.2], chars=[C(J, 0, 1.2, 0, 'sit', y=-0.3)], fx=['dunkel'], sfx=['hum']),
  S('huette', L('erz', 'Dann dreht sich das Bild. Langsam. Zu dem, der filmt.', '[very slow, chilling]'), cam='push', focus=X, angle=180, chars=[C(X, 0, 2.6, 180, 'turn', head0=-120, t0=0.2, dur=0.7)], fx=['dunkel'], sfx=['heartbeat', 'riser']),
  S('huette', L(J, 'Das war direkt neben meinem Bett.', '[horrified whisper]'), cam='extreme', focus=J, angle=-15, chars=[C(J, -0.6, 0.6, -15, 'fear')], cut='hard', sfx=['hit']),
  S('huette', L(La, 'Mia. Gib mir die Kamera.', '[cold, controlled]'), cam='close', focus=La, angle=150, chars=[C(La, 0.4, 0.4, 150, 'stand')]),
  S('huette', L(M, 'Warum? Was weißt du, Lara?', '[suspicious, shaky]'), cam='ots', over=La, focus=M, side=-1, chars=[C(La, 0.4, 0.4, 210, 'stand'), C(M, -0.8, -0.9, 30, 'filmen')]),
  S('huette', L(La, 'Nichts. Ich will nur nicht, dass er uns noch mal sieht.', '[whispering, lying]'), cam='dutch', focus=La, angle=170, roll=-10, chars=[C(La, 0.4, 0.4, 170, 'down')]),
  S('huette', L('erz', 'Das letzte Bild auf der Karte hat die Uhrzeit von jetzt. Es zeigt die fünf. Von oben. Aus der Ecke unter dem Dach.', '[slow, ominous]'), cam='top', focus='main', h=1.95, chars=[C(J, -0.6, 0.6, 200, 'stand'), C(M, -0.8, -0.9, 30, 'filmen'), C(La, 0.4, 0.4, 210, 'stand'), C(B, 0.9, -0.6, 250, 'stand'), C(T, 0.1, 1.4, 180, 'stand')], fx=['dunkel'], sfx=['riser']),
  S('huette', L(T, 'Er winkt.', '[soft, delighted, creepy]'), camPos=[-3.6, 2.9, 2.6], camTo=[-3.5, 2.85, 2.5], look=[0, 0.8, -0.3], cut='hard', chars=[C(T, 0.1, 1.4, 120, 'point')], sfx=['hit'], post=0.5),
  END(5, 'DAS GÄSTEBUCH', 'Manche Kameras filmen nicht. Sie beobachten.')])

# ---------- 5 DAS GÄSTEBUCH ----------
E[5] = ('Das Gästebuch', [
  OPEN('Lies die letzte Seite nicht.', 'Auf dem Tisch liegt ein altes Gästebuch. Rotes Leder. Kalt wie Eis.', set='huette', camPos=[1.3, 1.25, 0.5], camTo=[1.0, 1.15, 0.2], look=[0.75, 0.86, -0.25], focus='buch', sfx=['room', 'hum']),
  S('huette', L(J, 'Neunzehnhundertvierundsiebzig. Martin, Susi, Klaus, Petra, Uwe. Fünf Personen.', '[reading slowly]', say=None), cam='ots', over=J, focus='buch', side=1, chars=[SIT(J, 'J', pose='down')]),
  S('huette', L(J, 'Am nächsten Tag: sechs Personen.', '[whispering]'), cam='close', focus=J, angle=15, chars=[SIT(J, 'J', pose='down')], sfx=['heartbeat']),
  S('huette', L(M, 'Und dann?', '[scared]'), cam='close', focus=M, angle=-10, chars=[SIT(M, 'M', headY=-30)]),
  S('huette', L(J, 'Vier. Drei. Zwei. Eins.', '[slow, chilling]'), cam='push', focus='buch', angle=30, fx=['dunkel'], sfx=['clock']),
  S('huette', L('erz', 'Der letzte Eintrag ist mit zitternder Hand geschrieben. Drei Worte.', '[slow, ominous]'), cam='creep', focus='buch', angle=-20, d0=2.5, d1=0.9, h=0.4, sfx=['riser']),
  S('huette', L(J, 'Zählt euch nicht.', '[horrified whisper]'), cam='extreme', focus=J, angle=5, cut='hard', chars=[SIT(J, 'J')], sfx=['hit']),
  S('huette', L(B, 'Das ist Fake. Irgendein Spinner hat das reingeschrieben.', '[angry, scared]'), cam='close', focus=B, angle=-25, chars=[SIT(B, 'B')]),
  S('huette', L(La, 'Blätter um, Jonas.', '[quiet, knowing]'), cam='close', focus=La, angle=165, chars=[SIT(La, 'L')]),
  S('huette', L('erz', 'Die nächste Seite ist neu. Die Tinte noch feucht. Darauf: ihre Namen. In einer Schrift, die keiner von ihnen kennt.', '[very slow, whispering]'), cam='top', focus='buch', h=1.2, sfx=['heartbeat', 'hum']),
  S('huette', L(J, 'Jonas. Mia. Ben. Lara. Tim. Und eine Zahl. Sechs Personen.', '[reading, trembling]'), cam='ots', over=B, focus=J, side=-1, chars=[SIT(J, 'J', pose='down'), SIT(B, 'B')]),
  S('huette', L(T, 'Da steht noch was. Ganz unten. Für morgen.', '[small, curious]'), cam='close', focus=T, angle=190, chars=[SIT(T, 'T')]),
  S('huette', L('erz', 'Morgen. Fünf Personen. Und ein Name ist durchgestrichen.', '[slow, chilling]'), cam='creep', focus='buch', angle=60, d0=2, d1=0.8, h=0.35, fx=['dunkel'], sfx=['riser']),
  S('huette', L(B, 'Warum … steht da mein Name?', '[voice breaking, whispering]'), cam='extreme', focus=B, angle=-5, cut='hard', chars=[SIT(B, 'B', pose='fear')], sfx=['hit', 'heartbeat'], post=0.5),
  END(6, 'DER KELLER', 'Das Buch zählt mit. Und es irrt sich nie.')])

# ---------- 6 DER KELLER ----------
E[6] = ('Der Keller', [
  OPEN('Geh nicht runter.', 'Unter dem Teppich ist eine Luke. Ben will wissen, wer das Buch schreibt.', set='huette', cam='top', focus='main', h=1.9, chars=[C(B, 0.6, 1.3, 180, 'down'), C(J, -0.5, 1.8, 150, 'stand')], fx=['dunkel'], sfx=['room']),
  S('keller', L('erz', 'Eine Treppe. Kalte Luft. Eine Glühbirne, die von allein schwingt.', '[slow, tense]'), cam='creep', focus='main', angle=20, d0=6, d1=3, h=0.6, chars=[C(B, 1.8, 1.6, 180, 'walk', move=[-0.6, -0.8], y=0.0), C(J, 1.8, 2.4, 180, 'walk', move=[-0.4, -0.6])], sfx=['drip', 'hum', 'steps']),
  S('keller', L(B, 'Da hängen Jacken. Alte Jacken. Die sind nass.', '[whispering, disturbed]'), cam='close', focus=B, angle=-60, chars=[C(B, 1.8, -1.0, -90, 'stand', cold=True)]),
  S('keller', L(M, 'Leute … die Wand.', '[barely audible]'), cam='ots', over=M, focus='wand', side=1, chars=[C(M, -0.4, 0.2, 180, 'filmen')], sfx=['drip', 'heartbeat']),
  S('keller', L('erz', 'Namen. Eingeritzt in den Stein. Martin. Susi. Klaus. Petra. Uwe. Und darunter … frisch.', '[slow, chilling whisper]'), cam='track', focus='wand', angle=0, dist=2.2, travel=2.6, sfx=['riser']),
  S('keller', L(La, 'Mia. Ben. Lara. Jonas.', '[reading, whispering]'), cam='close', focus=La, angle=200, chars=[C(La, 0.6, -0.5, 200, 'stand')]),
  S('keller', L(J, 'Und Tim? Wo ist Tims Name?', '[confused, scared]'), cam='close', focus=J, angle=-20, chars=[C(J, -1.0, -0.4, -20, 'stand')]),
  S('keller', L(T, 'Ich brauch keinen.', '[softly, smiling]'), cam='extreme', focus=T, angle=160, chars=[C(T, -0.2, 0.8, 160, 'stand')], cut='hard', sfx=['hit']),
  S('keller', L('erz', 'Oben knallt die Luke zu. Die Birne schwingt. Licht. Dunkel. Licht.', '[fast, tense]'), cam='low', focus='main', angle=10, chars=[C(J, -1.0, -0.4, 160, 'fear'), C(La, 0.6, -0.5, 160, 'fear'), C(M, -0.4, 0.2, 160, 'filmen'), C(B, 1.0, 0.4, 160, 'fear')], sfx=['hit', 'heartbeat']),
  S('keller', L('erz', 'Neben der Treppe steht jemand. Ganz still.', '[very slow, whispering]'), cam='creep', focus=X, angle=-160, d0=5, d1=2.6, chars=[C(X, 1.5, 2.0, 200, 'stare')], fx=['dunkel'], sfx=['riser']),
  S('keller', L('erz', 'Die Birne schwingt zurück. Und er ist weg.', '[whispering]'), cam='creep', focus='treppe', angle=-160, d0=2.6, d1=2.4, sfx=['hum']),
  S('keller', L(B, 'Leute? Warum habt ihr die Luke zugemacht? Lasst mich rein!', '[muffled, from above, knocking]', radio=True), cam='low', focus='treppe', angle=180, h=-0.6, sfx=['hit', 'steps']),
  S('keller', L(J, 'Das … das ist Bens Stimme.', '[horrified whisper]'), cam='close', focus=J, angle=10, chars=[C(J, -1.0, -0.4, 10, 'fear')]),
  S('keller', L('erz', 'Aber Ben steht genau neben ihm.', '[slow, chilling]'), cam='ots', over=J, focus=B, side=-1, chars=[C(J, -1.0, -0.4, 60, 'fear'), C(B, 0.0, -0.2, -110, 'stare')], cut='hard', sfx=['hit'], post=0.6),
  END(7, 'BEN IST WEG', 'Zwei Stimmen. Ein Gesicht. Welcher Ben ist echt?')])

# ---------- 7 BEN IST WEG ----------
E[7] = ('Ben ist weg', [
  OPEN('Erinnerst du dich an Ben?', 'Am Morgen ist ein Schlafsack leer. Kalt. Als hätte nie jemand darin gelegen.', set='huette', cam='creep', focus='main', angle=160, d0=5, d1=2, chars=[C(J, -0.6, 1.4, 180, 'down')], sfx=['room', 'hum']),
  S('huette', L(J, 'Ben? Ben!', '[calling, worried]'), cam='close', focus=J, angle=150, chars=[C(J, -0.6, 1.4, 150, 'stand')]),
  S('aussen', L('erz', 'Draußen nur Wind. Keine Spuren. Nicht eine.', '[slow, tense]'), fx=['sturm'], cam='wide', focus='main', angle=-10, chars=[C(J, 0, -1.5, 180, 'look'), C(M, -1, -1.8, 200, 'filmen')]),
  S('huette', L(M, 'Das Gästebuch. Fünf Personen. Ben ist durchgestrichen.', '[whispering, shaking]'), cam='ots', over=M, focus='buch', side=1, chars=[SIT(M, 'M', pose='down')]),
  S('huette', L(T, 'Wer ist Ben?', '[innocent, curious]'), cam='close', focus=T, angle=180, chars=[SIT(T, 'T')], cut='hard', sfx=['hit']),
  S('huette', L(J, 'Was? Ben! Unser Freund! Er sitzt jeden Abend da!', '[angry, desperate]'), cam='dutch', focus=J, angle=20, roll=12, chars=[SIT(J, 'J', pose='point')]),
  S('huette', L(M, 'Jonas … er ist auf keinem Video mehr.', '[voice breaking]'), cam='close', focus=M, angle=-20, chars=[SIT(M, 'M', pose='filmen')]),
  S('huette', L('erz', 'Mia spult zurück. Der Abend am Tisch. Lachen. Suppe. Und an Bens Platz: ein leerer Stuhl.', '[slow, ominous]'), cam='orbit', focus='tisch', angle=40, chars=[SIT(J, 'J'), SIT(M, 'M'), SIT(La, 'L'), SIT(T, 'T')], fx=['dunkel'], sfx=['hum']),
  S('huette', L(La, 'Bei mir fängt es auch an. Ich weiß nicht mehr, wie er gelacht hat.', '[crying softly]'), cam='extreme', focus=La, angle=170, chars=[SIT(La, 'L', pose='down')]),
  S('huette', L(J, 'Ich erinnere mich an ihn. Noch.', '[determined whisper]'), cam='push', focus=J, angle=0, chars=[SIT(J, 'J')], sfx=['heartbeat']),
  S('huette', L('erz', 'In der Nacht wird Jonas wach. Am Tisch klappert ein Löffel.', '[very slow, whispering]'), cam='creep', focus='tisch', angle=150, d0=6, d1=3.2, fx=['dunkel'], trans='fade', sfx=['hum', 'clock']),
  S('huette', L('erz', 'Jemand isst. Im Dunkeln. Auf Bens Platz.', '[slow, chilling]'), cam='ots', over=J, focus=X, side=1, chars=[C(J, -1.8, 2.0, 140, 'stand'), C(X, 1.1, -1.15, 0, 'sit', headY=0)], fx=['dunkel'], sfx=['heartbeat', 'riser']),
  S('huette', L(X, 'Jetzt sind wir wieder fünf.', '[deep, slow, whispering]'), cam='close', focus=X, angle=0, chars=[C(X, 1.1, -1.15, 0, 'turn', sit=True, head0=-150, t0=0.1, dur=0.6)], fill=1.5, cut='hard', sfx=['hit'], post=0.5),
  END(8, 'DIE STIMME IM FUNKGERÄT', 'Wer vergessen wird, ist nicht tot. Er ist nur … draußen.')])

# ---------- 8 DIE STIMME IM FUNKGERÄT ----------
E[8] = ('Die Stimme im Funkgerät', [
  OPEN('Mach nicht auf.', 'Um drei Uhr nachts rauscht das kaputte Funkgerät.', set='huette', cam='creep', focus='radio', angle=-60, d0=4, d1=1.2, fx=['dunkel'], sfx=['static', 'hum']),
  S('huette', L(B, 'Hallo? Hört mich jemand? Es ist so kalt …', '[weak, shivering, desperate]', radio=True), cam='extreme', focus='radio', angle=-90, fx=['dunkel'], sfx=['static', 'wind']),
  S('huette', L(J, 'Ben! Ben, wo bist du?', '[desperate, shouting]'), cam='close', focus=J, angle=-40, chars=[C(J, -3.4, 0.9, -80, 'fear')]),
  S('huette', L(B, 'Hinter der Hütte. Ich seh euer Licht. Bitte. Macht die Tür auf.', '[crying, pleading]', radio=True), cam='ots', over=J, focus='radio', side=-1, chars=[C(J, -3.4, 0.9, -80, 'fear')], sfx=['static']),
  S('huette', L(J, 'Ich hol ihn rein!', '[determined]'), cam='track', focus=J, angle=60, chars=[C(J, 0.5, 0.4, 160, 'run', move=[1.6, -2])], sfx=['steps']),
  S('huette', L(La, 'Nein! Das ist nicht Ben!', '[screaming]'), cam='dutch', focus=La, angle=200, roll=-14, chars=[C(La, 2.4, -2.5, 20, 'stand')], cut='hard', sfx=['hit']),
  S('huette', L(M, 'Woher willst du das wissen?', '[angry, crying]'), cam='close', focus=M, angle=-30, chars=[C(M, 1.0, 1.0, -40, 'stand')]),
  S('huette', L(B, 'Lara … ich weiß, was du damals getan hast.', '[suddenly calm, deep, slow]', radio=True), cam='push', focus='radio', angle=-80, fx=['dunkel'], sfx=['static', 'riser']),
  S('huette', L(La, 'Hör auf. Hör auf!', '[panicked whisper]'), cam='extreme', focus=La, angle=180, chars=[C(La, 2.4, -2.5, 180, 'hide')], sfx=['heartbeat']),
  S('huette', L('erz', 'Dann klopft es. Nicht an der Tür. Am Fenster.', '[slow, chilling]'), cam='creep', focus='fenster', angle=-90, d0=5, d1=2, sfx=['hit', 'wind']),
  S('huette', L('erz', 'Klopf. Klopf. Klopf. Immer im selben Takt. Wie ein Herz.', '[whispering]'), cam='ots', over=M, focus='fenster', side=1, chars=[C(M, 2.6, 0.8, 90, 'filmen')], sfx=['heartbeat']),
  S('huette', L('erz', 'Hinter dem Glas steht jemand in Bens roter Jacke.', '[very slow]'), cam='push', focus='fenster', angle=-90, chars=[C(X, 5.0, 0.2, -90, 'stare')], fx=['dunkel'], sfx=['riser']),
  S('huette', L(X, 'Darf ich rein? Ich hab doch einen Platz.', '[deep, slow, whispering, with Bens voice]'), cam='close', focus=X, angle=-90, chars=[C(X, 5.0, 0.2, -90, 'stare', hollow=0.85)], fill=1.4, cut='hard', sfx=['hit'], post=0.6),
  END(9, 'DER WALD', 'Wer klopft, will nicht rein. Er will dich raus.')])

# ---------- 9 DER WALD ----------
E[9] = ('Der Wald', [
  OPEN('Folge nicht den Bäumen.', 'Im Morgengrauen gehen Jonas und Mia in den Wald. Sie wollen Ben finden.', set='schneewald', cam='crane', focus='main', angle=10, chars=[C(J, -0.3, 2, 180, 'walk', move=[0, -2.5]), C(M, 0.5, 2.8, 180, 'walk', move=[0, -2.5])], sfx=['wind', 'steps']),
  S('schneewald', L(M, 'Hier war mal ein Weg. Jetzt ist hier nur noch Weiß.', '[whispering, cold]'), cam='close', focus=M, angle=20, chars=[C(M, 0.5, 0, 20, 'frieren')]),
  S('schneewald', L(J, 'Da! An dem Ast! Bens Jacke!', '[shouting]'), cam='ots', over=J, focus='jacke', side=1, chars=[C(J, 0.0, -3.0, 180, 'point')], sfx=['wind', 'hit']),
  S('schneewald', L('erz', 'Die Jacke ist steif gefroren. In der Tasche: Bens Handy. Ein Video. Aufgenommen heute Nacht.', '[slow, tense]'), cam='close', focus='jacke', angle=10, sfx=['wind', 'hum']),
  S('schneewald', L(B, 'Wenn ihr das seht … zählt nicht. Er zählt mit euch. Und wer übrig bleibt …', '[whispering, terrified, crying]', radio=True), cam='extreme', focus=M, angle=30, chars=[C(M, 0.9, -5.6, 30, 'filmen')], sfx=['static', 'heartbeat']),
  S('schneewald', L(M, 'Das Video bricht ab.', '[shaking]'), cam='close', focus=M, angle=-10, chars=[C(M, 0.9, -5.6, -10, 'down')]),
  S('schneewald', L('erz', 'Mia hebt die Kamera. Auf dem Display: Bäume. Und zwischen den Bäumen … Gestalten.', '[slow, chilling]'), cam='ots', over=M, focus='tief', side=-1, chars=[C(M, 0.9, -5.6, 180, 'filmen'), C(X, -2.5, -13, 0, 'stare', alpha=0.6), C(X, 2.0, -16, 0, 'stare', alpha=0.6)], sfx=['riser', 'wind']),
  S('schneewald', L(M, 'Jonas. Ich zähle sechs. Ohne Kamera sehe ich keinen.', '[barely audible]'), cam='close', focus=M, angle=20, chars=[C(M, 0.9, -5.6, 20, 'filmen')], sfx=['heartbeat']),
  S('schneewald', L(J, 'Runter mit der Kamera. Nicht hinsehen. Rückwärts gehen.', '[whispering, urgent]'), cam='track', focus=J, angle=80, chars=[C(J, 0.0, -5.2, 0, 'walk', move=[0, 1.2])], sfx=['steps', 'wind']),
  S('schneewald', L('erz', 'Mia senkt die Kamera.', '[very slow]'), cam='close', focus=M, angle=180, chars=[C(M, 0.9, -5.6, 180, 'stand')], sfx=['hum']),
  S('schneewald', L('erz', 'Und einer steht direkt vor ihr. So nah, dass ihr Atem an ihm gefriert.', '[slow, whispering, chilling]'), cam='ots', over=M, focus=X, side=1, chars=[C(M, 0.9, -5.6, 180, 'fear'), C(X, 0.9, -6.4, 0, 'stare')], cut='hard', sfx=['hit', 'heartbeat']),
  S('schneewald', L(X, 'Du hast mich gezählt.', '[deep, slow, whispering]'), cam='extreme', focus=X, angle=0, chars=[C(X, 0.9, -6.4, 0, 'stare', tilt=10, hollow=0.9)], fill=1.4, sfx=['riser']),
  S('schneewald', L(M, 'Jonas! Lauf!', '[screaming]'), cam='dutch', focus=M, angle=150, roll=18, chars=[C(M, 0.9, -5.6, 150, 'run', move=[-0.5, 2.5])], cut='hard', sfx=['hit', 'wind'], post=0.5),
  END(10, 'LARA WEISS ES', 'Was du zählst, zählt auch dich.')])

# ---------- 10 LARA WEISS ES ----------
E[10] = ('Lara weiß es', [
  OPEN('Sie war schon mal hier.', 'Jonas und Mia schaffen es zurück. Lara sitzt am Kamin. Sie hat geweint.', set='huette', cam='creep', focus=La, angle=60, d0=5, d1=2.2, chars=[C(La, -2.4, -1.3, 40, 'down')], sfx=['room']),
  S('huette', L(J, 'Lara. Was hast du damals getan?', '[cold, demanding]'), cam='ots', over=J, focus=La, side=1, chars=[C(J, -0.6, 0.4, 230, 'stand'), C(La, -2.4, -1.3, 40, 'down')]),
  S('huette', L(La, 'Ich war acht. Wir waren hier. Papa, Mama und ich. Drei.', '[quiet, shaking]'), cam='close', focus=La, angle=40, chars=[C(La, -2.4, -1.3, 40, 'stand')], sfx=['room', 'hum']),
  S('huette', L('erz', 'Zehn Jahre früher. Dieselbe Hütte. Derselbe Sturm.', '[slow, eerie]'), era=1974, cam='wide', focus='main', angle=20, chars=[C('larakind', -0.4, 0.8, 180, 'stand')], trans='fade', sfx=['wind', 'room'], fx=['dunkel']),
  S('huette', L(La, 'In der zweiten Nacht saß ein Junge an unserem Tisch. Klein. Grüne Jacke. Er hat mich angelächelt.', '[whispering, haunted]'), era=1974, cam='close', focus=T, angle=180, chars=[C(T, 0, 0.55, 180, 'sit')], sfx=['hum']),
  S('huette', L(La, 'Er hat gesagt: Wenn du mich mitnimmst, darf Mama bleiben.', '[crying, whispering]'), era=1974, cam='extreme', focus='larakind', angle=170, chars=[C('larakind', -0.4, 0.8, 170, 'down')], sfx=['heartbeat']),
  S('huette', L(La, 'Und ich hab ja gesagt.', '[barely audible, broken]'), cam='extreme', focus=La, angle=40, chars=[C(La, -2.4, -1.3, 40, 'down')], cut='hard', sfx=['hit']),
  S('huette', L(M, 'Lara … Tim trägt eine grüne Jacke.', '[slowly realizing, terrified]'), cam='close', focus=M, angle=-20, chars=[C(M, 0.4, 1.0, -40, 'stand')]),
  S('huette', L(La, 'Seit dieser Nacht hab ich einen kleinen Bruder. Und alle tun so, als wäre er immer da gewesen.', '[whispering, desperate]'), cam='push', focus=La, angle=60, chars=[C(La, -2.4, -1.3, 60, 'stand')], sfx=['riser']),
  S('huette', L(J, 'Wo ist Tim jetzt?', '[whispering]'), cam='close', focus=J, angle=200, chars=[C(J, -0.6, 0.4, 200, 'look')], sfx=['heartbeat']),
  S('huette', L('erz', 'Niemand hat ihn heute gesehen. Aber auf dem Tisch stehen wieder sechs Teller. Fein säuberlich gedeckt.', '[slow, ominous]'), cam='top', focus='tisch', h=1.9, fx=['dunkel'], sfx=['hum']),
  S('huette', L(T, 'Du hast es ihnen gesagt, Lara.', '[soft, disappointed, childlike]'), cam='ots', over=La, focus=T, side=-1, chars=[C(La, -2.4, -1.3, 0, 'fear'), C(T, -2.3, 0.4, 180, 'stand')], cut='hard', sfx=['hit']),
  S('huette', L(T, 'Jetzt muss ich mir eine neue Schwester suchen.', '[sweet, slow, creepy whisper]'), cam='extreme', focus=T, angle=180, chars=[C(T, -2.3, 0.4, 180, 'stand', tilt=12, hollow=0.7)], fill=1.3, sfx=['riser'], post=0.6),
  END(11, 'NEUNZEHNHUNDERTVIERUNDSIEBZIG', 'Manche Brüder werden nicht geboren. Sie werden eingeladen.')])

# ---------- 11 1974 ----------
E[11] = ('1974', [
  OPEN('So fing alles an.', 'Neunzehnhundertvierundsiebzig. Fünf Freunde erreichen die Hütte. Der Hüttenwirt wartet schon.', set='aussen', era=1974, fx=['sturm'], cam='wide', focus='main', angle=10, chars=[C('wirt', 0, -2.9, 0, 'stand'), C('m74a', -1, 0.5, 180, 'walk', move=[0, -1]), C('m74b', 0, 1.2, 180, 'walk', move=[0, -1]), C('m74c', 1, 0.8, 180, 'walk', move=[0, -1])], sfx=['wind', 'steps']),
  S('huette', L('wirt', 'Setzt euch. Und hört gut zu. Hier oben gibt es eine Regel.', '[old man, gravelly, serious]'), era=1974, cam='close', focus='wirt', angle=20, chars=[C('wirt', -2.2, -1.4, 40, 'stand')], sfx=['room']),
  S('huette', L('wirt', 'Wenn der Sturm kommt, kommt einer dazu. Er setzt sich an euren Tisch. Zählt euch niemals laut.', '[old man, whispering]'), era=1974, cam='ots', over='m74a', focus='wirt', side=1, chars=[C('m74a', -0.6, 0.2, 230, 'stand'), C('wirt', -2.2, -1.4, 40, 'stand')]),
  S('huette', L('erz', 'Uwe lacht. Und zählt. Eins. Zwei. Drei. Vier. Fünf.', '[slow, ominous]'), era=1974, cam='orbit', focus='tisch', angle=30, chars=[C('m74a', -1.1, -1.15, 0, 'sit'), C('m74b', 0, -1.15, 0, 'sit'), C('m74c', 1.1, -1.15, 0, 'sit'), C('m74d', -1.1, 0.55, 180, 'sit'), C('m74e', 0, 0.55, 180, 'count', sit=True)], sfx=['room', 'clock']),
  S('huette', L(X, 'Sechs.', '[deep, slow whisper]'), era=1974, cam='push', focus=X, angle=180, chars=[C(X, 1.1, 0.55, 180, 'sit')], fx=['dunkel'], cut='hard', sfx=['hit']),
  S('huette', L('erz', 'Am nächsten Morgen fehlt Martin. Und niemand erinnert sich an ihn. Nur der Wirt.', '[slow, chilling]'), era=1974, cam='track', focus='wirt', angle=30, chars=[C('wirt', 0.2, 1.3, 200, 'down')], trans='fade', sfx=['hum']),
  S('huette', L('wirt', 'Der Berg nimmt einen. Und schickt einen zurück, der nie da war.', '[old man, whispering, sad]'), era=1974, cam='extreme', focus='wirt', angle=200, chars=[C('wirt', 0.2, 1.3, 200, 'stand')], sfx=['riser']),
  S('huette', L('erz', 'Susi. Klaus. Petra. Jede Nacht einer weniger. Bis nur noch Uwe übrig ist. Allein am Tisch.', '[slow, whispering]'), era=1974, cam='creep', focus='tisch', angle=160, d0=6, d1=2.5, chars=[C('m74e', 0, 0.55, 180, 'down', sit=True)], fx=['dunkel'], sfx=['clock']),
  S('huette', L('erz', 'Er schreibt drei Worte ins Buch. Zählt euch nicht. Dann setzt er die Kapuze auf.', '[very slow]'), era=1974, cam='close', focus='m74e', angle=170, chars=[C('m74e', 0, 0.55, 170, 'down')], sfx=['heartbeat']),
  S('huette', L('erz', 'Und sein Gesicht … wird weiß wie Schnee.', '[slow, chilling whisper]'), era=1974, cam='push', focus=X, angle=180, chars=[C(X, 0, 0.55, 180, 'sit')], fx=['dunkel'], sfx=['riser']),
  S('huette', L(J, 'Der Sechste … war mal einer von ihnen.', '[horrified whisper]'), cam='close', focus=J, angle=20, chars=[C(J, -0.6, 0.4, 20, 'fear')], cut='hard', sfx=['hit']),
  S('huette', L(M, 'Und wer verschwindet … wird der nächste.', '[realizing, crying]'), cam='close', focus=M, angle=-20, chars=[C(M, 0.4, 1.0, -20, 'stand')]),
  S('huette', L('erz', 'Am Fenster steht wieder jemand. Rote Jacke. Weißes Gesicht. Und er winkt. Wie Ben immer gewinkt hat.', '[slow, chilling]'), cam='creep', focus='fenster', angle=-90, d0=5, d1=1.6, chars=[C(X, 5.0, 0.2, -90, 'point')], fx=['dunkel'], sfx=['riser', 'wind']),
  S('huette', L(B, 'Ich bin jetzt der Sechste, Jonas. Und morgen … holen wir dich.', '[deep, slow, whispering, sad]', radio=True), cam='extreme', focus='fenster', angle=-90, cut='hard', sfx=['static', 'hit'], post=0.6),
  END(12, 'DER GIPFEL', 'Der Sturm vergisst niemanden. Er tauscht nur.')])

# ---------- 12 DER GIPFEL ----------
E[12] = ('Der Gipfel', [
  OPEN('Ganz oben ist Netz.', 'Auf dem Gipfel steht ein alter Funkmast. Die letzte Chance, Hilfe zu rufen.', set='gipfel', fx=['sturm'], camPos=[6, 7, 14], camTo=[3, 3, 7], look=[0, 2, -3], focus='kreuz', sfx=['wind', 'riser']),
  S('gipfel', L(J, 'Weiter! Nicht stehen bleiben! Nicht zählen!', '[shouting over wind]'), fx=['sturm'], cam='track', focus=J, angle=80, chars=[C(J, 0, 3, 180, 'walk', move=[0, -2]), C(M, -0.8, 4, 180, 'walk', move=[0, -2]), C(La, 0.8, 4.6, 180, 'walk', move=[0, -2])], sfx=['wind', 'steps']),
  S('gipfel', L(La, 'Wo ist Tim? Er war doch gerade noch hinter mir.', '[panicked, out of breath]'), fx=['sturm'], cam='close', focus=La, angle=-20, chars=[C(La, 0.8, 2.6, 160, 'look')]),
  S('gipfel', L('erz', 'Hinter ihnen im Schnee: drei Spuren nebeneinander. Und eine vierte. Kleiner. Die rückwärts läuft.', '[slow, chilling]'), fx=['sturm'], cam='low', focus='main', angle=180, sfx=['wind', 'heartbeat']),
  S('gipfel', L(J, 'Hallo? Hier sind vier Jugendliche, Hütte am Nordgrat! Wir brauchen Hilfe!', '[shouting into radio, desperate]'), fx=['sturm'], cam='ots', over=M, focus=J, side=1, chars=[C(J, 1.0, -1.2, 120, 'point'), C(M, 0, 0.2, 200, 'frieren')], sfx=['wind', 'static']),
  S('gipfel', L('wirt', 'Bergwacht hier. Wir sehen euch auf der Wärmebildkamera. Wie viele seid ihr?', '[calm, radio voice]', radio=True), fx=['sturm'], cam='close', focus=J, angle=60, chars=[C(J, 1.0, -1.2, 60, 'stand')], sfx=['static']),
  S('gipfel', L(J, 'Vier. Wir sind vier.', '[out of breath]'), fx=['sturm'], cam='extreme', focus=J, angle=40, chars=[C(J, 1.0, -1.2, 40, 'stand')]),
  S('gipfel', L('wirt', 'Nein. Auf dem Bild seid ihr sechs. Zwei stehen direkt hinter euch.', '[slow, confused, radio voice]', radio=True), fx=['sturm'], cam='creep', focus=J, angle=0, d0=6, d1=2.5, chars=[C(J, 1.0, -1.2, 180, 'fear'), C(M, 0, 0.2, 180, 'fear')], sfx=['static', 'riser']),
  S('gipfel', L('erz', 'Langsam drehen sie sich um.', '[very slow, whispering]'), fx=['sturm'], cam='low', focus=M, angle=180, chars=[C(M, 0, 0.2, 0, 'fear'), C(J, 1.0, -1.2, 0, 'fear')], sfx=['heartbeat']),
  S('gipfel', L('erz', 'Am Gipfelkreuz: Tim. Und neben ihm, in roter Jacke … Ben. Beide ohne Gesicht.', '[slow, chilling whisper]'), fx=['sturm'], cam='push', focus='kreuz', angle=0, chars=[C(T, -0.6, -2.4, 0, 'stare', hollow=0.8), C(X, 0.6, -2.5, 0, 'stare')], sfx=['riser', 'wind']),
  S('gipfel', L(La, 'Tim … komm her. Bitte.', '[crying, whispering]'), fx=['sturm'], cam='ots', over=La, focus=T, side=1, chars=[C(La, -0.4, 0.6, 180, 'stand'), C(T, -0.6, -2.4, 0, 'stare', hollow=0.8)]),
  S('gipfel', L(T, 'Ich war nie dein Bruder, Lara. Ich war immer der Fünfte.', '[sweet, cold, childlike whisper]'), fx=['sturm'], cam='extreme', focus=T, angle=0, chars=[C(T, -0.6, -2.4, 0, 'stare', tilt=10, hollow=0.8)], fill=1.4, sfx=['hit']),
  S('gipfel', L('erz', 'Der Sturm verschluckt die beiden. Und mit ihnen … Lara.', '[slow, ominous]'), fx=['sturm'], cam='wide', focus='kreuz', angle=20, chars=[C(La, -0.4, -1.2, 0, 'walk', move=[0, -1.5])], sfx=['wind', 'riser']),
  S('gipfel', L(M, 'Lara! LARA!', '[screaming]'), fx=['sturm'], cam='dutch', focus=M, angle=180, roll=-16, chars=[C(M, 0, 0.2, 0, 'fear')], cut='hard', sfx=['hit'], post=0.5),
  END(13, 'WEISSE STILLE', 'Zwei sind übrig. Aber wie viele kommen zurück?')])

# ---------- 13 WEISSE STILLE ----------
E[13] = ('Weiße Stille', [
  OPEN('Hört ihr das?', 'Am Morgen hört der Sturm auf. Und plötzlich ist es still. Weiße Stille.', set='aussen', fx=['noschnee'], camPos=[0, 10, 26], camTo=[0, 3, 11], look=[0, 2, -6], focus='huette', sfx=[]),
  S('aussen', L('erz', 'Ein Pistenbully kämpft sich den Hang hinauf. Die Bergwacht.', '[slow, calm]'), fx=['noschnee'], cam='wide', focus='main', angle=-20, chars=[C(J, -0.4, -2, 180, 'frieren'), C(M, 0.5, -2.2, 180, 'frieren')], sfx=['wind']),
  S('huette', L('erz', 'Drinnen sitzt jemand am Tisch. Löffelt Suppe. Als wäre nichts gewesen.', '[slow, eerie]'), cam='creep', focus=B, angle=180, d0=5, d1=2.4, chars=[SIT(B, 'B')], sfx=['room']),
  S('huette', L(B, 'Da seid ihr ja! Wo wart ihr die ganze Nacht?', '[cheerful, normal]'), cam='close', focus=B, angle=-10, chars=[SIT(B, 'B', headY=20)]),
  S('huette', L(M, 'Ben? Ben! Du lebst!', '[crying, relieved]'), cam='ots', over=B, focus=M, side=-1, chars=[SIT(B, 'B'), C(M, -0.2, 1.4, 180, 'stand')]),
  S('huette', L(La, 'Natürlich lebt er. Was ist mit euch los?', '[confused, light]'), cam='close', focus=La, angle=170, chars=[SIT(La, 'L')], cut='hard', sfx=['hit']),
  S('huette', L(J, 'Lara? Du warst … am Gipfel … mit Tim.', '[stunned whisper]'), cam='extreme', focus=J, angle=20, chars=[C(J, -0.8, 1.6, 170, 'fear')]),
  S('huette', L(La, 'Wer ist Tim?', '[innocent, puzzled]'), cam='push', focus=La, angle=170, chars=[SIT(La, 'L')], sfx=['heartbeat']),
  S('huette', L('erz', 'Niemand erinnert sich an Tim. Nicht Lara. Nicht Mia. Nicht Ben. Nur Jonas.', '[slow, whispering]'), cam='orbit', focus='tisch', angle=30, chars=[SIT(M, 'M'), SIT(B, 'B'), SIT(La, 'L'), C(J, -1.8, 1.4, 150, 'stand')], sfx=['room', 'hum']),
  S('aussen', L('wirt', 'So. Durchzählen bitte, bevor wir losfahren.', '[friendly rescuer, radio voice]', radio=True), fx=['noschnee'], cam='wide', focus='main', angle=10, chars=[C(J, -1.2, -1.5, 180, 'stand'), C(M, -0.4, -1.4, 180, 'stand'), C(B, 0.4, -1.5, 180, 'stand'), C(La, 1.2, -1.4, 180, 'stand')], sfx=['wind']),
  S('aussen', L(M, 'Eins. Zwei. Drei. Vier.', '[slow, relieved]'), fx=['noschnee'], cam='track', focus=M, angle=20, chars=[C(J, -1.2, -1.5, 0, 'stand'), C(M, -0.4, -1.4, 0, 'count'), C(B, 0.4, -1.5, 0, 'stand'), C(La, 1.2, -1.4, 0, 'stand')]),
  S('aussen', L('erz', 'Und da ist sie wieder. Die Stimme. Ganz leise. Direkt neben Jonas.', '[very slow, chilling whisper]'), fx=['noschnee'], cam='ots', over=J, focus=X, side=-1, chars=[C(J, -1.2, -1.5, 0, 'fear'), C(X, -2.0, -1.6, 0, 'stare')], sfx=['heartbeat', 'riser']),
  S('aussen', L(X, 'Fünf.', '[deep, slow, whispering right behind]'), fx=['noschnee'], cam='extreme', focus=X, angle=60, chars=[C(X, -2.0, -1.6, 60, 'stare', tilt=10)], cut='hard', sfx=['hit']),
  S('aussen', L('erz', 'Im Pistenbully macht Mia ein letztes Foto. Vier lachende Freunde. Und Jonas … ohne Gesicht.', '[slow, ominous]'), fx=['noschnee'], cam='push', focus='jonasx', angle=0, chars=[C('jonasx', -1.2, -1.5, 0, 'stare')], sfx=['riser']),
  S('huette', L('erz', 'Oben in der Hütte deckt jemand den Tisch. Für sechs.', '[very slow, whispering]'), cam='creep', focus='tisch', angle=200, d0=5, d1=1.8, fx=['dunkel'], sfx=['hum', 'clock']),
  S('huette', L(J, 'Ich hab Hunger.', '[deep, slow, whispering, Jonas and the sixth voice together]'), cam='close', focus='jonasx', angle=180, chars=[C('jonasx', 1.1, 0.55, 180, 'turn', sit=True, head0=170, t0=0.05, dur=0.6)], fx=['dunkel'], fill=1.4, cut='hard', sfx=['hit'], post=1.2),
  S('leere', L('erz', 'Wir waren fünf. Wir sind fünf. Aber einer von uns … war nie da.', '[quiet, ominous, slow]'), black=True, title='WEISSE STILLE', sub='ENDE … ODER?', cut='hard', pre=0.8, post=1.0)])

# Jonas ohne Gesicht im letzten Bild: eigener Figur-Eintrag 'jonasx'
for nr, (titel, shots) in E.items():
    for sh in shots:
        if 'set_' in sh: sh.pop('set_')
        for l in sh['lines']:
            if l.get('say') is None: l.pop('say', None)
            if any(ch.isdigit() for ch in l['text']) and 'say' not in l: print('ZAHL!', nr, l['text'])
    json.dump({'nr': nr, 'titel': titel, 'shots': shots}, open(os.path.join(OUT, f'{nr:02d}.json'), 'w'), ensure_ascii=False, indent=0)
print('ok', sorted(E))
