import unittest, os
from unittest.mock import patch, MagicMock
from app import create_app
from werkzeug.datastructures import FileStorage


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.sample_audio_file = FileStorage(filename="test_audio.webm")
        self.sample_video_file = FileStorage(filename="test_video.webm")

    def tearDown(self):
        file_path = "uploads/existing_file.webm"
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                f.close()
            os.remove(file_path)

    def test_get_existing_upload_file(self):
        with open("uploads/existing_file.webm", "w") as f:
            f.write("dummy content")

        try:
            response = self.client.get("/uploads/existing_file.webm")
            self.assertEqual(response.status_code, 200)
        finally:
            os.remove("uploads/existing_file.webm")

    def test_get_non_existing_upload_file(self):
        response = self.client.get("/uploads/nonexistent_file.webm")
        self.assertEqual(response.status_code, 404)

    @patch("routes.merge_audio_video", return_value="uploads/output.mp4")
    @patch("pathlib.Path.is_file", return_value=True)
    def test_merge_with_valid_files(self, mock_is_file, mock_merge):
        data = {
            "audio": (self.sample_audio_file, "audio.webm"),
            "video": (self.sample_video_file, "video.webm"),
        }

        response = self.client.post(
            "/api/merge", content_type="multipart/form-data", data=data
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertIn("videoPath", response.json)

    def test_merge_missing_audio_or_video(self):
        data = {"audio": (self.sample_audio_file, "audio.webm")}
        response = self.client.post(
            "/api/merge", content_type="multipart/form-data", data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Missing audio or video file")

    def test_merge_empty_filenames(self):
        empty_audio_file = FileStorage(filename="")
        data = {
            "audio": (empty_audio_file, ""),
            "video": (self.sample_video_file, "video.webm"),
        }
        response = self.client.post(
            "/api/merge", content_type="multipart/form-data", data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "No selected file")

    def test_merge_disallowed_file_extensions(self):
        disallowed_audio_file = FileStorage(filename="audio.txt")
        data = {
            "audio": (disallowed_audio_file, "audio.txt"),
            "video": (self.sample_video_file, "video.webm"),
        }
        response = self.client.post(
            "/api/merge", content_type="multipart/form-data", data=data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "File type not allowed")

    def test_merge_error_during_process(self):
        error_msg_prefix = "Output video not found after processing."

        with patch(
            "services.merge_service.merge_audio_video",
            side_effect=Exception("Error: Command ffmpeg failed with return code 1."),
        ):
            data = {
                "audio": (self.sample_audio_file, "audio.webm"),
                "video": (self.sample_video_file, "video.webm"),
            }
            response = self.client.post(
                "/api/merge", content_type="multipart/form-data", data=data
            )

            self.assertEqual(response.status_code, 500)
            self.assertTrue(response.json["error"].startswith(error_msg_prefix))
