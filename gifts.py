"""
gifts.py - Cadeau-systeem voor Sinterklaas quiz
"""

import ui
import tts
from config import GIFT_MIN_PERCENTAGE


# ========== CADEAU DATABASE ==========
# Per moeilijkheidsniveau één cadeau
GIFTS = {
    "Makkelijk": {
        "name": "Pieten-danseres",
        "description": "Een leuke dansende piet-pop!",
        "emoji": "🎭",
        "ascii": r"""
        ╔═══════════════╗
        ║  🎭 PIET 🎭  ║
        ║   danseres    ║
        ║               ║
        ║   💃 ~ 💃 ~ 💃 ║
        ╚═══════════════╝
        """
    },
    "Normaal": {
        "name": "Goeie Boek met Gedichten",
        "description": "Een geheim boek vol grappige Sinterklaas-gedichten!",
        "emoji": "📚",
        "ascii": r"""
        ╔═══════════════╗
        ║  📚 BOEK 📚  ║
        ║  Gedichten    ║
        ║               ║
        ║  Sint's       ║
        ║  Geheimen     ║
        ╚═══════════════╝
        """
    },
    "Moeilijk": {
        "name": "Echte Sinterklaas-Hoed",
        "description": "Sint's beroemde rode hoed met goudstrik!",
        "emoji": "👒",
        "ascii": r"""
        ╔═══════════════╗
        ║  👒 HOED 👒  ║
        ║   van Sint    ║
        ║               ║
        ║    🎀 ~ 🎀    ║
        ║    (rood)     ║
        ╚═══════════════╝
        """
    }
}


def get_gift(difficulty):
    """
    Haal cadeau op voor gegeven moeilijkheidsniveau.
    
    Args:
        difficulty (str): 'Makkelijk', 'Normaal', of 'Moeilijk'
    
    Returns:
        dict: Gift-data of None als niet gevonden
    """
    return GIFTS.get(difficulty, None)


def check_gift_earned(total_score, max_score, difficulty):
    """
    Check of quiz-prestatie cadeau verdient.
    
    Args:
        total_score (int): Behaalde punten
        max_score (int): Maximale punten
        difficulty (str): Moeilijkheidsniveau
    
    Returns:
        dict: Gift-data als verdiend, None anders
    """
    if max_score == 0:
        return None
    
    percentage = (total_score / max_score) * 100
    
    # Check minimum percentage
    if percentage >= GIFT_MIN_PERCENTAGE:
        return get_gift(difficulty)
    
    return None


def show_gift_screen(gift):
    """
    Toon mooie gift-reveal screen.
    
    Args:
        gift (dict): Gift-data
    """
    if not gift:
        return
    
    ui.clear_screen()
    ui.print_title("🎁 JE HEBT EEN CADEAU VERDIEND! 🎁")
    print()
    
    # ASCII-art
    print(gift["ascii"])
    print()
    
    # Cadeau-naam en beschrijving
    ui.print_box(
        f"{gift['emoji']} {gift['name']} {gift['emoji']}\n\n{gift['description']}",
        color_name="YELLOW",
        width=50
    )
    print()
    
    # TTS
    message = f"Gefeliciteerd! Je hebt het volgende cadeau verdiend: {gift['name']}!"
    tts.speak_success_message(message)
    
    # Wacht op Enter
    input("Druk Enter om door te gaan...")


def show_no_gift_screen(total_score, max_score, min_percentage):
    """
    Toon boodschap als cadeau niet verdiend is.
    
    Args:
        total_score (int): Behaalde punten
        max_score (int): Maximale punten
        min_percentage (int): Minimaal benodigd percentage
    """
    ui.clear_screen()
    ui.print_title("😔 BIJNA! 😔")
    
    if max_score > 0:
        percentage = (total_score / max_score) * 100
        print(f"\nJe haalde {percentage:.1f}%")
        print(f"Je hebt minstens {min_percentage}% nodig voor een cadeau.\n")
    
    print("Probeer het volgende keer beter!")
    print("Sint geeft je nog een kans! 🎄\n")
    
    tts.speak("Volgende keer beter!")
    
    input("Druk Enter om terug te gaan...")


def show_gift_info():
    """
    Toon welke cadeaus je kan winnen per niveau.
    """
    ui.clear_screen()
    ui.print_title("🎁 CADEAUS PER NIVEAU")
    
    print(f"\nJe kunt cadeaus winnen met {GIFT_MIN_PERCENTAGE}% of hoger!\n")
    
    for level, gift in GIFTS.items():
        print(f"\n{level}:")
        print(f"  → {gift['emoji']} {gift['name']}")
        print(f"     {gift['description']}")
    
    print()
    input("Druk Enter om terug te gaan...")
