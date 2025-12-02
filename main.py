"""""""""# GitHub Copilot – PROJECT CONTEXT (LEZEN VOORDAT JE CODE SCHRIJFT)

main.py - Entry point van de Surprise Sinterklaas Console Game

main.py - Entry point van de Surprise Sinterklaas Console Game

Dit is de hoofd-event-loop met:


import sys
import random
import ui
import tts
import gifts
from config import DIFFICULTY_LEVELS, DEFAULT_NUM_QUESTIONS
from quiz import run_quiz_game, Quiz
from minigames import show_minigames_menu
from maintenance import show_maintenance_menu


def show_main_menu():
    """Toon en verwerk hoofdmenu."""
    while True:
        ui.clear_screen()
        ui.print_banner()
        print()
        options = [
            "Quiz starten",
            "Minigames",
            "Cadeaus info",
            "Instellingen",
            "Test geluid/stem",
            "Afsluiten",
        ]
        ui.print_menu("HOOFDMENU", options)
        print("\n💡 Tip: Druk Ctrl+M voor onderhoudsmenu (vragen beheren)")
        print()
        try:
            choice = input("Jouw keuze (1-6): ").strip()
            if choice == "1":
                quiz_menu()
            elif choice == "2":
                show_minigames_menu()
            elif choice == "3":
                gifts.show_gift_info()
            elif choice == "4":
                settings_menu()
            elif choice == "5":
                test_audio()
            elif choice == "6":
                say_goodbye()
                break
            else:
                ui.print_warning("Ongeldige keuze! Kies 1-6.")
        except KeyboardInterrupt:
            print("\n")
            response = input("Druk Ctrl+M voor onderhoudsmenu, of Ctrl+C opnieuw om af te sluiten: ").strip()
            if response.upper() == "M":
                show_maintenance_menu()


def quiz_menu():
    """Quiz-selectiemenu."""
    ui.clear_screen()
    ui.print_title("QUIZ")
    print("Kies je moeilijkheidsniveau:\n")
    for i, level in enumerate(DIFFICULTY_LEVELS, 1):
        print(f"  {i}. {level}")
    print("\n  0. Teruggaan")
    try:
        choice = input("\nKeuze: ").strip()
        if choice == "0":
            return
        elif choice in ["1", "2", "3"]:
            idx = int(choice) - 1
            difficulty = DIFFICULTY_LEVELS[idx]
            ui.clear_screen()
            ui.print_title(f"Quiz - {difficulty}")
            print(f"Hoeveel vragen wil je beantwoorden?")
            print(f"(standaard: {DEFAULT_NUM_QUESTIONS})\n")
            try:
                num = input("Aantal vragen (Enter voor standaard): ").strip()
                if num:
                    num_questions = int(num)
                    if num_questions < 1:
                        num_questions = DEFAULT_NUM_QUESTIONS
                else:
                    num_questions = DEFAULT_NUM_QUESTIONS
            except ValueError:
                num_questions = DEFAULT_NUM_QUESTIONS
            run_quiz_game(difficulty, num_questions)
        else:
            ui.print_warning("Ongeldige keuze!")
    except KeyboardInterrupt:
        ui.print_warning("\nTerug naar menu...")


def settings_menu():
    """Instellingen-menu."""
    while True:
        ui.clear_screen()
        ui.print_title("INSTELLINGEN")
        tts_status = "AAN" if tts.TTS_ENABLED else "UIT"
        options = [
            f"TTS (Tekst-naar-spraak): {tts_status}",
            "TTS testen",
            "Over dit spel",
            "Teruggaan",
        ]
        ui.print_menu("INSTELLINGEN", options)
        try:
            choice = input("Jouw keuze (1-4): ").strip()
            if choice == "1":
                toggle_tts()
            elif choice == "2":
                test_audio()
            elif choice == "3":
                show_about()
            elif choice == "4":
                break
            else:
                ui.print_warning("Ongeldige keuze!")
        except KeyboardInterrupt:
            break


def toggle_tts():
    """Toggle TTS aan/uit."""
    ui.clear_screen()
    if tts.TTS_ENABLED:
        ui.print_warning("TTS is momenteel AAN.")
        print("\nLet op: TTS is hardcoded in config.py.")
        print("Je kunt het hier niet wijzigen.")
    else:
        ui.print_info("TTS is momenteel UIT.")
        print("\nOm TTS aan te zetten, wijzig config.py:")
        print("  TTS_ENABLED = True")
    input("\nDruk Enter om terug te gaan...")


def test_audio():
    """Test TTS-functionaliteit."""
    ui.clear_screen()
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

            sys.exit(1)

                        ui.print_warning("Ongeldige keuze!")

        # Start menu

        sys.exit(0)

        import traceback
        sys.exit(1)def toggle_tts():    try:#      zodat de game automatisch start na autologin.



    """Toggle TTS aan/uit."""

if __name__ == "__main__":
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
        quiz = Quiz()
        if not quiz.questions:
            print("ERROR: Geen vragen geladen!")
            print("Controleer: vragen.csv")
            sys.exit(1)
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

    main()    ui.clear_screen()        choice = input("\nKeuze: ").strip()#    - Houd hier rekening mee: de code moet zich “netjes” gedragen in een pure TTY.


    

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
