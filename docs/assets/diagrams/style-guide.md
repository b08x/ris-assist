# Style Guide — RIS Assist (project-local skin)

The **single source of truth** for diagram colors, typography, and tokens in this project. Overrides the diagram-design skill's shipped default skin. Every diagram generated for this repo reads from this file, not from the skill's own `references/style-guide.md`.

Two coordinated skins: **Clinical Parchment** (light) and **Clinical Parchment Night** (dark), sampled from the project reference boards `/home/b08x/.syncopated/skills/clinical_parchment_light.jpeg` and `/home/b08x/.syncopated/skills/clinical_parchment_dark.jpeg`. They share typography and layout grammar but carry different surface systems and accent rules.

---

## Semantic roles

Every token is referred to by **semantic role**, not by hex value. Diagram specs say `accent`, not `#D29624`.

| Role | Purpose | Light | Dark |
|---|---|---|---|
| `paper` | Page background, default node fill | `#FDFDF9` (low-fatigue reading canvas) | `#0A0A0B` (night canvas) |
| `paper-2` | Diagram container bg, secondary fill | `#F8F8F0` (warm neutral surface) | `#161618` (night surface) |
| `ink` | Primary text, primary stroke | `#2D3142` (jet-black violet) | `#E4E4E7` (night ink) |
| `muted` | Secondary text, default arrow stroke | `#4F5D75` (blue-slate) | `#A1A1AA` (muted ink) |
| `soft` | Sublabels, boundary labels | `#7A8399` | `#71717A` |
| `rule` | Hairline borders | `rgba(45,49,66,0.12)` | `#27272A` |
| `rule-solid` | Stronger borders, baselines | `#BFC0C0` | `#3F3F46` |
| `accent` | Focal / 1–2 max per diagram | `#C09241` (ochre; border/fill only) | `#C09241` (ochre; border/fill only) |
| `accent-tint` | Fill for accent-bordered boxes | `rgba(192,146,65,0.12)` | `rgba(192,146,65,0.12)` |
| `accent-hover` | Active/hover accent treatment | `#7161A1` (purple interaction accent) | `#C4B5FD` (lavender hover) |
| `link` | HTTP/API calls, external arrows | `#7161A1` (purple) | `#C4B5FD` (light lavender) |

**Accent rule:** light ochre (`#C09241`) is reserved for borders, fills, and warning surfaces — never text on paper. Purple (`#7161A1`) carries interactive/active states. Dark lavender (`#A78BFA`) carries interactive feedback. One focal accent treatment per diagram, 1–2 elements max.

---

## Series palette (multi-series chart types only)

For chart types that distinguish overlapping entities (radar, scatter, line). The 1-focal rule still holds — `accent` is reserved for the focal series.

| Token | Light | Dark |
|---|---|---|
| `series-1` | `#7C8F6F` (sage) | `#9CAF8F` |
| `series-2` | `#7161A1` (purple) | `#A78BFA` |
| `series-3` | `#C09241` (ochre) | `#C4B5FD` |
| `series-4` | `#8C7D70` (taupe) | `#B88670` |
| `series-5` | `#5C6B73` (slate) | `#8D8298` |

Fills sit at `0.18` opacity light, `0.22` dark; strokes use full color. Keep ochre and purple semantics distinct; don't backfill chart colors to non-chart types.

---

## Typography

| Role | Family | Size | Weight | Usage |
|---|---|---|---|---|
| `title` | Literata (serif) | 1.75rem | 600 | Page H1, document titles |
| `node-name` | Geist Sans | 12px | 600 | Human-readable structural labels |
| `sublabel` | Geist Mono | 9px | 400 | Ports, protocols, URLs, field types |
| `eyebrow` | Geist Mono | 7–8px | 500, tracked 0.18em, uppercase | Type tags, axis labels |
| `arrow-label` | Geist Mono | 8px | 400, tracked 0.06em | Arrow annotations |
| `callout` | Literata *italic* | 14px | 400 | Editorial asides only |

Technical labels use `Geist Mono`; names use `Geist Sans`; titles and document prose use `Literata`. The mono face is reserved for technical/UI labels, not body prose.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600;700&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400;1,7..72,600&display=swap" rel="stylesheet">
```

---

## Stroke, radius, spacing

| Token | Value |
|---|---|
| `stroke-thin` | `0.8` |
| `stroke-default` | `1` |
| `stroke-strong` | `1.2` |
| `radius-sm` | `4` |
| `radius-md` | `6` |
| `radius-lg` | `8` |
| `grid` | `4` (every coord, size, gap divisible by 4) |

---

## Node type → treatment

| Type | Fill | Stroke |
|---|---|---|
| `focal` (1–2 max) | `accent-tint` | `accent` |
| `backend` | `#ffffff` | `ink` |
| `store` | `ink @ 0.05` | `muted` |
| `external` | `ink @ 0.03` | `ink @ 0.30` |
| `input` | `muted @ 0.10` | `soft` |
| `optional` | `ink @ 0.02` | `ink @ 0.20` dashed `4,3` |
| `security` | `accent @ 0.05` | `accent @ 0.50` dashed `4,4` |

---

## Dark variant notes

- Dark is a **separate palette**, not a brightness inversion of light — it carries the same ochre accent for borders and focal tints.
- On dark surfaces, keep serif body/annotation text `font-smoothing: antialiased` to avoid light-on-dark bloom on high-DPI screens.
- Opacities key off each skin's own ink channel: light `rgba(18,18,18,X)`, dark `rgba(228,228,231,X)`.

## Constraints

- **1-accent**: one focal accent treatment per diagram; light ochre/purple or dark lavender according to semantic role.
- **Ochre text prohibition**: `#C09241` is for light-theme borders/fills/warnings, never text on paper.
- **No rainbow**: other hues are series-palette or `muted` variants.
- **Paper is warm, not pure white**: `#FDFDF9`; pure white only for `backend` node fills.
- **Mono is scoped**: Geist Mono is for technical/UI labels; Literata is for document prose.
- **Dot pattern optional**, not default; ~10% ink opacity when enabled.
- **Container clean by default**: diagram sits on paper; framed variant is opt-in.
