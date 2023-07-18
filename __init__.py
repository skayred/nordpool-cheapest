import logging
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nordpool-cheapest"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            [
                {
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
            ]
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    _LOGGER.error("Initial")
    """Set up the Hourly Calendar Event component."""
    if DOMAIN not in config:
        return True
    
    nordpool = config[DOMAIN].get("nordpool")

    _LOGGER.error("Nordpool reading")
    _LOGGER.error(nordpool)

    for entry_config in config[DOMAIN].get("events"):
        title = entry_config.get("name", "Hourly Event")
        start_hour = entry_config.get("start_hour")
        end_hour = entry_config.get("end_hour")
        length = entry_config.get("length")

        _LOGGER.info("Configuring %s with title '%s' and events: %s, %s, %s", DOMAIN, title, start_hour, end_hour, length)

    return True
