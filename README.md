# KBSR Ball Traits

Every ball trait in **Kuroko's Basketball: Street Rivals** (global server): effects, tier II/III values, trait icons, and which ball collections carry each trait.

**Live page:** https://kbsrlab.com

## Why this exists
The game has no public wiki, and trait details only show up in in-game tooltips. Ball boxes rotate through the shop and rewards each month, so a collection's traits can only be logged while its boxes are available. This page gathers what's been seen in one searchable place, so players can plan builds and recognize traits in the auction without waiting for the next rotation.

## Features
- Filter by objective: each shot type (3PT, Mid-Range, Close-Range, Layup, Dunk), Steal, Block, Contest, Rebound, Energy and more
- Filter by ball collection, with match counts on each filter
- Search trait names and effects
- Icons for each tier, so you can recognize traits in the auction at a glance
- Cards line up row by row, so icons and values are easy to compare side by side
- Light and dark themes that follow your device setting

## Status
Most traits are logged. Collection lists and some tier values are still partial and fill in as boxes cycle back into the shop. Missing values show on the page as "Not seen yet" or "Numbers not logged" rather than guesses.

## How it works
A static site with no build step and no dependencies, served by Cloudflare Pages from `main`. Changes go through a pull request; every branch gets a preview build, and merging to `main` deploys. Only the `site/` folder is published. The page fetches the trait data and renders the filterable cards with plain JavaScript.

```
site/                 everything the page loads (the only folder Cloudflare publishes)
  index.html          page markup
  _headers            security headers Cloudflare sends with every page
  robots.txt, sitemap.xml   search engine hints
  css/styles.css      styles, including light and dark themes
  js/app.js           filtering and rendering
  js/vendor/          third-party scripts (GoatCounter)
  data/traits.json    all trait data: effects, tier values, collections
  images/icons/       trait icons, one per tier (<trait>-ii.webp, <trait>-iii.webp)
scripts/              data checker and asset version tool, with their tests (not published)
tests/                page code tests, Node's built-in runner (not published)
docs/design/          design references and decision records (not published)
```

Every PR runs the "Checks" workflow: it validates the trait data, confirms the `?v=` version tags match their files, and runs all tests. Don't merge a PR while it's red (once it's a required check in branch protection, GitHub blocks the merge). Run the same checks locally with `python3 scripts/validate_traits.py`, `python3 scripts/version_assets.py --check`, `python3 -m unittest discover -s scripts` and `node --test tests/*.test.mjs`.

Effect text is copied from in-game tooltips on the global server. Where the game's translation is unclear, any clarification is in [square brackets] so it's distinguishable from the game's own wording.

## Corrections
Corrections and screenshots come in through the two Google Forms linked in the page footer ("Report a correction" and "Send screenshots"), or by email to contact@kbsrlab.com. Log each one with the trait name, tier and ball.

## Privacy
The page counts anonymous visits and filter use with [GoatCounter](https://www.goatcounter.com) and Cloudflare Web Analytics: no cookies, no personal data, no cross-site tracking.

## License
The [MIT License](LICENSE) covers the code in this repository (HTML, CSS, JavaScript), the site's original artwork (the favicon and home-screen icon), and the structure and editorial content of the trait data. It does not cover material from Kuroko's Basketball: Street Rivals: the trait icons in `site/images/icons/` and the in-game tooltip text quoted in `site/data/traits.json` belong to the game's publishers. The GoatCounter script in `site/js/vendor/` keeps its own ISC license.

Fan-made reference, not affiliated with the game's publishers. Trait icons are the publisher's artwork.
