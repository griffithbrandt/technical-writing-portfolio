# Code Documentation Best Practices

**Document ID**: VESTA-CODE-001  
**Version**: 1.0  
**Last Updated**: November 2024  
**Purpose**: Demonstrating clear code documentation techniques

## Overview

This document showcases documentation practices implemented in the VESTA project, demonstrating how clear documentation enhances code maintainability and reduces service complexity.

## Documentation Levels

### 1. Module-Level Documentation

```python
#!/usr/bin/env python3
"""
VESTA: Virtual Enhanced Speech and Text Assistant

This module implements the core voice assistant functionality including:
- Hotword detection via audio and touch input
- Speech recognition and natural language processing
- Response generation using OpenAI API
- Text-to-speech output

Architecture:
    Main thread handles input detection
    Worker threads process API calls and audio generation
    
Requirements:
    - Raspberry Pi 5 with I2S microphones
    - Python 3.9+ with dependencies in requirements.txt
    - Valid OpenAI API key in environment
"""
```

**Key Elements:**
- Purpose statement
- Feature overview
- Architecture notes
- Requirements list

### 2. Class Documentation

```python
class VestaAssistant:
    """
    Main VESTA assistant class handling voice interaction pipeline.
    
    This class orchestrates all components of the voice assistant including
    audio capture, speech recognition, AI processing, and voice synthesis.
    
    Attributes:
        client (OpenAI): Configured OpenAI client instance
        sample_rate (int): Audio sampling rate in Hz (default: 44100)
        recording_duration (int): Query recording window in seconds
        hotwords (list): Recognized activation phrases
        
    Example:
        >>> assistant = VestaAssistant()
        >>> assistant.run()  # Starts main listening loop
        
    Note:
        Requires OPENAI_API_KEY environment variable
        Audio device configuration in ALSA required
    """
```

**Documentation Standards:**
- Clear purpose description
- Attributes documented with types
- Usage examples provided
- Important notes highlighted

### 3. Method Documentation

```python
def _detect_hotword(self) -> bool:
    """
    Detect activation through touch sensor or voice command.
    
    Checks for activation in priority order:
    1. Touch sensor (immediate response)
    2. Audio hotword (2-second window)
    
    The audio detection is skipped if touch is detected for 
    faster response time and reduced CPU usage.
    
    Returns:
        bool: True if activation detected, False otherwise
        
    Raises:
        AudioException: If microphone initialization fails
        
    Side Effects:
        - Records 2 seconds of audio (if no touch)
        - Creates temporary WAV file
        - Logs detection events
        
    Performance:
        Touch: <50ms response
        Audio: 2-3s including recognition
    """
```

**Best Practices Shown:**
- Parameter types specified
- Return values documented
- Side effects noted
- Performance characteristics included

### 4. Inline Documentation

```python
def _record_audio(self, duration: int) -> Optional[str]:
    """Record audio for specified duration."""
    try:
        # Use 44.1kHz for compatibility with speech recognition
        # Higher rates don't improve recognition accuracy
        recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16'  # 16-bit for smaller files
        )
        
        # Wait for recording to complete
        # sd.rec is non-blocking by default
        sd.wait()
        
        # Save to temporary file
        # Using NamedTemporaryFile for automatic cleanup
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,  # We'll delete manually after processing
            suffix='.wav'
        )
        temp_path = temp_file.name
        temp_file.close()
        
        # Write audio data
        # scipy.io.wavfile handles WAV header creation
        write(temp_path, self.sample_rate, recording)
        
        return temp_path
        
    except Exception as e:
        # Log but don't crash - audio issues are recoverable
        logger.error(f"Recording failed: {e}")
        return None
```

**Inline Standards:**
- Explain "why" not just "what"
- Document non-obvious decisions
- Note external dependencies
- Clarify error handling strategy

### 5. Configuration Documentation

```python
# Audio configuration
self.sample_rate = 44100      # Industry standard, best compatibility
self.channels = 1             # Mono sufficient for speech
self.recording_duration = 4   # Balanced for typical queries
self.hotword_duration = 2     # Minimum reliable detection window

# Hardware pin assignments (BCM numbering)
# These match the PCB rev 3.1 layout - DO NOT CHANGE
GPIO_ASSIGNMENTS = {
    'I2S_BCLK': 18,      # Pin 12 physical
    'I2S_LRCLK': 19,     # Pin 35 physical  
    'I2S_DATA': 20,      # Pin 38 physical
    'LED_DATA': 21,      # Pin 40 physical
}

# API Configuration
API_TIMEOUT = 8.0        # Seconds - prevents hanging on network issues
MODEL = "gpt-4o-mini"    # Optimized for speed vs. quality
MAX_RETRIES = 3          # Balance between reliability and response time
```

**Configuration Best Practices:**
- Group related settings
- Document units and ranges
- Explain tradeoff decisions
- Warn about critical values

### 6. Error Handling Documentation

```python
try:
    # Attempt primary recognition service
    text = recognizer.recognize_google(audio).lower()
    
except sr.UnknownValueError:
    # Expected when no clear speech detected
    # Not logged as error - happens frequently in normal use
    logger.debug("No speech detected in audio")
    return None
    
except sr.RequestError as e:
    # Network or API issues - attempt fallback
    logger.warning(f"Google API failed: {e}, trying offline")
    try:
        # Sphinx offline recognition - lower quality but works
        text = recognizer.recognize_sphinx(audio).lower()
    except Exception:
        # Complete failure - service will need inspection
        logger.error("All recognition methods failed")
        return None
```

**Error Documentation Standards:**
- Explain what each exception means
- Document recovery strategies
- Differentiate severity levels
- Guide troubleshooting approach

### 7. Complex Algorithm Documentation

```python
def _calculate_cache_key(self, query: str) -> str:
    """
    Generate deterministic cache key for query storage.
    
    Algorithm:
    1. Normalize text (lowercase, strip whitespace)
    2. Remove common variations that don't affect meaning
    3. Generate MD5 hash of normalized text
    
    This approach ensures:
    - "What's the weather?" == "what is the weather"
    - "Hey what's up" != "Hey what's down"
    - Cache keys are filesystem-safe
    
    The MD5 hash is used for speed, not security. Collisions
    are acceptable as they only affect cache efficiency.
    
    Args:
        query: Raw user query text
        
    Returns:
        32-character hexadecimal cache key
        
    Example:
        >>> _calculate_cache_key("What's the WEATHER?")
        'a1b2c3d4e5f6789...'
    """
    # Normalization steps with reasoning
    normalized = query.lower().strip()
    
    # Common contractions that don't change meaning
    replacements = {
        "what's": "what is",
        "where's": "where is",
        "who's": "who is",
        "won't": "will not",
    }
    
    for contraction, expanded in replacements.items():
        normalized = normalized.replace(contraction, expanded)
    
    # Generate hash - MD5 is fast and collision-resistant enough
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()
```

### 8. Testing Documentation

```python
def test_microphone_levels():
    """
    Diagnostic test for microphone input levels.
    
    Test Procedure:
    1. Record 3 seconds of ambient noise
    2. Calculate RMS level
    3. Verify within acceptable range
    
    Expected Results:
    - Quiet room: -45 to -50 dB
    - Normal environment: -35 to -45 dB
    - Noisy environment: > -35 dB
    
    Troubleshooting:
    - No signal (-inf dB): Check connections
    - Constant high level: Check for interference
    - Clipping (0 dB): Reduce gain
    """
```

## Documentation Tools Integration

### Docstring Formats

**Google Style** (Recommended for Python):
```python
def send_query(self, text: str, timeout: float = 8.0) -> str:
    """Send query to language model.
    
    Args:
        text: User query text
        timeout: Maximum wait time in seconds
        
    Returns:
        Generated response text
        
    Raises:
        APIError: If API call fails
        TimeoutError: If timeout exceeded
    """
```

**Type Hints** (Enhanced clarity):
```python
from typing import Optional, List, Dict, Union

def process_audio(
    audio_data: np.ndarray,
    sample_rate: int = 44100,
    channels: int = 1
) -> Optional[str]:
    """Process audio data with full type information."""
```

### Automated Documentation

**Generating API Docs**:
```bash
# Using pydoc
pydoc -w vesta_main

# Using Sphinx
sphinx-apidoc -o docs/ vesta/

# Using pdoc3
pdoc --html --output-dir docs vesta_main
```

## Code Review Checklist

### Documentation Requirements
- [ ] Module has descriptive docstring
- [ ] All public methods documented
- [ ] Complex logic has inline comments
- [ ] Configuration values explained
- [ ] Error handling documented
- [ ] Examples provided for non-obvious usage
- [ ] Type hints on all parameters
- [ ] Side effects noted
- [ ] Performance characteristics documented
- [ ] Dependencies listed

## Real-World Impact

### Before Documentation
```python
def proc(d):
    r = sd.rec(int(d * 44100), 44100, 1, 'int16')
    sd.wait()
    return r
```

**Issues:**
- Purpose unclear
- Magic numbers
- No error handling
- Maintenance nightmare

### After Documentation
```python
def record_audio_segment(duration_seconds: float) -> Optional[np.ndarray]:
    """
    Record audio from default microphone.
    
    Args:
        duration_seconds: Recording duration (0.1 to 60.0)
        
    Returns:
        Audio data as int16 numpy array, None if failed
        
    Note:
        Uses system default audio input at 44.1kHz mono
    """
    SAMPLE_RATE = 44100  # Standard CD quality
    CHANNELS = 1         # Mono for speech recognition
    
    try:
        audio_data = sd.rec(
            int(duration_seconds * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16'
        )
        sd.wait()  # Block until recording complete
        return audio_data
        
    except sd.PortAudioError as e:
        logger.error(f"Audio hardware error: {e}")
        return None
```

**Benefits:**
- Self-documenting code
- Clear error handling
- Maintainable constants
- Type safety

---

**Key Takeaway**: Good documentation is not about quantity but about answering the "why" behind the code. Every comment should help future maintainers (including yourself) understand decisions and avoid pitfalls.