MKL / MUBASHEER KC — PROFILE MAINTENANCE
======================================

README.md is the public profile. It links to the deployed portfolio and four
verified repositories. Keep essential project scope in native Markdown as well
as SVG alternative text. Audit evidence and limitations: docs/profile-audit.md.

SOURCE OF TRUTH
---------------
scripts/profile_svg.py             Shared palette, typography and SVG helpers.
scripts/render_profile_ui.py       Header (desktop/mobile), footer, CTAs and UI.
scripts/render_project_cards.py    Four projects, canonical repository names,
                                  scope labels and desktop/mobile cards.
scripts/generate_activity.py       GitHub GraphQL fetch, statistics and calendar.
assets/brand/mkl-monogram.svg      Official portfolio mark; see SOURCES.md.
assets/projects/logos/            Preserved project-owned artwork.
assets/toolkit/icons/             Preserved local Devicon assets and attribution.

Generated SVGs must be changed through their Python source, then regenerated.
The optional profile, focus, section and secondary CTA assets remain available;
the public README omits duplicate panels. All visible artwork is static, with
explicit obsidian backgrounds and ivory text for GitHub theme independence.
External fonts, JavaScript, foreignObject and remote image badges are unnecessary.

LOCAL REBUILD (Python 3.12+; standard library only)
------------------------------------------------
  python scripts/render_profile_ui.py
  python scripts/render_project_cards.py
  python scripts/generate_activity.py --from-cache
  python scripts/validate_profile.py
  git diff --check

--from-cache reads data/contributions.json and preserves its timestamp and
contents. It never contacts GitHub. It does not refresh the contribution data.

DAILY ACTIVITY
--------------
.github/workflows/update-profile-activity.yml fetches contribution data daily.
Its existing schedule, timezone, permissions, secret reference and commit steps
are preserved. The default generator invocation still fetches fresh data.
For a live local refresh, provide GITHUB_TOKEN or GH_TOKEN through the process
environment using your credential manager; never place a token in tracked files,
command history, example commands or screenshots. Do not print the environment.
Windows may need the standard tzdata package for live ZoneInfo date handling;
the existing Linux workflow has the IANA timezone database.

REVIEW / PUBLISH
----------------
  git status --short
  git diff --check
  git diff --stat
  git diff

Review the desktop/mobile previews and the diff before approving publication.
No commit or push is part of this modernization. Do not force-push.
