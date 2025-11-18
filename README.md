# 🎄 Surprise Sinterklaas Console Game 🎄

Een interactieve terminal-spel voor Sinterklaas, gebouwd in Python met:
- **Quiz** met moeilijkheidsniveaus (Makkelijk/Normaal/Moeilijk)
- **Meerkeuze en waar/onwaar vragen** in Nederlands
- **Minigames** (Roulette, Opdrachten, Soundboard)
- **Nederlandse Text-to-Speech** via espeak-ng
- **Gedetailleerde scoring** en feedback
- **Full ASCII/ANSI-kleuren** UI

## 📁 Projectstructuur

```
surprise_console/
├── main.py              # Entry point, hoofdmenu, event-loop
├── ui.py                # ANSI-kleuren, ASCII-art, kaders, banners
├── config.py            # Instellingen (TTS, moeilijkheid, kleuren)
├── tts.py               # TTS-abstractie (espeak-ng)
├── quiz.py              # Quiz-engine, vraagverwerking, scoring
├── minigames.py         # Minigames (roulette, opdrachten, soundboard)
├── gifts.py             # Cadeau-systeem
├── maintenance.py       # Onderhoudsmenu (CRUD voor vragen)
├── vragen.csv           # Vraagenbank (CSV-format)
└── README.md            # Dit bestand
```

## 🚀 Installatie

### Vereisten
- **Python 3.6+**
- Voor TTS op Linux: `espeak-ng` en `mbrola-nl2`

### Op Linux (LMDE/Debian)

```bash
# Installeer espeak-ng en MBROLA
sudo apt-get update
sudo apt-get install espeak-ng mbrola mbrola-nl2

# Clone/download het project
cd ~/surprise_console  # of je gekozen directory

# Start het spel
python3 main.py
```

### Op Windows (geen TTS, alleen testen)

```powershell
# Download/clone project
cd C:\Code\surprise_console

# Start het spel (TTS zal gracefully degraderen)
python main.py
```

## 🎮 Hoe te Spelen

1. **Hoofdmenu**: Kies uit:
   - Quiz starten
   - Minigames
   - Instellingen
   - Test geluid/stem
   - Afsluiten

2. **Quiz**:
   - Kies moeilijkheidsniveau
   - Voer aantal vragen in (of gebruik standaard 10)
   - Beantwoord vragen met A/B/C/D (meerkeuze) of A/B (waar/onwaar)
   - Druk 'R' om vraag te herhalen (TTS)
   - Zie gedetailleerd resultaat na afloop

3. **Minigames**:
   - **Roulette**: 3 willekeurige vragen uit alle niveaus
   - **Sint's Opdrachten**: Grappige taken van Sint
   - **Soundboard**: Grappige TTS-boodschappen

## ⚙️ Configuratie

Wijzig `config.py` voor:
- **TTS_ENABLED**: Zet TTS aan/uit
- **TTS_VOICE**: Stemkeuze (bijv. "mb-nl2")
- **DIFFICULTY_LEVELS**: Voeg niveaus toe/wijzig
- **COLORS**: Pas ANSI-kleuren aan
- **POINTS_PER_QUESTION**: Wijzig puntenstelsel

## 📊 Vragen Toevoegen

Voeg vragen toe aan `vragen.csv` **of** gebruik het **Onderhoudsmenu**!

### Optie 1: CSV-bestand aanpassen

```csv
vraagtekst,antwoord_A,antwoord_B,antwoord_C,antwoord_D,juist_antwoord,type,moeilijkheid
"Vraag hier?","Optie A","Optie B","Optie C","Optie D","A",multiple,Normaal
"Waar/onwaar vraag?","Waar","Onwaar",,,,"tf",Makkelijk
```

**Kolommen:**
- `vraagtekst`: De vraag (tussen aanhalingstekens)
- `antwoord_A`, `B`, `C`, `D`: Antwoordopties (voor multiple choice)
- `juist_antwoord`: Letter van juiste antwoord (A/B/C/D)
- `type`: "multiple" of "tf" (true/false)
- `moeilijkheid`: "Makkelijk", "Normaal", of "Moeilijk"

**Voorbeelden:**
```csv
"Wanneer vieren we Sinterklaas?","5 december","3 oktober","25 december","1 januari","A",multiple,Makkelijk
"Is Sint Nicolaas een echte historische figuur?","Waar","Onwaar",,,,"tf",Normaal
```

### Optie 2: Onderhoudsmenu (CRUD)

**Veel gemakkelijker!** Beheer vragen direct in het spel zonder CSV-bewerking.

#### Toegang
- Druk **`Ctrl+M`** op het hoofdmenu
- Of kies in het menu

#### Functies

**1. ➕ Nieuwe vraag toevoegen**
- Kies vraagtype (meerkeuze of waar/onwaar)
- Selecteer moeilijkheidsniveau
- Voer vraagtekst in
- Voer antwoorden in
- Selecteer juiste antwoord
- ✅ Automatisch naar CSV opgeslagen!

**2. 📋 Alle vragen tonen**
- Sorteerd per moeilijkheidsniveau
- Toon eerste 50 karakters van vraag

**3. ✏️ Vraag wijzigen**
- Selecteer vraag
- Wijzig: vraagtekst, antwoorden, juiste antwoord, moeilijkheid
- ✅ Automatisch opgeslagen

**4. 🗑️ Vraag verwijderen**
- Selecteer vraag
- Bevestiging voordat verwijderd
- ✅ Automatisch opgeslagen

#### CSV Auto-save
- ✅ Elke wijziging direct naar `vragen.csv`
- ✅ Geen handmatige export
- ✅ Veilig in git (backup)

## 🔊 TTS Installatie (Linux)

```bash
# LMDE/Debian
sudo apt-get install espeak-ng mbrola mbrola-nl2

# Controleer installatie
espeak-ng -v mb-nl2 "Hallo Sint!"
```

Stemmen:
- `mb-nl1`: MBROLA Nederlands v1
- `mb-nl2`: MBROLA Nederlands v2 (aanbevolen)
- `nl`: Standaard espeak-ng Nederlands

## 🎯 Autostart op LMDE

Voeg dit toe aan `~/.bash_profile`:

```bash
if [ "$(tty)" = "/dev/tty1" ]; then
    python3 ~/surprise_console/main.py || true
fi
```

## 📝 Modules Overzicht

### `main.py`
- Hoofdmenu en event-loop
- Quiz-menu met moeilijkheidskeuze
- Minigames-menu
- Instellingen
- TTS-test
- **Ctrl+M hotkey voor onderhoudsmenu**

### `ui.py`
- `print_title()`, `print_success()`, `print_error()`, etc.
- `print_box()` - Mooie kaders
- `print_banner()` - Sinterklaas banner
- `print_menu()` - Menu-renderer
- `print_score_card()` - Gedetailleerd resultaatscherm
- `animated_text()` - Letter-voor-letter animatie

### `config.py`
- TTS-instellingen
- Moeilijkheidsniveaus
- Puntentelling
- ANSI-kleuren
- Bestandspaden

### `tts.py`
- `speak()` - Spreek tekst uit
- `speak_question()` - Spreek vraag uit
- `speak_feedback()` - Spreek feedback uit
- `test_tts()` - Test TTS-functionaliteit
- Graceful degradatie op Windows (print alleen)

### `quiz.py`
- `Quiz` class
- `load_questions()` - Laad CSV
- `get_questions_by_difficulty()` - Filter vragen
- `run_quiz()` - Quiz-loop
- `show_final_score()` - Eindresultaat

### `maintenance.py` ✨ NIEUW!
- `QuestionManager` class - CRUD operaties
- `add_question()` - Voeg vraag toe (interactief)
- `list_questions()` - Toon alle vragen
- `edit_question()` - Wijzig vraag
- `delete_question()` - Verwijder vraag
- `show_maintenance_menu()` - Toegankelijk via Ctrl+M
- **Auto-save naar CSV na elke wijziging**

### `minigames.py`
- `play_roulette()` - 3 willekeurige vragen
- `play_opdracht()` - Grappige taken
- `play_soundboard()` - TTS-boodschappen
- `show_minigames_menu()` - Minigames-menu

## 🎨 ASCII-Art

Het spel bevat:
- Sinterklaas ASCII-art
- Cadeaupakketten
- Mooie kaders en decoraties
- ANSI-kleuraccentering

## ⌨️ Controles

| Actie | Controle |
|-------|----------|
| Menu opties | 1, 2, 3, 4, 5 |
| Quiz antwoord | A, B, C, D |
| Waar/Onwaar | A (Waar), B (Onwaar) |
| Vraag herhalen | R |
| Teruggaan | 0 of Ctrl+C |
| Volgende scherm | Enter |

## 📌 Notities

- **Windows Testing**: TTS werkt gracefully niet (geen geluid), maar alle logica werkt
- **Linux Runtime**: Op LMDE zal TTS full werken via espeak-ng
- **CSV-aanpassingen**: Wijzig `vragen.csv` om vragen toe te voegen/wijzigen
- **Performance**: Game draait snel op oude hardware (MacBook Intel LMDE)

## 🐛 Troubleshooting

### TTS werkt niet
```bash
# Controleer espeak-ng
which espeak-ng
espeak-ng -v mb-nl2 "Test"

# Installeer opnieuw
sudo apt-get install --reinstall espeak-ng mbrola mbrola-nl2
```

### Vragen laden niet
- Controleer `vragen.csv` bestaat in dezelfde directory als `main.py`
- Zorg voor correct CSV-format (komma's, aanhalingstekens)

### Kleuren werken niet
- Waarschijnlijk terminal ondersteunt ANSI niet
- Wijzig COLORS in `config.py` naar lege strings

## 📄 Licentie

Sinterklaas Traditioneel™ 🎄

---

**Gemaakt met GitHub Copilot**  
**Fijne Sinterklaas!** 🎄
