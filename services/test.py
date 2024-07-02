import numpy as np
import madmom
import librosa

# Function to convert frequency to musical note
def frequency_to_note_name(freq):
    A4 = 440.0
    C0 = A4 * pow(2, -4.75)
    if freq == 0:
        return "Rest"
    h = round(12 * np.log2(freq / C0))
    octave = h // 12
    n = h % 12
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return note_names[n] + str(octave)

# Function to detect onsets and frequencies
def detect_onsets_and_frequencies(audio_path):
    # Load audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Use madmom to detect onsets
    proc = madmom.features.onsets.OnsetPeakPickingProcessor(fps=100)
    act = madmom.features.onsets.RNNOnsetProcessor()(audio_path)
    onsets = proc(act)

    # Use librosa to detect pitches
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    
    onset_frequencies = []
    for onset in onsets:
        onset_sample = int(onset * sr)
        pitch = pitches[:, onset_sample]
        magnitude = magnitudes[:, onset_sample]
        frequency = pitch[np.argmax(magnitude)]
        note = frequency_to_note_name(frequency)
        onset_frequencies.append((onset, frequency, note))
    
    return onset_frequencies

# Example usage
audio_path = '/Users/karthikeyannagarajan/Documents/FinalYearProject/MusicNoteFinder/musicFile/unknown.wav'
onset_frequencies = detect_onsets_and_frequencies(audio_path)
for onset, frequency, note in onset_frequencies:
    print(f"Onset: {onset:.2f}s, Frequency: {frequency:.2f}Hz, Note: {note}")
