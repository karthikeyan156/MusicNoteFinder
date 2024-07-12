import numpy as np
import soundfile as sf
from scipy.signal import find_peaks

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

def find_pitch(segment, sr):
    windowed = segment * np.hanning(len(segment))
    spectrum = np.abs(np.fft.rfft(windowed))
    frequency = np.fft.rfftfreq(len(segment), 1.0 / sr)
    peak_idx, _ = find_peaks(spectrum)
    if len(peak_idx) == 0:
        return 0
    peak_freq = frequency[peak_idx]
    peak_magnitude = spectrum[peak_idx]
    max_peak = peak_freq[np.argmax(peak_magnitude)]
    return max_peak

def detect_onsets(signal, sr, frame_size=2048, hop_size=512, threshold=0.5):
    # Compute the spectral flux
    frames = np.array([signal[i:i+frame_size] for i in range(0, len(signal) - frame_size, hop_size)])
    magnitudes = np.abs(np.fft.rfft(frames, axis=1))
    diff = np.diff(magnitudes, axis=0)
    diff[diff < 0] = 0
    flux = np.sum(diff, axis=1)

    # Normalize the flux
    flux = (flux - np.mean(flux)) / np.std(flux)

    # Detect peaks in the normalized flux
    peaks, _ = find_peaks(flux, height=threshold)
    onset_times = peaks * hop_size / sr
    onset_samples = peaks * hop_size

    return onset_times, onset_samples

def analyze_audio_soundFile(filename):
    # Read the audio file
    y, sr = sf.read(filename)
    
    # Ensure mono audio
    if y.ndim > 1:
        y = y.mean(axis=1)
    
    # Detect onsets
    onset_times, onset_samples = detect_onsets(y, sr)
    
    music_data = []
    for i in range(len(onset_samples) - 1):
        onset_sample = onset_samples[i]
        offset_sample = onset_samples[i + 1]
        duration = (offset_sample - onset_sample) / sr
        segment = y[onset_sample:onset_sample + sr // 10]
        pitch = find_pitch(segment, sr)
        note = freq_to_note_name(pitch)
        onset_time = onset_sample / sr
        music_data.append({
            "onset": onset_time,
            "offset": onset_time + duration,
            "duration": duration,
            "pitch": round(pitch, 2),
            "note": note
        })
    
    # Handle the last onset to the end of the file
    if len(onset_samples) > 0:
        onset_sample = onset_samples[-1]
        offset_sample = len(y)
        duration = (offset_sample - onset_sample) / sr
        segment = y[onset_sample:onset_sample + sr // 10]
        pitch = find_pitch(segment, sr)
        note = freq_to_note_name(pitch)
        onset_time = onset_sample / sr
        music_data.append({
            "onset": onset_time,
            "offset": onset_time + duration,
            "duration": duration,
            "pitch": round(pitch, 2),
            "note": note
        })
    return {"music_data": music_data}


