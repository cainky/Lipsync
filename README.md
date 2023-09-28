# Lipsync

A simple GUI app to synchronize recorded audio with video lip movements using the Wav2Lip-HQ model.

## Features

- **Live Recording**: Record your own audio and video directly from the app.
- **Lip Synchronization**: Automatically apply the audio recording to the video to make the lips match the speech.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cainky/Lipsync.git
   ```

2. Navigate to the repository directory:
   ```bash
   cd Lipsync
   ```

3. Make sure you put the necessary model files into backend/wav2lip-hq/checkpoints as described in the [wav2lip-hq directory](https://github.com/Markfryazino/wav2lip-hq)

4. Make sure to create a Python 3.7 virtual environment for wav2lip-hq using the following steps:
```bash
cd backend/wav2lip-hq
```
```bash
pyenv install 3.7.0
pyenv local 3.7.0
python -m venv wav2lipenv
```

5. Install the requirements in the virtualenv
```bash
wav2lipenv/bin/python -m pip install -r requirements.txt
```

6. Change directory back to backend, install Poetry and the required packages for the backend (assuming you have Python already installed):
   ```bash
   deactivate
   cd ..
   curl -sSL https://install.python-poetry.org | python3 -
   poetry install
   ```
   
7. Run the backend app:
   ```bash
   poetry run app.py
   ```
   
8. Install the required packages for the frontend (assuming you have npm already installed)
   ```bash
   cd ../frontend
   npm install
   ```
9. Make an .env file. You can copy the .env.example file and rename it to .env as a starting point

10. Run the frontend app:
   ```bash
   npm run build
   npm run dev
   ```

Frontend will be at http://localhost:5173
Backend will be at http://localhost:5000

## Docker
- In the root project directory, run
```bash
docker-compose build
docker-compose up
```

- Frontend container is at http://localhost:3000
- Backend container is at http://localhost:5000


## Usage

1. **Record Audio**: Click the 'Record Audio' button and speak into your microphone.
2. **Record Video**: Click the 'Record Video' button and record a video clip.
3. **Merge Recordings**: Click the 'Merge Recordings' button and wait for the process to complete. Your output video will be appear when it's ready.

## License

This project is licensed under the terms of the [MIT License.](https://github.com/cainky/Lipsync/blob/main/LICENSE)
