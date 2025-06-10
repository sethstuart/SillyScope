# SillyScope: Oscilloscope Art Tone Generator WebApp Skeleton

import gradio as gr
import numpy as np
import sounddevice as sd
import threading
from oscilloscope_utils import vector_path_to_audio, reorder_path, image_to_vectors

# Global state
audio_thread = None
is_playing = False

# Constants
SAMPLE_RATE = 44100

# Playback

def play_audio(vectors):
    global is_playing
    is_playing = True
    audio_data = vector_path_to_audio(reorder_path(vectors))
    sd.play(audio_data, samplerate=SAMPLE_RATE, blocking=True)
    is_playing = False

def start_playback(vectors):
    global audio_thread, is_playing
    if not is_playing:
        audio_thread = threading.Thread(target=play_audio, args=(vectors,))
        audio_thread.start()

def stop_playback():
    global is_playing
    is_playing = False
    sd.stop()

# Drawing handler
def draw_handler(img):
    return image_to_vectors(img)

# Demos
def clock_demo():
    return [(np.cos(a), np.sin(a)) for a in np.linspace(0, 2 * np.pi, 100)]

def cube_demo():
    return [(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]

def spaceship_demo():
    return [(0, 0), (0.5, 1), (1, 0), (0.5, -0.5), (0, 0)]

# Tone Generator
def generate_tone(note, octave, duration):
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    sr = 48000
    a4_freq, tones_from_a4 = 440, 12 * (octave - 4) + (note - 9)
    frequency = a4_freq * 2 ** (tones_from_a4 / 12)
    duration = int(duration)
    audio = np.linspace(0, duration, duration * sr)
    audio = (20000 * np.sin(audio * (2 * np.pi * frequency))).astype(np.int16)
    return sr, audio

# Interface
with gr.Blocks() as demo:
    with gr.Tab("Draw"):
        editor = gr.ImageEditor()
        start = gr.Button("Start (Spacebar)")
        stop = gr.Button("Stop")

        editor.change(fn=draw_handler, inputs=editor, outputs=None)
        start.click(fn=start_playback, inputs=editor.change(draw_handler), outputs=None)
        stop.click(fn=stop_playback)

    with gr.Tab("Demos"):
        clock = gr.Button("Clock")
        cube = gr.Button("Cube")
        ship = gr.Button("Spaceship")

        clock.click(lambda: start_playback(clock_demo()))
        cube.click(lambda: start_playback(cube_demo()))
        ship.click(lambda: start_playback(spaceship_demo()))

    with gr.Tab("Tone Generator"):
        gr.Interface(
            fn=generate_tone,
            inputs=[
                gr.Dropdown(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"], type="index"),
                gr.Slider(4, 6, step=1),
                gr.Textbox(value="1", label="Duration in seconds"),
            ],
            outputs="audio"
        )

demo.launch()
