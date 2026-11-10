<!-- Title: Conventional Commits, e.g. `feat(data): log Clutch Player II values` (it becomes the commit on main). -->

## What and why

<!-- Traits/collections added or corrected, and where the values came from (screenshot, form submission). -->

## Preview

<!-- Cloudflare preview link: https://<branch>.kbsr-ball-traits.pages.dev -->

## Review

- **Risk:** low / medium / high <!-- high = anything on the always-Nik list in CLAUDE.md -->
- **Needs Nik's review:** yes / no <!-- per the repo's autonomy level in CLAUDE.md -->
- **code-reviewer:** LGTM / LGTM with nits / changes requested
- **Series:** <!-- e.g. "2 of 3, depends on #12", or delete -->

## Checklist

- [ ] `python3 scripts/validate_traits.py` passes
- [ ] `updated` in `site/data/traits.json` set to today (America/Los_Angeles), if data changed
- [ ] Checked the preview build; new outside resources added to the CSP in `site/_headers`
- [ ] New icons are 96px WebP crops (icon crops only, no full screenshots)
- [ ] No secrets, personal emails, or Google Sheet/Doc IDs (the repo and its history are public)
- [ ] "KBSR Ball Build Planner" sheet (Traits tab) rebuilt from `traits.json`, if collections changed
