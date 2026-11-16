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
