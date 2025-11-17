"""
minigames.py - Minigames: Roulette, Opdrachten, Soundboard
"""

import random
import ui
import tts
from quiz import Quiz
from config import POINTS_PER_QUESTION


def play_roulette():
    """
    Roulette-minigame: gok een willekeurige vraag van alle niveaus!
    """
    ui.clear_screen()
    ui.print_title("🎰 ROULETTE 🎰")
    
    print("""
    Sint stelt je UNO willekeurig gekozen vraag voor!
    Je hebt 3 kansen. Elk goed antwoord geeft je punten.
    """)
    
    quiz = Quiz()
    if not quiz.questions:
        ui.print_error("Geen vragen beschikbaar.")
        return
    
    total_score = 0
    chances = 3
    
    tts.speak("Welkom bij de roulette! Laten we beginnen!")
    
    for chance in range(chances):
        ui.clear_screen()
        ui.print_title(f"🎰 Roulette - Kans {chance + 1}/3")
        
        # Pak willekeurige vraag
        question = random.choice(quiz.questions)
        vraagtekst = question.get('vraagtekst', '').strip('"')
        juist_antwoord = question.get('juist_antwoord', '').strip()
        type_vraag = question.get('type', 'multiple').strip()
        moeilijkheid = question.get('moeilijkheid', 'Normaal').strip()
        
        print(f"Moeilijkheid: {moeilijkheid}\n")
        print(f"❓ {vraagtekst}\n")
        
        tts.speak_question(vraagtekst)
        
        # Verwerk antwoord
        if type_vraag == "tf":
            options_display = {
                'A': 'Waar',
                'B': 'Onwaar'
            }
            for k, v in options_display.items():
                print(f"  {k}. {v}")
            
            antwoord = input("\nJe antwoord (A/B): ").strip().upper()
            if antwoord not in ['A', 'B']:
                antwoord = ''
        else:
            for letter in ['A', 'B', 'C', 'D']:
                val = question.get(f'antwoord_{letter}', '').strip('"')
                if val:
                    print(f"  {letter}. {val}")
            
            antwoord = input("\nJe antwoord (A/B/C/D): ").strip().upper()
            if antwoord not in ['A', 'B', 'C', 'D']:
                antwoord = ''
        
        # Check antwoord
        is_correct = antwoord.upper() == juist_antwoord.upper()
        points = POINTS_PER_QUESTION.get(moeilijkheid, 1) if is_correct else 0
        
        print()
        if is_correct:
            ui.print_success(f"Correct! +{points} punten!")
            tts.speak_feedback(True)
            total_score += points
        else:
            ui.print_error(f"Fout! Het antwoord was {juist_antwoord}.")
            tts.speak_feedback(False, juist_antwoord)
        
        if chance < chances - 1:
            input("\nDruk Enter voor volgende vraag...")
    
    # Eindscherm
    ui.clear_screen()
    ui.print_title("🎰 Roulette VOORBIJ 🎰")
    print(f"\n✨ Je hebt {total_score} punten behaald! ✨\n")
    tts.speak_success_message(f"Je hebt {total_score} punten behaald!")
    input("Druk Enter om terug te gaan...")


def play_opdracht():
    """
    Opdracht-minigame: Sint geeft je grappige opdrachten!
    """
    ui.clear_screen()
    ui.print_title("📋 SINT'S OPDRACHTEN 📋")
    
    opdrachten = [
        "Zeg 'Sint is cool!' met een grappig accent!",
        "Maak het gekste geluid dat je kunt maken!",
        "Zeg je naam achteruit drie keer snel!",
        "Dans de Macarena (of iets geks) gedurende 10 seconden!",
        "Zeg de alphabet achteruit!",
        "Imiteer een Piet en zeg 'Ha ha ha!'",
        "Zing een stukje van een Sinterklaas-lied!",
        "Zeg 'Goedemorgen Sint!' zo hard mogelijk!",
        "Maak het gekste gezicht in de spiegel!",
        "Zeg tien maal achter elkaar 'Sint-Sinterklaas-Sint'!",
    ]
    
    print("\nSint gaat je een grappige opdracht geven!\n")
    input("Druk Enter...")
    
    # Kies willekeurige opdracht
    opdracht = random.choice(opdrachten)
    
    ui.clear_screen()
    ui.print_title("🎭 Je Opdracht")
    print(f"\n{opdracht}\n")
    
    # Spreek opdracht uit
    tts.speak(f"Je opdracht is: {opdracht}")
    
    # Wacht
    print("Druk Enter als je klaar bent...")
    input()
    
    # Random feedback
    feedback = [
        "Ha! Sint vindt je grappig!",
        "Mooi werk! Sint is trots!",
        "Briljant! Je bent een echte Piet!",
        "Geweldig gedaan! Sint lacht!",
        "Prima! Jij verdient een cadeautje!",
    ]
    
    ui.clear_screen()
    msg = random.choice(feedback)
    ui.print_success(msg)
    tts.speak_success_message(msg)
    
    input("\nDruk Enter om terug te gaan...")


def play_soundboard():
    """
    Soundboard-minigame: Luister naar grappige TTS-boodschappen van Sint!
    """
    ui.clear_screen()
    ui.print_title("🔊 SINT'S SOUNDBOARD 🔊")
    
    messages = [
        "Hallo! Ik ben Sint Nicolaas! Fijne Sinterklaas!",
        "Pas op! Piet ziet je!",
        "Wie stout is geweest, krijgt minder cadeaus!",
        "Je hoeft geen cadeaus in je schoen te eten!",
        "Mijn paard Amerigo zegt heehaw!",
        "Ik kom uit het goeie boek!",
        "De pieten helpen me altijd!",
        "Zie je de piet!",
        "Sint Nicolaas... Sint Nicolaas! Goedemorgen meneer Sint Nicolaas!",
        "Cadeaus! Cadeaus! Cadeaus!",
    ]
    
    print("\nZe mij een grappige boodschap van Sint!\n")
    
    for i, msg in enumerate(messages, 1):
        print(f"  {i}. {msg[:50]}...")
    
    print(f"\n  0. Teruggaan")
    
    while True:
        try:
            choice = input("\nWelke boodschap? (0-10): ").strip()
            choice = int(choice)
            
            if choice == 0:
                break
            elif 1 <= choice <= len(messages):
                ui.clear_screen()
                selected_msg = messages[choice - 1]
                print(f"\n🎤 {selected_msg}\n")
                tts.speak(selected_msg, speed=140)
                input("\nDruk Enter voor volgende...")
                
                # Toon menu opnieuw
                ui.clear_screen()
                ui.print_title("🔊 SINT'S SOUNDBOARD 🔊")
                print("\nZe mij een grappige boodschap van Sint!\n")
                for i, msg in enumerate(messages, 1):
                    print(f"  {i}. {msg[:50]}...")
                print(f"\n  0. Teruggaan")
            else:
                ui.print_warning("Keuze niet geldig!")
        except ValueError:
            ui.print_warning("Voer een getal in!")
    
    ui.clear_screen()


def show_minigames_menu():
    """Toon minigames-menu."""
    while True:
        ui.clear_screen()
        ui.print_banner()
        print()
        
        options = [
            "🎰 Roulette - Willekeurige vragen!",
            "📋 Sint's Opdrachten - Grappige taken!",
            "🔊 Soundboard - Grappige boodschappen!",
            "Teruggaan naar hoofdmenu",
        ]
        
        ui.print_menu("MINIGAMES", options)
        
        try:
            choice = input("Jouw keuze (1-4): ").strip()
            
            if choice == "1":
                play_roulette()
            elif choice == "2":
                play_opdracht()
            elif choice == "3":
                play_soundboard()
            elif choice == "4":
                break
            else:
                ui.print_warning("Ongeldige keuze!")
        except KeyboardInterrupt:
            ui.print_warning("\nTerug naar menu...")
            break
