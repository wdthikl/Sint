"""
main.py - Entry point van de Surprise Sinterklaas Console Game
Hoofd-event-loop en menu's
"""

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
            "Onderhoudsmenu (vragen beheren)",  # Toegevoegd als optie 7
        ]
        ui.print_menu("HOOFDMENU", options)
        print()
        try:
            choice = input("Jouw keuze (1-7): ").strip()
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
            elif choice == "7":
                show_maintenance_menu()
            else:
                ui.print_warning("Ongeldige keuze! Kies 1-7.")
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
            print(f"Controleer: vragen.csv")
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
