import os
import unittest

from video_generator.fb_yt_long_video_generator.A_core.A1_config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_config_values(self):
        self.assertEqual(self.config.get('fb_yt_long_video_generator', 'test_value'), 'default_value')

    def test_config_file_exists(self):
        self.assertTrue(os.path.exists('video_generator/fb_yt_long_video_generator/A_core/A1_config.py'))

if __name__ == '__main__':
    unittest.main()
