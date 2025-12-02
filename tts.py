tts.py - Text-to-Speech abstractie (espeak-ng)
Graceful degradatie op Windows (print alleen)

"""
tts.py - Text-to-Speech abstractie (espeak-ng)
Graceful degradatie op Windows (print alleen)
"""


import subprocess
import sys
import os
from config import TTS_ENABLED, TTS_LANG, TTS_VOICE, TTS_SPEED



def is_linux():
    """
    Controleer of we op Linux draaien.
    """
    return sys.platform.startswith("linux")



def speak(text, voice=None, speed=None):
    """
    Spreek tekst uit via espeak-ng (Linux) of simuleer op Windows.

    Args:
        text (str): Tekst om uit te spreken
        voice (str, optional): Stem (default: config.TTS_VOICE)
        speed (int, optional): Spreeksnelheid (default: config.TTS_SPEED)
    """
    if not TTS_ENABLED or not text or not text.strip():
        return
    voice = voice or TTS_VOICE
    speed = speed or TTS_SPEED
    if is_linux():
        try:
            cmd = [
                "espeak-ng",
                "-v", voice,
                "-s", str(speed),
                text
            ]
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            # espeak-ng niet geïnstalleerd of timeout
            pass
    else:
        # Windows: geen echte TTS, alleen simulatie
        print(f"[TTS] {text}")



def speak_question(question_text):
    """
    Spreek een vraag uit.

    Args:
        question_text (str): Vraagtekst
    """
    speak(question_text, voice=TTS_VOICE)



def speak_options(options):
    """
    Spreek antwoord-opties uit.

    Args:
        options (list): Lijst van optie-strings (A, B, C, D)
    """
    if not options:
        return
    for i, option in enumerate(options, 1):
        speak(f"Optie {chr(64 + i)}: {option}", speed=TTS_SPEED - 20)



def speak_feedback(is_correct, correct_answer=None):
    """
    Spreek feedback uit (goed/fout).

    Args:
        is_correct (bool): Was het antwoord correct?
        correct_answer (str, optional): Het juiste antwoord (als fout)
    """
    if is_correct:
        # Altijd "Goed zo!" voor consistentie
        speak("Goed zo!", speed=TTS_SPEED + 20)
    else:
        if correct_answer:
            text = f"Helaas, fout. Het juiste antwoord was {correct_answer}."
        else:
            text = "Helaas, dat is fout!"
        speak(text, speed=TTS_SPEED)



def speak_success_message(message):
    """
    Spreek een succes-boodschap uit.
    """
    speak(message, speed=TTS_SPEED + 10)



def speak_warning(text):
    """
    Spreek een waarschuwing uit.
    """
    speak(text, speed=TTS_SPEED - 10)



def test_tts():
    """
    Test TTS-functionaliteit.

    Returns:
        bool: True als TTS werkt, False anders
    """
    if not TTS_ENABLED:
        return False
    if not is_linux():
        print("[TTS] Windows gedetecteerd - TTS zal simuleren (geen werkelijk geluid)")
        return True
    test_text = "Dit is een test van de Sinterklaas console."
    try:
        subprocess.run(
            ["espeak-ng", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        print("[TTS] espeak-ng werkt! Testtekst wordt uitgesproken...")
        speak(test_text)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("[TTS] espeak-ng niet gevonden of timeout.")
        print("[TTS] Installeer espeak-ng: sudo apt-get install espeak-ng mbrola mbrola-nl2")
        return False
    except Exception as e:
        print(f"[TTS] Fout bij testen: {e}")
        return False
