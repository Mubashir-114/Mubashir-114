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

assets/projects/*.svg
  Generated, responsive project cards with project-owned logos and accents.

assets/projects/logos/*
  Optimized local copies of logo artwork sourced from each featured repository.
  See assets/projects/logos/SOURCES.md for exact paths.

assets/ui/*.svg
  Generated section rails and responsive profile, focus, and toolkit panels.

assets/toolkit/icons/*.svg
  Local Devicon v2.17.0 technology icons. See the adjacent SOURCES.md.

assets/activity/activity.svg
  Generated activity visualization. Do not hand-edit it.

assets/cta/*.svg
  Compact hero call-to-action cards used immediately under the header.

data/contributions.json
  Public contribution data used by the renderer. Do not hand-edit it.

scripts/generate_activity.py
  Fetches GitHub GraphQL contribution calendar data and renders
  assets/activity/activity.svg plus data/contributions.json.

scripts/render_project_cards.py
  Generates the four project-card SVGs. Edit project content in this script,
  then rerun it rather than hand-editing the generated card files.

scripts/render_profile_ui.py
  Generates the section rails plus the profile, focus, and toolkit panels.

.github/workflows/update-activity.yml
  Refreshes the contribution data and SVG once a day and can also be run
  manually from GitHub Actions.

LOCAL REFRESH
-------------

Refresh activity through GitHub Actions, or locally with a token:

  $env:GH_PROFILE_USER = "Mubashir-114"
  $env:GITHUB_TOKEN = "<token with public GraphQL access>"
  python scripts/generate_activity.py
  python scripts/render_project_cards.py
  python scripts/render_profile_ui.py

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
