"""Seasonal Glass: automatic seasonal decorations for the dashboards.

The integration:
- serves the plugin files (www/ folder) on /seasonal_glass/ and loads it on every frontend page
  (no Lovelace resource to add by hand);
- exposes the settings chosen in "Configure" on /api/seasonal_glass/impostazioni (login required: it also
  holds the personal days; pages outside the frontend use the automatic calendar);
- creates the "Period" sensor (sensor.py), which sends an internal notification when the decoration changes,
  and the periods calendar (calendar.py);
- offers the seasonal_glass.preview service: shows a period on every device for a few minutes
  (the plugin reads it from the same endpoint, within ~30 seconds).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import voluptuous as vol

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import HomeAssistantView, StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, PERIODI, URL_BASE, converti_opzioni

CARTELLA = Path(__file__).parent
PIATTAFORME = ["sensor", "calendar"]
SCHEMA_PREVIEW = vol.Schema({
    vol.Required("period"): cv.string,
    vol.Optional("minutes", default=10): vol.All(vol.Coerce(int), vol.Range(min=0, max=1440)),
})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    dati = hass.data.setdefault(DOMAIN, {})
    if not dati.get("registrato"):  # paths and script are registered once per boot
        manifest = await hass.async_add_executor_job((CARTELLA / "manifest.json").read_text, "utf-8")
        versione = json.loads(manifest)["version"]
        await hass.http.async_register_static_paths(
            [StaticPathConfig(URL_BASE, str(CARTELLA / "www"), False)]
        )
        hass.http.register_view(ConfigView(hass))
        add_extra_js_url(hass, f"{URL_BASE}/seasonal-glass.js?v={versione}")
        hass.services.async_register(DOMAIN, "preview", _preview, schema=SCHEMA_PREVIEW)
        dati["registrato"] = True
    dati["opzioni"] = dict(entry.options)
    entry.async_on_unload(entry.add_update_listener(_opzioni_cambiate))
    await hass.config_entries.async_forward_entry_setups(entry, PIATTAFORME)
    return True


async def _preview(call: ServiceCall) -> None:
    """period = id (halloween, natale, ricorrenza_1...) or "normal" ("normale" still works); minutes = 0 cancels."""
    hass, pid, minuti = call.hass, call.data["period"].strip().lower(), call.data["minutes"]
    if pid == "normal":
        pid = "normale"
    dati = hass.data[DOMAIN]
    validi = {p["id"] for p in PERIODI} | {r["id"] for r in converti_opzioni(dati.get("opzioni", {})).get("ricorrenze", [])}
    if pid not in validi | {"normale"}:
        raise ServiceValidationError(f"Unknown period: {pid}. Valid: normal, {', '.join(sorted(validi))}")
    if minuti == 0:
        dati.pop("anteprima", None)
    else:
        dati["anteprima"] = {"id": "off" if pid == "normale" else pid, "fino": int((time.time() + minuti * 60) * 1000)}


async def _opzioni_cambiate(hass: HomeAssistant, entry: ConfigEntry) -> None:
    hass.data[DOMAIN]["opzioni"] = dict(entry.options)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # the script stays loaded until the restart, but without settings it goes back to the automatic calendar
    hass.data[DOMAIN]["opzioni"] = {}
    return await hass.config_entries.async_unload_platforms(entry, PIATTAFORME)


class ConfigView(HomeAssistantView):
    """Current settings in the format the JS plugin expects."""

    url = "/api/seasonal_glass/impostazioni"
    name = "api:seasonal_glass:impostazioni"

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    async def get(self, request):
        dati = self.hass.data.get(DOMAIN, {})
        out = converti_opzioni(dati.get("opzioni", {}))
        if (a := dati.get("anteprima")) and a["fino"] > time.time() * 1000:
            out["anteprima"] = a
        return self.json(out)
