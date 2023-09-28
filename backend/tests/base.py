import unittest
from __init__ import create_app
from utils import (
    get_checkpoints_dir,
    get_full_path,
    get_wav2lip_env_dir,
    get_python_executable,
)


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        checkpoint_dir = get_checkpoints_dir(self.app.config)
        self.CHECKPOINT_PATH = get_full_path(checkpoint_dir, "wav2lip_gan.pth")
        self.SEGMENTATION_PATH = get_full_path(checkpoint_dir, "face_segmentation.pth")
        self.SR_PATH = get_full_path(checkpoint_dir, "esrgan_max.pth")

        wav2lip_env_dir = get_wav2lip_env_dir(self.app.config)
        self.python_executable = get_python_executable(wav2lip_env_dir)

    def tearDown(self):
        self.app_context.pop()
