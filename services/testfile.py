import librosa
import numpy as np
def extract_musical_notes01(filename, sr=22050, hop_length=512):
    try:
        # Load the audio file
        y, sr = librosa.load(filename, sr=sr)

        # Find onsets
        onsets = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)

        # Iterate over each onset
        for i, onset in enumerate(onsets):
            # Calculate the duration until the next onset
            next_onset_time = onsets[i+1] if i < len(onsets) - 1 else len(y) / sr
            duration_until_next_onset = next_onset_time - onset
            
            # Extract the pitch at the onset time
            onset_frame = librosa.time_to_frames(onset, sr=sr, hop_length=hop_length)


            #pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            # Select the predominant pitch at each time step (frame)
           # predominant_pitches = [pitches[magnitudes[:, t].argmax(), t] for t in range(pitches.shape[1])]
            predominant_pitches = np.array(onset_frame)

            # Filter out 0 frequencies (no pitch detected)
            predominant_pitches = predominant_pitches[predominant_pitches > 0]
            print(predominant_pitches)
            # Convert frequencies to musical notes
            notes = [librosa.hz_to_note(pitch) for pitch in predominant_pitches]
            print(f"Onset at {onset} seconds, Note :  {notes}, duration until next onset: {duration_until_next_onset} seconds")
            
    except Exception as e:
        print("Error:", e)

# Extract the pitches and magnitudes
   

    
