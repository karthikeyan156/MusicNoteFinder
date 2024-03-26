import aubio
import numpy as np

# A simple mapping function from frequency to note names, for demonstration.
# This is a very basic implementation and might not cover all edge cases or provide precise note naming with accidentals.
def freq_to_note_simple(frequency):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    A4 = 440.0
    C0 = A4 * pow(2, -4.75)
    if frequency == 0: return None
    h = round(12 * np.log2(frequency / C0))
    octave = h // 12
    n = h % 12
    return note_names[n] + str(octave)

def extract_musical_notes_aubio(filename):
    # Parameters for pitch detection
    hop_size = 512  # Samples per frame
    win_size = 2048  # FFT size
    samplerate = 0  # Use the original samplerate of the file
    
    # Create pitch detection object
    pitch_o = aubio.pitch("default", win_size, hop_size, samplerate)
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(0.8)

    # Create source object
    source = aubio.source(filename, samplerate, hop_size)
    samplerate = source.samplerate
    
    pitches = []
    confidences = []

    # Process the entire file
    while True:
        samples, read = source()
        pitch = pitch_o(samples)[0]
        confidence = pitch_o.get_confidence()

        if confidence > 0.8: # Consider pitches with high confidence
            pitches.append(pitch)

        if read < hop_size: # End of file
            break

    # Convert frequencies to musical notes
    notes = [freq_to_note_simple(pitch) for pitch in pitches if pitch > 0]

    return notes

# Example usage
filename = "/Users/karthikeyannagarajan/Documents/FinalYearProject/MusicNoteFinder/piano-g_G#_major.wav"
notes = extract_musical_notes_aubio(filename)
print(notes)
