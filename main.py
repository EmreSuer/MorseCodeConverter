import tkinter as tk
from tkinter import messagebox
import pygame
import time
import threading

# Features to Include
#   User Input:
#     Accept input strings from the user.
#     Support letters, numbers, and basic punctuation (e.g., , . ?).
#   Morse Code Conversion:
#     Use a dictionary to map characters to Morse code.
#     Handle case-insensitivity (e.g., treat A and a the same).
#   Error Handling:
#     Inform the user if they enter unsupported characters.
#   Output:
#     Display the Morse code equivalent of the input string.
#     Optionally, save the result to a text file.
#   Optional Features:
#     Support reverse conversion (Morse code back to text).
#     Play Morse code audio (use a library like playsound or pydub).
#     Include a "help" option to explain the Morse code representation.



# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.',
    '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}

# Reverse Dictionary for Morse to Text
REVERSE_MORSE_CODE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}

# Initialize pygame for audio
pygame.mixer.init()

# Global flag for stopping audio playback
stop_audio_flag = False


# Load audio files
def load_audio_files():
    try:
        dot_sound = pygame.mixer.Sound("dot.wav")
        dash_sound = pygame.mixer.Sound("dash.wav")
        return dot_sound, dash_sound
    except FileNotFoundError:
        messagebox.showerror("Error", "Audio files are missing! Please ensure 'dot.wav' and 'dash.wav' exist.")
        return None, None


# Function to play Morse code as sound
def play_morse_code(morse_code, speed_factor):
    global stop_audio_flag
    dot_sound, dash_sound = load_audio_files()
    if not dot_sound or not dash_sound:
        return

    stop_audio_flag = False  # Reset stop flag at the beginning of playback
    for char in morse_code:
        if stop_audio_flag:
            break  # Stop playing if the stop flag is set
        if char == '.':
            dot_sound.play()  # Play dot sound (short beep)
            time.sleep(0.2 / speed_factor)  # Adjust timing based on speed
        elif char == '-':
            dash_sound.play()  # Play dash sound (long beep)
            time.sleep(0.6 / speed_factor)  # Adjust timing based on speed
        elif char == ' ':
            time.sleep(0.2 / speed_factor)  # Pause between characters
        elif char == '/':
            time.sleep(0.8 / speed_factor)  # Longer pause between words


# Function to convert text to Morse code
def text_to_morse(text):
    text = text.upper()
    morse_code = []
    for char in text:
        if char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char])
        else:
            return f"Error: Unsupported character '{char}'"
    return ' '.join(morse_code)


# Function to convert Morse code to text
def morse_to_text(morse_code):
    words = morse_code.split(' / ')  # Morse code words are separated by '/'
    decoded_text = []
    for word in words:
        characters = word.split()  # Characters are separated by spaces
        for char in characters:
            if char in REVERSE_MORSE_CODE_DICT:
                decoded_text.append(REVERSE_MORSE_CODE_DICT[char])
            else:
                return f"Error: Unsupported Morse code '{char}'"
        decoded_text.append(' ')  # Add a space between words
    return ''.join(decoded_text).strip()


# Function to start audio playback in a separate thread
def play_audio():
    global stop_audio_flag
    morse_code = output_box.get("1.0", tk.END).strip()
    if not morse_code:
        messagebox.showerror("Error", "No Morse code to play.")
        return
    # messagebox.showinfo("Audio Playback", "Playing Morse code...")
    stop_audio_flag = False
    speed_factor = speed_slider.get()  # Get the selected speed factor from the slider
    # Start a new thread to play audio so the GUI remains responsive
    threading.Thread(target=play_morse_code, args=(morse_code, speed_factor)).start()


# Function to stop audio playback
def stop_audio():
    global stop_audio_flag
    stop_audio_flag = True  # Set the stop flag to true to stop playback
    pygame.mixer.stop()  # Stop any currently playing sound


def show_help():
    help_text = """
    Morse Code is a system of encoding text characters using sequences of dots and dashes:

    A: .-     B: -...   C: -.-.   D: -..    E: .    F: ..-. 
    G: --.    H: ....   I: ..     J: .---   K: -.-    L: .-..
    M: --     N: -.     O: ---    P: .--.   Q: --.-   R: .-.
    S: ...    T: -      U: ..-    V: ...-   W: .--    X: -..-
    Y: -.--   Z: --..   1: .----  2: ..---  3: ...--  4: ....-
    5: .....  6: -....  7: --...  8: ---..  9: ----.  0: -----

    Special Characters:
    . : .-.-.-   , : --..--   ? : ..--..   - : -....-   / : -..-.
    Space between words: / 

    This application converts text to Morse code and vice versa.


    ! To convert a morse code into a text version, each character must be separated with SPACE.
    ! Likewise, each word must be separated with " / " to get a accurate result.

    Audio Speed is 1.0 by default. However can be modified by slider.
    """
    messagebox.showinfo("Morse Code Help", help_text)


# Tkinter GUI
def convert_to_morse():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Please enter text to convert.")
        return
    result = text_to_morse(text)
    if "Error" in result:
        messagebox.showerror("Conversion Error", result)
    else:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, result)
        messagebox.showinfo("Conversion Successful", "Text converted to Morse code successfully!")


def convert_to_text():
    morse_code = text_input.get("1.0", tk.END).strip()
    if not morse_code:
        messagebox.showerror("Error", "Please enter Morse code to convert.")
        return
    result = morse_to_text(morse_code)
    if "Error" in result:
        messagebox.showerror("Conversion Error", result)
    else:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, result)
        messagebox.showinfo("Conversion Successful", "Morse code converted to text successfully!")


# Create main window
root = tk.Tk()
root.title("Morse Code Converter")
root.geometry("600x450")

# Title Label
title_label = tk.Label(root, text="Morse Code Converter", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Input Text Area
input_label = tk.Label(root, text="Input:")
input_label.pack()
text_input = tk.Text(root, height=5, width=50)
text_input.pack(pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

to_morse_button = tk.Button(button_frame, text="Convert to Morse Code", command=convert_to_morse, bg="lightblue")
to_morse_button.grid(row=0, column=0, padx=10)

to_text_button = tk.Button(button_frame, text="Convert to Text", command=convert_to_text, bg="lightyellow")
to_text_button.grid(row=0, column=1, padx=10)

play_button = tk.Button(button_frame, text="Play Morse Code", command=play_audio, bg="lightgreen")
play_button.grid(row=0, column=2, padx=10)

stop_button = tk.Button(button_frame, text="Stop Audio", command=stop_audio, bg="red")
stop_button.grid(row=0, column=3, padx=10)

help_button = tk.Button(button_frame, text="Help", command=show_help, bg="Yellow")
help_button.grid(row=0, column=4, padx=10)

# Speed Control Slider
speed_label = tk.Label(root, text="Audio Speed:")
speed_label.pack(pady=5)

speed_slider = tk.Scale(root, from_=0.5, to_=2.0, orient=tk.HORIZONTAL, resolution=0.1)
speed_slider.set(1.0)  # Default speed is 1x
speed_slider.pack()

# Output Text Area
output_label = tk.Label(root, text="Output:")
output_label.pack()
output_box = tk.Text(root, height=5, width=50, state=tk.NORMAL)
output_box.pack(pady=5)

# Run the main loop
root.mainloop()
