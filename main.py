""""""# GitHub Copilot – PROJECT CONTEXT (LEZEN VOORDAT JE CODE SCHRIJFT)

main.py - Entry point van de Surprise Sinterklaas Console Game

main.py - Entry point van de Surprise Sinterklaas Console Game#

Dit is de hoofd-event-loop met:

- Hoofdmenu# Ik wil een terminal-only Sinterklaas / surprise “console game” bouwen in Python.

- Quiz starten

- MinigamesDit is de hoofd-event-loop met:# De game draait NIET op Windows, maar op een aparte LMDE (Linux Mint Debian Edition) machine:

- Instellingen

- TTS test- Hoofdmenu#

- Cadeaus info

"""- Quiz starten#   - Hardware: oude MacBook (Intel), waarop LMDE staat



import sys- Minigames#   - De LMDE-machine boot ZONDER GUI, direct in een TTY (pure terminal, multi-user.target)

import ui

import tts- Instellingen#   - Autologin op tty1 is ingesteld met systemd/getty

import gifts

from config import (- TTS test#   - Na autologin moet uiteindelijk automatisch mijn Python-game starten

    DIFFICULTY_LEVELS,

    DEFAULT_NUM_QUESTIONS,"""#

)

from quiz import run_quiz_game# Belangrijk:

from minigames import show_minigames_menu

import sys# - Ik ontwikkel de code op Windows 11 in VS Code met GitHub Copilot.



def show_main_menu():import ui# - Ik TEST de code NIET op Windows; runtime is Linux (LMDE).

    """Toon en verwerk hoofdmenu."""

    while True:import tts# - Uitrol naar de LMDE-machine gebeurt bijvoorbeeld via Pastebin, scp of git.

        ui.clear_screen()

        ui.print_banner()from config import (#

        print()

            DIFFICULTY_LEVELS,# DOEL VAN HET PROJECT

        options = [

            "Quiz starten",    DEFAULT_DIFFICULTY,# ---------------------

            "Minigames",

            "Cadeaus info",    DEFAULT_NUM_QUESTIONS,# Een interactieve Sinterklaas/surprise-console in de terminal, met:

            "Instellingen",

            "Test geluid/stem",)# - ASCII-art (banners, kaders, simpele “animaties”)

            "Afsluiten",

        ]from quiz import run_quiz_game# - Kleur in de terminal via ANSI escape codes (bijvoorbeeld \033[1;31m voor rood)

        

        ui.print_menu("HOOFDMENU", options)from minigames import show_minigames_menu# - Een of meerdere spelvormen, o.a.:

        

        try:#   - Quiz (meerkeuzevragen, A/B/C/D)

            choice = input("Jouw keuze (1-6): ").strip()

            #   - Mogelijk minigames (roulette / opdrachten / soundboard) – later

            if choice == "1":

                quiz_menu()def show_main_menu():# - Geluid/Text-to-Speech in het NEDERLANDS op de LMDE-machine

            elif choice == "2":

                show_minigames_menu()    """Toon en verwerk hoofdmenu."""#

            elif choice == "3":

                gifts.show_gift_info()    while True:# TTS / GELUID:

            elif choice == "4":

                settings_menu()        ui.clear_screen()# - Op de LMDE-machine zullen we gebruikmaken van espeak-ng en/of mbrola met Nederlandse stemmen.

            elif choice == "5":

                test_audio()        ui.print_banner()#   Voorbeelden die uiteindelijk moeten werken in Linux:

            elif choice == "6":

                say_goodbye()        print()#     espeak-ng -v nl "Dit is een test"

                break

            else:        #     espeak-ng -v mb-nl2 "Dit is een Nederlandse MBROLA-stem"

                ui.print_warning("Ongeldige keuze! Kies 1-6.")

        except KeyboardInterrupt:        options = [# - In de Python-code mag je uitgaan van het aanroepen van deze tools via subprocess.

            say_goodbye()

            break            "Quiz starten",# - Op Windows test ik TTS NIET; ik test alleen de logica (geen geluid).



            "Minigames",#

def quiz_menu():

    """Quiz-selectiemenu."""            "Instellingen",# FUNCTIONELE EISEN (HOOG NIVEAU)

    ui.clear_screen()

    ui.print_title("QUIZ")            "Test geluid/stem",# --------------------------------

    

    print("Kies je moeilijkheidsniveau:\n")            "Afsluiten",# 1) Terminal-UI:

    

    for i, level in enumerate(DIFFICULTY_LEVELS, 1):        ]#    - Volledig tekst/ASCII, geen GUI.

        print(f"  {i}. {level}")

            #    - Gebruik ANSI-kleuren voor titels, waarschuwingen, succes, etc.

    print("\n  0. Teruggaan")

            ui.print_menu("HOOFDMENU", options)#    - Een hoofdmenu met opties zoals:

    try:

        choice = input("\nKeuze: ").strip()        #        1. Start quiz

        

        if choice == "0":        try:#        2. Instellingen (bijv. moeilijkheid, aantal vragen)

            return

        elif choice in ["1", "2", "3"]:            choice = input("Jouw keuze (1-5): ").strip()#        3. Test geluid / stem

            idx = int(choice) - 1

            difficulty = DIFFICULTY_LEVELS[idx]            #        4. Afsluiten

            

            # Vraag aantal vragen            if choice == "1":#

            ui.clear_screen()

            ui.print_title(f"Quiz - {difficulty}")                quiz_menu()# 2) Quiz-engine (eerste spel dat we bouwen):

            

            print(f"Hoeveel vragen wil je beantwoorden?")            elif choice == "2":#    - Vragenstructuur met:

            print(f"(standaard: {DEFAULT_NUM_QUESTIONS})\n")

                            show_minigames_menu()#        - vraagtekst (Nederlands)

            try:

                num = input("Aantal vragen (Enter voor standaard): ").strip()            elif choice == "3":#        - 4 opties (A/B/C/D)

                if num:

                    num_questions = int(num)                settings_menu()#        - juiste antwoord

                    if num_questions < 1:

                        num_questions = DEFAULT_NUM_QUESTIONS            elif choice == "4":#    - Scoring (bijv. aantal goede antwoorden, eventueel strafpunten).

                else:

                    num_questions = DEFAULT_NUM_QUESTIONS                test_audio()#    - Simpele loop: vraag tonen -> invoer (A/B/C/D) -> feedback -> volgende vraag.

            except ValueError:

                num_questions = DEFAULT_NUM_QUESTIONS            elif choice == "5":#    - Feedback tonen in kleur (groen = goed, rood = fout).

            

            # Start quiz                say_goodbye()#    - Optioneel TTS: vraag en/of feedback laten uitspreken (alleen in Linux runtime).

            run_quiz_game(difficulty, num_questions)

        else:                break#

            ui.print_warning("Ongeldige keuze!")

    except KeyboardInterrupt:            else:# 3) Architectuur:

        ui.print_warning("\nTerug naar menu...")

                ui.print_warning("Ongeldige keuze! Kies 1-5.")#    - Graag een modulaire opzet:



def settings_menu():        except KeyboardInterrupt:#      - bijv. modules zoals:

    """Instellingen-menu."""

    while True:            say_goodbye()#        - game_main.py of main.py (entry point)

        ui.clear_screen()

        ui.print_title("INSTELLINGEN")            break#        - ui.py (kleurfuncties, ASCII helpers)

        

        tts_status = "AAN" if tts.TTS_ENABLED else "UIT"#        - quiz.py (quizlogica en vraagstructuren)

        

        options = [#        - tts.py (abstractie rond espeak-ng/mbrola)

            f"TTS (Tekst-naar-spraak): {tts_status}",

            "TTS testen",def quiz_menu():#        - config.py (instellingen zoals aantal vragen, TTS aan/uit)

            "Over dit spel",

            "Teruggaan",    """Quiz-selectiemenu."""#    - De code moet leesbaar en uitbreidbaar zijn.

        ]

            ui.clear_screen()#

        ui.print_menu("INSTELLINGEN", options)

            ui.print_title("QUIZ")# 4) Uitvoer/gebruik:

        try:

            choice = input("Jouw keuze (1-4): ").strip()    #    - De game draait in een oneindige loop tot de gebruiker kiest om af te sluiten.

            

            if choice == "1":    print("Kies je moeilijkheidsniveau:\n")#    - In de terminal kan de gebruiker met het toetsenbord keuzes maken (bijv. 1/2/3 in het menu, A/B/C/D bij quiz).

                toggle_tts()

            elif choice == "2":    #

                test_audio()

            elif choice == "3":    for i, level in enumerate(DIFFICULTY_LEVELS, 1):# 5) Autostart op LMDE (context, NIET om nu te implementeren):

                show_about()

            elif choice == "4":        print(f"  {i}. {level}")#    - Op de LMDE-machine zal ik in ~/.bash_profile iets doen als:

                break

            else:    #         if [ "$(tty)" = "/dev/tty1" ]; then

                ui.print_warning("Ongeldige keuze!")

        except KeyboardInterrupt:    print("\n  0. Teruggaan")#             python3 ~/surprise/main.py || true

            break

    #         fi



def toggle_tts():    try:#      zodat de game automatisch start na autologin.

    """Toggle TTS aan/uit."""

    ui.clear_screen()        choice = input("\nKeuze: ").strip()#    - Houd hier rekening mee: de code moet zich “netjes” gedragen in een pure TTY.

    

    if tts.TTS_ENABLED:        #

        ui.print_warning("TTS is momenteel AAN.")

        print("\nLet op: TTS is hardcoded in config.py.")        if choice == "0":# WAT IK NU VAN COPILOT WIL

        print("Je kunt het hier niet wijzigen.")

    else:            return# -------------------------

        ui.print_info("TTS is momenteel UIT.")

        print("\nOm TTS aan te zetten, wijzig config.py:")        elif choice in ["1", "2", "3"]:# 1) STEL MIJ EERST VRAGEN:

        print("  TTS_ENABLED = True")

                idx = int(choice) - 1#    - Stel mij eerst een reeks GERICHTE vragen (bijvoorbeeld 5–10 stuks) om onduidelijkheden te verhelderen, zoals:

    input("\nDruk Enter om terug te gaan...")

            difficulty = DIFFICULTY_LEVELS[idx]#      - Hoeveel vraagtypes ik wil (alleen meerkeuze A/B/C/D of meer)?



def test_audio():            #      - Hoe “fantasievol” de ASCII-art moet zijn (simpel vs uitgebreid)?

    """Test TTS-functionaliteit."""

    ui.clear_screen()            # Vraag aantal vragen#      - Of TTS standaard aan of uit moet staan in de game-logica?

    ui.print_title("TTS TEST")

                ui.clear_screen()#      - Of ik een JSON/CSV-bestand voor vragen wil, of hardcoded lijsten?

    if not tts.test_tts():

        ui.print_warning("TTS-test mislukt! Controleer espeak-ng op Linux.")            ui.print_title(f"Quiz - {difficulty}")#      - Of er verschillende moeilijkheidsniveaus / rondes moeten zijn?

        print("\nOp Linux installeren:")

        print("  sudo apt-get install espeak-ng mbrola mbrola-nl2")            #      - Hoe ik wil dat fouten/scores gepresenteerd worden (bv. scoreboard aan het einde)?

    else:

        ui.print_success("TTS lijkt te werken!")            print(f"Hoeveel vragen wil je beantwoorden?")#

        print("\nAls je op Linux bent en espeak-ng geïnstalleerd is,")

        print("zul je een test-boodschap horen.")            print(f"(standaard: {DEFAULT_NUM_QUESTIONS})\n")# 2) DAARNA:

    

    input("\nDruk Enter om terug te gaan...")            #    - Stel een VOORGESTELDE projectstructuur voor (bestanden + korte uitleg).



            try:#    - Genereer vervolgens stapsgewijs:

def show_about():

    """Toon informatie over het spel."""                num = input("Aantal vragen (Enter voor standaard): ").strip()#      a) Een basis main.py met:

    ui.clear_screen()

    ui.print_title("OVER DIT SPEL")                if num:#         - hoofdmenu

    

    about_text = """                    num_questions = int(num)#         - kleurfuncties (of gebruik vanuit ui.py)

Surprise Sinterklaas Console

Versie 1.0                    if num_questions < 1:#         - eenvoudige event-loop



Een interactieve terminal-spel voor Sinterklaas!                        num_questions = DEFAULT_NUM_QUESTIONS#      b) Een ui.py met:



FEATURES:                else:#         - kleurhelpers (bijv. success(), error(), title())

- Quiz met moeilijkheidsniveaus

- Meerkeuze- en waar/onwaar vragen                    num_questions = DEFAULT_NUM_QUESTIONS#         - ASCII-bannerfunctie voor de start

- Minigames (Roulette, Opdrachten, Soundboard)

- Cadeaus verdienen met goede scores            except ValueError:#      c) Een quiz.py met:

- Nederlandse tekst-naar-spraak (TTS) via espeak-ng

- Gedetailleerde scoring en feedback                num_questions = DEFAULT_NUM_QUESTIONS#         - eenvoudige datastructuur voor vragen

- Volledig in ASCII/ANSI-kleuren

            #         - een functie run_quiz() die de quiz afhandelt

CONTROLES:

- Kies opties met nummers (1, 2, 3, etc.)            # Start quiz#      d) Een tts.py met:

- Bij vragen: A, B, C, D (of J/N voor waar/onwaar)

- Druk 'R' om vragen te herhalen (TTS)            run_quiz_game(difficulty, num_questions)#         - functies als say(text: str, voice: str = "nl")

- Ctrl+C om af te sluiten

        else:#         - implementatie via subprocess voor espeak-ng / mbrola

CADEAUS:

- Verdien cadeaus door de quiz goed af te ronden!            ui.print_warning("Ongeldige keuze!")#         - veilige fallback (bijvoorbeeld: als TTS faalt, alleen printen)

- Elk moeilijkheidsniveau heeft een ander cadeau

- Minimum 70% om te winnen    except KeyboardInterrupt:#



REQUIREMENTS (Linux):        ui.print_warning("\nTerug naar menu...")# 3) HOU REKENING MET:

- Python 3.6+

- espeak-ng#    - ik test logica op Windows (dus geen Linux-specifieke paden hardcoderen),

- mbrola-nl2 (voor Nederlandse stemmen)

#      maar TTS en Linux-commando’s zullen pas op de LMDE-machine echt werken.

CREDITS:

Gemaakt met GitHub Copilotdef settings_menu():#    - gebruik bij voorkeur standaard Python 3 modules (subprocess, json, etc.).

Sinterklaas Traditioneel™

    """Instellingen-menu."""#

🎄 Fijne Sinterklaas! 🎄

    """    while True:# GRAAG:

    

    print(about_text)        ui.clear_screen()# - Duidelijke, moderne Python 3-code.

    input("Druk Enter om terug te gaan...")

        ui.print_title("INSTELLINGEN")# - Consistente stijl (bijvoorbeeld snake_case, type hints zijn welkom).



def say_goodbye():        # - Where relevant, korte comments in het Nederlands.

    """Zeg tot ziens."""

    ui.clear_screen()        tts_status = "AAN" if tts.TTS_ENABLED else "UIT"#

    ui.print_banner()

    print()        # BEGIN NU:

    

    farewell_messages = [        options = [# - Lees bovenstaande context.

        "Tot ziens! Veel sterkte met pakjesavond!",

        "Dag! Sint ziet je nog wel!",            f"TTS (Tekst-naar-spraak): {tts_status}",# - Stel me eerst concrete vragen in de stijl:

        "Fijne Sinterklaas! Zien we je volgende jaar!",

        "Bye! De pieten zwaaien!",            "TTS testen",#     "Vraag 1: ...", "Vraag 2: ..."

        "Tot ziens! Veel plezier met je cadeaus!",

    ]            "Over dit spel",# - Wacht op mijn antwoorden.

    

    import random            "Teruggaan",# - Begin daarna pas met het voorstellen van de projectstructuur en de eerste code.

    msg = random.choice(farewell_messages)

    print(colored(msg, "GREEN"))        ]

    print()        

            ui.print_menu("INSTELLINGEN", options)

    tts.speak(msg)        

    print("\nDanku voor het spelen! 🎄\n")        try:

            choice = input("Jouw keuze (1-4): ").strip()

            

def colored(text, color_name):            if choice == "1":

    """Helper om tekst te kleuren."""                toggle_tts()

    from config import COLORS            elif choice == "2":

    color = COLORS.get(color_name, "")                test_audio()

    reset = COLORS["RESET"]            elif choice == "3":

    return f"{color}{text}{reset}"                show_about()

            elif choice == "4":

                break

def main():            else:

    """Main entry point."""                ui.print_warning("Ongeldige keuze!")

    try:        except KeyboardInterrupt:

        # Controleer vragen            break

        from quiz import Quiz

        quiz = Quiz()

        if not quiz.questions:def toggle_tts():

            print("ERROR: Geen vragen geladen!")    """Toggle TTS aan/uit."""

            print(f"Controleer: vragen.csv")    ui.clear_screen()

            sys.exit(1)    

            if tts.TTS_ENABLED:

        # Start menu        ui.print_warning("TTS is momenteel AAN.")

        show_main_menu()        print("\nLet op: TTS is hardcoded in config.py.")

    except KeyboardInterrupt:        print("Je kunt het hier niet wijzigen.")

        print("\n\nGame afgebroken.")    else:

        sys.exit(0)        ui.print_info("TTS is momenteel UIT.")

    except Exception as e:        print("\nOm TTS aan te zetten, wijzig config.py:")

        print(f"\nFATALE FOUT: {e}")        print("  TTS_ENABLED = True")

        import traceback    

        traceback.print_exc()    input("\nDruk Enter om terug te gaan...")

        sys.exit(1)



def test_audio():

if __name__ == "__main__":    """Test TTS-functionaliteit."""

    main()    ui.clear_screen()

    ui.print_title("TTS TEST")
    
    if not tts.test_tts():
        ui.print_warning("TTS-test mislukt! Controleer espeak-ng op Linux.")
        print("\nOp Linux installeren:")
        print("  sudo apt-get install espeak-ng mbrola mbrola-nl2")
    else:
        ui.print_success("TTS lijkt te werken!")
        print("\nAls je op Linux bent en espeak-ng geïnstalleerd is,")
        print("zul je een test-boodschap horen.")
    
    input("\nDruk Enter om terug te gaan...")


def show_about():
    """Toon informatie over het spel."""
    ui.clear_screen()
    ui.print_title("OVER DIT SPEL")
    
    about_text = """
Surprise Sinterklaas Console
Versie 1.0

Een interactieve terminal-spel voor Sinterklaas!

FEATURES:
- Quiz met moeilijkheidsniveaus
- Meerkeuze- en waar/onwaar vragen
- Minigames (Roulette, Opdrachten, Soundboard)
- Nederlandse tekst-naar-spraak (TTS) via espeak-ng
- Gedetailleerde scoring en feedback
- Volledig in ASCII/ANSI-kleuren

CONTROLES:
- Kies opties met nummers (1, 2, 3, etc.)
- Bij vragen: A, B, C, D (of J/N voor waar/onwaar)
- Druk 'R' om vragen te herhalen (TTS)
- Ctrl+C om af te sluiten

REQUIREMENTS (Linux):
- Python 3.6+
- espeak-ng
- mbrola-nl2 (voor Nederlandse stemmen)

CREDITS:
Gemaakt met GitHub Copilot
Sinterklaas Traditioneel™

🎄 Fijne Sinterklaas! 🎄
    """
    
    print(about_text)
    input("Druk Enter om terug te gaan...")


def say_goodbye():
    """Zeg tot ziens."""
    ui.clear_screen()
    ui.print_banner()
    print()
    
    farewell_messages = [
        "Tot ziens! Veel sterkte met pakjesavond!",
        "Dag! Sint ziet je nog wel!",
        "Fijne Sinterklaas! Zien we je volgende jaar!",
        "Bye! De pieten zwaaien!",
        "Tot ziens! Veel plezier met je cadeaus!",
    ]
    
    import random
    msg = random.choice(farewell_messages)
    print(colored(msg, "GREEN"))
    print()
    
    tts.speak(msg)
    print("\nDanku voor het spelen! 🎄\n")


def colored(text, color_name):
    """Helper om tekst te kleuren."""
    from config import COLORS
    color = COLORS.get(color_name, "")
    reset = COLORS["RESET"]
    return f"{color}{text}{reset}"


def main():
    """Main entry point."""
    try:
        # Controleer vragen
        from quiz import Quiz
        quiz = Quiz()
        if not quiz.questions:
            print("ERROR: Geen vragen geladen!")
            print(f"Controleer: vragen.csv")
            sys.exit(1)
        
        # Start menu
        show_main_menu()
    except KeyboardInterrupt:
        print("\n\nGame afgebroken.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFATALE FOUT: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
