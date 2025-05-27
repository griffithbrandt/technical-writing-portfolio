# SERVICE BULLETIN

**Bulletin Number**: VSB-2024-003  
**Issue Date**: November 15, 2024  
**Priority**: MANDATORY  
**Affected Models**: VESTA v3.0 - v3.0.9  
**Serial Numbers**: VTA-001

---

## SUBJECT: Critical Microphone Array Grounding Issue

### SAFETY NOTICE
⚠️ **WARNING**: Disconnect power before performing this service procedure. Failure to properly ground the microphone array may result in permanent damage to the I2S interface.

### ISSUE DESCRIPTION

Field reports indicate intermittent voice recognition failures in approximately 15% of VESTA units manufactured between September 1 and October 31, 2024. Root cause analysis has identified inadequate grounding of the MEMS microphone shields, resulting in electromagnetic interference (EMI) from the LED ring power supply.

**Symptoms Include:**
- Voice commands work intermittently (30-70% success rate)
- Clicking or buzzing in audio recordings
- Error code A003 appearing in logs
- Microphone sensitivity degrading over time

### AFFECTED COMPONENTS

| Component | Part Number | Description |
|-----------|-------------|-------------|
| Microphone Array PCB | VESTA-PCB-MIC-v1 | Dual MEMS microphone board |
| Ground Wire | N/A | Missing in affected units |
| Shielding Tape | 3M-1345 | Conductive adhesive tape |

### INSPECTION PROCEDURE

**Time Required**: 10 minutes

1. **Remove Top Shell**
   - Extract 4x M3 screws at 45°, 135°, 225°, 315°
   - Carefully lift shell, noting LED ring cable

2. **Visual Inspection**
   - Locate microphone array PCB beneath top port
   - Check for ground wire between PCB and chassis
   - **PASS**: Black wire connecting PCB ground to shell ground point
   - **FAIL**: No ground wire present

3. **Electrical Test**
   ```
   Using multimeter in continuity mode:
   - Probe 1: Microphone PCB ground pad
   - Probe 2: USB-C shell ground
   - PASS: <1Ω resistance
   - FAIL: >10Ω or open circuit
   ```

### REPAIR PROCEDURE

**Time Required**: 20 minutes  
**Skill Level**: Intermediate

#### Required Materials
- 22 AWG stranded wire (black, 10cm)
- Soldering iron (350°C)
- Flux paste
- Conductive tape (3M-1345)
- Isopropyl alcohol (99%)

#### Step-by-Step Instructions

1. **Prepare Ground Wire**
   - Cut 10cm of 22 AWG black wire
   - Strip 5mm from each end
   - Tin both ends with solder

2. **Attach to Microphone PCB**
   - Locate GND pad on PCB edge
   - Apply flux to pad
   - Solder wire to GND pad
   - Hold for 3 seconds until solid

3. **Route Ground Wire**
   - Guide wire along existing cable path
   - Avoid crossing speaker wires
   - Secure with existing cable ties

4. **Connect to Chassis Ground**
   - Locate ground post near USB-C port
   - Wrap wire clockwise around post
   - Solder connection
   - Verify <1Ω resistance

5. **Apply EMI Shielding**
   - Cut 30mm x 20mm conductive tape
   - Apply over microphone PCB bottom
   - Press firmly for 10 seconds
   - Ensure tape contacts ground wire

6. **Verification Testing**
   ```bash
   # Run microphone diagnostic
   sudo vesta-diag --mic-test --verbose
   
   # Expected output:
   # Mic 1: PASS (SNR: 58dB)
   # Mic 2: PASS (SNR: 57dB)
   # Ground: PASS (<1Ω)
   ```

### POST-REPAIR VALIDATION

1. **Functional Test**
   - Reassemble unit completely
   - Power on and wait for blue LED
   - Say "Hey VESTA" from 1 meter
   - Verify response within 2 seconds
   - Repeat 10 times (>90% success required)

2. **Audio Quality Check**
   ```bash
   # Record test sample
   arecord -D plughw:1,0 -f S16_LE -r 44100 -d 5 test.wav
   
   # Analyze for noise
   sox test.wav -n stat 2>&1 | grep "RMS"
   # RMS amplitude should be < -45dB with no speech
   ```

3. **Update Service Record**
   - Log repair date in unit history
   - Update firmware to v3.1.0
   - Apply "VSB-2024-003 COMPLETE" sticker

### PARTS AVAILABILITY

| Part | Order Code | Available |
|------|------------|-----------|
| Repair Kit | VESTA-SVC-003 | In stock |
| Ground Wire (100 pack) | VESTA-WIRE-22B | In stock |
| Conductive Tape | VESTA-TAPE-EMI | Limited |

Order through standard service channels or contact:
- Email: parts@vesta-support.com
- Phone: 1-800-VESTA-99

### QUALITY ASSURANCE

Units repaired under this bulletin are eligible for:
- Extended warranty (additional 6 months)
- Priority support status
- Free firmware updates for 2 years

Failed repairs should be escalated to Level 3 support with:
- Pre and post-repair diagnostic logs
- Photos of ground connection
- Audio samples demonstrating issue

### PREVENTION IN NEW UNITS

Manufacturing has implemented the following changes as of November 1, 2024:
1. Automated ground wire installation
2. 100% continuity testing at assembly
3. EMI shielding pre-applied to all PCBs
4. Updated QC checklist item #47

### TECHNICAL BACKGROUND

The issue occurs due to coupling between the high-frequency PWM signal driving the WS2812B LED ring (800kHz) and the unshielded I2S data lines. Without proper grounding, the microphone array PCB acts as an antenna, introducing noise into the audio signal path. The noise manifests as periodic spikes coinciding with LED color transitions.

Oscilloscope measurements show 120mV peak-to-peak noise on affected units, compared to <10mV on properly grounded systems. The added ground path provides a low-impedance return for coupled currents, preventing them from affecting the sensitive microphone inputs.

### REPORTING

Service centers must report completion through the online portal:
1. Navigate to https://service.vesta-assistant.com
2. Enter unit serial number
3. Select "VSB-2024-003" from bulletin menu
4. Upload post-repair diagnostic log
5. Submit completion certificate

**Deadline**: All affected units must be serviced by January 31, 2025

### CONTACT INFORMATION

**Technical Questions**:
- Email: engineering@vesta-assistant.com
- Slack: #service-bulletin-003

**Parts & Logistics**:
- Email: logistics@vesta-assistant.com
- Phone: 1-800-VESTA-00

**Escalation**:
- Level 3 Support: l3support@vesta-assistant.com
- Engineering Hotline: +1-555-VESTA-EN

---

**Document Control**:
- Author: Grifith Brandt
- Next Review: December 15, 2024

**Revision History**:
| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 15, 2024 | Initial release |
| 1.1 | Nov 18, 2024 | Added continuity test values |
| 1.2 | Nov 22, 2024 | Updated parts availability |