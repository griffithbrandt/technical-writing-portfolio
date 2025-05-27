# VESTA Error Code Reference Guide

**Document ID**: VESTA-ERR-001  
**Version**: 1.5  
**Last Updated**: November 2024  
**For Model**: VESTA v3.x

## How to Use This Guide

1. Identify error code from LED pattern or log file
2. Find code in appropriate category
3. Follow resolution steps in order
4. Escalate if issue persists after all steps

## LED Error Patterns

### Critical Errors (Red Patterns)
| Pattern | Code | Meaning | Immediate Action |
|---------|------|---------|------------------|
| Solid Red | E001 | No API Key | Check environment configuration |
| Fast Blink Red | E002 | Hardware initialization failed | Check I2C/I2S connections |
| Slow Blink Red | E003 | Audio system failure | Verify USB DAC connected |
| Red + Blue Alt | E004 | Memory exhausted | Restart system |
| 3 Red Flashes | E005 | Critical temperature | Check ventilation |

### Warning States (Yellow Patterns)
| Pattern | Code | Meaning | Resolution |
|---------|------|---------|------------|
| Solid Yellow | W101 | Network connecting | Wait up to 60 seconds |
| Pulse Yellow | W102 | API rate limited | Reduce query frequency |
| Yellow Fade | W103 | Low signal quality | Check microphone placement |
| Yellow + Blue | W104 | Cache nearly full | Consider cache cleanup |

## System Error Codes

### Audio Subsystem (A000-A999)

#### A001: Microphone Not Detected
**Symptoms:**
- No response to voice commands
- Log shows "Failed to initialize I2S"

**Resolution:**
1. Verify I2S connections:
   ```bash
   gpio readall | grep -E "18|19|20"
   ```
2. Check for conflicting audio devices:
   ```bash
   arecord -l
   ```
3. Reload I2S kernel module:
   ```bash
   sudo modprobe -r snd_soc_bcm2835_i2s
   sudo modprobe snd_soc_bcm2835_i2s
   ```

#### A002: Speaker Output Failure
**Symptoms:**
- No audio output
- Log shows "ALSA: Device not found"

**Resolution:**
1. List audio devices:
   ```bash
   aplay -l
   ```
2. Test specific device:
   ```bash
   speaker-test -D plughw:1 -c 2
   ```
3. Check USB DAC LED status
4. Verify amplifier power connections

#### A003: Audio Buffer Overflow
**Symptoms:**
- Choppy or distorted audio
- CPU usage spikes during playback

**Resolution:**
1. Increase ALSA buffer size:
   ```bash
   echo "defaults.pcm.dmix.rate 44100" >> ~/.asoundrc
   echo "defaults.pcm.dmix.format S16_LE" >> ~/.asoundrc
   ```
2. Reduce system load
3. Check for thermal throttling

### Network Errors (N000-N999)

#### N001: DNS Resolution Failure
**Log Entry:** `socket.gaierror: [Errno -3] Temporary failure`

**Resolution:**
1. Test DNS:
   ```bash
   nslookup api.openai.com
   ```
2. Update DNS servers:
   ```bash
   echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
   ```
3. Flush DNS cache:
   ```bash
   sudo systemd-resolve --flush-caches
   ```

#### N002: SSL Certificate Error
**Log Entry:** `ssl.SSLError: certificate verify failed`

**Resolution:**
1. Update certificates:
   ```bash
   sudo apt update && sudo apt install ca-certificates
   ```
2. Sync system time:
   ```bash
   sudo ntpdate -s time.nist.gov
   ```
3. Check proxy settings

#### N003: Connection Timeout
**Log Entry:** `TimeoutError: Request timed out after 8.0s`

**Resolution:**
1. Test connectivity:
   ```bash
   ping -c 4 api.openai.com
   curl -I https://api.openai.com
   ```
2. Check firewall rules
3. Verify router configuration

### API Errors (P000-P999)

#### P001: Invalid API Key
**Response:** `401 Unauthorized`

**Resolution:**
1. Verify key in environment:
   ```bash
   grep OPENAI_API_KEY /home/pi/vesta/env.env
   ```
2. Test key directly:
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```
3. Regenerate key if compromised

#### P002: Rate Limit Exceeded
**Response:** `429 Too Many Requests`

**Resolution:**
1. Check current usage in OpenAI dashboard
2. Implement request throttling:
   ```python
   time.sleep(1)  # Add between requests
   ```
3. Upgrade API plan if needed

#### P003: Model Not Available
**Response:** `404 Model not found`

**Resolution:**
1. Verify model name in code
2. Check model availability:
   ```bash
   curl https://api.openai.com/v1/models
   ```
3. Update to available model

### Hardware Errors (H000-H999)

#### H001: I2C Bus Error
**Log Entry:** `OSError: [Errno 121] Remote I/O error`

**Resolution:**
1. Scan I2C bus:
   ```bash
   sudo i2cdetect -y 1
   ```
2. Check pull-up resistors (4.7kΩ)
3. Reduce I2C speed:
   ```bash
   sudo nano /boot/config.txt
   # Add: dtparam=i2c_baudrate=50000
   ```

#### H002: GPIO Already in Use
**Log Entry:** `RuntimeError: Channel already in use`

**Resolution:**
1. Check for conflicting processes:
   ```bash
   sudo lsof | grep GPIO
   ```
2. Release GPIO:
   ```python
   GPIO.cleanup()
   ```
3. Restart GPIO daemon:
   ```bash
   sudo systemctl restart pigpiod
   ```

#### H003: Touch Sensor Not Responding
**Symptoms:**
- Touch input ignored
- MPR121 not detected at 0x5A

**Resolution:**
1. Verify I2C address:
   ```bash
   i2cget -y 1 0x5a 0x5d
   ```
2. Reset sensor:
   ```python
   # Power cycle the sensor
   GPIO.output(SENSOR_POWER_PIN, GPIO.LOW)
   time.sleep(0.5)
   GPIO.output(SENSOR_POWER_PIN, GPIO.HIGH)
   ```
3. Check capacitive pads for moisture

### System Errors (S000-S999)

#### S001: Python Module Import Failure
**Log Entry:** `ImportError: No module named 'openai'`

**Resolution:**
1. Verify virtual environment:
   ```bash
   which python3
   pip list | grep openai
   ```
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```
3. Check Python version compatibility

#### S002: File System Full
**Log Entry:** `OSError: [Errno 28] No space left on device`

**Resolution:**
1. Check disk usage:
   ```bash
   df -h
   du -sh /home/pi/vesta/data/*
   ```
2. Clear cache:
   ```bash
   rm -rf /home/pi/vesta/data/responses/*
   ```
3. Remove old logs:
   ```bash
   sudo journalctl --vacuum-time=2d
   ```

#### S003: Permission Denied
**Log Entry:** `PermissionError: [Errno 13] Permission denied`

**Resolution:**
1. Check file ownership:
   ```bash
   ls -la /home/pi/vesta/
   ```
2. Fix permissions:
   ```bash
   sudo chown -R pi:pi /home/pi/vesta/
   chmod 755 /home/pi/vesta/vesta_main.py
   ```
3. Add user to required groups:
   ```bash
   sudo usermod -a -G audio,i2c,gpio pi
   ```

## Performance Warning Codes

### W201: High CPU Temperature
**Threshold:** >70°C

**Action:**
1. Check temperature:
   ```bash
   vcgencmd measure_temp
   ```
2. Improve ventilation
3. Add heatsinks if not present

### W202: Memory Pressure
**Threshold:** <100MB free

**Action:**
1. Check memory:
   ```bash
   free -h
   ```
2. Kill unnecessary processes
3. Increase swap space

### W203: Slow Response Time
**Threshold:** >10s total response

**Action:**
1. Check network latency
2. Review cache hit rate
3. Optimize prompt length

## Common Error Combinations

### "VESTA Won't Respond" Checklist
If experiencing E001 + A001 + H003:
1. Power cycle entire system
2. Check all cable connections
3. Reload all kernel modules
4. Run full diagnostic suite

### "Intermittent Failures" Pattern
If seeing W103 + N003 + S003:
1. Check for electromagnetic interference
2. Verify power supply stability
3. Replace USB cables
4. Shield I2C lines

## Diagnostic Tools

### Quick Health Check Script
```bash
#!/bin/bash
echo "=== VESTA Health Check ==="
echo "Temperature: $(vcgencmd measure_temp)"
echo "Memory: $(free -h | grep Mem | awk '{print $3"/"$2}')"
echo "Audio Devices: $(aplay -l | grep -c card)"
echo "I2C Devices: $(i2cdetect -y 1 2>&1 | grep -c "UU\|[0-9a-f][0-9a-f]")"
echo "API Status: $(curl -s -o /dev/null -w "%{http_code}" https://api.openai.com)"
echo "Cache Size: $(du -sh /home/pi/vesta/data/responses/ | cut -f1)"
```

### Log Analysis Commands
```bash
# Most frequent errors
grep ERROR /var/log/vesta.log | cut -d' ' -f5- | sort | uniq -c | sort -nr | head -10

# Error timeline
grep -E "ERROR|WARNING" /var/log/vesta.log | tail -20

# Specific error tracking
journalctl -u vesta -p err --since "1 hour ago"
```

## Escalation Procedures

### Level 1: User Resolvable
- LED pattern identification
- Power cycling
- Cable reseating
- Cache clearing

### Level 2: Technical Support
- Log file analysis
- Component testing
- Software reinstallation
- Configuration changes

### Level 3: Engineering
- Hardware replacement
- Firmware updates
- Design modifications
- Root cause analysis

---

**Quick Reference Card:**
```
Most Common Fixes:
1. Power cycle: Unplug for 30 seconds
2. Clear cache: rm -rf data/responses/*
3. Check connections: All cables seated
4. Restart service: sudo systemctl restart vesta
5. Update software: git pull && pip install -r requirements.txt
```

**Related Documents:**
- VESTA-DIAG-001: Diagnostic Procedures
- VESTA-USER-001: User Manual
- VESTA-LOG-001: Log Analysis Guide