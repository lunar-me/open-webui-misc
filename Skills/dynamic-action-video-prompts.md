---
name: dynamic-action-video-prompts
description: Transform a static reference image into three diverse short action-scene prompts for image-to-video generation, while preserving the original subjects, environment, and visual identity.
---

# Dynamic Action Scene Prompt Generator

## Purpose

Transform a static image into **three distinct short action-scene prompts** for an image-to-video generation model.

Unlike a simple image-animation prompt, these prompts should create a **small, self-contained event** that unfolds over time: something happens, develops, and reaches a believable outcome.

The result should feel like a spontaneous moment captured on a cellphone, not a pre-planned cinematic sequence.

The reference image is the source of truth.

---

## Core Principle

**Animate what is already there. Escalate it into action without inventing a new scene.**

The generated action must remain strongly grounded in the reference image.

Preserve:

- Existing people or characters
- Existing objects
- Existing clothing
- Existing architecture
- Existing landscape
- Existing location
- Existing lighting and general atmosphere
- Existing spatial relationships
- Existing time-of-day cues

Do NOT introduce major:

- Characters
- Objects
- Locations
- Vehicles
- Animals
- Weapons
- Buildings
- Props
- Weather events
- Environmental changes

unless they are already visible in the reference image or the user explicitly requests them.

---

# What Counts as "Action"

The action should be more substantial than merely making the image move.

Good action usually contains:

1. **Trigger** — something begins to happen.
2. **Development** — the subject reacts, moves, interacts, or the situation changes.
3. **Outcome** — the event reaches a small but clear conclusion.

Examples:

- A person notices something and quickly turns toward it.
- Someone begins walking, accelerates, and reaches another person.
- A person picks something up, reacts to it, and changes direction.
- Two existing people interact and their interaction changes the situation.
- Someone loses balance, catches themselves, and recovers.
- A person opens an already-visible door and disappears through it.
- An existing object falls, rolls, swings, breaks loose, or is caught.
- A person reacts to an existing environmental event such as wind, water, smoke, dust, or movement.
- Someone moves from one visible part of the environment to another.

The event should feel like something that could naturally have happened immediately before and after the photographed moment.

---

# Reference-Image Grounding

Before writing the prompts, silently determine:

- Who or what is present?
- What are they doing already?
- What objects could plausibly be interacted with?
- What parts of the environment could participate in the action?
- What directions of movement are physically possible?
- What relationships between subjects already exist?
- What could reasonably happen next?

Do not invent information simply because it would make the scene more exciting.

If the image contains only one person sitting in a room, do not suddenly create a second person, a car chase, a fight, or a new location.

If the image contains several people and objects, use those existing elements as the action vocabulary.

---

# Three-Prompt Diversity

Generate exactly **3 substantially different action scenarios**.

The prompts must not be simple variations of the same event.

Each should explore a different combination of:

- Action
- Character behavior
- Movement
- Interaction
- Camera response
- Escalation
- Outcome / ending

The three prompts should feel like **three plausible alternate realities of what happened immediately after the photograph was taken.**

### Prompt 1 — Natural Action

Create a believable, relatively grounded event that could naturally follow from the image.

Focus on realistic human or environmental behavior.

### Prompt 2 — More Dynamic Action

Create a more energetic or surprising event using only existing subjects and environmental elements.

The action can be faster, more physical, or more reactive, but must remain plausible.

### Prompt 3 — Alternative Outcome

Create a distinctly different action and ending.

Do not merely increase the intensity of Prompt 1 or 2.

Explore a different possible chain of events that could happen in the same scene.

---

# Endings Matter

Each prompt must have a **clear ending**.

The video should not simply stop while something is happening.

The ending can be subtle:

- The person reaches a destination.
- Someone catches an object.
- A person turns and walks away.
- The subjects stop and look at each other.
- An object comes to rest.
- Someone regains balance.
- The person exits the visible frame.
- The action settles into a new stable position.
- The subjects react to what just happened.

The three prompts should ideally have **different endings**.

The ending must remain consistent with the visible environment.

---

# Action Scale

Think in terms of a **short real-world event**, not an entire story.

The scene should generally contain:

**one trigger → one chain of action → one outcome**

Avoid multi-stage narratives containing several unrelated events.

Do not turn a photograph into an entire movie plot.

The action should be large enough to clearly distinguish it from simple image animation, but small enough to remain believable within the original scene.

---

# Camera Behavior

The camera is a person casually recording the event with a cellphone.

The camera should react naturally to the action.

Possible behaviors include:

- Slight handheld shake as the action begins
- Quick instinctive reframing
- Small pan following a moving subject
- Camera operator stepping backward
- Brief loss of framing
- Autofocus briefly shifting
- Exposure adjusting as the camera changes direction
- Subject partially leaving frame before the camera catches up
- Slight motion blur during fast movement
- Imperfect stabilization
- Camera tilting or rotating slightly while following the action

Do not force camera movement into every prompt.

The camera should respond to the action rather than dictate it.

Avoid polished cinematic movements such as:

- Perfect dolly shots
- Crane shots
- Drone movements
- Perfect tracking shots
- Elaborate choreographed camera paths
- Impossible camera repositioning

unless the reference image clearly implies such a setup.

---

# Realism and Physics

All motion must feel physically plausible.

Consider:

- Weight
- Momentum
- Gravity
- Balance
- Friction
- Human reaction time
- Object inertia
- Clothing and hair responding to movement
- Contact between bodies and surfaces
- Natural acceleration and deceleration

Avoid:

- Teleportation
- Instant acceleration
- Impossible body movement
- Rubber-like limbs
- Floating objects
- Objects changing identity
- Sudden unexplained appearances
- Major environmental transformations
- Physically impossible camera movement

---

# Candid Cellphone Aesthetic

Every prompt should feel like an accidental or spontaneous recording.

The footage should be:

- Handheld
- Casual
- Imperfect
- Unpolished
- Immediate
- Observational
- Realistic

Use cellphone-camera characteristics selectively:

- Mild handheld shake
- Slight framing errors
- Natural autofocus behavior
- Exposure adaptation
- Ordinary motion blur
- Slight rolling-shutter artifacts when appropriate
- Imperfect timing
- Ambient environmental movement

Do not make the footage look like a professional film production.

Avoid excessive phrases such as:

- "epic cinematic shot"
- "Hollywood-style action"
- "perfect composition"
- "masterful camera movement"
- "dramatic cinematic lighting"
- "blockbuster sequence"

---

# Prompt Structure

Each prompt should naturally communicate:

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

Do not label these sections inside the generated prompt. Write each prompt as one cohesive paragraph.

---

# Temporal Continuity

The generated video should feel like the **next few seconds after the reference photograph**.

Do not jump forward in time.

Avoid:

- Major changes of location
- Different clothing
- Different weather
- New time of day
- Completely changed lighting
- Characters appearing from nowhere
- Objects appearing without explanation

The scene should remain recognizably the same environment from beginning to end.

---

# Diversity Without Scene Invention

When searching for different scenarios, vary the **behavior and outcome**, not the world.

For example, if the image contains:

- Two people
- A table
- A cup
- A doorway

Possible variations could include:

1. One person quickly reaches for the cup, nearly knocks it over, catches it, and laughs.
2. One person stands and moves toward the doorway while the other reacts and follows.
3. The two people briefly interact over the table, causing the cup to slide, which one person stops before it falls.

These are different actions and endings while remaining inside the same visual world.

Do NOT turn the scene into:

- A car chase
- A fight with a new character
- A fire
- A police arrival
- A completely different location

unless those elements are already present or explicitly requested.

---

# Output Requirements

Return exactly **3 numbered prompts**.

Each prompt must contain **100–200 words**.

Use this format:

### 1.
[100–200 word action-scene prompt]

### 2.
[100–200 word action-scene prompt]

### 3.
[100–200 word action-scene prompt]

Do not add:

- An introduction
- An explanation
- A summary
- A negative prompt
- A list of assumptions
- Commentary about the reference image

unless the user explicitly requests it.

---

# Final Quality Check

Before responding, silently verify:

- Exactly 3 prompts
- Every prompt is 100–200 words
- Each prompt describes a genuine short action scene
- Each contains a trigger, development, and outcome
- The three actions are meaningfully different
- The three endings are meaningfully different
- The action remains in roughly the same environment
- Existing subjects and objects are prioritized
- No unsupported major characters or objects were introduced
- No unexplained location changes occurred
- The reference image remains visually recognizable
- Motion is physically plausible
- Camera behavior feels like casual cellphone footage
- Camera movement reacts to the action
- The prompts do not read like polished movie scripts
- The prompts describe the continuation of the image rather than recreating the image