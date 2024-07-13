import unittest
import os
import numpy as np
import soundfile as sf
import librosa
from services.bestmix import (
    onset_detect_librosa_default,
    onset_detect_librosa_backtrack,
    onset_detect_librosa_custom,
    onset_detect_aubio_hfc,
    onset_detect_aubio_complex,
    onset_detect_aubio_energy,
    freq_to_note_name,
    detect_pitch_aubio,
    analyze_audio_characteristics,
    choose_best_onset_detection,
    analyze_audio_file
)

class TestAudioAnalysis(unittest.TestCase):
    def setUp(self):
        self.test_audio_filename = 'test_tone.wav'
        self.sr = 22050  # Sample rate
        self.duration = 1.0  # seconds
        self.frequency = 440.0  # A4 note
        t = np.linspace(0, self.duration, int(self.sr * self.duration), endpoint=False)
        self.test_tone = 0.5 * np.sin(2 * np.pi * self.frequency * t)
        sf.write(self.test_audio_filename, self.test_tone, self.sr)
    
    def tearDown(self):
        if os.path.exists(self.test_audio_filename):
            os.remove(self.test_audio_filename)

    def test_onset_detect_librosa_default(self):
        y, sr = librosa.load(self.test_audio_filename, sr=self.sr)
        onset_times = onset_detect_librosa_default(y, sr)
        self.assertIsInstance(onset_times, np.ndarray)
    
    def test_onset_detect_librosa_backtrack(self):
        y, sr = librosa.load(self.test_audio_filename, sr=self.sr)
        onset_times = onset_detect_librosa_backtrack(y, sr)
        self.assertIsInstance(onset_times, np.ndarray)
    
    def test_onset_detect_librosa_custom(self):
        y, sr = librosa.load(self.test_audio_filename, sr=self.sr)
        onset_times = onset_detect_librosa_custom(y, sr)
        self.assertIsInstance(onset_times, np.ndarray)
    
    def test_onset_detect_aubio_hfc(self):
        onset_times = onset_detect_aubio_hfc(self.test_audio_filename)
        self.assertIsInstance(onset_times, list)
    
    def test_onset_detect_aubio_complex(self):
        onset_times = onset_detect_aubio_complex(self.test_audio_filename)
        self.assertIsInstance(onset_times, list)
    
    def test_onset_detect_aubio_energy(self):
        onset_times = onset_detect_aubio_energy(self.test_audio_filename)
        self.assertIsInstance(onset_times, list)
    
    def test_freq_to_note_name(self):
        note_name = freq_to_note_name(self.frequency)
        self.assertEqual(note_name, 'A4')
    
    def test_detect_pitch_aubio(self):
        onset_times = [0.0]  # Assuming the tone starts immediately
        pitches = detect_pitch_aubio(self.test_audio_filename, onset_times)
        self.assertIsInstance(pitches, list)
        self.assertGreater(len(pitches), 0)
    
    def test_analyze_audio_characteristics(self):
        characteristics = analyze_audio_characteristics(self.test_audio_filename)
        self.assertIsInstance(characteristics, dict)
        self.assertIn('tempo', characteristics)
        self.assertIn('spectral_centroid', characteristics)
        self.assertIn('zero_crossing_rate', characteristics)
    
    def test_choose_best_onset_detection(self):
        characteristics = {
            'tempo': 130,
            'spectral_centroid': 3000,
            'zero_crossing_rate': 0.1
        }
        method = choose_best_onset_detection(characteristics)
        self.assertIsInstance(method, str)
    
    def test_analyze_audio_file(self):
        result = analyze_audio_file(self.test_audio_filename)
        self.assertIsInstance(result, dict)
        self.assertIn('method_used', result)
        self.assertIn('onsets', result)
        self.assertIn('notes', result)

if __name__ == '__main__':
    unittest.main()
