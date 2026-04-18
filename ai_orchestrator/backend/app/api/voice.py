from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from app.services.voice_to_task import process_voice_command
import openai
import os
import tempfile

router = APIRouter()

class VoicePayload(BaseModel):
    audio_base64: Optional[str] = None
    test_text: Optional[str] = None

@router.post("/task")
async def handle_voice_task(payload: VoicePayload):
    """Принимает текст и создаёт задачи через LLM."""
    result = process_voice_command(test_text=payload.test_text)
    links = [f"https://dashboard.example.com/task/{i}" for i in range(len(result.tasks))]
    return {
        "voice_decomposition": result,
        "task_links": links
    }

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Принимает аудиофайл (webm/wav) → транскрибирует через OpenAI Whisper.
    Если ключ невалидный — возвращает ошибку.
    """
    stt_api_key = os.getenv("ALEM_STT_API_KEY", "")
    
    # Сохраняем временный файл
    suffix = ".webm" if "webm" in (file.content_type or "") else ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    wav_path = tmp_path + ".wav"
    upload_path = tmp_path
    filename = "voice.webm"
    mime = "audio/webm"

    try:
        if not stt_api_key or stt_api_key == "mock":
            os.unlink(tmp_path)
            return {"transcript": None, "error": "no_alem_key"}

        import subprocess
        try:
            # Конвертируем WebM из браузера в чистый WAV (16kHz), который 100% поддерживается любым движком
            subprocess.run(
                ["ffmpeg", "-y", "-i", tmp_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", wav_path],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            upload_path = wav_path
            filename = "voice.wav"
            mime = "audio/wav"
        except FileNotFoundError:
            return {"transcript": None, "error": "ffmpeg_not_installed"}
        except subprocess.CalledProcessError:
            return {"transcript": None, "error": "ffmpeg_conversion_failed"}
        
        # Реальная транскрипция через Alem Speech-to-Text
        import requests
        headers = {
            "Authorization": f"Bearer {stt_api_key}"
        }
        files = {
            "file": (filename, open(upload_path, "rb"), mime)
        }
        data = {
            "model": "speech-to-text",
            "language": "ru"
        }
        response = requests.post("https://llm.alem.ai/v1/audio/transcriptions", headers=headers, files=files, data=data)
        
        if response.status_code != 200:
            return {"transcript": None, "error": f"API {response.status_code}: {response.text}"}
            
        transcription_data = response.json()
        return {"transcript": transcription_data.get("text", ""), "error": None}
    
    except Exception as e:
        return {"transcript": None, "error": str(e)}
    finally:
        try:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            if os.path.exists(wav_path):
                os.unlink(wav_path)
        except:
            pass
