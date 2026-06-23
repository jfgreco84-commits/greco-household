# Best Solution — Logo / Thumbnail Handoff

**Date:** 2026-06-23
**Owner:** Justin Greco (jfgreco84@gmail.com)
**Status:** ⏸️ Blocked on repo access — design not yet built. Resume tomorrow.

---

## 🎯 The goal (one sentence)

Replace the logo/thumbnail for the **Best Solution polish reorder website** with a
**brand-new image built in the exact style of the purple/gold "BEST SOLUTION" flyer**
(a clean branded badge — diamond logo + "Professional Jewelry & Glass Polish").

The thumbnail is what shows up as the **home-screen icon / link-preview card** titled
**"Best Solution Polish - Reorder."**

---

## 🚧 Why it stopped (read this first)

The live site lives in its **own repo**, which was **not in this session's allowed list**:

- **Target repo:** `jfgreco84-commits/bestsolution`
  → deploys to **https://jfgreco84-commits.github.io/bestsolution/**
  → description: *"Best Solution polish reorder page (Dot Dynasty LLC)"*
- **This session was scoped only to:** `jfgreco84-commits/greco-household`

Every attempt to read/write `bestsolution` returned:
> Access denied: repository "jfgreco84-commits/bestsolution" is not configured for this session.

The on-the-fly "add repo" tools were **not loaded** in this session, so it couldn't be
self-fixed. The fix is to **start the next session with `bestsolution` in scope** (steps below).

---

## ✅ How to resume tomorrow (iPhone steps)

1. Open **claude.ai/code** in Safari (or the Claude app).
2. Tap **New session** (the **+**).
3. For the **repository**, pick **`jfgreco84-commits/bestsolution`**
   (type "bestsolution" in the search box if needed).
   - If you can pick a 2nd repo too, also add **`greco-household`** (so this handoff is visible).
4. Start the session.
5. **Re-attach the 3 reference photos** (📎 icon → Photos):
   - The wide purple promo flyer (IMG_7205)
   - The full detailed flyer with the bottle + 2-step process (IMG_7207)
   - The 6-bottle product lineup on white (IMG_7203)
6. Paste this prompt:

> Read this handoff: `best-solution/THUMBNAIL_HANDOFF.md` in greco-household (or I'm
> re-pasting the spec below). Build a new logo/thumbnail for THIS bestsolution site in
> the exact purple/gold "BEST SOLUTION" flyer style — a clean branded badge with the
> diamond logo and "Professional Jewelry & Glass Polish." Render real PNGs, wire them
> into index.html (apple-touch-icon, favicon, og:image, twitter:image, plus og:title /
> og:description), commit, and open a **draft PR**.

---

## 🎨 Design spec (so the build is exact)

**Concept:** Clean branded **badge** (NOT a busy mini-flyer). Must stay sharp at small
icon sizes (~120px home-screen icon) while clearly matching the flyer.

**Colors (pulled from the flyers):**
- Purple background gradient: bright violet center `#7B2CBF`→`#8E3FD0`, deep edges `#3D1366`→`#2A0A4A`
- Gold accents: `#F5C542` / `#E8B923`, deep gold `#C9952A`
- Text: white `#FFFFFF`

**Layout (square icon):**
- Rounded-square deep-purple radial-gradient background, subtle thin **gold ring** inset.
- Centerpiece: a faceted **diamond emblem** (white/silver with gold facets + a sparkle), echoing the brand's diamond "Ⓒ" logo.
- Wordmark **BEST SOLUTION** in heavy condensed white caps (stacked: BEST / SOLUTION).
- Under it, small gold letter-spaced caps: **PROFESSIONAL JEWELRY & GLASS POLISH**.
- Optional tiny gold tag: **SINCE 1985**. A couple of small sparkles for polish.

**Two deliverables (PNG):**
1. **Square icon** — render at 1024×1024 (also export/derive 512 + 180 for `apple-touch-icon`).
2. **Link-share card** — 1200×630 (`og:image`): diamond + wordmark on the left, taglines
   ("No Acid • No Ammonia • No Abrasives", "Safe on Stones, Tough on Tarnish") on the right.

**Meta tags to add/update in `index.html` `<head>`:**
```html
<link rel="apple-touch-icon" href="best-solution-icon-180.png">
<link rel="icon" type="image/png" sizes="512x512" href="best-solution-icon-512.png">
<meta property="og:title" content="Best Solution Polish — Reorder">
<meta property="og:description" content="Professional Jewelry & Glass Polish — No Acid, No Ammonia, No Abrasives. Restore the shine, reclaim the value.">
<meta property="og:image" content="https://jfgreco84-commits.github.io/bestsolution/best-solution-og.png">
<meta property="og:url" content="https://jfgreco84-commits.github.io/bestsolution/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://jfgreco84-commits.github.io/bestsolution/best-solution-og.png">
```
> ⚠️ First step in the new session: **read the existing `index.html` `<head>`** in
> `bestsolution` — it may already have icon/og tags to replace rather than duplicate.
> Also confirm the deployed path/filenames (GitHub Pages serves from the repo root).

---

## 🛠️ Technical notes (environment — confirmed working)

- **Node** v22 is available. Network/npm works.
- **SVG → PNG rasterizer:** `@resvg/resvg-js` (prebuilt binary, no system deps). Install:
  `npm install @resvg/resvg-js` (~1s). Use it to render the SVG badge to PNG.
- **Fonts** (curated, local): `/mnt/skills/examples/canvas-design/canvas-fonts/`
  - Wordmark: **BigShoulders-Bold.ttf** (condensed heavy) or **BricolageGrotesque-Bold.ttf**
  - Subtitle / taglines: **Outfit-Bold.ttf**, **WorkSans-Bold.ttf**, or **InstrumentSans-Bold.ttf**
  - Point resvg at this dir via its `font: { fontDirs: [...] }` option.
- No Chromium / ImageMagick / PIL / cairosvg present — use the SVG+resvg path above.
- **Heads-up:** the scratchpad and any npm installs do **not** persist between sessions.
  Re-install resvg in the new session. Commit the generated PNGs into the `bestsolution`
  repo so they deploy.

---

## 🗂️ Repo map (Best Solution family)

| Repo | Purpose | Pages URL |
|------|---------|-----------|
| **`bestsolution`** ← TARGET | Public polish **reorder** page | jfgreco84-commits.github.io/bestsolution/ |
| `best-solution-app` | Personal sales tracker app (froggy master) | …/best-solution-app/ |
| `best-solution-blank` | Blank tracker template (Batman) | |
| `best-solution-isaiah` / `best-solution-anthony` | Crew trackers | |
| `greco-household` | Household finance hub + this handoff | |

> Note: the `greco-household` repo's `best-solution/` folder holds the **tracker app**
> source (froggy-personal.html etc.), which is a *different* thing from the public
> **reorder page** in the `bestsolution` repo. The thumbnail change is for the **reorder
> page** (`bestsolution`).

---

## 📌 TL;DR
1. New session **scoped to `jfgreco84-commits/bestsolution`**.
2. Re-attach the 3 flyer/bottle photos.
3. Paste the prompt above (or point me at this file).
4. I build the purple/gold badge PNGs, wire the `<head>`, and open a draft PR.
