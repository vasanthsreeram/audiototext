import os
from pydub import AudioSegment
import speech_recognition as sr

print(os.getcwd())
os.chdir('/Users/vasanth/Desktop/Projects/audiototext')
def transcribe_audio(file_path):
    # Load the audio file
    audio = AudioSegment.from_mp3(file_path)

    # Initialize the recognizer
    r = sr.Recognizer()

    # Splitting the audio in chunks of 30 seconds to avoid memory issues and improve recognition accuracy
    chunks = [audio[i:i + 30000] for i in range(0, len(audio), 30000)]  # 30-sec chunks
    transcripts = []

    for i, chunk in enumerate(chunks):
        # Exporting chunk to wav as recognizer works with wav files
        print(f"Processed chunk {i+1}/{len(chunks)}")

        chunk_path = f'temp_chunk{i}.wav'
        chunk.export(chunk_path, format="wav")
        
        # Recognizing the chunk
        with sr.AudioFile(chunk_path) as source:
            audio_listened = r.record(source)
            
            try:
                # Using google recognizer to convert audio to text
                text = r.recognize_google(audio_listened)
                transcripts.append(text)
            except sr.UnknownValueError:
                # Unable to understand the audio chunk
                transcripts.append("[Unintelligible]")
            except sr.RequestError:
                # API was unreachable or unresponsive
                transcripts.append("[Error: Request failed]")
        
        # Delete the temporary chunk file
        os.remove(chunk_path)

    return ' '.join(transcripts)

if __name__ == "__main__":
    audio_file_path = 'c3838080-de64-4b20-bf9f-399da25a741d.mp3'  # Replace with your audio file path
    transcription = transcribe_audio(audio_file_path)
    print(transcription)
    with open('transcription.txt', 'w') as f:
        f.write(transcription)
