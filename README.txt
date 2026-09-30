MUBASHIR-114 PROFILE MAINTENANCE
================================

This repository powers https://github.com/Mubashir-114.

PROFILE STRUCTURE
-----------------

README.md
  The public profile content. Keep claims grounded in public work and keep the
  selected-project list short.

assets/header.svg
  Responsive hero artwork. Uses SVG/CSS animation only and includes a reduced
  motion fallback.

assets/footer.svg
  Small closing visual used at the end of the profile.

contrib-heatmap.svg
  Generated activity visualization. Do not hand-edit it.

data/contributions.json
  Public contribution data used by the renderer. Do not hand-edit it.

scripts/fetch_contributions.py
  Fetches public contribution data directly from GitHub.

scripts/render_heatmap_svg.py
  Renders data/contributions.json into contrib-heatmap.svg.

.github/workflows/update-profile-art.yml
  Refreshes the contribution data and SVG once a day and can also be run
  manually from GitHub Actions.

LOCAL REFRESH
-------------

Install the lightweight workflow dependencies:

  python -m pip install -r scripts/requirements.txt

Refresh and render:

  $env:GH_PROFILE_USER = "Mubashir-114"
  python scripts/fetch_contributions.py
  python scripts/render_heatmap_svg.py

PUBLISHING
----------

Review changes before publishing:

  git status --short
  git diff --check
  git diff

Then commit and push normally. Do not force-push this profile repository.

GITHUB ACTIONS
--------------

The workflow declares contents: write, which is required to commit refreshed
activity data. In repository settings, Actions workflow permissions must allow
read and write access. The workflow can then be triggered manually once from
the Actions tab; the daily schedule handles later updates.
