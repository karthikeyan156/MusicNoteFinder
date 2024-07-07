import unittest
import os
import numpy as np
import soundfile as sf
from services.librosa import analyze_audio_librosa  # Replace 'your_module' with the actual module name

class TestAnalyzeAudioLibrosa(unittest.TestCase):
    def setUp(self):
        # Setup a test audio file path
        self.test_audio_filename = 'test_audio.wav'
        # Create a dummy audio file for testing (1 second of silence)
        self.sr = 22050  # Sample rate
        self.duration = 1.0  # seconds
        self.test_tone = np.zeros(int(self.sr * self.duration))
        sf.write(self.test_audio_filename, self.test_tone, self.sr)

    def tearDown(self):
        # Clean up the test audio file
        if os.path.exists(self.test_audio_filename):
            os.remove(self.test_audio_filename)

    def test_analyze_audio_librosa(self):
        # Call the function
        result = analyze_audio_librosa(self.test_audio_filename)
        
        # Define the expected result (adjust this to your actual expected output)
        expected_result = {
            "music_data": []
        }
        
        # Check if the output is as expected
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
