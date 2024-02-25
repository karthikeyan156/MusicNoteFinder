import librosa
import numpy as np

def extract_musical_notes(filename: str):
    # Load the audio file
    y, sr = librosa.load(filename)

    # Extract the pitches and magnitudes
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    # Select the predominant pitch at each time step (frame)
    predominant_pitches = [pitches[magnitudes[:, t].argmax(), t] for t in range(pitches.shape[1])]
    predominant_pitches = np.array(predominant_pitches)

    # Filter out 0 frequencies (no pitch detected)
    predominant_pitches = predominant_pitches[predominant_pitches > 0]

    # Convert frequencies to musical notes
    notes = [librosa.hz_to_note(pitch) for pitch in predominant_pitches]

    return notes
