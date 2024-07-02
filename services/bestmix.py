import librosa
import soundfile as sf
import aubio
import numpy as np

# Onset Detection Functions for Librosa
def onset_detect_librosa_default(y, sr):
    onsets = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onsets, sr=sr)
    return onset_times

def onset_detect_librosa_backtrack(y, sr):
    onsets = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
    onset_times = librosa.frames_to_time(onsets, sr=sr)
    return onset_times

def onset_detect_librosa_custom(y, sr):
    onsets = librosa.onset.onset_detect(y=y, sr=sr, pre_max=20, post_max=20, delta=0.3, wait=30)
    onset_times = librosa.frames_to_time(onsets, sr=sr)
    return onset_times

# Onset Detection Functions for Aubio
def onset_detect_aubio_hfc(filename):
    win_s = 512
    hop_s = win_s // 2
    s = aubio.source(filename, 0, hop_s)
    samplerate = s.samplerate
    onset = aubio.onset("hfc", win_s, hop_s, samplerate)
    onsets = []
    while True:
        samples, read = s()
        if onset(samples):
            onsets.append(onset.get_last_s())
        if read < hop_s:
            break
    return onsets

def onset_detect_aubio_complex(filename):
    win_s = 512
    hop_s = win_s // 2
    s = aubio.source(filename, 0, hop_s)
    samplerate = s.samplerate
    onset = aubio.onset("complex", win_s, hop_s, samplerate)
    onsets = []
    while True:
        samples, read = s()
        if onset(samples):
            onsets.append(onset.get_last_s())
        if read < hop_s:
            break
    return onsets

def onset_detect_aubio_energy(filename):
    win_s = 512
    hop_s = win_s // 2
    s = aubio.source(filename, 0, hop_s)
    samplerate = s.samplerate
    onset = aubio.onset("energy", win_s, hop_s, samplerate)
    onsets = []
    while True:
        samples, read = s()
        if onset(samples):
            onsets.append(onset.get_last_s())
        if read < hop_s:
            break
    return onsets

# Pitch Detection and Note Conversion
def freq_to_note_name(frequency):
    A4 = 440.0
    C0 = A4 * pow(2, -4.75)
    if frequency == 0:
        return "N/A"
    h = round(12 * np.log2(frequency / C0))
    octave = h // 12
    n = h % 12
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return note_names[n] + str(octave)

def detect_pitch_aubio(filename, onset_times):
    win_s = 512
    hop_s = win_s // 2
    s = aubio.source(filename, 0, hop_s)
    samplerate = s.samplerate
    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(0.8)
    
    pitches = []
    total_frames = 0
    onset_frames = [int(onset_time * samplerate / hop_s) for onset_time in onset_times]
    onset_idx = 0
    
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        if onset_idx < len(onset_frames) and total_frames // hop_s == onset_frames[onset_idx]:
            note = freq_to_note_name(pitch)
            pitches.append(note)
            onset_idx += 1
        total_frames += read
        if read < hop_s:
            break
    
    return pitches

# Feature Extraction Function
def analyze_audio_characteristics(filename):
    y, sr = librosa.load(filename, sr=None)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    
    avg_spectral_centroid = np.mean(spectral_centroid)
    avg_zero_crossing_rate = np.mean(zero_crossing_rate)
    
    return {
        'spectral_centroid': avg_spectral_centroid,
        'zero_crossing_rate': avg_zero_crossing_rate,
        'tempo': tempo
    }

# Selection Function
def choose_best_onset_detection(audio_characteristics):
    if audio_characteristics['tempo'] > 120 and audio_characteristics['spectral_centroid'] > 2500:
        # Likely fast-paced music with high-pitched elements
        return 'librosa_custom'
    elif audio_characteristics['tempo'] > 120:
        # Likely fast-paced music
        return 'librosa_default'
    elif audio_characteristics['zero_crossing_rate'] < 0.05 and audio_characteristics['spectral_centroid'] < 1500:
        # Likely monophonic with low spectral centroid
        return 'aubio_energy'
    elif audio_characteristics['zero_crossing_rate'] < 0.05:
        # Likely monophonic
        return 'aubio_hfc'
    elif audio_characteristics['spectral_centroid'] > 3000:
        # Likely high-pitched sounds
        return 'librosa_backtrack'
    else:
        # Default case for more complex audio
        return 'aubio_complex'

# Main Analysis Function
def analyze_audio_file(filename):
    audio_characteristics = analyze_audio_characteristics(filename)
    best_method = choose_best_onset_detection(audio_characteristics)
    
    y, sr = librosa.load(filename, sr=None)
    
    if best_method == 'librosa_default':
        onsets = onset_detect_librosa_default(y, sr)
    elif best_method == 'librosa_backtrack':
        onsets = onset_detect_librosa_backtrack(y, sr)
    elif best_method == 'librosa_custom':
        onsets = onset_detect_librosa_custom(y, sr)
    elif best_method == 'aubio_hfc':
        onsets = onset_detect_aubio_hfc(filename)
    elif best_method == 'aubio_complex':
        onsets = onset_detect_aubio_complex(filename)
    elif best_method == 'aubio_energy':
        onsets = onset_detect_aubio_energy(filename)
    else:
        raise ValueError(f"Unsupported method: {best_method}")
    
    notes = detect_pitch_aubio(filename, onsets)
    
    return {
        "method_used": best_method,
        "onsets": onsets,
        "notes": notes
    }
