# SpeechProcessor

The `SpeechProcessor` class provides functionality to transcribe audio files and translate the transcriptions into different languages using AssemblyAI and Google Translator.

## Requirements

- Python 3.9+
- AssemblyAI API key
- `dotenv` for environment variable management
- `deep_translator` for translation

## Installation

1. Clone the repository.
2. Install the required packages (in a virtual environement):
    ```sh
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the root directory and add your AssemblyAI API key:
    ```
    AAI_SETTINGS_API_KEY=your_api_key_here
    ```

## Usage

### Initialization

```python
from SpeechProcessor import SpeechProcessor

processor = SpeechProcessor(api_key="your_api_key", enable_logging=True, speech_model="nano")
```
NOTE: two models are available, "nano" and "best"

### Transcribe an Audio File

```python
transcription_result = processor.transcribe("path/to/audio/file.ogg")
print(transcription_result)
```

### Translate a Transcription

```python
translation_result = processor.translate(transcription_result, target_lang="fr")
print(translation_result)
```

### Transcribe and Translate in One Step

```python
result = processor.transcribe_and_translate("path/to/audio/file.ogg", target_lang="fr")
print(result)
```

## Example

```python
import os
import json
from SpeechProcessor import SpeechProcessor

processor = SpeechProcessor(api_key="your_api_key", enable_logging=False, speech_model="nano")

# Transcribe and translate all audio files in the 'from_yt' directory to French
ogg_files = [os.path.join('from_yt', file) for file in os.listdir('from_yt') if file.endswith('.ogg') or file.endswith('.mp3')]
for file in ogg_files:
    full_process_result = processor.transcribe_and_translate(file, "fr")
    print(json.dumps(full_process_result, indent=4, ensure_ascii=False))
    print()
```


## For more information, visit [AssemblyAI](https://www.assemblyai.com).
