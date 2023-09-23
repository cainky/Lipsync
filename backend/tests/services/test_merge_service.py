import unittest
from unittest.mock import patch, MagicMock
import os
from services import merge_service
from app import create_app


class TestMergeService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.pop()

    def setUp(self):
        self.sample_audio_file = MagicMock(spec=["filename", "save"])
        self.sample_audio_file.filename = "test_audio.webm"
        self.sample_video_file = MagicMock(spec=["filename", "save"])
        self.sample_video_file.filename = "test_video.webm"

    def tearDown(self):
        # Using a list of paths to make future additions easier
        paths_to_remove = [
            "uploads/test_audio.webm",
            "uploads/test_video.webm",
            "uploads/output.mp4",
        ]
        for path in paths_to_remove:
            if os.path.exists(path):
                os.remove(path)

    @patch("os.path.exists", return_value=True)
    @patch("os.remove")
    @patch("subprocess.run")
    def test_merge_audio_video(self, mock_run, mock_remove, mock_exists):
        mock_run.return_value = MagicMock(returncode=0)

        output_path = merge_service.merge_audio_video(
            self.sample_audio_file, self.sample_video_file
        )

        self.assertIn(
            "output.mp4", output_path, "The output path should contain 'output.mp4'"
        )
        expected_audio_path = os.path.join(
            os.getcwd(), "uploads", merge_service.DEFAULT_AUDIO_FILENAME
        )
        self.sample_audio_file.save.assert_called_with(expected_audio_path)

        expected_video_path = os.path.join(
            os.getcwd(), "uploads", merge_service.DEFAULT_VIDEO_FILENAME
        )
        self.sample_video_file.save.assert_called_with(expected_video_path)

    @patch("os.path.exists", return_value=False)
    @patch("os.remove")
    @patch("subprocess.run")
    def test_merge_audio_video_failure(self, mock_run, mock_remove, mock_exists):
        mock_run.return_value = MagicMock(returncode=1, stderr="Error in Wav2Lip")

        with self.assertRaisesRegex(
            Exception, "Error:"
        ):
            merge_service.merge_audio_video(
                self.sample_audio_file, self.sample_video_file
            )

    @patch("os.path.exists", return_value=False)
    @patch("os.remove")
    @patch("services.wav2lip_inference.run_command")
    def test_merge_audio_video_with_invalid_audio_format(
        self, mock_run_command, mock_remove, mock_exists
    ):
        mock_run_command.side_effect = Exception("Invalid audio format")
        # Use a non-webm audio file to simulate an invalid format
        self.sample_audio_file.filename = "test_audio.mp3"

        with self.assertRaisesRegex(Exception, "Invalid audio format"):
            merge_service.merge_audio_video(
                self.sample_audio_file, self.sample_video_file
            )
