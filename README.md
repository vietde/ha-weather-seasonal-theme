# Weather Season

A Home Assistant theme whose background follows the weather, the season,
and day/night — built for the Homeview dashboard.

- The sky follows `weather.forecast_home`, the season (from the month) and
  day/night (`sun.sun`): sunny skies differ by season, plus cloudy, rain,
  storm, snow, fog and clear-night skies, darkened after sunset.
- Animated particles fall over the screen: snow, autumn leaves, spring
  petals, rain streaks, twinkling stars, drifting clouds, fog.
- A scene band sits along the bottom: a snow bank in snow/winter, water
  in rain, a leaf pile in autumn. Thunderstorms add a soft lightning flash.
- Cards go glassy (translucent + blur) so the sky shows through.

Pure CSS — no image downloads, nothing to host.

## Requirements

- [card-mod](https://github.com/thomasloven/lovelace-card-mod) (the theme uses
  a `card-mod-view` template to paint the background).
- Your `configuration.yaml` needs the standard themes line (Home Assistant
  adds it when it creates the file):
  ```yaml
  frontend:
    themes: !include_dir_merge_named themes
  ```

## Install

Add this repository as a custom repository in HACS / the Marketplace with
category **theme**, then download it. The Marketplace reloads themes after
installing. Then set a dashboard's theme to **weather-season** (Dashboard
settings → Theme), or set it as your profile theme.

## Day/night modes (v0.3.0)

The theme has two looks: the base variables are the night (dark) look and
`modes.light` is the day (bright) look. The sky templates already follow the
sun themselves (night starts at sun elevation −2°). The button-card templates
read their colors from the theme's `--neo-*` variables, so the cards go
bright in the day and dark at night along with everything else.

Which look shows is decided by the frontend's light/dark **mode** — a
per-device setting in your profile (Profile → Theme → Light / Dark / Auto),
not something an automation can flip. In Home Assistant 2026.11,
`frontend.set_theme` only sets the *default theme names* for light and dark
mode; it cannot switch the mode itself (verified against the 2026.11.0
source: `homeassistant/components/frontend/services.py` — the service has no
mode-switching path, and the Seasonal Glass README's day/night automation
only re-points the light default theme). So the day/night setup is:

1. Set your profile theme mode to **Auto** (HA app or web → your profile →
   Theme → Auto).
2. Set your phone to switch appearance automatically (iOS: Settings →
   Display & Brightness → Automatic, Sunset to Sunrise).

The phone then flips light at sunrise and dark at sunset, Home Assistant
follows, and this theme renders its day or night look — with Seasonal Glass
decorations following the same switch. To preview the daytime look at night,
temporarily set the profile theme mode to Light, then back to Auto.

## Also in this repo: Seasonal Glass (English fork)

This repo also holds an English fork of
[Seasonal Glass](https://github.com/pietroguidetti02/ha-seasonal-glass)
(v0.2.1 → 0.2.2): the HACS integration that decorates every dashboard per
season and holiday. See [SEASONAL-GLASS.md](SEASONAL-GLASS.md).

Install it by hand — copy `custom_components/seasonal_glass/` into your Home
Assistant `/config/custom_components/` (replacing the upstream files) and
restart. This repo is registered in HACS as the Weather Season theme, so HACS
cannot install the integration from it.
