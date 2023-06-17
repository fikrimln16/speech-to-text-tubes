import os
from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

app = FastAPI()

# Path ke file kredensial
keyfile = "key.json"

# Membaca informasi kredensial dari file kredensial
creds = service_account.Credentials.from_service_account_file(keyfile)

CONFIGS = {
    '.mp3': speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.MP3,
    sample_rate_hertz=48000,
    language_code='id-ID',
    alternative_language_codes=['en-US'],
   ),
    '.m4a': speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.AAC,
        sample_rate_hertz=44100,
        language_code='id-ID',
        alternative_language_codes=['en-US'],
    )
}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):

    # Menginisialisasi klien Google Cloud Speech-to-Text dengan kredensial
    client = speech.SpeechClient(credentials=creds)

    audio_content = await file.read()

    # Mengkonfigurasi permintaan ke layanan Speech-to-Text
    audio = speech.RecognitionAudio(content=audio_content)
    config = CONFIGS[Path(file.filename).suffix]

 
    # Mengirim permintaan transkripsi ke layanan Speech-to-Text
    response = client.recognize(request={"config": config, "audio": audio})


    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return {"transcripts": transcripts}