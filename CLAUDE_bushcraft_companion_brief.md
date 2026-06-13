# CLAUDE CODE BRIEF
## Offline Bushcraft & Survival Companion — PWA v1.0

---

## Project Identity

**App name:** Bushcraft Companion  
**Tagline:** "Knowledge weighs nothing."  
**Platform:** Single-file HTML PWA — deployed to GitHub Pages  
**Monetisation:** One-time purchase gate (premium unlock flag via localStorage for now; payment integration deferred)  
**Offline-first:** 100% — no network calls, no auth, no cloud  
**Target:** Australian outdoor users — campers, hikers, bushwalkers, 4WD, preppers

---

## Tech Stack

- **Single file:** `index.html` — all CSS and JS inline, zero build step
- **Storage:** localStorage for notes, settings, unlock state, challenge progress
- **Content:** All survival content bundled as JS constants (objects/arrays) directly in the file
- **Icons/images:** SVG inline only — no external image dependencies
- **PWA:** Web App Manifest + Service Worker for installability and offline caching
- **Fonts:** Google Fonts via `<link>` in `<head>` — Space Grotesk (headings), Inter (body) — both loaded with `display=swap`
- **No frameworks, no npm, no build tooling**

---

## Design System

### Philosophy
Dark field tool aesthetic. Feels like a premium field manual digitised — not a social app, not a nature blog. Think Garmin meets Peak Design: functional, readable, dark by default, premium in proportion. Every screen should work in direct sunlight and at 2am with a dim screen.

### Colour Tokens (CSS custom properties on `:root`)

```css
--bg:          #1A1A17;   /* near-black, warm undertone */
--surface:     #252520;   /* card/module backgrounds */
--elevated:    #2E2E28;   /* nav, modal, elevated surfaces */
--border:      #3A3A34;   /* dividers, outlines */
--text-primary:#F0EDE6;   /* primary readable text */
--text-secondary:#8C8A82; /* labels, meta, secondary info */
--accent:      #D4622A;   /* burnt orange — emergency, fire, primary CTA */
--nature:      #6B8C5A;   /* muted olive green — plants, nature, safe */
--warning:     #C9952A;   /* amber — caution, weather, prepare */
--danger:      #B83B3B;   /* dark red — danger, toxic, injury */
--success:     #4A7C59;   /* confirmation, completed challenge */
```

### Typography

```
Display / Module titles: Space Grotesk, 700, uppercase, tracked wider (letter-spacing: 0.08em)
Section headings:        Space Grotesk, 600
Body / content text:     Inter, 400, line-height 1.65, max-width 65ch
Labels / metadata:       Inter, 500, 0.75rem, uppercase, letter-spacing 0.1em, color: var(--text-secondary)
Emergency text:          Space Grotesk, 700, large (1.5rem+), var(--accent)
```

### Spacing Scale
Use a consistent 8px base grid: 8, 16, 24, 32, 48, 64px.

### Touch Targets
Minimum 48px tap height on all interactive elements. Emergency mode: 72px minimum.

### Signature Design Element
**Module entry cards** use a left-side coloured border bar (4px, rounded) in the module's theme colour — no icons, no images. The category label sits above the title in small caps. This creates a field-manual ledger feel. Consistent across all content modules.

### Component Patterns

**Card:**
```
background: var(--surface)
border-radius: 6px
border-left: 4px solid [module colour]
padding: 16px 20px
```

**Button — Primary:**
```
background: var(--accent)
color: #fff
border-radius: 4px
padding: 14px 24px
font: Space Grotesk 600
no box-shadow
```

**Button — Ghost:**
```
border: 1px solid var(--border)
color: var(--text-primary)
background: transparent
```

**Section label:**
```
font: Inter 500, 0.7rem, uppercase, letter-spacing 0.12em
color: var(--text-secondary)
margin-bottom: 8px
```

---

## App Architecture

### Navigation
Bottom tab bar (mobile-first). Five tabs:

| Tab | Icon (SVG) | Label |
|-----|-----------|-------|
| Home/Dashboard | Compass | Home |
| Encyclopedia | Book | Guides |
| First Aid | Cross | First Aid |
| Projects | Hammer | Projects |
| Notes | Pencil | Notes |

**Emergency Mode** is a floating button — persistent red/orange pill button top-right of every screen. Tapping it pushes the Emergency Mode overlay on top of everything.

### Screen Flow

```
App opens
  └─ Home Screen (quick access tiles + last viewed)
      ├─ Guides (Encyclopedia)
      │   ├─ Category list (Fire, Shelter, Water, Food, Signalling, Psychology)
      │   │   └─ Topic list within category
      │   │       └─ Article view (full content, offline)
      ├─ First Aid
      │   ├─ Category list (Bleeding, Burns, Hypothermia, Heat, Snakes, Spiders, Fractures, Shock, CPR)
      │   └─ Article view (step-by-step, numbered, clear)
      ├─ Knots (sub-section within Guides or its own tab — pick whichever fits nav)
      ├─ Projects
      │   ├─ Project list (difficulty filter)
      │   └─ Project detail (materials, steps, time)
      ├─ Notes
      │   ├─ Note list
      │   └─ Note editor (simple textarea, title, tag, timestamp)
      └─ Emergency Mode (overlay, always accessible)
```

---

## Module Specifications

### MODULE 1 — Home Screen

- Dark welcome header: `BUSHCRAFT COMPANION` in display font
- Row of quick-access tiles for the 4 most common emergencies (Water, Lost, Injured, Snake)
- "Recently Viewed" list (tracked in localStorage — last 5 articles)
- "Day X Offline" stat pulled from first-install timestamp (stored in localStorage)
- No images. SVG icons only.

---

### MODULE 2 — Survival Encyclopedia

**Categories and content to bundle (create realistic, accurate content — not placeholder lorem ipsum):**

#### FIRE
- Ferro Rod Technique
- Bow Drill Fire Starting
- Flint and Steel
- Fire Lay Types (Log Cabin, Teepee, Star, Long Fire)
- Fire Starting in Wet Conditions
- Reading Tinder Quality

#### SHELTER
- Lean-To Shelter
- Debris Hut / Debris Shelter
- Tarp Shelter Configurations
- Emergency Bivouac
- Site Selection Principles

#### WATER
- Finding Water Sources in the Bush
- Solar Still Construction
- Collecting Rain and Dew
- Water Filtration Methods (without equipment)
- Improvised Filtration (sand/charcoal/cloth)
- Water Purification (boiling, chemical)
- Signs of Water in Arid Terrain

#### FOOD
- Snare and Trap Basics
- Reading Animal Tracks (Australian species)
- Improvised Fishing Methods
- Food Preservation Without Refrigeration
- Caloric Priority in Survival

#### SIGNALLING
- Mirror Signalling Technique
- Ground-to-Air Signal Patterns
- Whistle Signals (International)
- Smoke Signals
- Building a Signal Fire

#### SURVIVAL PSYCHOLOGY
- The STOP Principle (Stop, Think, Observe, Plan)
- Managing Panic in the Field
- Decision Making Under Stress
- The Will to Survive
- Group Dynamics in Survival

**Content data structure:**

```javascript
const ENCYCLOPEDIA = [
  {
    id: "fire-ferro-rod",
    category: "fire",         // used for colour coding and filtering
    title: "Ferro Rod Technique",
    summary: "One sentence that appears in the card list.",
    difficulty: "beginner",   // beginner | intermediate | advanced
    time: null,               // estimated time if applicable
    content: `
      Full article content in plain text or minimal HTML.
      Use <h3>, <p>, <ul>, <li>, <strong> only.
      Keep it field-manual terse — no padding.
    `,
    tags: ["fire", "ignition", "essential"],
    australianNote: null      // optional string for AU-specific context
  }
];
```

**Minimum content required for v1:** 3–4 articles per category minimum. Write real, accurate bushcraft content — not placeholder text.

---

### MODULE 3 — Emergency First Aid

Critical module. Prioritise clarity above all else. 

**Categories:**

- Severe Bleeding (direct pressure, tourniquet, packing)
- Burns (classification, cooling, dressing)
- Hypothermia (recognition, warming protocols)
- Heat Stroke vs Heat Exhaustion
- Snake Bite — General Protocol
- **Australian Snake Bite (special section)**
  - Pressure Immobilisation Bandaging (PIB) — step by step, numbered
  - Eastern Brown Snake
  - Tiger Snake
  - Taipan
  - Red-Bellied Black
  - Death Adder
- **Spider Bite — Australian**
  - Funnel-Web (red card — call 000, antivenom)
  - Redback
  - White-Tail
- Fractures and Sprains (splinting)
- Shock Recognition and Treatment
- CPR (adult, current ARC guidelines structure)
- Drowning / Near Drowning Response
- Eye Injuries
- Allergic Reaction / Anaphylaxis

**Article structure for First Aid — strict format:**

```javascript
const FIRST_AID = [
  {
    id: "snake-eastern-brown",
    category: "snakes",
    title: "Eastern Brown Snake Bite",
    urgency: "critical",        // critical | urgent | standard
    australianOnly: true,
    callEmergency: true,        // renders a prominent "CALL 000" banner
    summary: "...",
    steps: [
      { step: 1, instruction: "Keep the patient still and calm.", warning: null },
      { step: 2, instruction: "Apply Pressure Immobilisation Bandage immediately.", warning: "Do NOT wash the bite site — venom traces assist identification." },
    ],
    doNot: ["Do not wash the bite site.", "Do not cut or suck the bite.", "Do not apply a tourniquet."],
    notes: "Optional additional field notes.",
    content: "Prose description for additional context below the steps."
  }
];
```

**First aid articles MUST display:**
- Urgency badge (Critical / Urgent / Standard) — colour coded (danger / warning / nature)
- "CALL 000" banner (red, prominent) when `callEmergency: true`
- Numbered steps — never prose paragraphs for the action steps
- DO NOT list (rendered with ✗ prefix, red text)

---

### MODULE 4 — Knot Library

**Knots to include (v1):**

| Knot | Category | Use Case |
|------|----------|----------|
| Bowline | Essential | Rescue loop, anchor |
| Clove Hitch | Camping | Attaching to posts |
| Taut-Line Hitch | Camping | Adjustable tent guy |
| Figure-Eight | Rescue | Stopper, anchor |
| Sheet Bend | Essential | Joining two ropes |
| Reef Knot | Camping | Joining same-weight rope |
| Timber Hitch | Bushcraft | Dragging logs |
| Half Hitch | Utility | Quick tie-off |
| Rolling Hitch | Utility | Rope on rope |
| Trucker's Hitch | 4WD/Camping | Load securing |
| Prusik Knot | Rescue | Ascending ropes |
| Fisherman's Knot | Fishing | Joining fishing line |

**No animations in v1** (too complex for single-file). Instead: numbered ASCII step diagrams rendered in a monospace block. Each knot shows:

```
- Name, category badge
- Strength rating (1–5 dots)
- Difficulty
- Best use cases (tags)
- Step-by-step instructions in plain text
- ASCII/text rope diagram where practical
```

Knot data structure:

```javascript
const KNOTS = [
  {
    id: "bowline",
    name: "Bowline",
    category: "essential",
    strengthRating: 5,
    difficulty: "intermediate",
    uses: ["rescue loop", "anchor point", "tying to tree"],
    steps: [
      "Form a small loop in the standing end of the rope.",
      "Pass the working end up through the loop from below.",
      "Take the working end around the standing part.",
      "Return the working end back down through the small loop.",
      "Tighten by pulling the standing part and the loop."
    ],
    tips: "Remember: the rabbit comes up through the hole, around the tree, and back down the hole.",
    asciiDiagram: null  // optional string if worthwhile
  }
];
```

---

### MODULE 5 — Bushcraft Projects

**Projects to include (v1):**

- Camp Chair (using logs + lashing)
- Tripod Pot Hanger
- Improvised Fishing Line and Hook
- A-Frame Tarp Setup (configuration guide)
- Improvised Stretcher
- Basic Debris Shelter (step-by-step construction)
- Improvised Water Filter (layered)

**Project data structure:**

```javascript
const PROJECTS = [
  {
    id: "tripod-pot-hanger",
    title: "Tripod Pot Hanger",
    category: "camp-cooking",
    difficulty: "beginner",    // beginner | intermediate | advanced
    timeMinutes: 20,
    materials: [
      "3× straight branches, 1.2–1.5m long",
      "Paracord or natural cordage",
      "1× hanging branch or hook"
    ],
    steps: [
      { step: 1, title: "Select three straight branches of similar length.", detail: "Look for hardwood where possible. Avoid green wood from eucalypts." },
    ],
    tips: "A longer hanging branch gives you better height control over the fire."
  }
];
```

---

### MODULE 6 — Offline Notes

Simple local journaling. Stored in localStorage as JSON array.

**Features:**
- Create, edit, delete notes
- Title + body text
- Tags (free text, comma separated)
- Timestamp (auto)
- Type field: `general | camp-log | hunting | fishing | survival-journal`

**UI:**
- Note list (sorted by newest)
- Tap to open/edit
- Bottom-right FAB to create new note
- No sync, no cloud, no account

**Data shape in localStorage key `bc_notes`:**

```javascript
[
  {
    id: "uuid-or-timestamp",
    title: "Camp at Lake Mackenzie",
    body: "Full note text...",
    tags: ["camping", "water"],
    type: "camp-log",
    createdAt: "2025-06-01T14:30:00Z",
    updatedAt: "2025-06-01T18:00:00Z"
  }
]
```

---

### MODULE 7 — Emergency Mode

**The most important UX in the app.** One tap from anywhere. Full-screen overlay.

**Design requirements:**
- Background: `#0D0D0B` (darker than app bg)
- Header: `EMERGENCY MODE` in Space Grotesk, 700, var(--accent), large
- Large grid of 2-column tiles — minimum 72px tap height each
- Each tile: icon (SVG), label, links directly to a specific first aid or survival article

**Tiles:**

| Label | Icon | Links To |
|-------|------|---------|
| I Need Water | Droplet | Water sourcing article |
| I Am Lost | Map pin | STOP Principle article |
| Injured Person | Cross | First Aid home |
| Snake Bite | Snake | Australian Snake Bite |
| Heart Stopped | Heart | CPR |
| Severe Bleeding | Blood drop | Bleeding article |
| Start a Fire | Flame | Fire basics |
| Build Shelter | Triangle/tent | Lean-to article |
| Signal Rescue | Signal wave | Signalling article |
| Heat Stroke | Sun | Heat Stroke article |

**No animation, no transitions** in Emergency Mode. Instant render.

**Exit:** `✕ EXIT EMERGENCY MODE` ghost button at bottom — requires two taps (first tap reveals confirm button) to prevent accidental exit.

---

## PWA Requirements

```html
<!-- In <head> -->
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#1A1A17">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
```

**manifest.json** (inline via blob or separate file):
```json
{
  "name": "Bushcraft Companion",
  "short_name": "Bushcraft",
  "start_url": ".",
  "display": "standalone",
  "background_color": "#1A1A17",
  "theme_color": "#1A1A17",
  "description": "The survival guide that works when nothing else does.",
  "icons": [
    { "src": "icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

**Service Worker** — register in a `<script>` tag at bottom of body:
```javascript
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js');
}
```

Service worker should cache `index.html` and itself on install. Serve from cache on fetch. Simple cache-first strategy.

---

## localStorage Key Conventions

| Key | Content |
|-----|---------|
| `bc_notes` | JSON array of user notes |
| `bc_recent` | JSON array of last 5 article IDs viewed |
| `bc_settings` | JSON object: `{ theme, nightMode, textSize }` |
| `bc_installed` | ISO date string of first launch |
| `bc_premium` | boolean (unlock state — for future payment gate) |
| `bc_challenges` | JSON object of completed challenge IDs |

---

## Content Guidelines

- Write real, accurate bushcraft and first aid content — not lorem ipsum
- Keep articles terse, field-manual style — bullets over prose where possible
- Australian context throughout — species, geography, emergency numbers (000 not 911)
- All first aid to reflect current Australian Resuscitation Council (ARC) protocols
- Snake bite = Pressure Immobilisation Bandaging, not tourniquet
- No fluff, no caveats beyond safety warnings, no "consult a professional before..." hedging unless genuinely critical

---

## File Output

Produce three files:

1. **`index.html`** — the complete single-file app (all CSS, JS, content inline)
2. **`sw.js`** — service worker (simple cache-first)
3. **`manifest.json`** — PWA manifest

No build step required. Open `index.html` directly in browser to test. Deploy all three to GitHub Pages root.

---

## What Is Deferred to V2

Do not build these in v1. Reference them in a `// TODO: v2` comment block if needed:

- Survival Challenges / gamification / badge system
- Plant, animal, tree, mushroom identification field guides (needs large dataset)
- Compass / navigation / map tools (needs device APIs)
- Weather indicator reference module
- AI Survival Advisor (needs API integration)
- On-device plant ID (needs ML)
- Knot animations (needs canvas/SVG animation work)
- Payment gateway integration
- Regional expansion packs (North America, NZ, Europe)
- Sync / backup of notes
- Search across all content

---

## Definition of Done — v1

- [ ] All 7 modules render correctly on mobile (375px viewport minimum)
- [ ] Emergency Mode accessible from all screens with one tap
- [ ] All first aid articles have urgency badge + 000 banner where appropriate
- [ ] Notes create/edit/delete working and persisted in localStorage
- [ ] Service worker registers and app is installable as PWA
- [ ] No network requests at runtime (fonts are the only exception on first load — acceptable)
- [ ] Dark theme is default and only theme for v1
- [ ] All content is real, accurate, Australia-appropriate
- [ ] Bottom nav works correctly on all modules
- [ ] Recent articles tracked in localStorage and shown on home screen
