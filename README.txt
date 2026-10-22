MUBASHEER KC — GITHUB PROFILE V3
================================

README.md presents the developer profile and four projects with source links,
their portfolio case studies, LinkedIn and the professional email address.
Current review: docs/profile-v3-review.md. The earlier profile-audit.md is a
historical record of V2, not the current visual specification.

SOURCE OF TRUTH
---------------
scripts/profile_svg.py             Shared SVG helpers and self-contained assets.
scripts/render_profile_ui.py       Editorial header/footer, section illustrations,
                                  CTAs, profile/focus panels and grouped toolkit.
scripts/render_project_cards.py    Project-owned logos, accents, descriptions,
                                  stacks, features and mobile/desktop cards.
scripts/generate_activity.py       Existing GitHub fetch/statistics/calendar.
assets/projects/logos/SOURCES.md   Attribution for actual project artwork.
assets/toolkit/SOURCES.md          Pinned official technology-icon attribution.

Edit generator source, then regenerate. Do not patch generated SVGs by hand.
The header's data-flow motion runs once for four seconds; reduced-motion mode
disables it. The default static state is complete. No monogram or portrait is
used. Opaque tinted surfaces preserve contrast across GitHub light/dark themes.

LOCAL REBUILD (Python 3.12+; standard library only)
------------------------------------------------
  python scripts/render_profile_ui.py
  python scripts/render_project_cards.py
  python scripts/validate_profile.py
  git diff --check

LOCAL VISUAL REVIEW (optional local QA packages + Chrome)
--------------------------------------------------------
  python scripts/preview_profile.py --compare

The local preview command uses Markdown, PyYAML and Playwright from your Python
environment or the ignored .profile-validation-deps directory. These packages
are not dependencies of the generators or daily workflow. preview_v3*.html/png
and preview_reference*.html/png are ignored local artifacts.

DAILY ACTIVITY — PRESERVED
---------------------------
The existing .github/workflows/update-profile-activity.yml, its schedule,
permissions and authentication are unchanged. The contribution generator,
committed data and responsive SVG are unchanged by V3. No manual workflow run
is required for this design review.

To rebuild the existing calendar from its committed data without network/token:
  python scripts/generate_activity.py --from-cache

The default invocation still fetches fresh GitHub data. If a live local refresh
is needed, supply GITHUB_TOKEN or GH_TOKEN through the process environment using
your credential manager. Never put credentials in tracked files, example
commands, shell history, screenshots or console output.

REVIEW / PUBLISH
----------------
  git status --short
  git diff --check
  git diff --stat
  git diff

No staging, commit or push is part of V3. Review the actual desktop/mobile
previews and wait for owner approval before publishing. Do not rewrite history.
