# Generic KB template (KCS-shaped)

Backlog E7.1, manual-mode fallback. Used when the site profile has no
article template of its own — labeled **generic — not yet tuned to this
site** in output, same convention as comms' generic templates. If the site
profile defines its own template shape, that governs instead of this.

Structure follows Knowledge-Centered Service (KCS) conventions loosely:
problem, environment, resolution, cause — kept simple because a paste-ready
draft under time pressure beats a complete taxonomy nobody fills in.

```
# [Title — symptom-oriented, not root-cause-oriented, e.g.
   "Orders not appearing on modality worklist after interface engine restart"]

## Environment
- System(s): [from site profile systems, or "[TBD]"]
- Scope observed: [one user / one modality / sitewide — from the worklog]

## Symptom
[What was observed — quote or closely paraphrase the worklog. Confidence
mark: this section is `confirmed` by definition, since it's what was
reported, not inferred.]

## Cause
[What the worklog states as the cause. Mark `confirmed` (root-caused and
verified), `likely` (strong evidence, not independently verified), or
`possible` (plausible, resolution worked without cause being isolated).
Never omit the mark to make the article read more authoritative than the
worklog supports.]

## Resolution
[Steps actually taken, in order, exactly as the worklog states them. Never
extend past what the worklog documents — a step that "would probably also
help" belongs in Suggestions below, not here.]

## Verification
[How resolution was confirmed, if stated. "Not stated" is a valid entry.]

## Related
[Ticket reference. Related articles, if known. Interface/system names per
site profile vocabulary.]

---
Suggestions (not part of the article — offer separately, never merged in):
[Anything that would improve the article but wasn't in the worklog — a
missing verification step, a related symptom worth cross-referencing, etc.]
```

## Field checklist (manual mode)

Before presenting a draft as complete, confirm each of these is either
filled or explicitly marked unknown — never silently blank:

- [ ] Title is symptom-oriented (what someone would search for), not an
      internal ticket number
- [ ] Environment names match site profile vocabulary where applicable
- [ ] Cause carries a confidence mark
- [ ] Resolution steps trace to the worklog, not to general knowledge of
      "how this is usually fixed"
- [ ] Verification stated or marked "not stated"
- [ ] Anything beyond the worklog is in Suggestions, not the article body
