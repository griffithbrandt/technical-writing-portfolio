# Diagnostic Procedure: VESTA Microphone Array Malfunction

**Document ID**: VESTA-DIAG-001  
**Revision**: 1.2  
**Last Updated**: November 2024  
**Complexity**: Level 2 - Intermediate

## Overview
This procedure guides technicians through diagnosing and resolving microphone array issues in the VESTA voice assistant system. Common symptoms include poor voice recognition, no audio input, or intermittent detection failures.

## Required Tools
- Digital multimeter
- Oscilloscope (optional)
- Small Phillips screwdriver
- Anti-static wrist strap
- Diagnostic software v2.1+

## Safety Precautions
⚠️ **WARNING**: Always disconnect power before handling internal components
- Use proper ESD protection
- Handle MEMS microphones with care - do not apply pressure to ports

## Initial Assessment 

### Step 1: Verify Symptom
1. Power on VESTA system
2. Observe LED status indicator:
   - **Solid Blue**: Normal operation
   - **Flashing Red**: Hardware fault detected
   - **No Light**: Power issue (see Power Diagnostic Guide)
3. Say "Hey VESTA" from 3 feet away
4. Document response:
   - [ ] No response
   - [ ] Delayed response (>2 seconds)
   - [ ] Incorrect transcription
   - [ ] Intermittent response

### Step 2: Quick Software Check
```bash
# Run built-in diagnostic
$ sudo vesta-diag --mic-test

# Expected output:
# Mic 1 (Left): OK - Signal level: -42dB
# Mic 2 (Right): OK - Signal level: -41dB
```

If software reports "FAIL", proceed to Hardware Diagnostics.

## Hardware Diagnostics 

### Step 3: Visual Inspection
1. Remove top cover (4 screws)
2. Inspect microphone modules for:
   - Physical damage or debris in ports
   - Loose connections on I2S bus
   - Corrosion on pins
   - Proper seating of components

### Step 4: Electrical Testing

#### 4.1 Power Supply Verification
Using multimeter, verify at test points:
- TP1 (VDD): 3.3V ± 0.1V
- TP2 (GND): 0V
- TP3 (BCLK): Square wave present (scope)

**Decision Point**: 
- Voltages correct → Continue to 4.2
- Voltages incorrect → See Power Supply Diagnostic

#### 4.2 I2S Communication Test
1. Connect oscilloscope to I2S test points
2. Verify signals:
   - BCLK: 2.8MHz clock signal
   - LRCLK: 44.1kHz word select
   - DATA: Active data stream when speaking

### Step 5: Component Isolation
1. Disconnect Mic 2 (right channel)
2. Run diagnostic with only Mic 1:
   ```bash
   $ sudo vesta-diag --mic-test --single
   ```
3. If Mic 1 passes alone, Mic 2 is faulty
4. Repeat test with only Mic 2 connected

## Resolution Procedures

### Issue A: Single Microphone Failure
1. Replace faulty INMP441 module (part #VESTA-MIC-001)
2. Ensure proper orientation (port facing up)
3. Apply thermal compound to mounting points
4. Secure with provided mounting clips

### Issue B: I2S Bus Communication Failure
1. Reflow solder joints on SMD breadboard
2. Check continuity on all I2S lines
3. Replace jumper wires if resistance >1Ω
4. Update firmware if communication protocol mismatch

### Issue C: Environmental Interference
1. Check for sources of ultrasonic noise
2. Verify acoustic isolation foam intact
3. Ensure 6+ inch separation from speakers
4. Implement software noise filtering if needed

## Verification

### Step 6: System Validation
1. Reassemble system
2. Run full diagnostic suite:
   ```bash
   $ sudo vesta-diag --full-test
   ```
3. Perform voice recognition test:
   - "Hey VESTA, what's the weather?"
   - "Hey VESTA, set a timer for 5 minutes"
   - Test from multiple angles and distances

### Step 7: Documentation
Record in service log:
- [ ] Initial symptom
- [ ] Diagnostic results
- [ ] Components replaced
- [ ] Verification test results
- [ ] Total service time

## Escalation
If issue persists after following this procedure:
1. Generate diagnostic report: `sudo vesta-diag --export`
2. Contact Level 3 support with report attached
3. Consider full audio subsystem replacement
