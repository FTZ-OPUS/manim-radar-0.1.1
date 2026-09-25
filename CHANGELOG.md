# Changelog

All notable changes to `manim-radar` are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] — 2026-09-25

### Added

- **Multi-dataset comparison on one chart** — pass `datasets=[dA, dB]` (or
  call `chart.compare(dA, dB)`); several polygons share one grid, morph
  together (`chart.morph_to([dA2, dB2])`, optional `stagger=`) and read from
  one shared full scale.
- **Legend + four number modes** for comparisons, chosen with
  `compare_numbers=`: `"legend"` (default — cleanest), `"all"` (per-vertex
  values in each dataset's colour), `"first"`, `"focus"` (numbers follow
  `chart.focus(i)`). `chart.focus(i)` / `chart.unfocus()` dim the other
  datasets as well.
- **`OverflowRadarChart`** (越界雷达图) — values above the full scale stab
  beyond the outer ring: dashed spoke extensions, a glowing "breach" where a
  spike pierces the ring, true (unclamped) read-outs riding the spikes, a
  `transition="burst"` morph and a `chart.burst_in()` entrance with overshoot.
  Works with comparison mode too — every dataset gets its own spikes, tracks,
  breaches and read-outs.
- **Camera helpers** — `chart.push_in()` / `chart.pull_out()` for plain
  scenes, plus a true-camera `CameraRig` for `MovingCameraScene`
  (`push_in` / `pull_out` / `focus_point` / `micro_push`). Attach a rig via
  `chart.attach_camera(rig)` and burst morphs auto-push towards the spike.
- **`chart.highlight_gap(a, b)`** — tints the crescent-shaped difference
  region between two datasets (each lobe in the winning dataset's colour),
  optionally live-following later morphs.
- `RadarReel` accepts comparison snapshots (a *list* of `RadarData` per step).

### Fixed

- `RadarReel` now morphs to the `emphasis="gap"` snapshot's data right after
  the glitch re-entrance (0.1.0 re-revealed the stale previous state).
- `CameraRig.pull_out()` scaled the frame in the wrong direction (it zoomed
  *in*) and did not recentre; it now restores the default full frame.
- `RadarChart.get_center()` returns the grid centre, so camera moves aimed at
  a chart no longer drift towards lopsided bounding boxes.
- `chart.push_in()` no longer crashes (`run_time` goes through
  `builder.set_run_time`, not `scale()`).
- Burst morphs dip to 20% of the target so the stab actually overshoots;
  a small dead-zone (`overflow_min_over`) keeps transient overshoots from
  popping spurious overflow read-outs.

## [0.1.0] — 2026-09-21

First release.

### Added

- `RadarChart` — an animated radar/spider chart as a real Manim `VGroup`
  (supports `shift` / `move_to` / `scale` / `rotate` / `FadeIn` / `FadeOut`).
- `RadarData` — immutable snapshot model with axes, values, name, colour,
  full scale, emphasis, hold and per-snapshot transition overrides.
- `RadarChart.morph_to(...)` — one command tweens values, full scale, colour,
  emphasis outline, opacity and nameplate in a single pass.
- Six transition presets: `smooth`, `dip`, `shockwave`, `zoom`, `glitch`, `stepped`.
- `RadarReel` — plays a whole list of snapshots (with black gaps) in one call.
- `RadarReveal`, `RadarFade`, `GlitchFlash` and `Shockwave` animations.
- `RollingNumber` — odometer-style value read-out with overflow labels (`10+`).
- `DeepSpace` — radial glow + corner vignette + nebula blobs + drifting stars,
  tinted by the chart colour.
- Three style presets (`neo`, `classic`, `minimal`) and five themes
  (`midnight`, `aurora`, `ember`, `violet`, `paper`).
- `RadarConfig` (~60 fields) and `RadarTheme` for full customisation.
- Legacy generations rebuilt on the library: `RadarV1Scene` (1.0) and
  `RadarV2Scene` (2.0), playing the bundled 23-snapshot demo reel.
- Cross-platform font fallback (`PingFang SC` → `Microsoft YaHei` → `Noto Sans CJK` …).
- `manim-radar` CLI: `themes`, `styles`, `template`, `demo --render`.
- Manim plugin entry point (`manim.plugins`) and example scenes under `examples/`.
- Test suite (41 tests) that runs without rendering.

[Unreleased]: https://github.com/FTZ-OPUS/manim-radar/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/FTZ-OPUS/manim-radar/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/FTZ-OPUS/manim-radar/releases/tag/v0.1.0
