# Overview

In this technical assessment, you will build a full-stack application that includes a single-page front-end application using React and a backend API using Python and Flask. The application aims to demonstrate your ability to work with various libraries and frameworks.

## Objective

Create an application that allows a user to perform three types of recordings:
1. A regular video recording used for training the Wav2Lip model.
2. A video-only recording.
3. An audio-only recording.

After these recordings are completed, your application should use a Flask backend API to combine the audio-only and video-only recordings into a single video using the Wav2lip-hq library.

**Note:** You can use additional libraries or packages to complete this assessment.

## Requirements

### Frontend:
- **Setup React App:** Create a new React application using Create React App or your preferred setup.
- **User Interface:** Develop a simple user interface with three buttons, each corresponding to the three types of recordings mentioned above.
- **Recording:** Use the React-media-recorder library to handle video and audio recording.
- **Sending Data:** Once each recording is finished, send the data to the Flask backend for processing. Use POST requests to upload the files.
- **Receiving Data:** Upon the backend completing processing, receive and display the final combined video on the frontend.

### Backend:
- **Setup Flask App:** Create a new Flask application with at least one API endpoint to handle the file upload and processing.
- **File Upload:** Receive the uploaded files from the frontend, and save them in a specific directory.
- **Processing:** Use the Wav2lip-hq library to combine the audio-only and video-only files into a single video.
- **Response:** Once the video is generated, send a response back to the frontend to confirm the process completion, including the final video.

### Bonus:
- Implement a progress bar during video processing.
- Use Docker for the application deployment.

## Submission

Your submission should include:
- All source code used to implement the full-stack application.
- A README file that explains how to run and test your service. Please also include basic API documentation.

## Evaluation Criteria

We'll evaluate your solution based on:
- **Correctness:** Does the solution accomplish the stated objectives?
- **Code quality:** Is the code organized, and can it be easily understood?
- **Testing:** Is the code adequately tested?
- **Documentation:** Is the service and its API well-documented?
