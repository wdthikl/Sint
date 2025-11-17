"""
ui.py - ANSI-kleuren, ASCII-art en terminal UI helpers
"""

import os
import time
from config import COLORS


def clear_screen():
    """Scherm leegmaken (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


def print_reset():
    """Reset alle ANSI-opmaak."""
    print(COLORS["RESET"], end="")


def colored(text, color_name):
    """Tekst in kleur retourneren."""
    color = COLORS.get(color_name, "")
    reset = COLORS["RESET"]
    return f"{color}{text}{reset}"


def print_title(text):
    """Titel in blauw en vetgedrukt."""
    print(colored(f"\n{'='*50}", "CYAN"))
    print(colored(f"  {text.center(46)}", "CYAN"))
    print(colored(f"{'='*50}\n", "CYAN"))


def print_subtitle(text):
    """Subtitel in magenta."""
    print(colored(f"\n{text}", "MAGENTA"))
    print(colored("-" * len(text), "MAGENTA"))


def print_success(text):
    """Succesmessage in groen met vinkje."""
    print(colored(f"✓ {text}", "GREEN"))


def print_error(text):
    """Foutmessage in rood met kruisje."""
    print(colored(f"✗ {text}", "RED"))


def print_info(text):
    """Informatiemessage in blauw."""
    print(colored(f"ℹ {text}", "BLUE"))


def print_warning(text):
    """Waarschuwing in geel."""
    print(colored(f"⚠ {text}", "YELLOW"))


def print_box(text, color_name="CYAN", width=50):
    """Text in een mooi kader."""
    lines = text.split("\n")
    max_len = max(len(line) for line in lines) if lines else 0
    box_width = max(width, max_len + 4)
    
    border = colored("╔" + "═" * (box_width - 2) + "╗", color_name)
    print(border)
    
    for line in lines:
        padding = box_width - len(line) - 4
        content = colored(f"║ {line.ljust(box_width - 4)} ║", color_name)
        print(content)
    
    border = colored("╚" + "═" * (box_width - 2) + "╝", color_name)
    print(border)


def print_banner():
    """Grote Sinterklaas banner."""
    banner = r"""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║          🎄 SURPRISE SINTERKLAAS CONSOLE 🎄              ║
    ║                                                            ║
    ║              Welkom bij het spel van Sint!               ║
    ║                                                            ║
    ║              (❄️ Pak de cadeaus! ❄️)                      ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(colored(banner, "CYAN"))


def print_menu(title, options):
    """
    Menu weergeven met nummered opties.
    
    Args:
        title (str): Titel van het menu
        options (list): Lijst van optie-strings
    
    Voorbeeld:
        print_menu("Hoofdmenu", ["Quiz starten", "Afsluiten"])
    """
    print()
    print(colored("┌" + "─" * 48 + "┐", "CYAN"))
    print(colored(f"│  {title.center(44)}  │", "CYAN"))
    print(colored("├" + "─" * 48 + "┤", "CYAN"))
    
    for i, option in enumerate(options, 1):
        line = f"  {i}. {option}"
        print(colored(f"│{line.ljust(48)}│", "CYAN"))
    
    print(colored("└" + "─" * 48 + "┘", "CYAN"))
    print()


def animated_text(text, delay=0.05):
    """
    Tekst letter-voor-letter weergeven (animatie).
    
    Args:
        text (str): Text om te animeren
        delay (float): Vertraging tussen letters in seconden
    """
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def print_stars(count=50):
    """Decoratieve sterrenrij."""
    print(colored("★ " * (count // 2), "YELLOW"))


def print_divider(char="─", length=50):
    """Scheidingslijn."""
    print(colored(char * length, "CYAN"))


def progress_bar(current, total, width=30):
    """
    ASCII progress bar retourneren.
    
    Args:
        current (int): Huidge voortgang
        total (int): Totaal
        width (int): Breedte van de bar
    
    Returns:
        str: Progress bar als string
    """
    if total == 0:
        percentage = 0
    else:
        percentage = (current / total) * 100
    
    filled = int((current / total) * width)
    bar = "█" * filled + "░" * (width - filled)
    
    return f"[{bar}] {percentage:.1f}%"


def print_score_card(score_data):
    """
    Mooie scorekaart weergeven.
    
    Args:
        score_data (dict): Dict met:
            - 'questions': lijst van vraag-resultaten
            - 'total_score': totale punten
            - 'max_score': maximale punten
            - 'difficulty': moeilijkheidsniveau
    """
    questions = score_data.get('questions', [])
    total = score_data.get('total_score', 0)
    max_pts = score_data.get('max_score', 0)
    difficulty = score_data.get('difficulty', 'Normaal')
    
    print()
    print(colored("╔" + "═" * 56 + "╗", "MAGENTA"))
    print(colored(f"║{'📊 JE RESULTAAT 📊'.center(56)}║", "MAGENTA"))
    print(colored("╠" + "═" * 56 + "╣", "MAGENTA"))
    print(colored(f"║ Moeilijkheidsniveau: {difficulty.ljust(34)}║", "MAGENTA"))
    print(colored(f"║ Totaal: {total}/{max_pts} punten".ljust(57) + "║", "MAGENTA"))
    
    if max_pts > 0:
        percentage = (total / max_pts) * 100
        bar = progress_bar(total, max_pts, width=40)
        print(colored(f"║ {bar.ljust(55)}║", "MAGENTA"))
        print(colored(f"║ Percentage: {percentage:.1f}%".ljust(57) + "║", "MAGENTA"))
    
    print(colored("╠" + "═" * 56 + "╣", "MAGENTA"))
    
    # Vragen-overzicht
    for i, q_data in enumerate(questions, 1):
        is_correct = q_data.get('correct', False)
        icon = colored("✓", "GREEN") if is_correct else colored("✗", "RED")
        q_text = q_data.get('question', '')[:40]
        pts = q_data.get('points', 0)
        
        line = f"║ Vraag {i}: {icon} {q_text.ljust(37)} ({pts}pts)"
        print(colored(line.ljust(57) + "║", "MAGENTA"))
        
        if not is_correct:
            correct_ans = q_data.get('correct_answer', '?')
            hint = f"║   → Antwoord was: {correct_ans}".ljust(57) + "║"
            print(colored(hint, "RED"))
    
    print(colored("╠" + "═" * 56 + "╣", "MAGENTA"))
    
    # Eindcommentaar
    if max_pts > 0:
        percentage = (total / max_pts) * 100
        if percentage >= 90:
            comment = "🏆 Uitstekend gedaan! Sint is trots! 🏆"
            color = "GREEN"
        elif percentage >= 70:
            comment = "🎉 Prima prestatie! Goed bezig! 🎉"
            color = "YELLOW"
        elif percentage >= 50:
            comment = "👍 Niet slecht! Nog wat oefenen... 👍"
            color = "YELLOW"
        else:
            comment = "📚 Volgende keer beter! Je kunt het! 📚"
            color = "RED"
        
        print(colored(f"║ {comment.center(54)}║", color))
    
    print(colored("╚" + "═" * 56 + "╝", "MAGENTA"))
    print()


def print_ascii_santa():
    """ASCII Sinterklaas."""
    print(colored(r"""
         ,d88b.d88b,
         88888888888
         `Y8888888Y'
           `Y888Y'
             `Y'
            / \
           /   \
          /  |  \
         /  _|_  \
        /  | | |  \
       /   | | |   \
      /   /| | |\   \
     /   / | | | \   \
    /   /  | | |  \   \
   /   /   |_|_|   \   \
  /   /    |[---]|   \   \
 /   /     |[|||]|    \   \
/   /      |[|||]|     \   \
   /       |[---]|      \
  /        =========      \
 /__________________________\
    """, "RED"))


def print_ascii_gift():
    """ASCII Cadeau."""
    print(colored(r"""
    ╔════════════╗
    ║  🎁  🎁  🎁  ║
    ║  🎀────────║
    ║  🎁  GIFT  ║
    ║  🎁  🎁  🎁  ║
    ╚════════════╝
    """, "YELLOW"))
