# Lipsync

A simple GUI app to synchronize recorded audio with video lip movements using the Wav2Lip model.

## Features

- **Audio Recording**: Record your own audio directly from the app.
- **Video Upload**: Upload a video of your choice.
- **Lip Synchronization**: Apply the audio recording to the video to make the lips match the speech.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cainky/Lipsync.git
   ```

2. Navigate to the repository directory:
   ```bash
   cd Lipsync
   ```

3. Install the required packages (assuming you have Python already installed):
   ```bash
   poetry install
   ```

4. Run the app:
   ```bash
   poetry run main.py
   ```

## Usage

1. **Record Audio**: Click the 'Record Audio' button and speak into your microphone.
2. **Record Video**: Click the 'Record Video' button and record a video clip.
3. **Sync**: Click the 'Sync' button and wait for the process to complete. Your output video will be saved in the 'outputs' directory.

## License

This project is licensed under the terms of the [MIT License.](https://github.com/cainky/Lipsync/blob/main/LICENSE)
