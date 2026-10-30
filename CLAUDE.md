# KBSR Ball Traits: notes for Claude

Static fan reference for ball traits in Kuroko's Basketball: Street Rivals (global server), served by GitHub Pages from `main` at https://nikhager.github.io/kbsr-ball-traits/. No build step and no dependencies.

## Files
- `index.html`: the whole page (HTML, CSS, JS). It fetches `traits.json` and renders filterable cards.
- `traits.json`: all data. `collections` is the ordered list for the collection dropdown; `traits` is the list of cards.
- `icons/<trait-id>-ii.png`, `icons/<trait-id>-iii.png`: tier icons, 124px square crops of the in-game trait badge.

## Trait entry shape
```json
{
  "id": "rising-strong",              // lowercase, hyphenated trait name
  "name": "Rising Strong",
  "category": "Rebounding",           // Offense, Handling, Defense, Hybrid, Rebounding, Energy
  "tags": ["Rebound"],                // filter chips, see list below
  "effect": "Exact in-game tooltip text, using tier III numbers where seen",
  "effectSource": "Tier III",         // tier the text came from, or "" if it's a summary of an unseen trait
  "trainingCamp": "",                 // Training Camp bonus text, or ""
  "tiers": {
    "II":  { "value": "+1.5 (+1.5 after a miss)", "icon": "icons/rising-strong-ii.png", "seenOn": "LG Kagami, ZONE Mura" },
    "III": { "value": "+2 (+2 after a miss)",     "icon": "icons/rising-strong-iii.png", "seenOn": "Autumn Moon" }
  },
  "collections": [{ "name": "Autumn Moon", "tiers": "III" }]
}
```
- Use `""` for an unknown value and `null` for a missing icon. The page shows "Not seen yet" or "Numbers not logged".
- Filter tags: 3PT, Mid-Range, Finishing, All shots, Open shots, Handling, Passing, Steal, Block, Contest, Rebound, Speed, Energy. Energy covers every energy-related trait (energy-scaling, Ultimate-triggered, energy gain). Steal covers every steal-triggered trait.
- Collection names must match an entry in `collections`.
- Effect text is copied verbatim from the game. The game has translation errors: put any editorial fill-in or correction in [square brackets] so it's clearly not the game's text, e.g. "reduces [Charge Rate] by 3%".

## Logging new traits from screenshots
1. Read the trait name, tier and numbers from the tooltip.
2. On a ball with two traits, the icon that was tapped shows dimmer. That tells you which icon goes with the open tooltip.
3. A trait keeps the same symbol at every tier; only the ring color changes (purple II, gold III). Paint Powerhouse has a backboard rectangle behind the arm; Absolute Core doesn't.
4. Update `traits.json`, add the icon PNG, and keep the owner's "KNBSR Ball Build Planner" Google Sheet (Traits tab) in sync.
5. Commit and push only when the owner asks.

## Constraints
- Public repo: never commit secrets, personal emails, Google Sheet/Doc IDs, or full screenshots (they show the player ID). Icon crops only.
- Icons are the game publisher's artwork. Don't add a license that claims them.
