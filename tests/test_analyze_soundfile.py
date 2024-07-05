import unittest
from services.soundfile import analyze_audio_soundFile

class TestAnalyzeAudioSoundFile(unittest.TestCase):

    def setUp(self):
        # Create a test tone (A4 note at 440 Hz)
        self.test_audio_filename = 'test_audio.wav'
        import numpy as np
        import soundfile as sf
        sr = 44100  # Sample rate
        t = np.linspace(0, 1.0, int(sr * 1.0), endpoint=False)  # 1 second duration
        test_tone = 0.5 * np.sin(2 * np.pi * 440 * t)
        sf.write(self.test_audio_filename, test_tone, sr)

    def tearDown(self):
        import os
        os.remove(self.test_audio_filename)

    def test_analyze_audio_soundFile(self):
        result = analyze_audio_soundFile(self.test_audio_filename)
        self.assertIn('music_data', result)
        self.assertGreater(len(result['music_data']), 0)
        # Check if the result has expected note details
        for note_data in result['music_data']:
            self.assertIn('note', note_data)
            self.assertIn('onset', note_data)
            self.assertIn('offset', note_data)
            self.assertIn('duration', note_data)
            self.assertIn('pitch', note_data)
            # Additional checks can be added here as needed

if __name__ == '__main__':
    unittest.main()
