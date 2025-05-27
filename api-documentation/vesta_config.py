# vesta_config.py
"""
VESTA Configuration Module

Last Updated: November 2024
Version: 3.1
"""

import os
from pathlib import Path

# ============================================================================
# AUDIO CONFIGURATION
# ============================================================================

AUDIO_CONFIG = {
    # Sampling Configuration
    'sample_rate': 44100,        # Hz - Standard CD quality, optimal for speech
    'channels': 1,               # Mono - sufficient for voice commands
    'bit_depth': 16,            # 16-bit provides good quality/size balance
    
    # Recording Windows
    'hotword_duration': 2.0,     # Seconds - minimum reliable detection window
    'query_duration': 4.0,       # Seconds - accommodates most voice queries
    'max_duration': 10.0,        # Seconds - prevents runaway recordings
    
    # Audio Devices (ALSA)
    'input_device': 'plughw:1,0',   # Hardware device bypasses ALSA mixing
    'output_device': 'plughw:1',    # USB DAC for quality output
    
    # Quality Settings
    'noise_threshold': -45,      # dB - ambient noise rejection level
    'vad_aggressiveness': 2,     # 0-3, higher = more aggressive filtering
}

# ============================================================================
# HARDWARE PIN ASSIGNMENTS
# ============================================================================
# CRITICAL: These match PCB revision 3.1 - DO NOT MODIFY without hardware changes

GPIO_PINS = {
    # I2S Audio Interface (BCM numbering)
    'I2S_BCLK': 18,             # Bit Clock - Pin 12 physical
    'I2S_LRCLK': 19,            # Word Select - Pin 35 physical  
    'I2S_DATA': 20,             # Serial Data - Pin 38 physical
    
    # I2C Touch Interface
    'I2C_SDA': 2,               # Data line - Pin 3 physical
    'I2C_SCL': 3,               # Clock line - Pin 5 physical
    
    # LED Control
    'LED_DATA': 21,             # WS2812B data - Pin 40 physical
    'LED_ENABLE': 22,           # Optional power control - Pin 15 physical
}

# I2C Addresses
I2C_DEVICES = {
    'touch_sensor': 0x5A,       # MPR121 default address
    'temp_sensor': 0x48,        # Optional temperature sensor
}

# ============================================================================
# API CONFIGURATION
# ============================================================================

API_CONFIG = {
    # OpenAI Settings
    'model': 'gpt-4o-mini',     # Optimized for speed vs cost
    'temperature': 0.7,         # Balance creativity/consistency
    'max_tokens': 150,          # Keep responses concise
    'timeout': 8.0,             # Seconds - prevent hanging
    
    # Retry Logic
    'max_retries': 3,           # API call retry attempts
    'retry_delay': 1.0,         # Seconds between retries
    'backoff_factor': 2.0,      # Exponential backoff multiplier
    
    # Rate Limiting
    'requests_per_minute': 20,   # Stay within tier limits
    'cooldown_period': 3.0,      # Seconds between requests
}

# ============================================================================
# FILE PATHS
# ============================================================================

# Base directory (relative to script location)
BASE_DIR = Path(__file__).parent

# Data directories
DATA_PATHS = {
    'cache_dir': BASE_DIR / 'data' / 'cache',
    'logs_dir': BASE_DIR / 'data' / 'logs',
    'audio_dir': BASE_DIR / 'data' / 'audio',
    'config_dir': BASE_DIR / 'config',
}

# Ensure directories exist
for path in DATA_PATHS.values():
    path.mkdir(parents=True, exist_ok=True)

# Configuration files
CONFIG_FILES = {
    'env_file': BASE_DIR / 'env.env',
    'prompt_file': BASE_DIR / 'prompt.txt',
    'hotwords_file': BASE_DIR / 'hotwords.json',
}

# ============================================================================
# PERFORMANCE TUNING
# ============================================================================

PERFORMANCE = {
    # Threading
    'worker_threads': 2,         # Parallel processing threads
    'queue_size': 10,           # Maximum queued requests
    
    # Caching
    'cache_enabled': True,       # Use response cache
    'cache_ttl': 86400,         # Seconds (24 hours)
    'max_cache_size': 1000,     # Maximum cached responses
    
    # Memory Management
    'audio_buffer_size': 4096,   # Samples per buffer
    'max_memory_mb': 300,       # Memory limit warning threshold
}

# ============================================================================
# FEATURE FLAGS
# ============================================================================

FEATURES = {
    'touch_sensor': True,        # Enable MPR121 touch activation
    'led_feedback': True,        # Visual status indicators
    'offline_mode': False,       # Fallback to local responses
    'debug_mode': os.getenv('DEBUG', 'False').lower() == 'true',
    'save_recordings': False,    # Store audio for training
}

# ============================================================================
# ERROR HANDLING
# ============================================================================

ERROR_RESPONSES = {
    # User-friendly error messages mapped to error codes
    'E001': "I need an API key to function. Please check the configuration.",
    'E002': "I'm having trouble with the audio system. Please check the connections.",
    'E003': "I can't connect to the internet right now. Please check the network.",
    'E004': "I'm experiencing high temperature. Please check ventilation.",
    'E005': "Memory is running low. A restart might help.",
    
    # Default fallback
    'DEFAULT': "I encountered an error. Please check the logs for details.",
}

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """
    Validate configuration values at startup.
    
    Returns:
        bool: True if valid, raises ConfigError otherwise
    """
    # Check audio settings
    assert 8000 <= AUDIO_CONFIG['sample_rate'] <= 48000, \
        "Sample rate must be between 8000 and 48000 Hz"
    
    # Check GPIO pins don't conflict
    pin_list = list(GPIO_PINS.values())
    assert len(pin_list) == len(set(pin_list)), \
        "GPIO pin conflict detected"
    
    # Check API timeout is reasonable
    assert 1.0 <= API_CONFIG['timeout'] <= 30.0, \
        "API timeout must be between 1 and 30 seconds"
    
    # Verify required files exist
    if not CONFIG_FILES['env_file'].exists():
        raise FileNotFoundError(f"Required file missing: {CONFIG_FILES['env_file']}")
    
    return True

# Run validation on import
if __name__ != "__main__":
    validate_config()