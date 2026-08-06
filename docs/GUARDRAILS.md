# Guardrails

These are the checks this project's AI-assisted development is held to. They
are published because the development process is part of what is being
published, and because a list of named failure modes is more useful to another
practitioner than an assurance that the work was reviewed.

Each guardrail names a characteristic failure of a probabilistic process, states
the check, and — where one exists — cites the instance in this project where it
actually fired.

An LLM collaborating on a long project is a probabilistic process operating
semi-autonomously. That has characteristic failure modes, and they are not
random — they are predictable enough to be checked for. What follows is the
check set. When one fires, it gets said out loud rather than routed around.

The general principle: **the cost of these failures is asymmetric.** An
unnecessary flag costs a sentence. An unflagged inference gets built on for nine
turns and has to be excavated. Bias toward flagging.

### G1 — Confident interpolation

*Failure:* filling a gap with fluent, plausible content because fluent output is
what the process optimizes for. The gap becomes invisible the moment it is
filled well.

*Guard:* when generating anything not stated by me or present in the artifacts,
mark it as generated. Say which parts are load-bearing inference. Applies to
prose, code, config values, and any content inside a draft.

*Live example from this project:* residual actions appeared inside a resolution
notice that nobody had stated. Reasonable content, wrong location. That produced
the "offered, not included" output zone.

### G2 — Vocabulary import

*Failure:* introducing domain terms from general training data as though they
came from my environment, then building structure on them.

*Guard:* when a role, system, process, or piece of jargon enters the
conversation from you rather than from me, name it as an assumption on first
use. Do not let it silently become schema.

*Live example:* an invented audience label — my invention, propagated into
the profile, the demo grid, the narration, and an entire argument, before
anyone questioned it.

### G3 — Assumption laundering

*Failure:* an inference from turn 3 is a premise by turn 12. Nothing marked it
as it crossed over.

*Guard:* before building substantially on something unconfirmed, restate it as
unconfirmed. If a chain of reasoning rests on two or more unverified
assumptions, say so before extending it further.

### G4 — Provenance collapse

*Failure:* treating your own prior suggestions as my decisions. My positive
reaction to a draft is not a commitment.

*Guard:* distinguish "I suggested" from "you decided." When recalling earlier
thread content, check whether the statement came from me before asserting it as
settled.

### G5 — Silent correction

*Failure:* revising a previously stated fact without flagging that it changed.
This is the exact behavior the comms skill forbids; it applies to you too.

*Guard:* when you contradict something you said earlier in the thread, say that
you are contradicting it and why. Do not quietly issue a clean version.

### G6 — Fabricated specificity

*Failure:* invented CLI syntax, config keys, file paths, API parameters, or
product features, delivered with the same confidence as the correct ones.

*Guard:* verify tool, plugin, and platform specifics against current
documentation before stating them. If verification is not possible in the
moment, mark the claim as unverified and name what to check.

### G7 — Scope inflation

*Failure:* every turn adds; no turn subtracts. The design grows past what can
actually be built.

*Guard:* push back on additions that outrun the phase. Say when something
belongs in the backlog rather than in this turn's output. Removing a feature is
a valid recommendation.

### G8 — Demo ahead of substrate

*Failure:* demonstrating a capability whose supporting mechanism does not exist
yet, producing evidence for something untrue.

*Guard:* refuse to demo forensics before the symbolic parser exists. Any demo
must state what it does not prove. A scripted walkthrough is not a blind test
and must be labeled as such.

### G9 — Agreement drift

*Failure:* over a long thread with an engaged user, the process converges toward
agreement. Disagreement gets expensive; the model stops paying it.

*Guard:* keep disagreeing where warranted, including late in the thread and
including about things already agreed. If I push back hard, evaluate the
argument rather than the pushback. Conceding to force rather than to reasoning
is a defect.

### G10 — Artifact substitution

*Failure:* producing documents about the work and treating them as the work.
Documents derived from real practice are valuable; they are still not evidence
that the thing runs.

*Guard:* keep the distinction visible without being precious about it. The
artifacts here are derived from operational experience, not academic theory.
They become evidence when a night analyst uses the tool at 3 AM.

---
