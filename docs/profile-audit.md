# MKL GitHub profile modernization

Reviewed and implemented locally on 22 October 2026 (Asia/Kolkata).

## Existing flaws

- The introduction, “current signal” panel and “now” panel repeated the same
  capabilities before visitors reached the work. Six image-based section rails
  and a large toolkit added considerable vertical space.
- The header used a terminal aesthetic and “MUBASHIR” instead of the portfolio's
  official MKL identity, “Mubasheer KC” name and editorial presentation. It had
  no dedicated mobile layout.
- Neither hero action opened the portfolio. FinTrack linked to the historical
  `budgetbee-app` repository name and omitted the current 2.0 identity/backend.
- Project cards were 760 × 264 on desktop and 360 × 278 on mobile. Metadata,
  capability chips and repeating “view repository” treatments competed with the
  actual project descriptions. Mobile toolkit labels reached 7.5–8.5 SVG pixels.
- The section-rail mobile CSS enlarged text within a fixed desktop coordinate
  layout, creating an overlap risk instead of a reflowing mobile section.
- CTA light-mode rules darkened text while leaving dark gradient backgrounds in
  place. Saturated accents and glowing details competed with the content.
- SMIL pulses, moving lines, cursors and sweeping accents added unnecessary
  motion. Hiding SMIL elements through CSS was an unreliable reduced-motion
  strategy. Contribution cells started at opacity zero and depended on CSS
  animation to become visible.
- Provia's scope did not distinguish simulated checkout from live payments.
  Nexo's description did not distinguish mock responses/retrieval from a live AI
  service. Broad “production-oriented” wording lacked these useful boundaries.
- The activity caption called the data public, while the generator correctly
  identifies it as contribution data available to the workflow token. The local
  activity snapshot was behind the already successful daily automation.

## Changes and preserved work

- Updated the existing profile journey: MKL introduction → portfolio CTA → short
  professional summary → four selected projects → current focus/toolkit →
  contribution activity → contact footer.
- Introduced the official vector monogram, obsidian `#0a0a0a`, warm ivory
  `#fcfaf5`, Georgia editorial headings and restrained cyan/violet accents.
  System fonts replace remote font dependencies in SVG images.
- Kept the original UI → API → DATA diagram motif as static header artwork.
  Preserved the project-owned logos, legacy FinTrack icon, local technology
  icons and attribution files. Added the current official graphite/champagne
  FinTrack mark as a separate optimized 96-pixel asset.
- Reduced project cards to 760 × 156 desktop and 360 × 204 mobile. Essential
  scope and limitations are selectable native Markdown, outside the images.
- Removed duplicate panels from the public README. Their generators and the
  optional panels/section rails/secondary CTAs remain available and have been
  brought into the same visual language.
- Added dedicated mobile header/footer layouts and a compact eight-icon toolkit.
  Replaced external badge requests with native contact links.
- Made artwork static. Explicit opaque backgrounds keep ivory text readable
  regardless of GitHub/OS theme combinations. All public images have useful alt
  text; generated SVGs have titles/descriptions. SVGs have no scripts,
  foreignObject, SMIL animation, or remote image/font dependencies.
- Preserved the contribution-fetching logic, date handling and data schema.
  Added `--from-cache` for token-free, deterministic local rendering. The single
  `activity.svg` contains a desktop annual calendar and a mobile six-month bar
  summary using real monthly totals. No extra workflow output needs staging.

## Verified project scope

| Project | Canonical source and evidence | Profile wording |
| --- | --- | --- |
| FinTrack 2.0 | [Flutter app](https://github.com/Mubashir-114/fintrack_app), [backend](https://github.com/Mubashir-114/fintrack_backend); app README implementation table, `lib/providers/budget_provider.dart`, `lib/repositories/analytics_repository.dart`, backend README | Accounts, transactions, budgets, reports, SMS review and deterministic FIN are implemented. Product remains in active development. Live currency conversion is planned. |
| kodehax academy | [Repository](https://github.com/Mubashir-114/kodehax_academy); README roadmap, `teacher/models.py`, `daily_challenges/views.py`, `chat/ai_service.py` | Learning/role workflows, challenges, assessments and Groq integration are implemented. AI requires configured service access. Further analytics/mobile coverage remain on the roadmap. |
| Provia | [Repository](https://github.com/Mubashir-114/Provia); `chat/consumers.py`, `payments/services.py`, `payments/views.py` | Booking and WebSocket chat are implemented; active development. Checkout renders `mock_payment.html`; `mock_success`/`mock_failure` explicitly simulate outcomes. No claim of live payment processing. |
| Nexo | [Frontend](https://github.com/Mubashir-114/Nexo-frontend); `src/store/useConversationStore.js` imports `generateMockResponse` and `mockRetrieve` | Frontend demonstration with domain-specific Zustand stores; responses and retrieval are mocked, with no live model connected. |

Identity, role, contact details, colors and typography were cross-checked against
the [live portfolio](https://mubashir-portfolio-orpin.vercel.app) and its read-only
`src/config/site.ts`, `src/config/projects.ts`, layout and stylesheet sources.
No portfolio code or other repository was changed. “Implemented” describes
repository functionality, not production readiness or an independently executed
end-to-end certification. No achievement, usage or performance metrics were added.

## Source of truth and rebuilt assets

- `scripts/profile_svg.py`: shared SVG helpers, palette and typography.
- `scripts/render_profile_ui.py`: header/footer (desktop and mobile), three CTAs,
  six optional section rails and six optional/profile/focus/toolkit panels.
- `scripts/render_project_cards.py`: four project records and eight SVG cards.
- `scripts/generate_activity.py`: existing fetch/data processing and rebuilt
  responsive calendar SVG.
- Total: **28 generated SVG outputs**. `assets/brand/mkl-monogram.svg` is an
  attributed source asset; `assets/projects/logos/fintrack-2.png` is an optimized
  copy of project-owned artwork. Existing logos and technology icons are retained.

Commands:

```text
python scripts/render_profile_ui.py
python scripts/render_project_cards.py
python scripts/generate_activity.py --from-cache
python scripts/validate_profile.py
git diff --check
```

## Workflow health

The latest five returned scheduled runs all completed successfully:

| Run | Started (UTC) | Result |
| --- | --- | --- |
| [39682224689](https://github.com/Mubashir-114/Mubashir-114/actions/runs/39682224689) | 2026-10-21 21:52 | Success |
| [39503087337](https://github.com/Mubashir-114/Mubashir-114/actions/runs/39503087337) | 2026-10-20 21:46 | Success |
| [39335651508](https://github.com/Mubashir-114/Mubashir-114/actions/runs/39335651508) | 2026-10-19 22:32 | Success |
| [39165583480](https://github.com/Mubashir-114/Mubashir-114/actions/runs/39165583480) | 2026-10-18 20:56 | Success |
| [39068226027](https://github.com/Mubashir-114/Mubashir-114/actions/runs/39068226027) | 2026-10-17 20:47 | Success |

The workflow file is unchanged. YAML parsing passed, including its existing
`0 0 * * *` schedule, `Asia/Kolkata` timezone, `contents: write`, concurrency,
Python setup and `${{ secrets.GITHUB_TOKEN }}` reference. No workflow was triggered,
no token was requested for local rendering and no token was added to any file.

The checkout was 19 automatic activity commits behind upstream. Its local branch
was advanced to those existing commits without creating a commit or changing
working files. The current contribution JSON is exactly the upstream snapshot
generated at `2026-10-21T21:52:32Z`; it was not fabricated or locally re-fetched.
The rebuilt artwork uses its range ending 21 October 2026.

## Validation

- All Markdown/HTML local references and anchors resolve; canonical repository
  links are used. The offline validator checked 31 unique references.
- All SVGs parse as XML. Generated SVG titles, unique IDs, safe elements and
  self-contained image references pass. Vendor icon files retain their original
  metadata and get accessible labels from the containing toolkit image.
- All three generators execute. Repeated rendering is byte-for-byte stable and
  leaves the contribution JSON and workflow unchanged. Contribution totals and
  active-day counts agree with the recorded daily data.
- The unchanged default activity command was exercised with a recorded GraphQL
  fixture in a temporary directory; data and SVG outputs passed. Missing-token
  behavior fails before network access. This was an offline pipeline check,
  not a new live Actions run.
- Local Chrome renders passed at 960 pixels in light/dark mode, 375 pixels in
  light/dark mode, and 320 pixels in dark mode. All images loaded; no horizontal
  overflow occurred. Browser text measurements found no clipped/overlapping SVG
  text in either desktop or mobile layouts. Reduced motion was enabled in these
  previews; the generated assets contain no animations in either preference.
- The portfolio homepage, all four case-study routes, all five featured source
  repositories, contribution overview and workflow page returned HTTP 200.
  FinTrack's case study passed on retry after a transient connection reset.
- LinkedIn returns HTTP 999 to automated clients. Its address matches the
  portfolio's owner-verified contact configuration; account reachability cannot
  be independently confirmed by this automated check. The email destination also
  matches that configuration; no email was sent.
- `git diff --check` passes. No new runtime or workflow dependencies were added.
  Markdown, PyYAML and Playwright were used only in ignored local validation
  tooling. Preview HTML/PNGs are ignored local review artifacts.

## Remaining limitations and review state

- Local previews approximate GitHub Markdown styling; final GitHub sanitization,
  image proxy caching and font fallback can differ. A published GitHub render
  cannot be verified before the approved commit/push.
- SVG text cannot reflow like native HTML. Dedicated mobile layouts and a
  responsive monthly activity summary address this; readable native project
  descriptions and a GitHub contribution-history link remain available.
- GitHub controls native Markdown typography. The editorial font treatment is
  confined to self-hosted artwork; Georgia substitutes for the portfolio's
  downloaded EB Garamond.
- Daily Actions scheduling may be delayed by GitHub. The date shown identifies
  the actual snapshot rather than implying real-time contribution data.
- This work inspects project source and documentation; it does not run those
  projects' deployments, payment systems or external AI services.

All modernization changes are local and unstaged. No new commit, push, pull
request, workflow run or portfolio deployment was created. Run `git status
--short` for the full file list before approval.
