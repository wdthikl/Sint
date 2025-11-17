"""
quiz.py - Quiz-engine met vraagverwerking, scoring en feedback
"""

import csv
import random
from config import (
    QUESTIONS_CSV,
    POINTS_PER_QUESTION,
    DIFFICULTY_LEVELS,
    TTS_REPEAT_KEY,
    GIFTS_ENABLED,
)
import ui
import tts
import gifts


class Quiz:
    """Quiz-engine."""
    
    def __init__(self):
        """Initialiseer quiz en laad vragen."""
        self.questions = []
        self.load_questions()
        self.current_question_idx = 0
        self.score_data = {
            'questions': [],
            'total_score': 0,
            'max_score': 0,
            'difficulty': 'Normaal',
        }
    
    def load_questions(self):
        """Laad vragen uit CSV."""
        try:
            with open(QUESTIONS_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.questions = list(reader)
            # print(f"[DEBUG] {len(self.questions)} vragen geladen")
        except FileNotFoundError:
            ui.print_error(f"Vragenbestand niet gevonden: {QUESTIONS_CSV}")
            self.questions = []
        except Exception as e:
            ui.print_error(f"Fout bij laden vragen: {e}")
            self.questions = []
    
    def get_questions_by_difficulty(self, difficulty, count=10):
        """
        Haal vragen op per moeilijkheidsniveau.
        
        Args:
            difficulty (str): 'Makkelijk', 'Normaal' of 'Moeilijk'
            count (int): Aantal vragen
        
        Returns:
            list: Geselecteerde vragen
        """
        filtered = [q for q in self.questions if q.get('moeilijkheid', '').strip() == difficulty]
        selected = random.sample(filtered, min(count, len(filtered)))
        return selected
    
    def run_quiz(self, difficulty="Normaal", num_questions=10):
        """
        Voer de quiz uit.
        
        Args:
            difficulty (str): Moeilijkheidsniveau
            num_questions (int): Aantal vragen
        """
        # Laad vragen voor dit niveau
        quiz_questions = self.get_questions_by_difficulty(difficulty, num_questions)
        
        if not quiz_questions:
            ui.print_error(f"Geen vragen gevonden voor niveau: {difficulty}")
            return
        
        # Reset score
        self.score_data = {
            'questions': [],
            'total_score': 0,
            'max_score': 0,
            'difficulty': difficulty,
        }
        
        # Bereken max punten
        points_per_q = POINTS_PER_QUESTION.get(difficulty, 1)
        self.score_data['max_score'] = len(quiz_questions) * points_per_q
        
        # Quiz starten
        ui.clear_screen()
        ui.print_title(f"Quiz - {difficulty}")
        print(f"\n📝 Je gaat {len(quiz_questions)} vragen beantwoorden.\n")
        
        input("Druk Enter om te starten...")
        
        # Loop door vragen
        for i, question_data in enumerate(quiz_questions, 1):
            ui.clear_screen()
            self._show_question(question_data, i, len(quiz_questions), difficulty)
    
    def _show_question(self, question_data, question_num, total_questions, difficulty):
        """
        Toon één vraag en verwerk antwoord.
        
        Args:
            question_data (dict): Vraag uit CSV
            question_num (int): Hudig vraagnummer
            total_questions (int): Totaal aantal vragen
            difficulty (str): Moeilijkheidsniveau
        """
        vraagtekst = question_data.get('vraagtekst', '').strip('"')
        type_vraag = question_data.get('type', 'multiple').strip()
        juist_antwoord = question_data.get('juist_antwoord', '').strip()
        
        # Toon vraag
        ui.print_title(f"Vraag {question_num}/{total_questions}")
        print(f"📌 {vraagtekst}\n")
        
        # Spreek vraag uit
        tts.speak_question(vraagtekst)
        
        # Toon opties en vraag invoer
        if type_vraag == "tf":
            # Waar/Onwaar
            antwoord = self._handle_tf_question(question_data)
        else:
            # Meerkeuze (A/B/C/D)
            antwoord = self._handle_multiple_choice(question_data)
        
        # Controleer antwoord
        is_correct = antwoord.upper() == juist_antwoord.upper()
        points = POINTS_PER_QUESTION.get(difficulty, 1) if is_correct else 0
        
        # Feedback tonen
        self._show_feedback(is_correct, juist_antwoord, question_data)
        
        # Voeg toe aan score
        self.score_data['questions'].append({
            'question': vraagtekst,
            'user_answer': antwoord,
            'correct_answer': juist_antwoord,
            'correct': is_correct,
            'points': points,
        })
        self.score_data['total_score'] += points
        
        # Wacht voordat volgende vraag
        if question_num < total_questions:
            input("\nDruk Enter voor volgende vraag...")
        else:
            input("\nDruk Enter voor je resultaat...")
    
    def _handle_multiple_choice(self, question_data):
        """
        Verwerk meerkeuzevraag (A/B/C/D).
        
        Returns:
            str: Gekozen antwoord (A/B/C/D)
        """
        options = {
            'A': question_data.get('antwoord_A', '').strip('"'),
            'B': question_data.get('antwoord_B', '').strip('"'),
            'C': question_data.get('antwoord_C', '').strip('"'),
            'D': question_data.get('antwoord_D', '').strip('"'),
        }
        
        # Toon opties
        for key, value in options.items():
            print(f"  {key}. {value}")
        
        print(f"\nTip: Druk '{TTS_REPEAT_KEY}' om de vraag te herhalen")
        
        # Wacht op invoer
        while True:
            try:
                antwoord = input("\nJe antwoord (A/B/C/D): ").strip().upper()
                
                if antwoord == TTS_REPEAT_KEY.upper():
                    # Herhaal vraag
                    vraagtekst = question_data.get('vraagtekst', '').strip('"')
                    tts.speak_question(vraagtekst)
                    print("\n(Vraag herhaald via TTS)")
                    continue
                
                if antwoord in ['A', 'B', 'C', 'D']:
                    return antwoord
                else:
                    ui.print_warning("Voer A, B, C of D in!")
            except KeyboardInterrupt:
                ui.print_warning("\nQuiz afgebroken.")
                return None
    
    def _handle_tf_question(self, question_data):
        """
        Verwerk waar/onwaar vraag.
        
        Returns:
            str: 'A' (Waar) of 'B' (Onwaar)
        """
        print("  A. Waar")
        print("  B. Onwaar")
        print(f"\nTip: Druk '{TTS_REPEAT_KEY}' om de vraag te herhalen")
        
        while True:
            try:
                antwoord = input("\nJe antwoord (A/B): ").strip().upper()
                
                if antwoord == TTS_REPEAT_KEY.upper():
                    vraagtekst = question_data.get('vraagtekst', '').strip('"')
                    tts.speak_question(vraagtekst)
                    print("\n(Vraag herhaald via TTS)")
                    continue
                
                if antwoord in ['A', 'B']:
                    return antwoord
                else:
                    ui.print_warning("Voer A of B in!")
            except KeyboardInterrupt:
                ui.print_warning("\nQuiz afgebroken.")
                return None
    
    def _show_feedback(self, is_correct, correct_answer, question_data):
        """
        Toon feedback op antwoord.
        
        Args:
            is_correct (bool): Was antwoord correct?
            correct_answer (str): Het juiste antwoord
            question_data (dict): Vraagdata
        """
        print()
        
        if is_correct:
            ui.print_success("Dat is correct!")
            tts.speak_feedback(True)
        else:
            ui.print_error(f"Helaas, dat is fout!")
            print(f"Het juiste antwoord was: {correct_answer}")
            tts.speak_feedback(False, correct_answer)
        
        print()
    
    def show_final_score(self):
        """Toon eindscore en check cadeaus."""
        ui.clear_screen()
        ui.print_score_card(self.score_data)
        
        # Spreek succes uit
        total = self.score_data['total_score']
        max_pts = self.score_data['max_score']
        difficulty = self.score_data['difficulty']
        
        if max_pts > 0:
            percentage = (total / max_pts) * 100
            if percentage >= 90:
                tts.speak_success_message("Uitstekend gedaan! Sint is trots op je!")
            elif percentage >= 70:
                tts.speak_success_message("Prima prestatie! Goed bezig!")
        
        # Check cadeau
        if GIFTS_ENABLED:
            self._check_and_show_gift(total, max_pts, difficulty)
    
    def _check_and_show_gift(self, total_score, max_score, difficulty):
        """
        Check en toon cadeau als verdiend.
        
        Args:
            total_score (int): Behaalde punten
            max_score (int): Maximale punten
            difficulty (str): Moeilijkheidsniveau
        """
        earned_gift = gifts.check_gift_earned(total_score, max_score, difficulty)
        
        if earned_gift:
            # Cadeau verdiend!
            gifts.show_gift_screen(earned_gift)
        else:
            # Niet genoeg punten
            gifts.show_no_gift_screen(
                total_score, 
                max_score,
                gifts.GIFT_MIN_PERCENTAGE
            )


def run_quiz_game(difficulty="Normaal", num_questions=10):
    """
    Wrapper-functie om quiz te starten.
    
    Args:
        difficulty (str): Moeilijkheidsniveau
        num_questions (int): Aantal vragen
    """
    quiz = Quiz()
    quiz.run_quiz(difficulty, num_questions)
    quiz.show_final_score()
