import aubio
import numpy as np

def freq_to_note(frequency):
    A4 = 440
    C0 = A4 * pow(2, -4.75)
    if frequency == 0:
        return "N/A"  # Silence or undefined
    h = round(12 * np.log2(frequency / C0))
    octave = h // 12
    n = h % 12
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return note_names[n] + str(octave)

def analyze_audio_aubio(filename):
    samplerate, win_s, hop_s = 44100, 1024, 512
    aubio_source = aubio.source(filename, samplerate, hop_s)
    aubio_pitch = aubio.pitch("default", win_s, hop_s, samplerate)
    aubio_pitch.set_unit("Hz")
    aubio_pitch.set_tolerance(0.8)
    aubio_onset = aubio.onset("default", win_s, hop_s, samplerate)

    music_data = []

    total_frames = 0  # Initialize total frames read

    while True:
        samples, read = aubio_source()  # Read frame
        total_frames += read  # Update total frames read
        if read == 0:  # End of file
            break
        is_onset = aubio_onset(samples)  # Check for onset
        pitch = aubio_pitch(samples)[0]  # Get pitch
        if is_onset:
            time = total_frames / float(samplerate)  # Calculate the time of the onset
            note = freq_to_note(pitch)  # Convert frequency to musical note
            music_data.append({'time': time, 'pitch': str(pitch), 'note': note})       
    return {"music_data":music_data}     

