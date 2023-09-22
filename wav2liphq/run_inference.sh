#!/bin/bash

# Set default values for environment variables
AUDIO_PATH=${AUDIO_PATH:-/app/wav2lip-hq/audio/default_audio.webm}
FACE_PATH=${FACE_PATH:-/app/wav2lip-hq/videos/default_face.webm}
OUTPUT_PATH=${OUTPUT_PATH:-/app/wav2lip-hq/results/default_output.mp4}

python inference.py \
    --audio "$AUDIO_PATH" \
    --face "$FACE_PATH" \
    --outfile "$OUTPUT_PATH" \
    "$@"
