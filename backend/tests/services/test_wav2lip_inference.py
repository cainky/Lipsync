import unittest
from unittest.mock import patch, MagicMock
from services.wav2lip_inference import run_wav2lip_inference


class TestWav2LipInference(unittest.TestCase):
    def setUp(self):
        self.face = "test_video.webm"
        self.audio = "test_audio.webm"
        self.outfile = "test_output.mp4"

    @patch("os.path.exists", return_value=True)
    @patch("subprocess.run")
    def test_successful_inference(self, mock_run, mock_exists):
        mock_run.return_value = MagicMock(returncode=0)

        output_path = run_wav2lip_inference(self.face, self.audio, self.outfile)

        self.assertEqual(output_path, self.outfile)
        cmd = [
            "python",
            "wav2lip-hq/inference.py",
            "--face",
            self.face,
            "--audio",
            self.audio,
            "--outfile",
            self.outfile,
            "--checkpoint_path",
            merge_service.CHECKPOINT_PATH,
            "--segmentation_path",
            merge_service.SEGMENTATION_PATH,
            "--sr_path",
            merge_service.SR_PATH,
        ]
        mock_run.assert_called_once_with(cmd, capture_output=True, text=True)

    @patch("os.path.exists", return_value=False)
    @patch("subprocess.run")
    def test_inference_output_not_found(self, mock_run, mock_exists):
        mock_run.return_value = MagicMock(returncode=0)

        with self.assertRaises(Exception) as context:
            run_wav2lip_inference(self.face, self.audio, self.outfile)

        self.assertTrue(
            "Output video not found after processing" in str(context.exception)
        )

    @patch("os.path.exists", return_value=True)
    @patch("subprocess.run")
    def test_inference_processing_failed(self, mock_run, mock_exists):
        mock_run.return_value = MagicMock(returncode=1, stderr="Error in Wav2Lip")

        with self.assertRaises(Exception) as context:
            run_wav2lip_inference(self.face, self.audio, self.outfile)

        self.assertTrue("Wav2Lip processing failed" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
