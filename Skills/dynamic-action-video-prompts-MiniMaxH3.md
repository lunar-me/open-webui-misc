---
name: dynamic-action-video-prompts-MiniMax-H3
description: Transform a static reference image into three diverse short action-scene prompts for image-to-video generation, while preserving the original subjects, environment, and visual identity, and generate a synchronized soundscape prompt for each action scenario.
---

# Dynamic Action Scene + Sound Prompt Generator for MiniMax H3

## Purpose

Transform a static image into **three distinct short action-scene prompts** for an image-to-video generation model.

For each visual action scenario, also create a corresponding **sound prompt** describing the environmental audio, subject sounds, object sounds, camera/operator sounds, and natural acoustic changes that would plausibly accompany the generated video.

The result should feel like a spontaneous moment captured on a cellphone, with **visual action and sound belonging to the same physical event**.

The reference image is the source of truth.

---

## Core Principle

**Animate what is already there. Escalate it into action without inventing a new scene.**

The generated action must remain strongly grounded in the reference image.

Preserve:

* Existing people or characters
* Existing objects
* Existing clothing
* Existing architecture
* Existing landscape
* Existing location
* Existing lighting and general atmosphere
* Existing spatial relationships
* Existing time-of-day cues
* Existing acoustic implications of the environment

Do NOT introduce major:

* Characters
* Objects
* Locations
* Vehicles
* Animals
* Weapons
* Buildings
* Props
* Weather events
* Environmental changes

unless they are already visible in the reference image or the user explicitly requests them.

The soundscape must follow the same rule: **do not add prominent sounds from sources that do not plausibly exist in the visible scene.**

---

# What Counts as "Action"

The action should be more substantial than merely making the image move.

Good action usually contains:

1. **Trigger** — something begins to happen.
2. **Development** — the subject reacts, moves, interacts, or the situation changes.
3. **Outcome** — the event reaches a small but clear conclusion.

Examples:

* A person notices something and quickly turns toward it.
* Someone begins walking, accelerates, and reaches another person.
* A person picks something up, reacts to it, and changes direction.
* Two existing people interact and their interaction changes the situation.
* Someone loses balance, catches themselves, and recovers.
* A person opens an already-visible door and disappears through it.
* An existing object falls, rolls, swings, breaks loose, or is caught.
* A person reacts to an existing environmental event such as wind, water, smoke, dust, or movement.
* Someone moves from one visible part of the environment to another.

The sound prompt should describe the **audible consequences of the same action**.

For example:

* Footsteps should correspond to walking or running.
* A dropped object should produce a plausible impact sound.
* Clothing movement may become audible during vigorous motion.
* A door opening should produce an appropriate mechanical sound.
* Wind should affect existing environmental elements and contribute to the ambience.
* A sudden camera movement may include subtle handling or microphone noise.

Do not add generic dramatic sound effects merely to make the event feel more cinematic.

---

# Reference-Image Grounding

Before writing the prompts, silently determine:

* Who or what is present?
* What are they doing already?
* What objects could plausibly be interacted with?
* What parts of the environment could participate in the action?
* What directions of movement are physically possible?
* What relationships between subjects already exist?
* What could reasonably happen next?
* What sounds would naturally exist in this environment?
* Which sounds would become louder, quieter, or change as the action develops?

Do not invent information simply because it would make the scene more exciting.

If the image contains only one person sitting in a room, do not suddenly create a second person, a car chase, a fight, or a new location.

If the image contains several people and objects, use those existing elements as the action and sound vocabulary.

---

# Three-Prompt Diversity

Generate exactly **3 substantially different action scenarios**.

The prompts must not be simple variations of the same event.

Each should explore a different combination of:

* Action
* Character behavior
* Movement
* Interaction
* Camera response
* Escalation
* Outcome / ending
* Sound dynamics

The three prompts should feel like **three plausible alternate realities of what happened immediately after the photograph was taken.**

Each soundscape should also be meaningfully different because it belongs to a different physical event.

### Prompt 1 — Natural Action

Create a believable, relatively grounded event that could naturally follow from the image.

Focus on realistic human or environmental behavior and its corresponding natural soundscape.

### Prompt 2 — More Dynamic Action

Create a more energetic or surprising event using only existing subjects and environmental elements.

The action can be faster, more physical, or more reactive, but must remain plausible.

The soundscape should become appropriately more active without becoming exaggerated or cinematic.

### Prompt 3 — Alternative Outcome

Create a distinctly different action and ending.

Do not merely increase the intensity of Prompt 1 or 2.

Explore a different possible chain of events that could happen in the same scene, with a distinct corresponding acoustic progression.

---

# Endings Matter

Each prompt must have a **clear ending**.

The video should not simply stop while something is happening.

The ending can be subtle:

* The person reaches a destination.
* Someone catches an object.
* A person turns and walks away.
* The subjects stop and look at each other.
* An object comes to rest.
* Someone regains balance.
* The person exits the visible frame.
* The action settles into a new stable position.
* The subjects react to what just happened.

The three prompts should ideally have **different endings**.

The soundscape should also resolve naturally with the visual ending.

For example:

* Footsteps slow and stop.
* An object rolls and becomes quiet.
* Movement settles back into environmental ambience.
* Voices or reactions fade naturally.
* A door closes and leaves the room quieter.
* Wind or room tone becomes prominent again.

Do not force a dramatic audio ending.

---

# Action Scale

Think in terms of a **short real-world event**, not an entire story.

The scene should generally contain:

**one trigger → one chain of action → one outcome**

Avoid multi-stage narratives containing several unrelated events.

Do not turn a photograph into an entire movie plot.

The action should be large enough to clearly distinguish it from simple image animation, but small enough to remain believable within the original scene.

The sound should follow the same temporal scale.

---

# Camera Behavior

The camera is a person casually recording the event with a cellphone.

The camera should react naturally to the action.

Possible behaviors include:

* Slight handheld shake as the action begins
* Quick instinctive reframing
* Small pan following a moving subject
* Camera operator stepping backward
* Brief loss of framing
* Autofocus briefly shifting
* Exposure adjusting as the camera changes direction
* Subject partially leaving frame before the camera catches up
* Slight motion blur during fast movement
* Imperfect stabilization
* Camera tilting or rotating slightly while following the action

Do not force camera movement into every prompt.

The camera should respond to the action rather than dictate it.

Avoid polished cinematic movements such as:

* Perfect dolly shots
* Crane shots
* Drone movements
* Perfect tracking shots
* Elaborate choreographed camera paths
* Impossible camera repositioning

unless the reference image clearly implies such a setup.

---

# Sound and Acoustic Behavior

Every prompt must have an accompanying **overall soundscape**.

The sound prompt should describe what the listener would realistically hear during the same short event.

Consider:

### Environmental Ambience

Use only sounds appropriate to the visible environment:

* Room tone
* Street ambience
* Distant traffic
* Wind
* Water
* Birds
* Machinery
* Crowd murmur
* Building ambience
* Footsteps on the visible surface
* Natural outdoor ambience

Do not automatically add music.

### Action Sounds

Describe sounds directly caused by the visible action:

* Footsteps
* Clothing movement
* Breathing
* Object impacts
* Object sliding or rolling
* Doors, handles, hinges, or furniture
* Surface contact
* Water movement
* Wind interacting with visible objects
* Human vocal reactions

### Spatial Realism

Sounds should behave as though they originate from the visible environment.

Consider:

* Distance from the microphone
* Relative loudness
* Directionality
* Reverberation
* Indoor vs. outdoor acoustics
* Surfaces reflecting or absorbing sound
* Sounds becoming louder as subjects approach
* Sounds becoming quieter as subjects move away

### Cellphone Microphone Aesthetic

The audio should feel like it was recorded by the same handheld cellphone.

Use subtle characteristics such as:

* Natural microphone compression
* Slight handling noise
* Mild wind interference when appropriate
* Uneven sound levels during camera movement
* Nearby sounds becoming briefly louder
* Distant ambience remaining relatively diffuse
* Minor microphone rustle caused by the operator

Do not overdo artificial audio artifacts.

Avoid:

* Studio-quality Foley
* Perfectly isolated dialogue
* Cinematic sound design
* Trailer impacts
* Artificial whooshes
* Dramatic music
* Orchestral scores
* Sound effects that have no visible source

unless the user explicitly requests them.

---

# Audio-Visual Synchronization

The **image-to-video prompt and sound prompt must describe the same event**.

Before responding, silently verify that every major audible event has a corresponding visible cause.

Examples:

* If the person runs, describe synchronized footsteps.
* If an object falls, describe its impact at the correct point in the action.
* If a door opens, describe the door movement and its sound together.
* If the subject moves farther away, reduce the perceived loudness of their movement.
* If the scene becomes still, allow the soundscape to settle into ambient noise.
* If the camera operator moves quickly, subtle handling noise may increase.

Do not create an audio event that contradicts the visual prompt.

The sound prompt should describe a **continuous soundscape**, not a list of disconnected sound effects.

---

# Candid Cellphone Aesthetic

Every prompt should feel like an accidental or spontaneous recording.

The footage should be:

* Handheld
* Casual
* Imperfect
* Unpolished
* Immediate
* Observational
* Realistic

Use cellphone-camera characteristics selectively:

* Mild handheld shake
* Slight framing errors
* Natural autofocus behavior
* Exposure adaptation
* Ordinary motion blur
* Slight rolling-shutter artifacts when appropriate
* Imperfect timing
* Ambient environmental movement

The audio should feel equally candid and naturally captured by the same phone.

Do not make the footage look or sound like a professional film production.

Avoid excessive phrases such as:

* "epic cinematic shot"
* "Hollywood-style action"
* "perfect composition"
* "masterful camera movement"
* "dramatic cinematic lighting"
* "blockbuster sequence"
* "cinematic sound design"
* "epic soundtrack"

---

# Prompt Structure

Each **image-to-video prompt** should naturally communicate:

### Beginning

Describe the immediate state of the scene and what triggers the action.

### Action

Describe the physical sequence in chronological order.

### Camera

Describe how the handheld cellphone camera reacts naturally to the event.

### Environment

Describe how existing environmental elements respond to the action.

### Ending

Describe a clear, believable final state.

Do not label these sections inside the generated image-to-video prompt. Write each prompt as one cohesive paragraph.

Each **sound prompt** should naturally communicate:

### Beginning

Describe the existing ambient sound and the first audible indication of the trigger.

### Development

Describe the sounds produced by the physical action, including changes in proximity, intensity, and acoustic environment.

### Ending

Describe how the soundscape settles when the visual action reaches its final state.

Write each sound prompt as one cohesive paragraph rather than a list of sound effects.

---

# Temporal Continuity

The generated video should feel like the **next few seconds after the reference photograph**.

Do not jump forward in time.

Avoid:

* Major changes of location
* Different clothing
* Different weather
* New time of day
* Completely changed lighting
* Characters appearing from nowhere
* Objects appearing without explanation

The scene should remain recognizably the same environment from beginning to end.

The soundscape must maintain the same temporal and environmental continuity.

---

# Diversity Without Scene Invention

When searching for different scenarios, vary the **behavior and outcome**, not the world.

For example, if the image contains:

* Two people
* A table
* A cup
* A doorway

Possible variations could include:

1. One person quickly reaches for the cup, nearly knocks it over, catches it, and laughs.
2. One person stands and moves toward the doorway while the other reacts and follows.
3. The two people briefly interact over the table, causing the cup to slide, which one person stops before it falls.

The corresponding soundscapes should differ:

1. A quick hand movement, cup rattling against the table, a brief laugh, then room ambience.
2. Chair movement, footsteps approaching the doorway, clothing movement, then footsteps and room ambience settling.
3. Cup scraping across the tabletop, a quick hand contact, a muted reaction, then quiet room tone.

These are different actions and endings while remaining inside the same visual world.

Do NOT turn the scene into:

* A car chase
* A fight with a new character
* A fire
* A police arrival
* A completely different location

unless those elements are already present or explicitly requested.

---

# Output Requirements

Return exactly **3 numbered multimodal prompts**.

Each prompt must contain:

1. An `integrated_multimodal_description` containing the shot number, timestamp, and image-to-video prompt.
2. An `overall_soundscape` containing the corresponding sound prompt.

Use this exact format:

### 1.

integrated_multimodal_description: [Shot 3] (0.00s)
[100–200 word image-to-video prompt]

overall_soundscape:
[Sound prompt describing the synchronized soundscape]

### 2.

integrated_multimodal_description: [Shot 4] (0.00s)
[100–200 word image-to-video prompt]

overall_soundscape:
[Sound prompt describing the synchronized soundscape]

### 3.

integrated_multimodal_description: [Shot 5] (0.00s)
[100–200 word image-to-video prompt]

overall_soundscape:
[Sound prompt describing the synchronized soundscape]

Use the shot numbers and timestamps exactly as required by the user if they provide different values. Otherwise use `[Shot 3] (0.00s)`, `[Shot 4] (0.00s)`, and `[Shot 5] (0.00s)`.

The `overall_soundscape` should be concise but specific enough to guide an audio-generation model.

Do not add:

* An introduction
* An explanation
* A summary
* A negative prompt
* A list of assumptions
* Commentary about the reference image

unless the user explicitly requests it.

---

# Final Quality Check

Before responding, silently verify:

* Exactly 3 prompts
* Every image-to-video prompt is 100–200 words
* Every prompt contains both required fields
* Every prompt uses the required shot/timestamp format
* Each prompt describes a genuine short action scene
* Each contains a trigger, development, and outcome
* The three actions are meaningfully different
* The three endings are meaningfully different
* The three soundscapes are meaningfully different
* Every soundscape corresponds directly to its visual action
* Audible events have plausible visible sources
* No unsupported major characters or objects were introduced
* No unexplained location changes occurred
* The reference image remains visually recognizable
* Motion is physically plausible
* Sound is physically and acoustically plausible
* Camera behavior feels like casual cellphone footage
* Audio feels like cellphone microphone capture
* Camera movement reacts to the action
* The prompts do not read like polished movie scripts
* The prompts describe the continuation of the image rather than recreating the image
* No unnecessary music or cinematic sound design was introduced
