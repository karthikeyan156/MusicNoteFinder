import librosa
import numpy as np

def analyze_audio_librosa(filename):
    def freq_to_note(frequency):
        A4 = 440
        C0 = A4 * pow(2, -4.75)
        if frequency == 0: return "N/A"  # Silence or undefined
        h = round(12 * np.log2(frequency / C0))
        octave = h // 12
        n = h % 12
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        return note_names[n] + str(octave)

    # Load the audio file
    y, sr = librosa.load(filename)

    music_data=[]

    # Detect onsets
    onsets = librosa.onset.onset_detect(y=y, sr=sr)

    # Convert onsets to samples
    onset_samples = librosa.frames_to_samples(onsets)

    # Estimate pitches and magnitudes
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    # Convert onset samples to frames for pitch tracking
    onset_frames = librosa.samples_to_frames(onset_samples)

    # For each onset, find the pitch
    for onset_frame in onset_frames:
        index = np.argmax(magnitudes[:, onset_frame])
        pitch = pitches[index, onset_frame]
        if pitch > 0:  # Ensuring that a pitch was actually found
            note = freq_to_note(pitch)
            time= librosa.frames_to_time(onset_frame, sr=sr)
            print(f'Onset at {librosa.frames_to_time(onset_frame, sr=sr)}s: {pitch:.2f} Hz, Note: {note}')
            music_data.append({"note":note,"Time":str(time),"pitch":str(round(pitch,2))})
        else:
            print(f'Onset at {librosa.frames_to_time(onset_frame, sr=sr)}s: No pitch detected')
    print(music_data)
    return {"music_data":music_data}