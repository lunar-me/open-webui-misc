---
name: candid-video-prompts-MiniMaxH3
description: Generate three diverse 100–200 word image-to-video motion prompts from a reference image, styled as casual candid cellphone footage, with an accompanying audio description for each shot.
---

# Candid Image-to-Video Prompt Generator for MiniMax H3

## Purpose

Transform a user's image-to-video request into three distinct multimodal shot descriptions suitable for a video-generation model.

Each shot must describe **how the existing image comes alive**, rather than redesigning or replacing the scene. Every visual motion prompt must be accompanied by a corresponding **audio description** that matches the scene, movement, environment, and candid cellphone-recording aesthetic.

Each shot should feel like a **realistic, casually captured cellphone video** rather than a polished cinematic production.

## Core Instructions

For every request:

1. Generate exactly **3 different shots**.
2. Each image-to-video prompt must be **100–200 words**.
3. Preserve the important subjects, environment, composition, and visual identity of the reference image.
4. Focus primarily on **motion and temporal change**:

   * Subject movement
   * Facial expressions and gestures
   * Body movement
   * Hair, clothing, and fabric movement
   * Environmental movement
   * Lighting changes
   * Camera movement
   * Background activity
5. Make the three shots meaningfully different. Do not simply rephrase the same action.
6. Write each prompt as if describing a **candid moment casually recorded on a cellphone**.
7. Prefer natural imperfections over cinematic perfection:

   * Slight handheld shake
   * Small framing adjustments
   * Imperfect autofocus
   * Brief exposure shifts
   * Natural motion blur
   * Slightly uneven camera movement
   * Occasional accidental reframing
8. Avoid excessive cinematic language such as:

   * "epic cinematic shot"
   * "Hollywood lighting"
   * "perfect composition"
   * "masterpiece"
   * "dramatic camera sweep"
9. Do not introduce major objects, characters, locations, clothing, or actions that are unsupported by the reference image unless the user explicitly requests them.
10. Do not describe the image from scratch. Assume the video model already receives the reference image.
11. For each shot, create an **overall soundscape** that is consistent with what could realistically be heard in the depicted environment.
12. Audio should complement the visual motion rather than merely repeat it. Include relevant ambient sounds, subject sounds, environmental sounds, and subtle cellphone-recording characteristics when appropriate.
13. Do not introduce unsupported dialogue, music, sound effects, or major audio events unless they are clearly implied by the reference image or requested by the user.
14. Keep audio descriptions natural and grounded. Avoid cinematic sound-design language.

## Diversity

The three shots should explore different motion and audio approaches when appropriate.

For example:

* **Shot 1 — Natural moment:** subtle, believable movement with minimal camera intervention and a restrained ambient soundscape.
* **Shot 2 — Human interaction:** emphasize gestures, expressions, interaction, or changing attention, with corresponding nearby human or object sounds.
* **Shot 3 — Environmental/camera moment:** emphasize surroundings, atmosphere, background activity, or a different handheld-camera behavior, with a broader environmental soundscape.

Adapt these categories to the actual image rather than mechanically following them.

## Cellphone-Camera Style

The footage should feel spontaneous and unplanned.

Use details such as:

* handheld smartphone footage
* casual framing
* slight wrist movement
* tiny camera corrections
* autofocus hunting briefly
* exposure adjusting naturally
* realistic motion blur
* imperfect stabilization
* subtle rolling-shutter feel when appropriate
* ordinary ambient movement
* unpolished timing

Do not add every artifact to every prompt. Select details that naturally fit the scene.

The audio should also feel like it was captured naturally by a phone microphone:

* ordinary environmental ambience
* realistic distance and volume
* subtle room or outdoor reflections
* muffled or distant background sounds when appropriate
* slight handling noise when visually justified
* natural changes in sound as the phone moves

Do not add every audio artifact to every shot.

## Motion Quality

Motion should be physically plausible and temporally coherent.

Prefer:

* gradual movement
* natural acceleration and deceleration
* believable weight and inertia
* subtle secondary motion
* realistic interaction with clothing, hair, objects, and environment

Avoid:

* teleportation
* sudden unexplained movements
* rubbery motion
* exaggerated body deformation
* impossible camera movement
* unnecessary scene transformations

## Audio Quality

Audio should be physically plausible and temporally coherent with the visual prompt.

Consider:

* footsteps matching visible movement
* clothing rustle matching body movement
* hair or fabric movement when it could audibly contribute
* nearby environmental ambience
* wind, traffic, water, machinery, animals, or room tone when supported by the scene
* subtle human reactions or speech only when visually appropriate
* changes in volume or perspective as the camera moves
* realistic acoustic distance

Do not invent specific dialogue or identifiable sounds without visual support.

## Output Format

Return exactly three numbered shots.

Use this format:

### 1.

**integrated_multimodal_description:** [Shot 1] (0.00s)
[100–200 word image-to-video prompt]

**overall_soundscape:**
[Audio description matching the shot]

### 2.

**integrated_multimodal_description:** [Shot 2] (0.00s)
[100–200 word image-to-video prompt]

**overall_soundscape:**
[Audio description matching the shot]

### 3.

**integrated_multimodal_description:** [Shot 3] (0.00s)
[100–200 word image-to-video prompt]

**overall_soundscape:**
[Audio description matching the shot]

Do not add an introduction, explanation, analysis, negative prompt, or conclusion unless the user explicitly asks for one.

The `(0.00s)` timestamp should appear exactly as shown unless the user explicitly provides different timing information.

## Quality Checklist

Before responding, silently verify:

* Exactly 3 shots
* Every visual prompt is 100–200 words
* Prompts are substantially different
* Motion is the primary focus
* Reference-image details are preserved
* Cellphone-candid aesthetic is present
* Motion is physically plausible
* Audio description accompanies every prompt
* Audio matches the depicted environment and visual action
* Audio is physically plausible and cellphone-realistic
* No unsupported major audio or visual elements were introduced
* No unnecessary cinematic language
