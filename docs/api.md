# Backend API Documentation

This documentation provides an overview of the Flask API implemented in the Lipsync Backend application. The API allows users to merge audio and video files and retrieve uploaded files.

## Routes

### `/uploads/<filename>`

- **HTTP Method**: GET
- **Description**: This route allows users to retrieve uploaded files by specifying the filename.
- **Parameters**:
  - `filename` (str): The name of the file to retrieve.
- **Example Request**:
  ```
  GET /uploads/example.mp4
  ```
- **Example Response**:
  - The requested file will be sent as a response.

### `/api/merge`

- **HTTP Method**: POST
- **Description**: This route is used for merging audio and video files.
- **Parameters**:
  - `audio` (file): The audio file to be merged.
  - `video` (file): The video file to be merged.
- **Example Request**:
  ```
  POST /api/merge
  ```
  - Request Body:
    - `audio` (multipart/form-data): The audio file to be merged.
    - `video` (multipart/form-data): The video file to be merged.
- **Example Response**:
  - **Success Response (HTTP 200 OK)**:
    - Content-Type: application/json
    - Body:
      ```json
      {
        "videoPath": "/uploads/merged_video.mp4"
      }
      ```
    - Description: If the merge operation is successful, the API returns the path to the merged video file.
  - **Error Responses**:
    - HTTP 400 Bad Request:
      - Content-Type: application/json
      - Body:
        ```json
        {
          "error": "Missing audio or video file"
        }
        ```
      - Description: Returned when either the audio or video file is missing in the request.
    - HTTP 400 Bad Request:
      - Content-Type: application/json
      - Body:
        ```json
        {
          "error": "No selected file"
        }
        ```
      - Description: Returned when no files are selected in the request.
    - HTTP 400 Bad Request:
      - Content-Type: application/json
      - Body:
        ```json
        {
          "error": "File type not allowed"
        }
        ```
      - Description: Returned when the file type is not allowed for merging.
    - HTTP 404 Not Found:
      - Content-Type: application/json
      - Body:
        ```json
        {
          "error": "Output file not found."
        }
        ```
      - Description: Returned when the output file is not found after the merge operation.
    - HTTP 500 Internal Server Error:
      - Content-Type: application/json
      - Body:
        ```json
        {
          "error": "<error_message>"
        }
        ```
      - Description: Returned when an internal server error occurs during the merge operation.

## `app.py`

This script initializes the Flask application and defines a simple endpoint, used to determine if the backend is working:

- **Endpoint**: `/`
- **HTTP Method**: GET
- **Description**: This endpoint returns a JSON response with a welcome message.
- **Example Response**:
  ```json
  {
    "message": "Lipsync Backend API"
  }
  ```
