---
title: style-guide-colors-typography-tokens
tags:
  - ui-design
  - interface-design
  - system-design
last updated: Friday, August 14th 2026, 8:23:59 am
---

# Style Guide

**The single source of truth for colors, typography, and tokens.** Every diagram draws from this — not from hex values inlined in other reference files. If you want to change the visual skin of Diagram Design, change this file.

Default skin is the **Clinical Parchment** palette — warm organic creams, jet-black ink, golden ochre accents, and botanical categorical markers. It is designed specifically to mimic high-end academic and scientific publishing.

*Note: This specific skin deprecates dark-mode inversion. To maintain the physical "paper" aesthetic, it remains light-mode locked.*

## Tokens

### Semantic Roles

Every token is referred to by **semantic role**, not by its hex value. Type references (`type-*.md`) and SKILL.md say `accent`, not `#D29624`.

|

| **Role** | **Purpose** | **Hex Value (Clinical Parchment)** |

| `paper` | Page background, default node fill | `#F6F4EB` (Warm Cream) |

| `paper-2` | Diagram container bg, secondary fill | `#EAE5D9` (Dusty Beige) |

| `ink` | Primary text, primary stroke | `#121212` (Near-Black) |

| `muted` | Secondary text, default arrow stroke | `#6B685C` (Desaturated Taupe) |

| `soft` | Sublabels, boundary labels | `#8A8679` (Light Taupe) |

| `rule` | Hairline borders | `rgba(18, 18, 18, 0.12)` |

| `rule-solid` | Stronger borders, baselines | `#D1CCBB` |

| `accent` | Focal / 1–2 max per diagram | `#D29624` (Golden Ochre) |

| `accent-tint` | Fill for accent-bordered boxes | `rgba(210, 150, 36, 0.12)` |

| `link` | HTTP/API calls, external arrows | `#6E62A6` (Muted Amethyst) |

> **Brand palette source:** This skin extracts its tokens directly from the Urolithin A Biotransformation infographic. It relies on a strict 1-Accent rule (Ochre) for interactive/focal elements.

### Series Palette (Multi-series cHart tYpes oNly)

A small set of botanical, editorial-tone colors for chart types that genuinely need to distinguish multiple overlapping entities. The "1-focal" rule still holds — `accent` (Ochre) is reserved for the focal series; the palette below covers the rest.

| **Token** | **Hex Value** | **Source** |

| `series-1` | `#A1B281` | Sage Green (Middleware node) |

| `series-2` | `#6E62A6` | Muted Amethyst (Hydrolysis node) |

| `series-3` | `#BA3636` | Rust Red (Warning/Error state) |

| `series-4` | `#8C7D70` | Earthy Taupe |

| `series-5` | `#5C6B73` | Clinical Slate |

Fills sit at `0.18` opacity; strokes use the full color. **Don't backfill these tokens to non-chart types** — architecture, swimlane, etc. continue to use muted-ink variants.

## Typography

The typography stack abandons generic geometric sans-serifs for a strict academic hierarchy. UI and technical elements use `Space Grotesk` and `Inter`, while document/prose elements use `Literata` and `Merriweather`.

| **Role** | **Family** | **Size** | **Weight** | **Usage** |

| `title` | Literata (Serif) | 1.75rem | 600 | Page H1, Diagram Titles |

| `node-name` | Space Grotesk (Sans) | 12px | 600 | Human-readable structural labels |

| `sublabel` | Inter (Sans) | 9px | 400 | Port, protocol, URL, field type |

| `eyebrow` | Inter (Sans) | 7–8px | 500, tracked 0.18em, uppercase | Type tags, axis labels |

| `arrow-label` | Inter (Sans) | 8px | 400, tracked 0.06em | Arrow annotations |

| `callout` | Merriweather *italic* | 14px | 400 | Editorial asides only |

### Font Stack

```shell
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Literata:ital,opsz,wght@0,7..72,600;1,7..72,600&family=Merriweather:ital,wght@0,400;1,400&family=Space+Grotesk:wght@600&display=swap" rel="stylesheet">

```

**Load-bearing rule:** `Literata` has the authoritative weight of an academic textbook for titles. `Space Grotesk` provides a slightly clinical, geometric edge for nodes that contrasts the serif document. `Inter` is highly legible for dense technical micro-copy.

## Stroke, Radius, Spacing

| **Token** | **Value** | **Use** |

| `stroke-thin` | `0.8` | Tag-box outlines, leaf nodes |

| `stroke-default` | `1` | Most strokes |

| `stroke-strong` | `1.2` | Emphasis strokes |

| `radius-sm` | `4` | Small tags |

| `radius-md` | `6` | Node boxes |

| `radius-lg` | `8` | Containers, rings |

| `grid` | `4` | Every coord, size, and gap is divisible by 4 (hard rule) |

## Node Type → Treatment

Semantic role combinations — reference these by name in type specs.

| **Type** | **Fill** | **Stroke** |

| `focal` (1–2 max) | `accent-tint` | `accent` |

| `backend` | `#ffffff` (white) | `ink` |

| `store` | `ink @ 0.05` | `muted` |

| `external` | `ink @ 0.03` | `ink @ 0.30` |

| `input` | `muted @ 0.10` | `soft` |

| `optional` | `ink @ 0.02` | `ink @ 0.20` dashed `4,3` |

| `security` | `accent @ 0.05` | `accent @ 0.50` dashed `4,4` |

## Customizing the Skin

### Constraints (Don't bReak tHese)

* **The Multi-Accent Trap**: Ochre (`#D29624`) is your engine. It is the *only* color allowed for primary execution nodes and focal accents. Amethyst and Sage are strictly for passive state indication (the Series palette).  
$1
* **Contrast**: `ink` (`#121212`) must remain near-black. Do not lighten it to gray, or it will fail WCAG AA on the `paper` background.  
$1
* **Dual-Engine Typography**: Do not cross-contaminate the sans-serif and serif stacks. Technical data uses `Inter`/`Space Grotesk`. Prose and Titles use `Merriweather`/`Literata`.  
$1
* **Paper is warm**: Pure white (`#FFFFFF`) is reserved *only* for backend node fills to make them pop off the canvas. The canvas itself must remain `#F6F4EB`.
