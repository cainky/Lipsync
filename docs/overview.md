# Lipsync - Technical Overview

Lipsync is a streamlined application designed to combine video and audio inputs to produce videos with accurately synchronized lip movements. At its core, the application leverages the power of the Wav2Lip-HQ model to achieve this synchronization.

## High-Level Architecture

### Frontend

The frontend is built using Vite+React, providing a user-friendly interface that allows users to:

1. Record audio.
2. Record video.
3. Merge the recorded audio and video to produce a single video with accurate lip movements.

Upon recording audio and video, the frontend sends the data to the backend Flask API for processing. Once processed, the final video is received and displayed on the frontend for the user.

### Backend

The backend is powered by Flask, a lightweight Python web framework. The backend handles several crucial tasks:

1. Receiving and saving audio and video recordings from the frontend.
2. Processing the recordings by:
    - Converting audio and video formats, if necessary.
    - Leveraging the Wav2Lip-HQ library to synchronize the video's lip movements with the provided audio.
3. Sending the processed video back to the frontend for user viewing.

The backend also utilizes the `ffmpeg` tool for media file conversions and operations.

### Wav2Lip-HQ Integration

The Wav2Lip-HQ model is a deep learning model trained to synchronize lip movements in videos based on the provided audio. The backend utilizes this model to produce videos with accurately synchronized lip movements.

## Docker Integration

For ease of deployment and ensuring consistent environments, Lipsync supports Docker containerization. With the provided Docker configurations:

1. The frontend and backend can be containerized into separate Docker containers.
2. These containers can be orchestrated together using `docker-compose`.

## How It All Comes Together

1. A user accesses the Lipsync application through a web browser.
2. They record audio and video through the frontend interface.
3. The frontend sends the recordings to the backend Flask API.
4. The backend processes the recordings, converting formats if necessary.
5. The Wav2Lip-HQ model is invoked to synchronize the video's lip movements with the audio.
6. The final synchronized video is sent back to the frontend.
7. The user can view and download the processed video from the frontend interface.

