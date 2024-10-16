import os
from dotenv import load_dotenv
from typing import Dict, Any, Union, Optional
import logging

import assemblyai as aai
from deep_translator import GoogleTranslator

load_dotenv()

class SpeechProcessor:

    def __init__(
        self, api_key: Optional[str] = None, enable_logging: bool = False, speech_model: str = 'nano'
    ):
        self.aai_api_key = api_key or os.getenv("AAI_SETTINGS_API_KEY")
        self.speech_model = speech_model
        self.transcriber = self._setup_transcriber()
        self.translator = None
        self.enable_logging = enable_logging

        if self.enable_logging:
            logging.basicConfig(
                level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
            )


    def _setup_transcriber(self) -> aai.Transcriber:
        model_mapping = {
            'nano': aai.SpeechModel.nano,
            'best': aai.SpeechModel.best
        }
        selected_model = model_mapping.get(self.speech_model, aai.SpeechModel.nano)
        
        config = aai.TranscriptionConfig(
            speech_model=selected_model, language_detection=True
        )
        aai.settings.api_key = self.aai_api_key
        return aai.Transcriber(config=config)


    def _setup_translator(self, target_lang: str) -> None:
        self.translator = GoogleTranslator(source="auto", target=target_lang)


    def _translate_text(self, text: str, target_lang: str) -> str:
        self._setup_translator(target_lang)
        
        # Check if the input is empty
        if not text.strip():
            return "Empty transcription, skipping translation."

        try:
            return self.translator.translate(text)
        except Exception as e:
            error_message = f"Translation failed: {str(e)}"
            
            if self.enable_logging:
                logging.error(error_message)
            
            # Return a partial translation or an error message
            return f"Partial translation due to error: {error_message}"


    def _transcribe_file(self, filename: str) -> Dict[str, Any]:
        base_filename = os.path.basename(filename)
        try:
            transcript = self.transcriber.transcribe(filename)
            transcript_text = transcript.text
            detected_language = transcript.json_response.get("language_code", "")
        except Exception as e:
            if self.enable_logging:
                logging.error(f"Transcription failed for local file {filename}: {str(e)}")
            return {
                "filename": base_filename,
                "detected_language": None,
                "transcript": f"Error: {str(e)}",
            }

        if not transcript_text.strip():
            if self.enable_logging:
                logging.warning(f"No valid content found in transcription for file: {base_filename}")
            return {
                "filename": base_filename,
                "detected_language": detected_language or "",
                "transcript": "No valid content",
            }

        return {
            "filename": base_filename,
            "detected_language": detected_language,
            "transcript": transcript_text.strip(),
        }


    def transcribe(self, audio_source: str) -> Dict[str, Any]:
        if self.enable_logging:
            logging.info(f"Transcribing: {audio_source}")
        
        result = self._transcribe_file(audio_source)
        return result


    def translate(
        self, input_data: Union[str, Dict[str, Any]], target_lang: str
    ) -> Dict[str, Any]:
        if isinstance(input_data, dict):
            original_text = input_data.get("transcript", "")
            detected_language = input_data.get("detected_language", "")
            filename = input_data.get("filename", "")
        else:
            original_text = input_data
            detected_language = ""
            filename = ""

        if self.enable_logging:
            logging.info(f"Translating to {target_lang}")

        # Check if detected language matches target language
        if detected_language and detected_language.lower() == target_lang.lower():
            return {
                "filename": filename,
                "original": original_text,
                "detected_language": detected_language,
                "translation": original_text,
                "target_language": target_lang,
            }

        translated_text = self._translate_text(original_text, target_lang)

        return {
            "filename": filename,
            "original": original_text,
            "detected_language": detected_language,
            "translation": translated_text,
            "target_language": target_lang,
        }


    def transcribe_and_translate(
        self, audio_source: str, target_lang: str
    ) -> Dict[str, Any]:
        transcription_result = self.transcribe(audio_source)
        translation_result = self.translate(transcription_result, target_lang)
        return translation_result