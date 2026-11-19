---
name: Arcane Gridiron
colors:
  surface: '#111317'
  surface-dim: '#111317'
  surface-bright: '#37393e'
  surface-container-lowest: '#0c0e12'
  surface-container-low: '#1a1c20'
  surface-container: '#1e2024'
  surface-container-high: '#282a2e'
  surface-container-highest: '#333539'
  on-surface: '#e2e2e8'
  on-surface-variant: '#d4c4b0'
  inverse-surface: '#e2e2e8'
  inverse-on-surface: '#2f3035'
  outline: '#9d8f7c'
  outline-variant: '#504535'
  surface-tint: '#fabc4d'
  primary: '#ffc665'
  on-primary: '#432c00'
  primary-container: '#e5a93c'
  on-primary-container: '#5e4000'
  inverse-primary: '#7e5700'
  secondary: '#ffb3af'
  on-secondary: '#68000d'
  secondary-container: '#a4001b'
  on-secondary-container: '#ffaea9'
  tertiary: '#10e7d2'
  on-tertiary: '#003731'
  tertiary-container: '#00c9b6'
  on-tertiary-container: '#004f47'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdead'
  primary-fixed-dim: '#fabc4d'
  on-primary-fixed: '#281900'
  on-primary-fixed-variant: '#604100'
  secondary-fixed: '#ffdad7'
  secondary-fixed-dim: '#ffb3af'
  on-secondary-fixed: '#410005'
  on-secondary-fixed-variant: '#930017'
  tertiary-fixed: '#41fce6'
  tertiary-fixed-dim: '#00deca'
  on-tertiary-fixed: '#00201c'
  on-tertiary-fixed-variant: '#005048'
  background: '#111317'
  on-background: '#e2e2e8'
  surface-variant: '#333539'
typography:
  headline-xl:
    fontFamily: Cinzel
    fontSize: 38px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: 0.08em
  headline-xl-mobile:
    fontFamily: Cinzel
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: 0.06em
  headline-lg:
    fontFamily: Cinzel
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
    letterSpacing: 0.05em
  headline-lg-mobile:
    fontFamily: Cinzel
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: 0.04em
  headline-md:
    fontFamily: Cinzel
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0.04em
  body-lg:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.06em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 9px
    fontWeight: '500'
    lineHeight: 12px
    letterSpacing: 0.08em
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1.25rem
  space-xl: 2rem
---

## Brand & Style

This design system blends **Tactile Dark Fantasy** with **High-Density Strategy Telemetry**. It bridges the visceral atmosphere of classic dungeon crawlers and table-top strategy with the surgical clarity required for AI pathfinding analytics, heuristics inspection, and engine performance metrics.

The visual style is characterized by:
- **Chiseled Structuralism:** Micro-chamfered containers, layered metallic bevels, and segmented diagnostic monitors reminiscent of enchanted stone slates and brass telemetry apparatus.
- **High-Contrast Luminescence:** Jewel-toned emitters against abyssal, noise-textured charcoals. Hero intelligence glows with gilded amber, adversary behaviors bleed ominous crimson, and algorithmic logic tracks with cold, luminous cyan.
- **Precision Information Density:** Uncluttered monospaced readouts, vector-crisp node graphs, and strict metric alignments that keep cognitive load manageable during real-time 60fps Pygame simulation loops.

## Colors

The palette employs deep obsidian and charcoal foundations punctuated by triad functional accents to differentiate competitive agents and algorithm states:

- **Neutral Foundations (`#0F1115` base):** Deep slate-charcoal scale ranging from void obsidian (`#08090B`) for simulation backgrounds, `#0F1115` for viewports, up to `#1C2027` and `#2A303C` for metallic structural panels and card plates.
- **Primary / Valor Gold (`#E5A93C`):** Denotes Hero AI state, gold reserve trackers, algorithmic heuristic wins, priority node expansions, and primary actions.
- **Secondary / Abyssal Crimson (`#D12D35`):** Denotes Monster AI aggression vectors, threat zones, hostile health pools, critical warnings, and lethal collisions.
- **Tertiary / Arcane Cyan (`#00E5D0`):** Reserved for algorithmic telemetry, BFS/A* open-closed list frontier paths, debug vectors, frame-time graphs, and sensory raycasts.
- **Surface Borders & Metallic Trim:** Burnished bronze (`#5A4D3B`) and cold steel (`#38414E`) used for metallic hairline divides.
- **Text & Contrast:** High-contrast warm chalk white (`#EDECE8`) for headlines and active values; muted ash (`#8E95A5`) for auxiliary keys and metadata.

## Typography

The typographic hierarchy employs three specialized typefaces to balance thematic atmosphere with data-heavy engineering:

1. **Cinzel (Display & Structural Titles):** Classical, engraved proportions that anchor the dark fantasy setting. Used exclusively in uppercase/small-caps for main view headings, victory banners, and primary container tabs.
2. **Space Grotesk (Interface Prose & Descriptions):** Clean, geometric grotesque with idiosyncratic structural details. Delivers high legibility for AI status descriptions, rule-set logs, and configuration tooltips.
3. **JetBrains Mono (Telemetry & Computational Readouts):** Rigid monospaced alignment for coordinates `(X, Y)`, cost weights `f(n) = g(n) + h(n)`, tick counters, path lengths, memory footprints, and frame rate diagnostics.

## Layout & Spacing

The layout is built around a dense, telemetry-focused fixed-viewport grid optimized for desktop game screens and responsive developer tools (target canvas: 1920x1080 and 1440x900 native display viewports).

- **Screen Distribution:**
  - **Left Rail (320px - 380px):** Hero AI Controller, heuristic tuners, inventory stats, state machine inspector.
  - **Center Arena (Fluid flex):** Primary Pygame graphical viewport featuring the tile dungeon, agent avatars, and overlaid BFS/A* frontier paths.
  - **Right Rail (320px - 380px):** Monster AI sensory range, threat calculation tree, behavior tree state, global event log.
  - **Bottom Dock (180px - 220px collapsible):** Time controls (Tick, Pause, 1x-10x Speed), real-time path computation charts, memory/GPU profiler.
- **Rhythm & Padding:** Strict 4px base increment. Data tables and stat matrices use `space-xs` and `space-sm` for compact utility, while macro panels utilize `space-lg` and `space-xl` for boundary definition.
- **Reflow Rules:** On narrower viewport displays (under 1200px), side rails dock into dual-tabbed slide-out slates to preserve full unscaled pixel clarity for the central dungeon arena.

## Elevation & Depth

Visual hierarchy is maintained through **Layered Metallic Plates**, **Chiseled Insets**, and **Chromatic Luminescence**:

- **Ground Plane (Level 0):** Hex `#08090B`, textured with subtle slate noise. Holds the primary simulation arena.
- **Sub-Panels & Data Wells (Inset Level):** Hex `#0B0D11` with a `1px` inner bevel (`inset 0 1px 2px rgba(0,0,0,0.8), inset 0 0 0 1px #1C2027`). Used for pathfinding telemetry logs and raw stat readouts.
- **Standard Surface Panels (Level 1):** Hex `#14171E` backed by dual hairline borders: an outer `1px` border of burnished iron (`#2A303C`) and a `1px` top edge highlight of cold steel (`#40495A`) simulating overhead light.
- **Floating Modals & Inspection Popovers (Level 2):** Hex `#1A1E27` framed with double brass/gold rules (`#5A4D3B`), supported by a heavy ambient drop shadow (`0 12px 32px rgba(0,0,0,0.75)`).
- **Glow & Energy Radiance:** Elements never cast generic white blurs. Hero critical states emit an ambient amber bloom (`rgba(229, 169, 60, 0.25)`), monster aggression triggers a crimson pulse (`rgba(209, 45, 53, 0.3)`), and path solutions produce an intense cyan rim-light (`rgba(0, 229, 208, 0.4)`).

## Shapes

The design system adopts a **Sharp Geometric Architecture (Level 0)** to reinforce the harsh, stone-and-metal brutalism of dungeon environments and military-grade AI control stations:

- **0px Corner Radii:** All panels, buttons, chips, and stat bars maintain razor-sharp right angles.
- **Chamfered Accents:** Core dialogue headers, hero meters, and primary action buttons feature 45-degree corner cutoffs (4px to 6px chamfers created via CSS polygon clips or custom Pygame polygon draws) evoking chiseled granite tablets.
- **Segmented Separators:** Grid dividers and divider lines use 1px broken-line hashes or etched grooves to convey precision instruments.

## Components

### Buttons & Interaction Controls
- **Hero / Action Prime:** `#16140F` background, framed in a solid `1px` border of `#E5A93C`, Cinzel font in gold with `0.06em` letter tracking. On hover: shifts to solid `#E5A93C` fill with `#08090B` ink and an 8px gold radial bloom.
- **Monster / Danger Trigger:** `#180D0E` background, `#D12D35` border, crimson label. Hover fills `#D12D35` with chalk-white text.
- **Diagnostics / Utility Buttons:** Monospaced, enclosed in cold steel `#38414E` outlines, turning neon `#00E5D0` on hover or active execution.

### Telemetry Chips & State Indicators
- Compact, flat capsules with 0px radius.
- Composed of a 6px status LED square (solid green for Idle, pulsing crimson for Target Acquired, flashing cyan for Path Recalculating) followed by an uppercase monospaced descriptor (`HERO_PATH: COST=42`).

### Agent Status Cards & Gauges
- **Hero Card:** Framed with metallic gold corner braces. Features dual segmented health/mana bars rendered in stepped blocks (not smooth gradients) to reflect discrete game ticks.
- **Monster Card:** Framed with jagged iron and dark ruby accent notches. Integrates an aggression heat index and field-of-view threat telemetry.

### Input Fields & Simulation Sliders
- **Numeric Tuners (Weights, Speed, Heuristic Epsilon):** Inset obsidian wells (`#090B0E`) flanked by `[-]` and `[+]` stepped increment buttons. Active values render in `#00E5D0`.
- **Sliders:** 2px cold-steel rail with a diamond-shaped or sharp rectangular metallic slider thumb (`#E5A93C` for agent settings, `#00E5D0` for algorithm weights).

### Checkboxes & Segmented Toggles
- Square-edged toggles with high-contrast inner glyphs.
- Checked state fills with `#14292B` (cyan tint) and an interior crisp cyan tick icon.
- Toggles switch with zero motion blur; state changes are crisp and immediate (100ms snap) matching frame synchronization needs.

### Domain-Specific Components
- **Frontier Path Grid Inspector:** Monospaced visual node ledger mapping Cartesian coordinates `(x, y)` to status (Open, Closed, Obstructed, Target) color-coded in cyan, gold, and crimson.
- **Tick Engine Controller:** Transport control deck (Rewind, Step Back, Play/Pause, Step Forward, Fast-Forward) built with heavy metallic relief buttons and a centered gold tick counter (`TICK: 004812`).