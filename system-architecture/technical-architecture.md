# VESTA System Architecture Document

**Document ID**: VESTA-ARCH-001  
**Version**: 2.0  
**Last Updated**: November 2024  
**Audience**: Service Engineers, Technical Staff

## Executive Summary

VESTA (Virtual Enhanced Speech and Text Assistant) is a voice-activated AI assistant combining embedded hardware with cloud-based natural language processing. This document provides technical staff with a comprehensive understanding of system components, data flow, and integration points for effective troubleshooting and service.

## System Overview

### Core Components

```
┌─────────────────────┐
│   User Interface    │
│  ┌──────────────┐   │     ┌─────────────────┐
│  │ Touch Sensor │   │     │   Cloud APIs    │
│  └──────┬───────┘   │     │                 │
│  ┌──────▼───────┐   │     │ ┌─────────────┐ │
│  │ Microphones  │   │────▶│ │   OpenAI    │ │
│  └──────┬───────┘   │     │ └─────────────┘ │
│  ┌──────▼───────┐   │     │ ┌─────────────┐ │
│  │  LED Ring    │   │◀────│ │ Google TTS  │ │
│  └──────┬───────┘   │     │ └─────────────┘ │
│  ┌──────▼───────┐   │     └─────────────────┘
│  │   Speakers   │   │
│  └──────────────┘   │
└─────────────────────┘
```

### Hardware Architecture

#### Processing Unit
- **Device**: Raspberry Pi 5 (8GB RAM)
- **OS**: Raspberry Pi OS (64-bit)
- **Storage**: 32GB SD Card (Class 10)
- **Power**: 27W USB-C PD

#### Audio Subsystem
```
Microphones (I2S) ──┐
                    ├──▶ Raspberry Pi ──▶ USB DAC ──▶ Amplifier ──▶ Speakers
Touch Sensor (I2C) ─┘         │
                              └──▶ LED Ring (GPIO)
```

### Software Architecture

#### Layer Model
```
┌─────────────────────────────────────┐
│        Application Layer            │
│    (vesta_main.py - Main Loop)      │
├─────────────────────────────────────┤
│        Service Layer                │
│  (Audio, Speech, AI, Threading)     │
├─────────────────────────────────────┤
│        Hardware Abstraction         │
│   (GPIO, I2S, I2C, USB, ALSA)      │
├─────────────────────────────────────┤
│        Operating System             │
│      (Linux Kernel & Drivers)       │
└─────────────────────────────────────┘
```

## Detailed Component Specifications

### 1. Audio Input System

#### Hardware Components
- **Microphones**: 2x INMP441 MEMS
  - Interface: I2S digital
  - Sampling: 44.1kHz, 24-bit
  - SNR: 61dB
  - Sensitivity: -26dBFS

#### Software Processing
```python
Audio Input Pipeline:
1. I2S Data Capture (44.1kHz stereo)
2. Buffer Accumulation (2-4 second windows)
3. Stereo to Mono Conversion
4. WAV File Generation
5. Speech Recognition Processing
```

#### Pin Connections
| Signal | GPIO Pin | Physical Pin |
|--------|----------|--------------|
| BCLK | GPIO 18 | Pin 12 |
| LRCLK | GPIO 19 | Pin 35 |
| DATA | GPIO 20 | Pin 38 |
| VDD | 3.3V | Pin 1 |
| GND | Ground | Pin 6 |

### 2. Voice Processing Pipeline

#### Detection Flow
```
Continuous Listening (2s chunks)
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ Hotword Present?│────▶│ Touch Detected? │
└────────┬────────┘ No  └────────┬────────┘
         │ Yes                   │ Yes
         ▼                       │
    Audio Feedback ◀─────────────┘
         │
         ▼
  Record Query (4s)
         │
         ▼
  Google Speech API ──fail──▶ Sphinx Offline
         │
         ▼
    Query Text
```

#### Hotword Detection
- Primary words: "vista", "vesta", "viesta"
- Alternative recognition: "vysta", "festa", "fiesta"
- Case-insensitive matching
- 2-second detection window

### 3. AI Processing System

#### Request Flow
```python
User Query → Cache Check → Cache Hit? → Return Cached
                ↓              ↓
               No             Yes
                ↓
         OpenAI API Call
                ↓
         gpt-4o-mini Model
                ↓
         Response Text
                ↓
         Cache Storage
```

#### API Configuration
- **Model**: gpt-4o-mini
- **Timeout**: 8 seconds
- **Token Limit**: Context-dependent
- **Temperature**: Default (0.7)
- **System Prompt**: Customizable via prompt.txt

#### Caching System
- **Key Generation**: MD5 hash of normalized query
- **Storage**: Local filesystem (data/responses/)
- **Format**: Plain text files
- **Eviction**: Manual (no automatic cleanup)

### 4. Audio Output System

#### Text-to-Speech Pipeline
```
Response Text
     │
     ▼
Google TTS API
     │
     ▼
  MP3 File
     │
     ▼
FFmpeg Convert
     │
     ▼
WAV @ 1.3x Speed
     │
     ▼
ALSA Playback
     │
     ▼
USB DAC → Amp → Speakers
```

#### Audio Specifications
- **DAC**: AudioQuest DragonFly
- **Amplifier**: PAM8302 (2.5W per channel)
- **Speakers**: 40mm, 4Ω, 3W rated
- **Playback Device**: ALSA plughw:1

### 5. User Interface Components

#### Touch Sensor (MPR121)
- **Interface**: I2C (Address 0x5A)
- **Channels**: 12 capacitive inputs
- **Response Time**: <100ms
- **Sensitivity**: Adjustable via registers

#### LED Ring (WS2812B)
- **LEDs**: 24-60 addressable RGB
- **Interface**: Single-wire serial (GPIO 21)
- **Power**: 5V, up to 3.6A at full white
- **Update Rate**: 400Hz

#### Status Indicators
| LED Pattern | System State | Meaning |
|-------------|--------------|---------|
| Breathing Blue | Starting | System initialization |
| Solid Blue | Ready | Awaiting activation |
| Pulsing Blue | Processing | Query being handled |
| Green | Speaking | Audio output active |
| Red | Error | Check diagnostics |
| Yellow | Network | Connecting to services |

## Data Flow Diagrams

### Main Execution Loop
```
┌─────────────┐
│    START    │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│  Main Loop  │────▶│ Check Touch  │
└──────┬──────┘     └──────┬───────┘
       │                   │ Touched
       ▼                   ▼
┌──────────────┐    ┌──────────────┐
│Listen Hotword│    │Process Query │
└──────┬───────┘    └──────┬───────┘
       │ Detected          │
       └──────────┬────────┘
                  ▼
           ┌──────────────┐
           │ Play Sound   │
           └──────┬───────┘
                  ▼
           ┌──────────────┐
           │Record Query  │
           └──────┬───────┘
                  ▼
           ┌──────────────┐
           │  New Thread  │
           └──────┬───────┘
                  ▼
           ┌──────────────┐
           │   Get LLM    │
           │   Response   │
           └──────┬───────┘
                  ▼
           ┌──────────────┐
           │Speak Response│
           └──────────────┘
```

### Threading Model
```
Main Thread                 Worker Thread
    │                           │
    ├─ Audio Detection          │
    ├─ Touch Monitoring         │
    ├─ LED Control              │
    │                           │
    └─ Spawn Thread ──────────▶ ├─ API Call
                                ├─ TTS Generation
                                ├─ Audio Playback
                                └─ Cleanup
```

## Network Architecture

### API Endpoints
| Service | Endpoint | Protocol | Port | Purpose |
|---------|----------|----------|------|---------|
| OpenAI | api.openai.com | HTTPS | 443 | LLM queries |
| Google TTS | translate.google.com | HTTPS | 443 | Speech synthesis |
| Google Speech | speech.googleapis.com | HTTPS | 443 | Speech recognition |

### Network Requirements
- **Bandwidth**: Minimum 1 Mbps
- **Latency**: <200ms recommended
- **Protocols**: HTTPS only
- **DNS**: System default

## Power Management

### Power States
1. **Active** (7-10W)
   - All systems operational
   - LED ring at full brightness
   - Audio amplifier powered

2. **Idle** (3-5W)
   - Listening for hotword
   - LED ring dimmed
   - Amplifier in standby

3. **Sleep** (1-2W)
   - Not implemented in current version
   - Future enhancement

### Power Distribution
```
USB-C PD (27W) ──┬─── RPi 5 (5V @ 5A max)
                 │
                 ├─── LED Ring (5V @ 1A)
                 │
                 ├─── Amplifier (5V @ 1A)
                 │
                 └─── Peripherals (3.3V @ 500mA)
```

## Error Handling & Recovery

### Automatic Recovery
1. **Network Failures**
   - Cached response fallback
   - Offline speech recognition
   - Retry with exponential backoff

2. **Audio Failures**
   - Automatic device re-initialization
   - Alternative audio paths
   - Diagnostic logging

3. **API Timeouts**
   - 8-second hard timeout
   - Fallback responses
   - Cache-first strategy

### Manual Intervention Required
- Hardware failures (mic, speaker)
- Persistent API authentication errors
- File system corruption
- Power supply issues

## Performance Metrics

### Response Times
| Operation | Typical | Maximum |
|-----------|---------|---------|
| Hotword Detection | 50ms | 200ms |
| Speech Recognition | 1-2s | 4s |
| API Response | 1-3s | 8s |
| TTS Generation | 500ms | 2s |
| Total Response | 3-5s | 15s |

### Resource Usage
- **CPU**: 15-40% during processing
- **RAM**: 150-300MB typical
- **Storage**: 1GB + cache
- **Network**: 10-50KB per query

## Security Considerations

### Data Privacy
- No audio stored without activation
- Queries cached locally only
- API key in environment variables
- No user identification

### Network Security
- HTTPS for all external communication
- No incoming connections required
- Local network only for configuration

## Maintenance Points

### Log Files
- Location: `/var/log/vesta/`
- Rotation: Daily, 7-day retention
- Levels: INFO, WARNING, ERROR

### Cache Management
```bash
# Check cache size
du -sh data/responses/

# Clear cache older than 30 days
find data/responses/ -mtime +30 -delete
```

### System Health Checks
```bash
# Audio system
aplay -l
arecord -l

# I2C devices
i2cdetect -y 1

# GPIO status
gpio readall

# Service status
systemctl status vesta.service
```

## Diagnostic Commands

### Quick Diagnostics
```bash
# Test microphones
python3 -c "from vesta_main import *; VestaAssistant()._record_audio(2)"

# Test speakers
speaker-test -c 2 -D plughw:1

# Test API connection
curl -I https://api.openai.com

# Check touch sensor
i2cget -y 1 0x5a 0x00
```

---

**Related Documents:**
- VESTA-DIAG-001: Diagnostic Procedures
- VESTA-API-001: API Reference
- VESTA-HARD-001: Hardware Assembly