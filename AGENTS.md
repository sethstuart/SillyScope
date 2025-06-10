# SillyScope Project - AGENTS.md

## Overview
**SillyScope** is a Gradio-based web application that allows users to create vector-based oscilloscope art by encoding 2D point data into stereo audio signals. The goal is to output these signals through a soundcard to an analog oscilloscope in X/Y mode, enabling dynamic line-art visualizations.

## Goals
- Enable mouse-drawing or image-upload workflows to generate shapes
- Convert user-generated or demo shapes into stereo waveforms
- Play waveforms as audio to produce real-time oscilloscope art
- Provide additional tone-generation tools for direct signal testing
- Offer built-in demos (clock, cube, spaceship, lissajous figures)
- Allow XY inversion toggle for better scope alignment

## Features
- **Draw Tab**: Draw or edit an image in `ImageEditor`, convert it to XY vectors, and play it on the oscilloscope.
- **Demos Tab**: Built-in procedurally generated shapes for fun and testing.
- **Tone Generator Tab**: Sine wave tone generator using musical pitch and octave.

## Current Implementation Status
- ✅ UI layout with three main tabs
- ✅ Audio playback of vectors using `sounddevice`
- ✅ Vector normalization and reordering
- ✅ Demo shapes implemented
- ✅ Tone generator working
- ⬜ Vectorization from images (`image_to_vectors`) is stubbed and needs OpenCV implementation
- ⬜ XY swap toggle not yet implemented

## Roadmap
### Phase 1 - MVP
- [x] Replace Sketchpad with ImageEditor for broader input types
- [x] Implement vector-to-audio path using normalized interpolation
- [x] Add demo shapes for validation
- [x] Add a basic tone generator tab
- [ ] Add checkbox to invert X and Y axes
- [ ] Complete `image_to_vectors(img)` using OpenCV edge detection

### Phase 2 - Visual Improvements
- [ ] Optimize point ordering using shortest-path strategies
- [ ] Add low-pass smoothing to waveform output
- [ ] Add toggle for sample rate and playback duration
- [ ] Implement blanking/jumping suppression if possible

### Phase 3 - Export & Share
- [ ] Allow download of WAV files
- [ ] Allow SVG import/export
- [ ] Persist or save vector art as demo

## Dev Setup
Always do the following before running:

python -m venv sillyscope
source sillyscope/bin/activate
pip install -r requirements.txt

Then launch the app:

python app/main.py

