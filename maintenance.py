
"""
maintenance.py - Vraagbeheer (CRUD) met Ctrl+M hotkey
"""


import csv
import os
import ui
import tts
from config import QUESTIONS_CSV, DIFFICULTY_LEVELS


class QuestionManager:
    """
    Beheer vragen in CSV.
    """
    
    def __init__(self):
        """
        Initialiseer question manager.
        """
        self.questions = []
        self.load_questions()
    
    def load_questions(self):
        """
        Laad vragen uit CSV.
        """
        try:
            with open(QUESTIONS_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.questions = list(reader)
        except FileNotFoundError:
            self.questions = []
    
    def save_questions(self):
        """
        Sla vragen op naar CSV.
        """
        try:
            fieldnames = [
                'vraagtekst', 'antwoord_A', 'antwoord_B', 'antwoord_C', 'antwoord_D',
                'juist_antwoord', 'type', 'moeilijkheid'
            ]
            
            with open(QUESTIONS_CSV, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.questions)
            
            ui.print_success(f"✓ Vragen opgeslagen naar {QUESTIONS_CSV}")
            return True
        except Exception as e:
            ui.print_error(f"Fout bij opslaan: {e}")
            return False
    
    def add_question(self):
        """
        Voeg interactief een nieuwe vraag toe.
        """
        ui.clear_screen()
        ui.print_title("➕ NIEUWE VRAAG TOEVOEGEN")
        
        # Vraag type
        print("\nVraagtype:")
        print("  1. Meerkeuze (A/B/C/D)")
        print("  2. Waar/Onwaar")
        
        while True:
            q_type = input("\nKeuze (1-2): ").strip()
            if q_type in ["1", "2"]:
                break
            ui.print_warning("Kies 1 of 2!")
        
        question_type = "multiple" if q_type == "1" else "tf"
        
        # Moeilijkheid
        print("\nMoeilijkheidsniveau:")
        for i, level in enumerate(DIFFICULTY_LEVELS, 1):
            print(f"  {i}. {level}")
        
        while True:
            diff_choice = input("\nKeuze (1-3): ").strip()
            if diff_choice in ["1", "2", "3"]:
                break
            ui.print_warning("Kies 1, 2 of 3!")
        
        difficulty = DIFFICULTY_LEVELS[int(diff_choice) - 1]
        
        # Vraagtekst
        print()
        vraagtekst = input("Vraagtekst: ").strip()
        if not vraagtekst:
            ui.print_warning("Vraagtekst mag niet leeg zijn!")
            return False
        
        new_question = {
            'vraagtekst': f'"{vraagtekst}"',
            'antwoord_A': '',
            'antwoord_B': '',
            'antwoord_C': '',
            'antwoord_D': '',
            'juist_antwoord': '',
            'type': question_type,
            'moeilijkheid': difficulty,
        }
        
        if question_type == "multiple":
            # Meerkeuze: 4 antwoorden
            print("\nAntwoorden (A, B, C, D):")
            for letter in ['A', 'B', 'C', 'D']:
                ans = input(f"  Antwoord {letter}: ").strip()
                new_question[f'antwoord_{letter}'] = f'"{ans}"' if ans else ''
            
            # Juiste antwoord
            while True:
                correct = input("\nJuiste antwoord (A/B/C/D): ").strip().upper()
                if correct in ['A', 'B', 'C', 'D']:
                    new_question['juist_antwoord'] = correct
                    break
                ui.print_warning("Voer A, B, C of D in!")
        
        else:
            # Waar/Onwaar
            print("\n  A. Waar")
            print("  B. Onwaar")
            
            while True:
                correct = input("\nJuiste antwoord (A/B): ").strip().upper()
                if correct in ['A', 'B']:
                    new_question['juist_antwoord'] = correct
                    break
                ui.print_warning("Voer A of B in!")
        
        # Voeg toe aan list
        self.questions.append(new_question)
        
        # Toon preview
        ui.clear_screen()
        ui.print_success("✓ Vraag toegevoegd!")
        print()
        self._show_question_preview(new_question)
        
        # Sla op
        if self.save_questions():
            tts.speak("Vraag opgeslagen!")
            input("\nDruk Enter om terug te gaan...")
            return True
        
        return False
    
    def list_questions(self):
        """
        Toon alle vragen.
        """
        ui.clear_screen()
        ui.print_title(f"📋 ALLE VRAGEN ({len(self.questions)} totaal)")
        
        if not self.questions:
            ui.print_warning("Geen vragen gevonden!")
            input("\nDruk Enter...")
            return
        
        # Groepeer per moeilijkheid
        for difficulty in DIFFICULTY_LEVELS:
            questions_in_level = [q for q in self.questions 
                                 if q.get('moeilijkheid', '').strip() == difficulty]
            
            if questions_in_level:
                print(f"\n{difficulty}:")
                print("─" * 60)
                
                for i, q in enumerate(questions_in_level, 1):
                    vraagtekst = q.get('vraagtekst', '').strip('"')
                    q_type = q.get('type', '').strip()
                    
                    type_emoji = "🔘" if q_type == "multiple" else "⚪"
                    print(f"  {i}. {type_emoji} {vraagtekst[:50]}...")
        
        print()
        input("Druk Enter om terug te gaan...")
    
    def delete_question(self):
        """
        Verwijder een vraag.
        """
        ui.clear_screen()
        ui.print_title("🗑️  VRAAG VERWIJDEREN")
        
        if not self.questions:
            ui.print_warning("Geen vragen om te verwijderen!")
            input("\nDruk Enter...")
            return
        
        # Toon vragen
        print("\nSelecteer vraag om te verwijderen:\n")
        for i, q in enumerate(self.questions, 1):
            vraagtekst = q.get('vraagtekst', '').strip('"')
            print(f"  {i}. {vraagtekst[:50]}...")
        
        print(f"\n  0. Annuleren")
        
        while True:
            try:
                choice = input("\nKeuze: ").strip()
                if choice == "0":
                    return False
                
                idx = int(choice) - 1
                if 0 <= idx < len(self.questions):
                    break
                else:
                    ui.print_warning("Ongeldige keuze!")
            except ValueError:
                ui.print_warning("Voer een getal in!")
        
        # Bevestiging
        question_to_delete = self.questions[idx]
        vraagtekst = question_to_delete.get('vraagtekst', '').strip('"')
        
        print(f"\nWil je echt verwijderen?\n  '{vraagtekst}'")
        confirm = input("\nBevestig (j/n): ").strip().lower()
        
        if confirm == 'j':
            self.questions.pop(idx)
            ui.print_success("✓ Vraag verwijderd!")
            
            if self.save_questions():
                tts.speak("Vraag verwijderd!")
                input("\nDruk Enter...")
                return True
        else:
            ui.print_warning("Annuleren...")
            input("\nDruk Enter...")
            return False
    
    def edit_question(self):
        """
        Wijzig een bestaande vraag.
        """
        ui.clear_screen()
        ui.print_title("✏️  VRAAG WIJZIGEN")
        
        if not self.questions:
            ui.print_warning("Geen vragen om te wijzigen!")
            input("\nDruk Enter...")
            return
        
        # Selecteer vraag
        print("\nSelecteer vraag:\n")
        for i, q in enumerate(self.questions, 1):
            vraagtekst = q.get('vraagtekst', '').strip('"')
            print(f"  {i}. {vraagtekst[:50]}...")
        
        print(f"\n  0. Annuleren")
        
        while True:
            try:
                choice = input("\nKeuze: ").strip()
                if choice == "0":
                    return False
                
                idx = int(choice) - 1
                if 0 <= idx < len(self.questions):
                    break
                else:
                    ui.print_warning("Ongeldige keuze!")
            except ValueError:
                ui.print_warning("Voer een getal in!")
        
        question = self.questions[idx]
        ui.clear_screen()
        ui.print_title("✏️  WIJZIGEN")
        
        # Toon huidge waarde
        self._show_question_preview(question)
        
        print("\n\nWat wil je wijzigen?")
        print("  1. Vraagtekst")
        print("  2. Antwoorden")
        print("  3. Juiste antwoord")
        print("  4. Moeilijkheid")
        print("  0. Annuleren")
        
        choice = input("\nKeuze: ").strip()
        
        if choice == "1":
            new_text = input("\nNieuwe vraagtekst: ").strip()
            if new_text:
                question['vraagtekst'] = f'"{new_text}"'
        
        elif choice == "2":
            if question.get('type', '').strip() == "multiple":
                print("\nNieuwe antwoorden (laat leeg om ongewijzigd te houden):")
                for letter in ['A', 'B', 'C', 'D']:
                    old = question.get(f'antwoord_{letter}', '').strip('"')
                    new = input(f"  Antwoord {letter} [{old}]: ").strip()
                    if new:
                        question[f'antwoord_{letter}'] = f'"{new}"'
        
        elif choice == "3":
            q_type = question.get('type', '').strip()
            if q_type == "multiple":
                valid = ['A', 'B', 'C', 'D']
            else:
                valid = ['A', 'B']
            
            while True:
                new_ans = input(f"\nNieuwe juiste antwoord ({'/'.join(valid)}): ").strip().upper()
                if new_ans in valid:
                    question['juist_antwoord'] = new_ans
                    break
                ui.print_warning(f"Voer {'/'.join(valid)} in!")
        
        elif choice == "4":
            print("\nNieuw moeilijkheidsniveau:")
            for i, level in enumerate(DIFFICULTY_LEVELS, 1):
                print(f"  {i}. {level}")
            
            while True:
                diff_choice = input("\nKeuze (1-3): ").strip()
                if diff_choice in ["1", "2", "3"]:
                    question['moeilijkheid'] = DIFFICULTY_LEVELS[int(diff_choice) - 1]
                    break
                ui.print_warning("Kies 1, 2 of 3!")
        
        else:
            ui.print_warning("Annuleren...")
            input("\nDruk Enter...")
            return False
        
        ui.clear_screen()
        ui.print_success("✓ Vraag gewijzigd!")
        print()
        self._show_question_preview(question)
        
        if self.save_questions():
            tts.speak("Vraag bijgewerkt!")
            input("\nDruk Enter...")
            return True
        
        return False
    
    def _show_question_preview(self, question):
        """
        Toon preview van vraag.
        """
        vraagtekst = question.get('vraagtekst', '').strip('"')
        q_type = question.get('type', '').strip()
        difficulty = question.get('moeilijkheid', '').strip()
        correct = question.get('juist_antwoord', '').strip()
        
        print(f"\n📌 {vraagtekst}")
        print(f"   Type: {q_type} | Niveau: {difficulty}")
        
        if q_type == "multiple":
            print("\n   Opties:")
            for letter in ['A', 'B', 'C', 'D']:
                ans = question.get(f'antwoord_{letter}', '').strip('"')
                marker = "✓" if letter == correct else " "
                print(f"     [{marker}] {letter}. {ans}")
        else:
            print("\n   Opties:")
            print(f"     [{'✓' if correct == 'A' else ' '}] A. Waar")
            print(f"     [{'✓' if correct == 'B' else ' '}] B. Onwaar")



def show_maintenance_menu():
    """
    Toon maintenance menu.
    """
    manager = QuestionManager()
    while True:
        ui.clear_screen()
        ui.print_title("🔧 ONDERHOUDSMENU - VRAAGBEHEER")
        options = [
            "Nieuwe vraag toevoegen",
            "Alle vragen tonen",
            "Vraag wijzigen",
            "Vraag verwijderen",
            "Teruggaan naar hoofdmenu",
        ]
        ui.print_menu("ONDERHOUD", options)
        try:
            choice = input("Keuze (1-5): ").strip()
            if choice == "1":
                manager.add_question()
            elif choice == "2":
                manager.list_questions()
            elif choice == "3":
                manager.edit_question()
            elif choice == "4":
                manager.delete_question()
            elif choice == "5":
                break
            else:
                ui.print_warning("Ongeldige keuze!")
        except KeyboardInterrupt:
            ui.print_warning("\nTeruggaan naar menu...")
            break
