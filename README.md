# Bushcraft Companion

> "Knowledge weighs nothing."

An offline-first Bushcraft & Survival Companion — a single-file HTML Progressive Web App (PWA) for Australian outdoor users: campers, hikers, bushwalkers, 4WD and preppers.

100% offline. No network calls, no auth, no cloud. Works in direct sunlight and at 2am on a dim screen.

## Features

- **Survival Encyclopedia** — 30 field-manual articles across Fire, Shelter, Water, Food, Signalling and Survival Psychology, with Australian context throughout.
- **Emergency First Aid** — 20 protocols aligned with Australian Resuscitation Council (ARC) guidance, including the full Australian snake set (Brown, Tiger, Taipan, Red-bellied Black, Death Adder), Pressure Immobilisation Bandaging, spiders, CPR (DRSABCD), and anaphylaxis. Urgency badges, CALL 000 banners, numbered steps and "Do Not" lists.
- **Knot Library** — 12 essential knots with strength ratings, step-by-step instructions and text diagrams.
- **Bushcraft Projects** — 7 practical builds from shelter to fishing kit.
- **Offline Notes** — a local field journal (create/edit/delete), stored on-device only.
- **Emergency Mode** — a full-screen, one-tap overlay reachable from any screen.

## Tech

- Single `index.html` — all CSS and JS inline, zero build step.
- `localStorage` for notes, recents, settings and install date.
- Web App Manifest + Service Worker for installability and offline caching.
- Fonts: Space Grotesk + Inter (Google Fonts, the only first-load network request).

## Run it

Open `index.html` directly in a browser, or visit the GitHub Pages URL. Install it to your home screen for full offline use.

## Disclaimer

This app is an educational field reference, not a substitute for professional first aid training or emergency medical care. In any emergency, call **000** (Australia).
