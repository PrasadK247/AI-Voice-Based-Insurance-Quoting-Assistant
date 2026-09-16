"""
UC189 - Voice API Endpoints
Handles speech-to-text, text-to-speech, and voice processing.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional
import base64
import uuid

from services.whisper_service import WhisperService
from services.elevenlabs_service import ElevenLabsService
from services.uniphore_service import UniphoreService
from utils.logger import setup_logger

try:
    from langgraph.workflow import InsuranceWorkflow
except (ImportError, AttributeError):
    from workflows.insurance_workflow import InsuranceWorkflow

router = APIRouter()
logger = setup_logger(__name__)


# ── Request / Response Models ──────────────────────────

class TranscribeRequest(BaseModel):
    audio_base64: str
    language: str = "en"
    format: str = "wav"


class TranscribeResponse(BaseModel):
    success: bool
    transcript: str
    confidence: float
    language: str
    duration_seconds: float
    intent: Optional[str] = None
    sentiment: Optional[str] = None


class SynthesizeRequest(BaseModel):
    text: str
    voice_id: str = "default"
    speed: float = Field(default=1.0, ge=0.5, le=2.0)


class SynthesizeResponse(BaseModel):
    success: bool
    audio_base64: str
    duration_seconds: float


class ConversationRequest(BaseModel):
    session_id: str
    audio_base64: Optional[str] = None
    text_input: Optional[str] = None
    language: str = "en"


class ConversationResponse(BaseModel):
    success: bool
    session_id: str
    user_message: str
    assistant_message: str
    audio_response_base64: Optional[str] = None
    intent: str
    sentiment: str
    next_action: str
    customer_profile: Optional[dict] = None
    risk_score: Optional[float] = None
    quote_data: Optional[dict] = None


# ── Endpoints ──────────────────────────────────────────

@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(request: TranscribeRequest):
    """Convert speech audio to text using Whisper STT."""
    logger.info("Transcribing audio input")

    try:
        whisper_service = WhisperService()
        result = await whisper_service.transcribe(
            audio_base64=request.audio_base64,
            language=request.language,
            audio_format=request.format,
        )

        # Analyze sentiment via Uniphore
        uniphore_service = UniphoreService()
        sentiment = await uniphore_service.analyze_sentiment(result["transcript"])

        return TranscribeResponse(
            success=True,
            transcript=result["transcript"],
            confidence=result.get("confidence", 0.9),
            language=result.get("language", request.language),
            duration_seconds=result.get("duration", 0.0),
            intent=result.get("intent"),
            sentiment=sentiment.get("sentiment", "neutral"),
        )

    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/synthesize", response_model=SynthesizeResponse)
async def synthesize_speech(request: SynthesizeRequest):
    """Convert text to speech using ElevenLabs TTS."""
    logger.info("Synthesizing speech output")

    try:
        elevenlabs_service = ElevenLabsService()
        result = await elevenlabs_service.synthesize(
            text=request.text,
            voice_id=request.voice_id,
            speed=request.speed,
        )

        return SynthesizeResponse(
            success=True,
            audio_base64=result["audio_base64"],
            duration_seconds=result.get("duration", 0.0),
        )

    except Exception as e:
        logger.error(f"Speech synthesis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")


@router.post("/conversation", response_model=ConversationResponse)
async def voice_conversation(request: ConversationRequest):
    """Handle a full voice conversation turn: transcribe → process → respond."""
    logger.info(f"Processing conversation turn for session {request.session_id}")

    try:
        user_message = request.text_input or ""

        # Transcribe if audio provided
        if request.audio_base64:
            whisper_service = WhisperService()
            stt_result = await whisper_service.transcribe(
                audio_base64=request.audio_base64,
                language=request.language,
            )
            user_message = stt_result["transcript"]

        if not user_message:
            raise HTTPException(status_code=400, detail="No audio or text input provided.")

        # Process with LangGraph workflow
        workflow = InsuranceWorkflow()
        wf_result = await workflow.process_turn(
            session_id=request.session_id,
            user_message=user_message,
        )

        # Synthesize response
        audio_response = None
        try:
            elevenlabs_service = ElevenLabsService()
            tts_result = await elevenlabs_service.synthesize(
                text=wf_result["response"]
            )
            audio_response = tts_result["audio_base64"]
        except Exception:
            logger.warning("TTS synthesis failed; returning text only.")

        return ConversationResponse(
            success=True,
            session_id=request.session_id,
            user_message=user_message,
            assistant_message=wf_result["response"],
            audio_response_base64=audio_response,
            intent=wf_result.get("intent", "general_inquiry"),
            sentiment=wf_result.get("sentiment", "neutral"),
            next_action=wf_result.get("next_action", "continue"),
            customer_profile=wf_result.get("customer_profile"),
            risk_score=wf_result.get("risk_score"),
            quote_data=wf_result.get("quote_data"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Conversation processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Conversation failed: {str(e)}")


@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """Upload an audio file for processing."""
    logger.info(f"Receiving audio upload: {file.filename}")

    try:
        contents = await file.read()
        audio_base64 = base64.b64encode(contents).decode("utf-8")
        file_id = f"audio_{uuid.uuid4().hex[:8]}"

        whisper_service = WhisperService()
        result = await whisper_service.transcribe(
            audio_base64=audio_base64,
            language="en",
        )

        return {
            "success": True,
            "file_id": file_id,
            "filename": file.filename,
            "transcript": result["transcript"],
            "confidence": result.get("confidence", 0.9),
        }

    except Exception as e:
        logger.error(f"Audio upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
