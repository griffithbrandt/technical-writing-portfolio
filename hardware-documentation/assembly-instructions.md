# VESTA Hardware Assembly Instructions

**Document ID**: VESTA-HARD-001  
**Revision**: 3.1  
**Last Updated**: November 2024  
**Assembly Time**: 45-60 minutes  
**Difficulty**: Intermediate

## Required Tools

- Phillips screwdriver (PH1)
- 2.5mm hex driver
- Anti-static wrist strap
- Tweezers
- Wire strippers
- Soldering iron (optional)
- Multimeter for testing

## Bill of Materials

### 3D Printed Components
| Part | Quantity | Print Settings |
|------|----------|----------------|
| Shell Bottom | 1 | 0.2mm layer, 20% infill, supports OFF |
| Shell Top | 1 | 0.2mm layer, 20% infill, supports OFF |

### Electronic Components
| Component | Model | Quantity |
|-----------|-------|----------|
| Raspberry Pi 5 | 8GB RAM | 1 |
| MEMS Microphone | INMP441 | 2 |
| Touch Sensor | MPR121 | 1 |
| USB DAC | AudioQuest DragonFly | 1 |
| Speakers | 40mm 4Ω 3W | 2 |
| LED Ring | WS2812B 120mm | 1 |
| Amplifier Board | PAM8302 | 1 |

### Fasteners
| Type | Size | Quantity | Usage |
|------|------|----------|-------|
| Machine Screw | M3 x 12mm | 4 | Shell assembly |
| Machine Screw | M2.5 x 6mm | 4 | Pi mounting |
| Heat-Set Insert | M3 x 5mm | 4 | Top shell |
| Standoff | M2.5 x 8mm | 4 | Pi spacing |

## Pre-Assembly Checklist

- [ ] All 3D printed parts inspected for defects
- [ ] Support material removed from prints
- [ ] Screw holes cleared with appropriate drill bit
- [ ] Electronic components tested
- [ ] Work area ESD-safe

## Assembly Instructions

### Step 1: Prepare Shell Components (10 minutes)

#### 1.1 Install Heat-Set Inserts
1. Heat soldering iron to 200°C
2. Place M3 insert on screw receiver in top shell
3. Gently press iron into insert until flush
4. Repeat for all 4 positions at 45°, 135°, 225°, 315°

**Decision Point**: 
- Inserts flush and straight → Continue to 1.2
- Inserts crooked → Reheat and adjust

#### 1.2 Test Fit Shell Halves
1. Align equatorial lips of both halves
2. Check for smooth rotation without binding
3. Verify screw holes align properly

### Step 2: Install Raspberry Pi Mount (15 minutes)

#### 2.1 Mount Preparation
The bottom shell includes integrated mounting posts at these positions:
- X: ±29mm (58mm spacing)
- Y: ±24.5mm (49mm spacing)
- Height: 8mm from base

#### 2.2 Install Standoffs
1. Thread M2.5 standoffs into each mounting post
2. Tighten until snug (do not overtighten)
3. Verify all standoffs are same height

#### 2.3 Mount Raspberry Pi
1. Align Pi holes with standoffs
2. Place Pi with USB-C facing shell USB port
3. Secure with M2.5 x 6mm screws
4. Leave 5mm clearance on all sides

### Step 3: Audio System Installation (15 minutes)

#### 3.1 Speaker Installation
1. Position speakers at ±90° locations
2. Align with hexagonal grille patterns
3. Hot glue speakers to internal surface
4. Route wires through cable channels in ribs

**Wire Routing**:
```
Speaker L → Amp L+ L- → Pi GPIO
Speaker R → Amp R+ R- → Pi GPIO
```

#### 3.2 Amplifier Mounting
1. Place amplifier on dedicated mount post
2. Position at X:35mm, Y:0mm
3. Secure with hot glue or double-sided tape
4. Connect speaker wires to output terminals

#### 3.3 USB DAC Connection
1. Insert DAC into bottom USB port of Pi
2. Ensure clearance from other components
3. Connect 3.5mm cable to amplifier input

### Step 4: Sensor Integration (10 minutes)

#### 4.1 Microphone Array Setup
1. Mount MEMS microphones on custom PCB
2. Position PCB centered under top mic port
3. Connect I2S signals:
   - VDD → 3.3V (Pin 1)
   - GND → Ground (Pin 6)
   - BCLK → GPIO 18 (Pin 12)
   - LRCLK → GPIO 19 (Pin 35)
   - DATA → GPIO 20 (Pin 38)

#### 4.2 Touch Sensor Installation
1. Place MPR121 in top shell recess
2. Dimensions: 51mm x 25.2mm x 4.5mm
3. Connect I2C signals:
   - VCC → 3.3V
   - GND → Ground
   - SDA → GPIO 2 (Pin 3)
   - SCL → GPIO 3 (Pin 5)

### Step 5: LED Ring Installation (5 minutes)

#### 5.1 LED Positioning
1. Place LED ring in equatorial channel
2. Ensure even spacing around circumference
3. Channel dimensions: 9.5mm wide x 3mm deep

#### 5.2 Power Connection
1. Connect LED VCC to 5V (Pin 2)
2. Connect LED GND to Ground
3. Connect LED DATA to GPIO 21 (Pin 40)
4. Add 470Ω resistor on data line

### Step 6: Final Assembly (10 minutes)

#### 6.1 Cable Management
1. Route all cables through rib channels
2. Secure with small zip ties if needed
3. Ensure no wires cross moving parts
4. Verify no pinch points at shell junction

#### 6.2 Pre-Assembly Test
Before closing shell:
1. Power on system
2. Verify LED ring illuminates
3. Test audio output
4. Check touch sensor response

#### 6.3 Shell Closure
1. Align top and bottom shells
2. Ensure LED ring seats properly
3. Insert M3 x 12mm screws at 45° intervals
4. Tighten in cross pattern (45°→225°→135°→315°)
5. Do not overtighten - plastic will strip

### Step 7: Validation (5 minutes)

#### 7.1 Visual Inspection
- [ ] Shell halves aligned with <0.5mm gap
- [ ] All screws seated properly
- [ ] USB-C port accessible
- [ ] Microphone port unobstructed
- [ ] Touch sensor area smooth

#### 7.2 Functional Test
1. Connect power via USB-C port
2. Wait for boot sequence (30 seconds)
3. Observe LED status:
   - Breathing blue → System starting
   - Solid blue → Ready for use
4. Say "Hey VESTA" from 1 meter away
5. Verify audio response

## Troubleshooting

### Issue: LED Ring Not Illuminating
1. Check 5V power at LED connections
2. Verify data line continuity
3. Test with example WS2812B code
4. Replace LED ring if defective

### Issue: No Audio Output
1. Verify DAC LED is illuminated
2. Check amplifier power connections
3. Test speakers with multimeter (4Ω)
4. Verify ALSA configuration

### Issue: Poor Voice Recognition
1. Check microphone port for obstructions
2. Verify I2S clock signals with scope
3. Test with single microphone
4. Adjust gain in software

### Issue: Shell Won't Close
1. Check for wire interference
2. Verify heat-set inserts are flush
3. Ensure Pi components clear shell
4. File down any print artifacts

## Maintenance

### Monthly
- Clean microphone port with compressed air
- Check screw tightness
- Inspect cable connections

### Quarterly
- Update system software
- Recalibrate touch sensor
- Clean speaker grilles

### Annually
- Replace thermal pads
- Re-tension all connections
- Full diagnostic check

## Design Notes

### Thermal Management
- Chimney effect ventilation through top/bottom
- 8 top vents at 25mm radius
- 27 bottom vents in 3x9 grid
- Natural convection cooling

### Acoustic Design
- Hexagonal speaker grilles for optimal sound
- Isolated speaker chambers
- Vibration dampening on amp mount
- Microphone wind screening

### Serviceability
- Modular component mounting
- Cable routing channels
- Easy shell separation
- Individual component access

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 3.1 | Nov 2024 | Added solid base plate |
| 3.0 | Oct 2024 | Redesigned Pi mounting |
| 2.1 | Sep 2024 | Improved LED channel |
| 2.0 | Aug 2024 | FDM optimization |

---

**Related Documents:**
- VESTA-DIAG-001: Diagnostic Procedures
- VESTA-USER-001: User Manual
- VESTA-API-001: API Reference
- VESTA-MECH-001: 3D Model Files