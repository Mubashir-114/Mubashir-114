# GitHub profile V3 — visual restoration

Local review prepared on 22 October 2026. Starting HEAD:
`d3c553c2e74c192e4fca09d0891228603c201282`. The starting working tree was clean.
No history reset, checkout, staging, commit or push is part of this work.

## Comparison and design decisions

Both reference commits were read with `git show` and rendered locally from their
actual README/assets. No reference commit was checked out over the working tree.

| Area | Visually rich reference `9deb0155de` | Published modernization `d3c553c2e7` | Restored V3 |
| --- | --- | --- | --- |
| Header | Terminal character, diagram and motion; limited mobile layout | Monogram and restrained editorial headline | Developer identity, larger editorial typography, blue/violet atmosphere and connected interface/service/mobile illustration; dedicated mobile composition |
| Project cards | 760 × 264; project-colored rails, descriptions and features | 760 × 156; small 24-pixel logos, sparse repeated surfaces | 960 × 324; green, blue/violet, gold and blue/purple tinted surfaces; 120-pixel logos, features and clear scope labels |
| Mobile cards | 360 × 278, some very small metadata | 360 × 204, compressed presentation | 360 × 350; 62-pixel logos, 27-pixel titles, 17-pixel descriptions, explicit stack wrapping and compact feature chips |
| Sections | Illustrated/numbered interface rails | Plain Markdown headings | Refined rails with numbered labels and meaningful section symbols; six separate mobile rail layouts |
| Toolkit | Grouped capability rows | Compressed eight-icon strip | Seven readable groups with actual project-relevant technology icons, including Next.js and TypeScript |
| Accuracy | Historical links and broad AI/payment claims | Correct canonical links and implementation boundaries | The same verified facts and limitations, with case studies promoted before source links |
| Motion | Repeated decorative animation | Entirely static | Four-second, one-cycle data-flow animation in the header; static base and reduced-motion override |

The desktop card aspect ratio restores approximately the original rendered
height when constrained to the same GitHub content width. Source SVG dimensions
are not fixed CSS pixel heights in the README: images scale with available width.
All cards remain individually clickable. Source repositories, the FinTrack
backend and all four case studies remain separate native Markdown links.

## Identity and portrait

- The developer is **Mubasheer KC — Full-Stack Developer & Flutter Engineer**.
- “Thoughtful interfaces. Connected experiences.” is preserved.
- The profile no longer displays a monogram in the header, footer, CTAs, section
  artwork or any generated asset. The unused monogram source/attribution files
  introduced by the previous modernization have been removed.
- The professional email address is unchanged; its account spelling is contact
  information, not decorative branding.
- `Neon Rim-Lit Creator Portrait(1).png` was not found in the profile workspace
  or accessible attachment files. **No portrait was used or substituted.** The
  header uses the existing connected-systems motif without duplicating the
  GitHub avatar or introducing a generated face.

## Authentic logo restoration

| Project | Result | Source |
| --- | --- | --- |
| FinTrack 2.0 | **Green logo restored.** Official obsidian-jade wallet/growth mark, optimized proportionally to 192 pixels and used with green accents. | [`assets/branding/logo_obsidian_jade.png`](https://github.com/Mubashir-114/fintrack_app/blob/main/assets/branding/logo_obsidian_jade.png), source blob `3da4d72ab746a9aaff97cdec1d973216bffabdc6`. The repository's `FinTrackLogo` component explicitly uses theme-specific official artwork. |
| kodehax academy | **Blue-violet logo restored.** Original colored circuit/shield mark, optimized proportionally to 189 × 192 pixels. | [`static/image/image.png`](https://github.com/Mubashir-114/kodehax_academy/blob/main/static/image/image.png), source blob `4e792a4cac2e0d7c23152e741c71e6c69d6cb8ea`. The monochrome `logo2.png` and `admin_favicon.png` candidates were inspected and rejected for this requested color treatment. |
| Provia | Existing gold/yellow project artwork preserved and enlarged. | Existing attributed local `provia.png`. |
| Nexo | Existing blue-purple vector artwork preserved and enlarged. | Existing attributed local `nexo.svg`. |

No logos were invented or recolored. Legacy local FinTrack/kodehax files remain
available, with attribution distinguishing them from the active card assets.

## Content and profile journey

1. Editorial introduction and **Visit My Portfolio ↗** CTA.
2. About/professional profile, followed by an illustrated approach panel.
3. Four branded projects with descriptions, stacks, features and native links.
4. Current-focus panel, including FinTrack 2.0 and connected finance workflows.
5. Technology groups: languages, frontend, backend, mobile, databases,
   systems/APIs and developer workflow. No proficiency scores or rankings.
6. Existing responsive contribution visualization.
7. Contact links and an understated developer-name footer.

FinTrack retains its implemented-versus-active-development distinction and planned
live currency conversion. Its stack remains Flutter, Dart, Node.js, Express and
MySQL. FIN is identified as deterministic. kodehax keeps the Groq configuration
requirement and roadmap boundary. Provia's checkout is explicitly simulated.
Nexo is explicitly a frontend demonstration with mocked responses/retrieval and
no connected live model. No achievement, adoption or performance metrics were added.

## Updated sources and assets

- `README.md`: restored visual journey, rail markup and case-study-first links.
- `README.txt`: current maintenance and review commands.
- `scripts/render_project_cards.py`: source of truth for larger project cards,
  authentic logo selection, accents, feature highlights and responsive typography.
- `scripts/render_profile_ui.py`: redesigned header/footer, CTAs, approach/focus
  panels, six section rails and grouped technology toolkit.
- `scripts/profile_svg.py`: shared self-contained tinted-surface/image helpers.
  Existing activity rendering helpers retain their behavior.
- `scripts/validate_profile.py`: focused local-reference/XML/reproducibility
  checks and finite-motion/visible-branding checks.
- `scripts/preview_profile.py`: repeatable local browser previews, optional
  reference-commit comparison, font-metric checks and motion checks. Its optional
  local QA packages do not become runtime or workflow dependencies.
- `assets/projects/logos/{fintrack-jade,kodehax-color}.png`: optimized authentic
  artwork; updated adjacent source attribution.
- Three additional, pinned Devicon v2.17.0 source SVGs: Next.js, TypeScript and
  GitHub Actions; updated toolkit attribution.
- **33 generated SVGs rebuilt:** two headers, two footers, three CTAs, eight
  project cards, twelve desktop/mobile section rails and six approach/focus/toolkit
  panels. Existing activity artwork is unchanged.
- `docs/profile-audit.md` is retained as the historical V2 report and points here.

## Local previews

The following are ignored local review files in `D:\\Github\\Mubashir-114`:

| Condition | File |
| --- | --- |
| Desktop dark, 1280-pixel viewport | `preview_v3_1280_dark.png` |
| Desktop light, 1280-pixel viewport | `preview_v3_1280_light.png` |
| Mobile dark, 390-pixel viewport | `preview_v3_390_dark.png` |
| Mobile light, 390-pixel viewport | `preview_v3_390_light.png` |
| Narrow mobile dark, 320-pixel viewport | `preview_v3_320_dark.png` |
| Local interactive README preview | `preview_v3.html` |
| Original visually rich reference | `preview_reference_9deb0155de.png` |
| Published modernization reference | `preview_reference_d3c553c2e7.png` |

Component detail previews begin with `preview_v3_detail_`. All previews use the
actual generated README assets. Historical previews embed the assets read from
their respective Git objects; they are not promotional mockups.

Reproduce locally:

```text
python scripts/render_profile_ui.py
python scripts/render_project_cards.py
python scripts/validate_profile.py
python scripts/preview_profile.py --compare
git diff --check
```

The preview command needs the optional local Markdown, PyYAML and Playwright
packages and local Chrome. They are already available in the ignored validation
directory for this review. Production generators use the Python standard library.

## Focused validation and automation safety

- SVG XML, 47 unique local/external README references, anchors, canonical links
  and alternative text pass structural checks. Regeneration is byte-for-byte stable.
- Actual project-logo candidates were visually inspected against repository
  artwork. Correct green and blue-violet palettes are used without substitution.
- All five desktop/mobile/theme conditions render without broken images or
  horizontal overflow. Browser text measurements find no clipping or overlapping
  SVG text in either desktop or mobile layouts.
- Normal-motion header animation is exactly four seconds and one iteration.
  Reduced-motion mode disables it. Content is visible with animation disabled;
  no initial hidden text/cells or SMIL animation is introduced.
- The contribution workflow, generator, chart and data have **no diff**. Existing
  schedule, timezone, permissions, authentication and staging paths are preserved.
- The five latest inspected scheduled runs succeeded; latest inspected run:
  [39682224689](https://github.com/Mubashir-114/Mubashir-114/actions/runs/39682224689),
  started 21 October 2026 at 21:52 UTC. No new workflow was triggered.
- HEAD remains the original `d3c553c2e74c192e4fca09d0891228603c201282`.
  Nothing has been staged, committed or pushed. No portfolio files were modified.
- Final working tree: 36 modified files, two deleted unused monogram files and
  13 new files; zero staged changes. Previews and local QA packages are ignored.

## Remaining limitations

- These local previews approximate GitHub Markdown styling. GitHub sanitization,
  Camo image caching, system font fallback and available profile width may change
  final presentation slightly. Publishing remains pending approval.
- SVG layout does not reflow like HTML. Desktop/mobile variants supply explicit
  layouts; essential scope remains native Markdown and image alternative text.
- CSS animation may be suppressed by a renderer. The static appearance remains
  complete and readable; no feature depends on animation support.
- The supplied portrait remains unavailable. No replacement face was generated.
- LinkedIn may reject automated clients (HTTP 999); its verified contact URL is
  retained. No message/email or LinkedIn action was sent.
- Contribution information retains the existing workflow snapshot rather than
  inventing a fresh count or implying a live update.
