# VESTA Technical Documentation Style Guide

**Version**: 2.0  
**Effective Date**: November 2024  
**Maintained By**: Documentation Team

## 1. Document Structure Standards

### 1.1 Header Format
All technical documents must begin with:
```
# [Document Title]

**Document ID**: [DEPT-TYPE-###]  
**Revision**: [X.Y]  
**Last Updated**: [Month Year]  
**Complexity**: Level [1-3] - [Basic/Intermediate/Advanced]
```

### 1.2 Section Hierarchy
- Use ATX-style headers (#, ##, ###)
- Maximum 3 levels of nesting
- Include section numbers for procedures

## 2. Writing Style

### 2.1 Voice and Tone
- **Active voice**: "Connect the cable" NOT "The cable should be connected"
- **Direct instructions**: Use imperative mood
- **Concise language**: Maximum 20 words per sentence when possible

### 2.2 Terminology Consistency

| Preferred Term | Avoid |
|----------------|-------|
| Select | Click on, Choose |
| Enter | Type in, Input |
| Verify | Check, Ensure |
| If...then | When...do |
| Power cycle | Restart, Reboot |

### 2.3 Acronym Usage
- Define on first use: "Light Emitting Diode (LED)"
- Maintain glossary for frequently used terms
- Never assume knowledge of industry acronyms

## 3. Formatting Standards

### 3.1 Lists
**Numbered Lists**: Use for sequential steps
1. Power off the device
2. Remove the cover
3. Inspect components

**Bulleted Lists**: Use for non-sequential items
- Tool A
- Tool B
- Tool C

### 3.2 Code and Commands
```bash
# Use code blocks for commands
$ sudo command --option
```

Inline code: Use `backticks` for inline references

### 3.3 Warnings and Notes

⚠️ **WARNING**: Use for safety-critical information

📝 **NOTE**: Use for important supplementary information

💡 **TIP**: Use for helpful suggestions

## 4. Visual Elements

### 4.1 Diagrams
- Minimum 300 DPI for printed docs
- SVG format preferred for web
- Include alt text for accessibility

### 4.2 Screenshots
- Highlight relevant areas with red boxes
- Crop to show only necessary elements
- Update with each major UI change

### 4.3 Tables
| Component | Specification | Notes |
|-----------|---------------|-------|
| Use tables | For specs | Keep it simple |
| Align text | Consistently | Left-align default |

## 5. Procedural Writing

### 5.1 Step Format
```
### Step N: [Action Summary]
1. [Specific action]
2. [Expected result]
3. [Next action]

**Decision Point**: 
- If [condition] → Go to Step X
- If [condition] → Go to Step Y
```

### 5.2 Time Estimates
Include realistic time estimates:
- (5 minutes) for quick checks
- (15 minutes) for detailed procedures
- (30+ minutes) for complex repairs

## 6. Review Process

### 6.1 Technical Review
- Engineering verification required
- Test all procedures before publication
- Version control through Git

### 6.2 Editorial Review
- Grammar and style check
- Consistency verification
- Accessibility compliance

## 7. XML/DITA Structure

### 7.1 Basic DITA Topic
```xml
<topic id="vesta-mic-diag">
  <title>Microphone Diagnostics</title>
  <body>
    <section>
      <title>Overview</title>
      <p>Diagnostic procedure for mic array.</p>
    </section>
    <section>
      <title>Prerequisites</title>
      <ul>
        <li>Digital multimeter</li>
        <li>ESD protection</li>
      </ul>
    </section>
  </body>
</topic>
```

### 7.2 Metadata Requirements
- Author name
- Creation date
- Last modified date
- Review status
- Target audience

## 8. File Naming Conventions

Format: `[PRODUCT]-[TYPE]-[NUMBER]-[VERSION]`

Examples:
- `vesta-diag-001-v2.md`
- `vesta-user-guide-v1.pdf`
- `vesta-api-ref-003-draft.xml`

## 9. Compliance

### 9.1 Accessibility
- WCAG 2.1 AA compliance
- Alt text for all images
- Logical heading structure
- Color-blind friendly diagrams

### 9.2 Localization Ready
- No embedded text in images
- Consistent terminology database
- Cultural neutrality

---

**Questions?** Contact the Documentation Team at docs@vesta-project.org