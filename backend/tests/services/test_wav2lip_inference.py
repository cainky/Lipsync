import unittest, os, subprocess
from unittest.mock import patch, MagicMock
from services.wav2lip_inference import (
    run_wav2lip_inference,
    CHECKPOINT_PATH,
    SEGMENTATION_PATH,
    SR_PATH,
)
from services import merge_service


class TestWav2LipInference(unittest.TestCase):
    def setUp(self):
        self.face = "test_video.webm"
        self.audio = "test_audio.webm"
        self.outfile = "test_output.mp4"

    def tearDown(self):
        # Clean up any files that might have been created
        if os.path.exists(self.face):
            os.remove(self.face)
        if os.path.exists(self.audio):
            os.remove(self.audio)
        if os.path.exists(self.outfile):
            os.remove(self.outfile)

    @patch("services.wav2lip_inference.os.remove")
    @patch(
        "services.wav2lip_inference.os.path.join",
        side_effect=lambda *args: "/".join(args),
    )
    @patch("os.path.exists", return_value=True)
    @patch("subprocess.run")
    def test_wav2lip_inference_successful(
        self, mock_run, mock_exists, mock_path_join, mock_remove
    ):
        mock_run.return_value = MagicMock(returncode=0)

        output_path = run_wav2lip_inference(self.face, self.audio, self.outfile)

        self.assertEqual(
            output_path, self.outfile, "Expected output path to match outfile path"
        )

        # Verify audio conversion
        audio_conversion_cmd = ["ffmpeg", "-y", "-i", self.audio, "test_audio.wav"]
        self.assertListEqual(mock_run.call_args_list[0][0][0], audio_conversion_cmd)

        # Verify video conversion
        video_conversion_cmd = ["ffmpeg", "-y", "-i", self.face, "test_video.mp4"]
        self.assertListEqual(mock_run.call_args_list[1][0][0], video_conversion_cmd)

        # Verify inference call
        inference_cmd = [
            "/wav2lipenv/bin/python",
            "inference.py",
            "--face",
            "test_video.mp4",
            "--audio",
            "test_audio.wav",
            "--outfile",
            self.outfile,
            "--checkpoint_path",
            CHECKPOINT_PATH,
            "--segmentation_path",
            SEGMENTATION_PATH,
            "--sr_path",
            SR_PATH,
        ]
        self.assertListEqual(mock_run.call_args_list[2][0][0], inference_cmd)

    @patch("os.path.exists", return_value=False)
    @patch("subprocess.run")
    def test_wav2lip_inference_output_not_generated(self, mock_run, mock_exists):
        mock_run.return_value = MagicMock(returncode=0)

        with self.assertRaises(Exception) as context:
            run_wav2lip_inference(self.face, self.audio, self.outfile)

        self.assertTrue(
            "Failed to convert test_audio.webm to .wav" in str(context.exception)
        )

    @patch("os.path.exists", return_value=True)
    @patch("subprocess.run")
    def test_wav2lip_inference_processing_error(self, mock_run, mock_exists):
        mock_run.return_value = MagicMock(returncode=1, stderr="Error in Wav2Lip")

        with self.assertRaises(Exception) as context:
            run_wav2lip_inference(self.face, self.audio, self.outfile)

        self.assertTrue(
            str(context.exception).startswith(
                f"Command 'ffmpeg -y -i test_audio.webm test_audio.wav' failed with return code 1."
            )
        )
        self.assertTrue("Error in Wav2Lip" in str(context.exception))

    @patch("os.path.exists", return_value=True)
    @patch(
        "subprocess.run",
        side_effect=[subprocess.CalledProcessError(1, "ffmpeg"), None, None],
    )
    def test_audio_conversion_error(self, mock_run, mock_exists):
        with self.assertRaises(Exception) as context:
            run_wav2lip_inference(self.face, self.audio, self.outfile)
        raised_exception = context.exception
        self.assertIn(
            "Command 'ffmpeg' returned non-zero exit status", str(raised_exception)
        )


if __name__ == "__main__":
    unittest.main()
