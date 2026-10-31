# KBSR Ball Traits

Every ball trait in **Kuroko's Basketball: Street Rivals** (global server): effects, tier II/III values, trait icons, and which ball collections carry each trait.

**Live page:** https://nikhager.github.io/kbsr-ball-traits/

## Why this exists
The game has no public wiki, and trait details only show up in in-game tooltips. Ball boxes rotate through the shop and rewards each month, so a collection's traits can only be logged while its boxes are available. This page gathers what's been seen in one searchable place, so players can plan builds and recognize traits in the auction without waiting for the next rotation.

## Features
- Filter by objective: 3PT, Mid-Range, Finishing, Steal, Block, Contest, Rebound, Energy and more
- Filter by ball collection, with match counts on each filter
- Search trait names and effects
- Icons for each tier, so you can recognize traits in the auction at a glance

## Status
Most traits are logged. Collection lists and some tier values are still partial and fill in as boxes cycle back into the shop. Missing values show on the page as "Not seen yet" or "Numbers not logged" rather than guesses.

## How it works
A single static page with no build step and no dependencies. `index.html` fetches `traits.json` and renders the filterable cards with plain JavaScript, served by GitHub Pages from `main`.

- `traits.json`: all trait data (effects, tier values, collections)
- `icons/`: trait icons, one per tier (`<trait>-ii.png`, `<trait>-iii.png`)

Effect text is copied from in-game tooltips on the global server. Where the game's translation is unclear, any clarification is in [square brackets] so it's distinguishable from the game's own wording.

## Corrections
Spotted a wrong value or a trait on a ball that isn't listed? [Open an issue](https://github.com/nikhager/kbsr-ball-traits/issues) with the trait name, tier and ball.

## Privacy
The page counts anonymous visits and filter use with [GoatCounter](https://www.goatcounter.com): no cookies, no personal data, no cross-site tracking.

Fan-made reference, not affiliated with the game's publishers. Trait icons are the publisher's artwork.
