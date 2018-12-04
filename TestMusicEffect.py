import unittest
import musicEffect

class TestMusicEffect(unittest.TestCase):
    
    def test_allow_extension_MP3(self):
        self.assertTrue(musicEffect.allowed_file("testfilename.mp3"))

    def test_not_allow_extension(self):
        self.assertFalse(musicEffect.allowed_file("testFilename.mp4"))

    if __name__ == '__main__':
        unittest.main()