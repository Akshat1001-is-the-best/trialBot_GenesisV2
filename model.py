import os
import subprocess
import speech_recognition as sr

def record_with_mic(duration=5, output_file="recording.aiff"):
    try:
        subprocess.run([
            "rec", "-q",  # Quiet mode
            output_file,
            "rate", "16000",  #for speech
            "channels", "1",   #mono
            "trim", "0", str(duration)
        ], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Requires 'sox'. Install with: brew install sox")
        return False

def live_speech_to_text():
    r = sr.Recognizer()
    
    while True:
        print("\nSpeak now (recording 5 seconds)...")
        if not record_with_mic(duration=5):
            break
            
        try:
            with sr.AudioFile("recording.aiff") as source:
                audio = r.record(source)
            text = r.recognize_google(audio)
            print("Text: ", text)
            return(text)
            
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("API unavailable")
        finally:
            os.remove("recording.aiff")

