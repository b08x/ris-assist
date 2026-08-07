# ServiceNow import format

Backlog E7.1. What the `knowledge` skill's HTML has to look like for
`scripts/html_to_docx.py` to produce a `.docx` that survives ServiceNow's
Word import without hand-repair afterwards.

The article's *shape* is `kb-template.md`. This file is the *mechanics* —
which tags convert, which silently degrade, and which are not worth using.
Every claim below is stated from the converter's actual behaviour, not from
what HTML generally supports. When the two disagree, the converter wins;
fix this file.

---

## Heading map

The converter shifts headings down one level, because ServiceNow renders the
article title separately from the body.

| HTML | DOCX | Size | Use for |
|---|---|---|---|
| `<h1>` | Title | 24 pt bold | The article title. Exactly one. |
| `<h2>` | Heading 1 | 18 pt bold | Major phases — Introduction, each ladder step, Verification, Cause, Escalation, Related |
| `<h3>` | Heading 2 | 14 pt bold | Numbered tasks inside a step: `1. Task name` |
| `<h4>` | Heading 3 | 12 pt bold | Sub-tasks. Rarely needed; a fourth level usually means the step should be split. |

Body font is Arial 11 pt throughout. Do not set fonts inline — the converter
sets them and inline styles are dropped.

## Inline formatting

| Markup | Renders as | Use for |
|---|---|---|
| `<strong>` / `<b>` | Bold | UI elements (**Device Manager**), named ports and buttons (**HDMI IN**), expected states (**ON**, **Signed**), confidence marks, `STOP` |
| `<code>` | Courier New 10 pt, red | Keyboard shortcuts (`Win + X`), paths, commands, service names, and the `[not stated]` / `[not in site profile]` gap tokens |
| `<span class="warning">` | Red bold | Stop conditions and patient-safety-adjacent warnings |
| `<pre>` | Courier New 9 pt in a shaded, bordered block | Log excerpts and multi-line commands, when the worklog contains them verbatim |
| `<a href="#anchor">` | Internal DOCX hyperlink | Cross-references between sections of the same article |

Bold is a signal, not emphasis. Bolding a whole sentence makes every bolded
UI element in the article stop reading as one.

## Lists

`<ul>` and `<ol>` both convert, and nest two levels — the second level is
indented 0.25" per level. Use `<ol>` where order is load-bearing (resolution
steps as recorded) and `<ul>` where it is not (checks that can be done in any
order).

Never hand-number list items. The converter applies List Number styling; a
manual `1.` inside an `<li>` produces `1. 1.`.

## Images

Images are referenced by the ID the session gives them:

```html
<img src="IMAGE_ID" alt="Device Manager with Display adapters expanded">
```

Rules:

1. Place the image **immediately after** the instruction it illustrates.
2. Use the exact ID provided. **Never invent a `src`** — a fabricated URL is
   fabricated specificity (GUARDRAILS G6) that survives into a published
   article.
3. Alt text describes what the reader should see in it, not "screenshot".
4. Images are centred by the converter; do not try to position them.

**What actually lands in the DOCX.** The converter embeds an image only when
`src` is a `data:image/...;base64,` URI, scaled to a maximum width of 6.5".
Any other `src` — including a bare ID — renders as a grey italic
`[Image: alt text]` placeholder. That is deliberate: a placeholder is an
honest gap, and a broken image link is not. The skill states which images
landed as placeholders rather than letting the analyst discover it after
upload.

**Screenshots and PHI.** A screenshot of a production worklist, study list,
or order detail almost certainly contains patient data. This plugin does not
ingest, redact, or de-identify it — see `docs/DATA-PROVENANCE.md`. When an
image is offered, say plainly that screenshot handling is the site's call
under its own policy, and keep drafting with placeholders if the answer is
no. Never embed an image that was not explicitly handed over for this
purpose.

## Callouts and tables

```html
<div class="callout warning">…</div>   <!-- pink background -->
<div class="callout info">…</div>      <!-- blue background -->
<div class="callout note">…</div>      <!-- grey background -->
```

Callouts convert to a single-cell bordered table with background shading.
Real tables (`<table>`/`<tr>`/`<th>`/`<td>`) convert with a grey header row
and grid borders. Keep tables to two or three columns — wider ones survive
the conversion but stop being readable in the ServiceNow article view.

## Metadata line

Immediately after the title, and required:

```html
<p class="metadata">KB0010624 | v1.0 | 2026-08-07</p>
```

Renders 10 pt grey. An unassigned article number is `KB[TBD]` — present and
visibly unfilled, per the gap-token convention. Omitting the line loses the
version, and an article with no version cannot be flagged stale later
(E7.5).

## Not worth using

These either drop silently or convert badly, and the article should not
depend on them:

- Inline `style` attributes, CSS classes other than the ones listed above,
  and anything in a `<head>` block
- Floating or right-aligned images
- Lists nested three or more levels deep
- Fonts other than Arial and Courier New
- Colour beyond black text, red warnings, and grey metadata

## Running the conversion

```bash
python3 scripts/html_to_docx.py article.html article.docx
```

Dependencies are `python-docx` and `Pillow`; the script carries a PEP 723
header, so `uv run scripts/html_to_docx.py …` resolves them without a
manual install. Without `Pillow` the script still runs — images fall back to
default sizing instead of being scaled to fit.
