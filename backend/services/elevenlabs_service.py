"""
UC189 - ElevenLabs Text-to-Speech Service
Converts text responses into realistic audio speech using ElevenLabs TTS API,
with a lightweight synthetic WAV audio fallback for local development.
"""

import base64
import struct
import httpx
from typing import Dict, Any

from config import get_settings
from utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)


class ElevenLabsService:
    """Service handling text-to-speech synthesis."""

    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY or ""
        self.voice_id = settings.ELEVENLABS_VOICE_ID or "21m00Tcm4TlvDq8ikWAM"  # Default 'Rachel'
        self.model_id = settings.ELEVENLABS_MODEL_ID or "eleven_monolingual_v1"

    async def synthesize(
        self,
        text: str,
        voice_id: str = "default",
        speed: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Synthesize speech from text.
        Returns: {"audio_base64": ..., "duration": ...}
        """
        logger.info(f"Synthesizing speech for: '{text[:50]}...'")

        selected_voice = self.voice_id if voice_id in ("default", "") else voice_id

        # Call ElevenLabs API if key is present
        if self.api_key and len(self.api_key) > 10:
            try:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice}"
                headers = {
                    "xi-api-key": self.api_key,
                    "Content-Type": "application/json",
                    "Accept": "audio/mpeg",
                }
                payload = {
                    "text": text,
                    "model_id": self.model_id,
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.8,
                    },
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.post(url, json=payload, headers=headers)
                    if response.status_code == 200:
                        audio_b64 = base64.b64encode(response.content).decode("utf-8")
                        duration = max(len(text.split()) / 2.5, 1.0)
                        return {
                            "audio_base64": audio_b64,
                            "duration": round(duration, 1),
                        }
                    else:
                        logger.warning(f"ElevenLabs error {response.status_code}: {response.text}")
            except Exception as e:
                logger.warning(f"ElevenLabs TTS call failed: {e}. Using synthetic audio fallback.")

        # Fallback: Generate a clean minimal PCM WAV header + tone
        audio_b64 = self._generate_synthetic_wav(text)
        duration = max(len(text.split()) / 3.0, 1.5)

        return {
            "audio_base64": audio_b64,
            "duration": round(duration, 1),
        }

    def _generate_synthetic_wav(self, text: str) -> str:
        """Generate a valid minimal WAV audio binary encoded in base64."""
        sample_rate = 8000
        num_samples = int(sample_rate * 0.5)  # 0.5 sec chime
        byte_rate = sample_rate * 2
        block_align = 2
        bits_per_sample = 16

        # Standard 44-byte WAV header
        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF",
            36 + num_samples * 2,
            b"WAVE",
            b"fmt ",
            16,
            1,  # PCM
            1,  # Mono
            sample_rate,
            byte_rate,
            block_align,
            bits_per_sample,
            b"data",
            num_samples * 2,
        )

        import math
        samples = []
        for i in range(num_samples):
            # Soft sine wave tone (440 Hz)
            val = int(12000 * math.sin(2 * math.pi * 440 * (i / sample_rate)) * math.exp(-i / 1500))
            samples.append(struct.pack("<h", val))

        wav_bytes = header + b"".join(samples)
        return base64.b64encode(wav_bytes).decode("utf-8")
