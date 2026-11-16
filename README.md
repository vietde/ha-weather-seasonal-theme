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
sun themselves (night starts at sun elevation −2°). Pair it with the
day/night automation from the
[Seasonal Glass README](https://github.com/pietroguidetti02/ha-seasonal-glass#daynight-the-automation-that-pairs-with-it)
— adapted to this theme, it calls `frontend.set_theme` with mode `light` at
sunrise and `dark` at sunset:

```yaml
automation:
  - alias: "Dashboard theme follows the sun"
    mode: single
    triggers:
      - trigger: numeric_state
        entity_id: sun.sun
        attribute: elevation
        below: -2
      - trigger: numeric_state
        entity_id: sun.sun
        attribute: elevation
        above: -2
      - trigger: homeassistant
        event: start
    actions:
      - action: frontend.set_theme
        data:
          mode: >
            {% if state_attr('sun.sun', 'elevation') | float(0) > -2 %}light{% else %}dark{% endif %}
```

The Homeview button-card templates read their colors from the theme's
`--neo-*` variables, so the cards go bright in the day and dark at night
along with everything else.

## Also in this repo: Seasonal Glass (English fork)

This repo also holds an English fork of
[Seasonal Glass](https://github.com/pietroguidetti02/ha-seasonal-glass)
(v0.2.1 → 0.2.2): the HACS integration that decorates every dashboard per
season and holiday. See [SEASONAL-GLASS.md](SEASONAL-GLASS.md).

Install it by hand — copy `custom_components/seasonal_glass/` into your Home
Assistant `/config/custom_components/` (replacing the upstream files) and
restart. This repo is registered in HACS as the Weather Season theme, so HACS
cannot install the integration from it.
