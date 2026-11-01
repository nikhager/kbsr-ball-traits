# App icon

Decision record for the site's browser-tab icon and iPhone home-screen icon (Nov 2026).

## Final

| Use | File | Design |
|---|---|---|
| Browser tab | `images/favicon.svg` (+ `images/favicon-32.png` fallback) | Orange ball in a gold ring, transparent background |
| iPhone home screen | `images/apple-touch-icon.png` (180×180) | Same ring ball, medium size, on a sky-blue tile styled after the in-game Basketball Shop |

Editable sources are in `sources/`. Re-render the PNGs from them if the design changes. All of it is original artwork, not game assets.

## Variants

Every option tried, as its own SVG in `variants/<name>.svg`. `catalog.png` shows them all with their names. To swap icons, refer to a variant by name (e.g. "use tile-speed-ring").

Naming: `tab-` = browser-tab icon (transparent), `tile-` = full-square home-screen tile. Then background, then ball style (`-ring` = gold-ring ball).

| Name | Description | Round |
|---|---|---|
| `tab-plain-ball` | Ball with dark outline, no ring | 1 |
| `tab-gold-ring` | **Shipped tab icon.** Ball in a gold ring | 1 |
| `tile-white-ring` | Gold-ring ball on white (first home-screen icon) | 2 |
| `tile-gold` | Gold gradient tile, ball with white outline | 2 |
| `tile-ball-fill` | Zoomed-in ball fills the tile | 2 |
| `tile-navy-ring` | Gold-ring ball on dark navy | 2 |
| `tile-hair-blue-ring` | Kuroko hair pale blue | 3 |
| `tile-speed-ring` | Loading-screen cyan into dark starfield | 3 |
| `tile-gray-ring` | Light gray gradient | 3 |
| `tile-deep-blue-ring` | Richer blue | 3 |
| `tile-loading-gray-ring` | Exact loading-screen gray | 4 |
| `tile-loading-streaks-ring` | Loading-screen gray with light streaks | 4 |
| `tile-loading-streaks-flat` | Streaks, flatter red-orange ball, no ring | 4 |
| `tile-inventory-ring` | Inventory card blue with bands and shadow | 5 |
| `tile-gold-frame` | Gold circular frame from the shop detail panel | 5 |
| `tile-shop-card` | Cream shop listing card with orange arc | 5 |
| `tile-shop-small` | Basketball Shop sky blue, small ball, shadow | 5 |
| `tile-shop-medium` | Shop tile, bigger ball, no ring | 6 |
| `tile-shop-large` | Shop tile, ball nearly edge to edge | 6 |
| `tile-shop-ring-medium-v1` | Shop tile, gold-ring ball, with upper-left line | 7 |
| `tile-shop-ring-large` | Shop tile, bigger gold-ring ball | 7 |
| `tile-shop-ring-medium` | **Shipped home-screen icon.** v1 without the upper-left line | 8 |

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
