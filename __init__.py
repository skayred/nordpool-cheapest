import logging
import voluptuous as vol
from .finder import CheapestFinder

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nordpool-cheapest"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: {
            vol.Required("name", default="Hourly Event"): str,
            vol.Required("nordpool", default="sensor.nordpool_kwh_fi_eur_3_10_024"): str,
            vol.Required("events"): [
                {
                    vol.Required("name"): str,
                    vol.Required("start_hour"): int,
                    vol.Required("end_hour"): int,
                    vol.Required("length"): int,
                }
            ],
        }
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    _LOGGER.error("Initial")
    """Set up the Hourly Calendar Event component."""
    if DOMAIN not in config:
        return True

    nordpool = config[DOMAIN]["nordpool"]
    sensor_state = hass.states

    _LOGGER.error(sensor_state.entity_ids())

    attributes = sensor_state.attributes

    # for entry_config in config[DOMAIN]["events"]:
    #     title = entry_config["name"]
    #     start_hour = entry_config["start_hour"]
    #     end_hour = entry_config["end_hour"]
    #     length = entry_config["length"]

    #     _LOGGER.error("Configuring %s with title '%s' and events: %s, %s, %s", DOMAIN, title, start_hour, end_hour, length)

    entity = CheapestFinder(config[DOMAIN]["events"], attributes)

    # Schedule the initial event creation
    await entity.async_create_events()

    return True
