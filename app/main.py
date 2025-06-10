# SillyScope: Oscilloscope Art Tone Generator WebApp Skeleton

import gradio as gr
import numpy as np
import sounddevice as sd
import threading

# Global state
audio_thread = None
is_playing = False

# Constants
SAMPLE_RATE = 44100

# Shape/vector data (simple example)
def generate_tone_from_vectors(vectors, duration=2):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    x = np.interp(t, np.linspace(0, duration, len(vectors)), [v[0] for v in vectors])
    y = np.interp(t, np.linspace(0, duration, len(vectors)), [v[1] for v in vectors])
    return np.stack([x, y], axis=-1)

def play_audio(vectors):
    global is_playing
    is_playing = True
    audio_data = generate_tone_from_vectors(vectors)
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

def draw_handler(img):
    # Placeholder: Convert img to vector list
    return [(0.1, 0.1), (0.2, 0.2), (0.3, 0.1), (0.1, 0.1)]

def clock_demo():
    # Placeholder clock shape
    return [(np.cos(a), np.sin(a)) for a in np.linspace(0, 2 * np.pi, 100)]

def cube_demo():
    # Placeholder 3D cube projected onto 2D
    return [(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]

def spaceship_demo():
    # Placeholder spaceship
    return [(0, 0), (0.5, 1), (1, 0), (0.5, -0.5), (0, 0)]

with gr.Blocks() as demo:
    with gr.Tab("Draw"):
        draw = gr.Sketchpad()
        start = gr.Button("Start (Spacebar)")
        stop = gr.Button("Stop")
        
        draw.change(fn=draw_handler, inputs=draw, outputs=None)
        start.click(fn=start_playback, inputs=draw.change(draw_handler), outputs=None)
        stop.click(fn=stop_playback)

    with gr.Tab("Demos"):
        clock = gr.Button("Clock")
        cube = gr.Button("Cube")
        ship = gr.Button("Spaceship")

        clock.click(lambda: start_playback(clock_demo()))
        cube.click(lambda: start_playback(cube_demo()))
        ship.click(lambda: start_playback(spaceship_demo()))

demo.launch()
