# VESTA API Reference Documentation

**Document ID**: VESTA-API-001  
**Version**: 1.0  
**Last Updated**: November 2024

## Overview

The VESTA Assistant API provides a Python-based interface for voice interaction, touch sensing, and AI-powered responses. This document details the core VestaAssistant class and its methods for integration and extension.

## Quick Start

```python
from vesta_main import VestaAssistant

# Initialize the assistant
assistant = VestaAssistant()

# Start the main loop
assistant.run()
```

## Class: VestaAssistant

The main class handling all VESTA operations including audio processing, speech recognition, and response generation.

### Constructor

```python
VestaAssistant()
```

**Initializes:**
- OpenAI client with API key from environment
- Audio configuration (44.1kHz, mono)
- Touch sensor (MPR121) if available
- Cache and sound effects directories
- System prompt from `prompt.txt`

**Environment Variables Required:**
- `OPENAI_API_KEY`: Your OpenAI API key

**Raises:**
- `SystemExit`: If API key not found
- `ImportError`: If required libraries missing

### Configuration Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `sample_rate` | int | 44100 | Audio sampling rate in Hz |
| `channels` | int | 1 | Number of audio channels (mono) |
| `recording_duration` | int | 4 | User query recording time (seconds) |
| `hotword_duration` | int | 2 | Hotword detection time (seconds) |
| `playback_device` | str | "plughw:1" | ALSA playback device identifier |
| `hotwords` | list | ["vista", "vesta", "viesta", "vysta", "festa", "fiesta"] | Recognized wake words |

### Core Methods

#### run()
```python
def run(self) -> None
```
Main execution loop. Continuously listens for hotword activation via audio or touch sensor.

**Behavior:**
1. Monitors for hotword detection
2. Plays acknowledgment sound when triggered
3. Records user query
4. Processes query in separate thread
5. Handles keyboard interrupts gracefully

**Example:**
```python
assistant = VestaAssistant()
try:
    assistant.run()  # Blocks until interrupted
except KeyboardInterrupt:
    print("Shutting down VESTA")
```

#### _detect_hotword()
```python
def _detect_hotword(self) -> bool
```
Detects activation through touch sensor or voice command.

**Returns:**
- `bool`: True if hotword detected, False otherwise

**Priority:**
1. Touch sensor (if available) - immediate response
2. Audio hotword detection - 2 second listening window

#### _get_user_query()
```python
def _get_user_query(self) -> Optional[str]
```
Records and transcribes user's voice query.

**Returns:**
- `str`: Transcribed text of user query
- `None`: If no speech detected or transcription failed

**Process:**
1. Records 4 seconds of audio
2. Attempts Google Speech Recognition
3. Falls back to Sphinx if Google fails
4. Cleans up temporary files

#### _get_response()
```python
def _get_response(self, query: str) -> str
```
Generates response using cached data or OpenAI API.

**Parameters:**
- `query` (str): User's transcribed question

**Returns:**
- `str`: Generated response text

**Features:**
- Response caching for repeated queries
- 8-second timeout for API calls
- Fallback responses for common query types
- Graceful error handling

**Cache Key Generation:**
```python
cache_key = hashlib.md5(query.lower().strip().encode()).hexdigest()
```

#### _speak_response()
```python
def _speak_response(self, text: str) -> None
```
Converts text to speech and plays through speakers.

**Parameters:**
- `text` (str): Response text to speak

**Process:**
1. Generate MP3 using Google TTS
2. Convert to WAV format
3. Apply 1.3x speed adjustment
4. Play through configured audio device

### Audio Processing Methods

#### _record_audio()
```python
def _record_audio(self, duration: int) -> Optional[str]
```
Records audio for specified duration.

**Parameters:**
- `duration` (int): Recording time in seconds

**Returns:**
- `str`: Path to temporary WAV file
- `None`: If recording failed

#### _transcribe_audio()
```python
def _transcribe_audio(self, audio_file: str) -> Optional[str]
```
Transcribes audio file to text using speech recognition.

**Parameters:**
- `audio_file` (str): Path to WAV audio file

**Returns:**
- `str`: Transcribed text (lowercase)
- `None`: If transcription failed

### Utility Methods

#### _convert_mp3_to_wav()
```python
def _convert_mp3_to_wav(self, input_path: str, output_path: str) -> None
```
Converts MP3 to WAV using FFmpeg with tempo adjustment.

**Parameters:**
- `input_path` (str): Source MP3 file path
- `output_path` (str): Destination WAV file path

**FFmpeg Command:**
```bash
ffmpeg -i input.mp3 -f wav -filter:a "atempo=1.3" -y output.wav
```

#### _play_audio()
```python
def _play_audio(self, audio_path: str) -> None
```
Plays audio file through ALSA sound system.

**Parameters:**
- `audio_path` (str): Path to audio file

#### _get_cache_key()
```python
def _get_cache_key(self, text: str) -> str
```
Generates MD5 hash for cache storage.

**Parameters:**
- `text` (str): Text to hash

**Returns:**
- `str`: 32-character hexadecimal hash

## Error Handling

The API implements comprehensive error handling:

### Audio Errors
```python
try:
    recording = sd.rec(...)
except Exception as e:
    logger.error(f"Error recording audio: {e}")
    return None
```

### API Timeout
```python
completion = self.client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    timeout=8.0  # 8-second timeout
)
```

### Fallback Responses
Common query patterns have predefined fallbacks:
- "what is" → Definition unavailable response
- "weather" → Weather service unavailable
- "how to" → Instructions unavailable

## Extension Points

### Custom Hotwords
Modify the `hotwords` list:
```python
assistant.hotwords.append("custom_word")
```

### Custom System Prompt
Create `prompt.txt` in the working directory:
```
You are VESTA, a helpful home assistant. 
Provide concise, friendly responses.
```

### Touch Sensor Integration
The API automatically detects MPR121 touch sensor:
```python
if TOUCH_SENSOR_AVAILABLE:
    # Touch sensor initialized
    # Any of 12 touch points trigger activation
```

## Threading Model

Query processing occurs in separate threads to maintain responsiveness:

```python
thread = threading.Thread(target=self._process_and_speak, args=(query,))
thread.daemon = True
thread.start()
```

This prevents blocking during:
- API calls to OpenAI
- Text-to-speech generation
- Audio playback

## File Structure

```
vesta/
├── vesta_main.py          # Main API implementation
├── prompt.txt             # System prompt (optional)
├── env.env               # Environment variables
├── data/
│   ├── responses/        # Cached responses
│   └── sound_effects/    # Audio feedback files
└── requirements.txt      # Python dependencies
```

## Dependencies

Required Python packages:
- `openai>=1.0.0`
- `python-dotenv`
- `SpeechRecognition`
- `sounddevice`
- `numpy`
- `scipy`
- `gtts`
- `playsound3`
- `adafruit-circuitpython-mpr121` (optional)

## Performance Considerations

- **Response Time**: Average 2-3 seconds with caching
- **Memory Usage**: ~150MB typical
- **CPU Usage**: Spikes during audio processing
- **Cache Size**: Unlimited (manual cleanup required)

## Security Notes

- API key stored in environment variable
- No audio recorded without hotword activation
- Cache stored locally only
- No network requests except to OpenAI and Google TTS

---

**Related Documents:**
- VESTA-USER-001: User Manual
- VESTA-DIAG-001: Diagnostic Procedures
- VESTA-HARD-001: Hardware Assembly Guide