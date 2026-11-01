# Web font subsets

Latin WOFF2 subsets of the fonts bundled with the engine (`skills/nhipdung/engine/assets/fonts/`), made for the guide so pages download about 215 KB instead of about 1.5 MB of TrueType files. Variable weight axes are kept.

| File | Source | License |
|---|---|---|
| `figtree-latin.woff2` | `figtree/Figtree-Variable.ttf` | SIL OFL 1.1 (`OFL-figtree.txt`) |
| `anton-latin.woff2` | `anton/Anton-Regular.ttf` | SIL OFL 1.1 (`OFL-anton.txt`) |
| `montserrat-latin.woff2` | `montserrat/Montserrat-Variable.ttf` | SIL OFL 1.1 (`OFL-montserrat.txt`) |
| `caveat-latin.woff2` | `caveat/Caveat-Variable.ttf` | SIL OFL 1.1 (`OFL-caveat.txt`) |
| `permanent-marker-latin.woff2` | `permanentmarker/PermanentMarker-Regular.ttf` | Apache License 2.0 (`LICENSE-permanent-marker.txt`) |

These are modified versions (subset and converted); none of the OFL fonts declares a Reserved Font Name, and the Apache-licensed font's change is this subsetting. Regenerate after changing a source font (fonttools 4.60.1):

```sh
uvx --from 'fonttools[woff]==4.60.1' pyftsubset skills/nhipdung/engine/assets/fonts/<dir>/<file>.ttf \
  --unicodes='U+0000-017F,U+0237,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD' \
  --layout-features='*' --flavor=woff2 --output-file=web/src/app/fonts/<name>-latin.woff2
```

Characters outside these ranges fall back to the system font stack in the tokens.

## Vietnamese pages

`/vi` pages load Latin + Vietnamese subsets instead (`fontVariablesFor('vi')` in `../fonts.ts`). They fill the same `--font-*-face` variables, so the tokens are unchanged. Figtree, Caveat, and Permanent Marker draw no Vietnamese letters, so those roles use the engine's extended-coverage fonts (the same `fallback` fonts `text_render.py` switches to); Anton and Montserrat keep their design:

| File | Source | Role | License |
|---|---|---|---|
| `plus-jakarta-sans-latin-vietnamese.woff2` | `plusjakartasans/PlusJakartaSans-Variable.ttf` | Figtree | SIL OFL 1.1 (`OFL-plus-jakarta-sans.txt`) |
| `anton-latin-vietnamese.woff2` | `anton/Anton-Regular.ttf` | Anton | SIL OFL 1.1 (`OFL-anton.txt`) |
| `montserrat-latin-vietnamese.woff2` | `montserrat/Montserrat-Variable.ttf` | Montserrat | SIL OFL 1.1 (`OFL-montserrat.txt`) |
| `sriracha-latin-vietnamese.woff2` | `sriracha/Sriracha-Regular.ttf` | Caveat | SIL OFL 1.1 (`OFL-sriracha.txt`) |
| `sedgwick-ave-display-latin-vietnamese.woff2` | `sedgwickavedisplay/SedgwickAveDisplay-Regular.ttf` | Permanent Marker | SIL OFL 1.1 (`OFL-sedgwick-ave-display.txt`) |
| `plus-jakarta-sans-800-latin-vietnamese.ttf`, `plus-jakarta-sans-600-latin-vietnamese.ttf` | Plus Jakarta Sans at `wght=800` and `wght=600` | Open Graph Figtree | SIL OFL 1.1 |
| `jetbrains-mono-700-latin-vietnamese.ttf` | `engine/project-template/assets/fonts/JetBrainsMono.ttf` at `wght=700` | Open Graph Mono | SIL OFL 1.1 (`OFL-jetbrains-mono.txt`) |

They use the Latin ranges above plus `U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB`, with the same pyftsubset and instancer commands. None of these fonts declares a Reserved Font Name.

The Open Graph renderer (Satori) reads neither WOFF2 nor variable axes, so `[locale]/opengraph-image.tsx` uses static TrueType instances with the same subset, plus the engine's static `Anton-Regular.ttf`:

| File | Source | License |
|---|---|---|
| `figtree-800-latin.ttf`, `figtree-600-latin.ttf` | `figtree/Figtree-Variable.ttf` at `wght=800` and `wght=600` | SIL OFL 1.1 (`OFL-figtree.txt`) |
| `jetbrains-mono-700-latin.ttf` | `engine/project-template/assets/fonts/JetBrainsMono.ttf` at `wght=700` | SIL OFL 1.1 (`OFL-jetbrains-mono.txt`) |

```sh
uvx --from 'fonttools[woff]==4.60.1' fonttools varLib.instancer <source>.ttf wght=<weight> -o /tmp/instance.ttf
uvx --from 'fonttools[woff]==4.60.1' pyftsubset /tmp/instance.ttf --unicodes='<same ranges as above>' \
  --layout-features='*' --output-file=web/src/app/fonts/<name>-<weight>-latin.ttf
```

The README art generator (`scripts/readme-art/`) embeds the WOFF2 subsets above in its SVGs and measures text with the static Figtree instances.
