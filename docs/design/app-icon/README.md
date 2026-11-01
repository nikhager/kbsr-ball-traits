# App icon

Decision record for the site's browser-tab icon and iPhone home-screen icon (Nov 2026).

## Final

| Use | File | Design |
|---|---|---|
| Browser tab | `images/favicon.svg` (+ `images/favicon-32.png` fallback) | Orange ball in a gold ring, transparent background |
| iPhone home screen | `images/apple-touch-icon.png` (180×180) | Same ring ball, medium size, on a sky-blue tile styled after the in-game Basketball Shop |

Editable sources are in `sources/`. Re-render the PNGs from them if the design changes. All of it is original artwork, not game assets.

## How we got there

| Round | File | What was tried | Outcome |
|---|---|---|---|
| 1 | `01-favicon-options.png` | Game balls, a trait badge, the loading-screen ball, two original drawings, at real tab size | Original ball in a gold ring: the only one that reads at 16px and isn't game art |
| 2 | `02-home-screen-full-bleed.png` | Full-bleed tiles to replace the white square iOS showed | Wanted Kuroko colors instead |
| 3 | `03-kuroko-palette.png` | Backgrounds from Kuroko's hair and the loading screen | Led to trying the loading-screen gray |
| 4 | `04-loading-screen-gray.png` | Exact loading-screen grays, with and without light streaks | Led to trying in-game ball backings |
| 5 | `05-ball-backings.png` | Inventory card, gold detail frame, shop listing card, Basketball Shop tile | Shop tile chosen; ball too small. Gold frame: no. Shop listing card: swoop, small ball and shadow rejected, background blends with the white outline |
| 6 | `06-shop-tile-ball-size.png` | Shop tile with a bigger ball, no shadow | Wanted the gold ring back |
| 7 | `07-shop-tile-gold-ring.png` | Gold-ring ball on the shop tile, two sizes | Medium chosen |
| 8 | `08-final.png` | Medium ring with the upper-left line removed | Shipped |

## Notes
- iOS saves the home-screen icon when the page is added and never refreshes it. After changing it, delete and re-add the shortcut.
- Idea for later: an icon picker (default icon, generic ball, or any collection ball, defaulting to the newest ball). It needs clean ball crops first.
