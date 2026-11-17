# Stack

Decision record for how the site is built, and when to change it (Nov 2026). The site was built before this was written down; the reasons below were recorded afterwards, from how the project actually works.

## Current

| Layer | Choice |
|---|---|
| Page | Plain HTML, CSS and JavaScript (`site/`). `app.js` fetches the data and renders the filterable cards. |
| Data | One file, `site/data/traits.json`, edited by hand through PRs. |
| Data checks | `scripts/validate_traits.py` (standard-library Python) stands in for a schema. |
| Tests | Python `unittest` for the scripts; Node's built-in test runner for `app.js`. |
| Hosting | Cloudflare Pages serves `site/` at kbsrlab.com and deploys on every merge to `main`. No build command. |
| CI | GitHub Actions ("Checks", PR title), CodeRabbit review, gitleaks. |
| Analytics | GoatCounter (self-hosted script) and Cloudflare Web Analytics. |

No framework, no build step, no dependencies.

## Why

- **The data is small and changes by hand.** About 33 traits and 28 collections, logged from screenshots. A JSON file that diffs cleanly in a PR beats a database or CMS at this size.
- **Nothing to maintain.** With no build and no packages, there's nothing to upgrade and nothing that breaks when a library changes. Every update is "edit JSON, add icon, merge."
- **Free, fast and safe.** Static hosting costs nothing, loads instantly and has no server to attack. A strict CSP with Trusted Types is easy to enforce when the page loads almost no outside code.
- **The validator replaces a schema.** It enforces what a database would: alphabetical, unique collections, valid tiers and tags, icon paths that exist.

## Alternatives considered

| Option | Verdict |
|---|---|
| Same stack + `// @ts-check` and JSDoc types | Smallest upgrade: editor type-checking with no build step. Worth doing any time. |
| TypeScript + Vite | Real types and a dev server, at the cost of a build step and `node_modules`. Worth it once `app.js` grows past a few hundred lines. |
| Astro | The pick for a v2 (see below). Renders pages to static HTML at build time, ships no JavaScript by default, has TypeScript built in, and checks data against schemas ("content collections"). |
| Next.js + Supabase | Overkill for a read-only reference. Only fits if the site needs accounts, open public editing, or live data such as an auction price tracker. |

## When to revisit

Move off the current stack when one of these is true:

- The site grows into a **wiki**: more kinds of data (players, awakenings, bond bonuses, collections) with pages that link to each other.
- **One page per trait** (or per player) is wanted, for search engines and Discord link previews.
- `app.js` gets large enough that type errors become a real risk.

## Wiki plan

If kbsrlab becomes a wiki and edits still come in as PRs and form submissions, move to **Astro**, likely with its **Starlight** docs theme (sidebar navigation, search, dark mode):

- Each data type becomes a content collection with a schema, replacing most of `validate_traits.py`.
- Trait, player and collection pages are generated from the data, with links between them.
- The filter UI stays interactive as a single "island"; everything else is static HTML.
- Site search via Pagefind (static, no server).
- Still deploys to Cloudflare Pages, with a build command added.

Migrate in stages, each its own PR series that ships on its own:

1. Move the current trait page to Astro with no visible changes.
2. Add player pages (awakening and bond data).
3. Add search.

If the public should edit directly, that's a different project: accounts, edit history, moderation and spam protection. Either use a wiki host (wiki.gg, Fandom) or build an app with auth and a database (Next.js + Supabase). A "suggest an edit" form feeding PRs, like the current correction form, covers most of the need without that.
