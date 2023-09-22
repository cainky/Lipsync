import unittest
from unittest.mock import patch, MagicMock
import os
from services import merge_service
from app import create_app


class TestMergeService(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.sample_audio_file = MagicMock(spec=["filename", "save"])
        self.sample_audio_file.filename = "test_audio.webm"

        self.sample_video_file = MagicMock(spec=["filename", "save"])
        self.sample_video_file.filename = "test_video.webm"

    def tearDown(self):
        self.ctx.pop()
        if os.path.exists("uploads/test_audio.webm"):
            os.remove("uploads/test_audio.webm")
        if os.path.exists("uploads/test_video.webm"):
            os.remove("uploads/test_video.webm")
        if os.path.exists("uploads/output.mp4"):
            os.remove("uploads/output.mp4")

    @patch("os.path.exists", return_value=True)
    @patch("os.remove")
    @patch("subprocess.run")
    def test_merge_audio_video(self, mock_run, mock_remove, mock_exists):
        mock_run.return_value = MagicMock(returncode=0)

        output_path = merge_service.merge_audio_video(
            self.sample_audio_file, self.sample_video_file
        )

        self.assertTrue(
            "output.mp4" in output_path, "Expected output.mp4 in the output path"
        )
        self.sample_audio_file.save.assert_called()
        self.sample_video_file.save.assert_called()

    @patch("os.path.exists", return_value=False)
    @patch("os.remove")
    @patch("subprocess.run")
    def test_merge_audio_video_failure(self, mock_run, mock_remove, mock_exists):
        mock_run.return_value = MagicMock(returncode=1, stderr="Error in Wav2Lip")

        with self.assertRaises(
            Exception, msg="Expected exception for failed video processing"
        ) as context:
            merge_service.merge_audio_video(
                self.sample_audio_file, self.sample_video_file
            )

        self.assertTrue(
            "Output video not found after processing" in str(context.exception)
        )
