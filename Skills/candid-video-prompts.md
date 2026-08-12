---
name: candid-video-prompts
description: Generate three diverse 100–200 word image-to-video motion prompts from a reference image, styled as casual candid cellphone footage.
---

# Candid Image-to-Video Prompt Generator

## Purpose

Transform a user's image-to-video request into three distinct motion prompts suitable for a video-generation model.

The prompts should describe **how the existing image comes alive**, rather than redesigning or replacing the scene.

Each prompt must feel like a **realistic, casually captured cellphone video** rather than a polished cinematic production.

## Core Instructions

For every request:

1. Generate exactly **3 different motion prompts**.
2. Each prompt must be **100–200 words**.
3. Preserve the important subjects, environment, composition, and visual identity of the reference image.
4. Focus primarily on **motion and temporal change**:
   - Subject movement
   - Facial expressions and gestures
   - Body movement
   - Hair, clothing, and fabric movement
   - Environmental movement
   - Lighting changes
   - Camera movement
   - Background activity
5. Make the three prompts meaningfully different. Do not simply rephrase the same action.
6. Write each prompt as if describing a **candid moment casually recorded on a cellphone**.
7. Prefer natural imperfections over cinematic perfection:
   - Slight handheld shake
   - Small framing adjustments
   - Imperfect autofocus
   - Brief exposure shifts
   - Natural motion blur
   - Slightly uneven camera movement
   - Occasional accidental reframing
8. Avoid excessive cinematic language such as:
   - "epic cinematic shot"
   - "Hollywood lighting"
   - "perfect composition"
   - "masterpiece"
   - "dramatic camera sweep"
9. Do not introduce major objects, characters, locations, clothing, or actions that are unsupported by the reference image unless the user explicitly requests them.
10. Do not describe the image from scratch. Assume the video model already receives the reference image.

## Diversity

The three prompts should explore different motion approaches when appropriate.

For example:

- **Prompt 1 — Natural moment:** subtle, believable movement with minimal camera intervention.
- **Prompt 2 — Human interaction:** emphasize gestures, expressions, interaction, or changing attention.
- **Prompt 3 — Environmental/camera moment:** emphasize surroundings, atmosphere, background activity, or a different handheld-camera behavior.

Adapt these categories to the actual image rather than mechanically following them.

## Cellphone-Camera Style

The footage should feel spontaneous and unplanned.

Use details such as:

- handheld smartphone footage
- casual framing
- slight wrist movement
- tiny camera corrections
- autofocus hunting briefly
- exposure adjusting naturally
- realistic motion blur
- imperfect stabilization
- subtle rolling-shutter feel when appropriate
- ordinary ambient movement
- unpolished timing

Do not add every artifact to every prompt. Select details that naturally fit the scene.

## Motion Quality

Motion should be physically plausible and temporally coherent.

Prefer:

- gradual movement
- natural acceleration and deceleration
- believable weight and inertia
- subtle secondary motion
- realistic interaction with clothing, hair, objects, and environment

Avoid:

- teleportation
- sudden unexplained movements
- rubbery motion
- exaggerated body deformation
- impossible camera movement
- unnecessary scene transformations

## Output Format

Return exactly three numbered prompts.

Use this format:

### 1.
[100–200 word prompt]

### 2.
[100–200 word prompt]

### 3.
[100–200 word prompt]

Do not add an introduction, explanation, analysis, negative prompt, or conclusion unless the user explicitly asks for one.

## Quality Checklist

Before responding, silently verify:

- Exactly 3 prompts
- Every prompt is 100–200 words
- Prompts are substantially different
- Motion is the primary focus
- Reference-image details are preserved
- Cellphone-candid aesthetic is present
- Motion is physically plausible
- No unnecessary cinematic language
- No unsupported major elements were introduced