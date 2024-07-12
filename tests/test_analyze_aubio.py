import unittest
import os
import numpy as np
import soundfile as sf
from services.aubio import analyze_audio_aubio  # Replace 'services.aubio' with the actual module name

class TestAnalyzeAudioAubio(unittest.TestCase):
    def setUp(self):
        # Setup a test audio file path
        self.test_audio_filename = 'test_audio.wav'
        # Create a test tone (1 second of A4, which is 440 Hz)
        self.sr = 44100  # Sample rate
        self.duration = 1.0  # seconds
        self.frequency = 440.0  # A4
        t = np.linspace(0, self.duration, int(self.sr * self.duration), endpoint=False)
        self.test_tone = 0.5 * np.sin(2 * np.pi * self.frequency * t)
        sf.write(self.test_audio_filename, self.test_tone, self.sr)

    def tearDown(self):
        # Clean up the test audio file
        if os.path.exists(self.test_audio_filename):
            os.remove(self.test_audio_filename)

    def test_analyze_audio_aubio(self):
        # Call the function
        result = analyze_audio_aubio(self.test_audio_filename)
        
        # Define the expected result (adjust this to your actual expected output)
        expected_result = {
            "music_data": [
                {"time": 0.0, "pitch": str(self.frequency), "note": "A4"}  # Expected result for a 440 Hz tone
            ]
        }
        
        # Check if the output contains the expected note
        self.assertGreater(len(result["music_data"]), 0, "No notes detected")
        detected_note = result["music_data"][0]
        
        # Convert detected_note["pitch"] to float before comparison
        self.assertEqual(detected_note["note"], "A4")

if __name__ == '__main__':
    unittest.main()
