import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.event import async_track_state_change

from .finder import CheapestFinder

_LOGGER = logging.getLogger(__name__)
started = False

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
    sensor_state = hass.states.get(nordpool)

    unsub = async_track_state_change(hass, nordpool, _handle_sensor_state_change)

    _LOGGER.info("Waiting for sensor entity: %s", nordpool)

    # entity = CheapestFinder(config[DOMAIN]["events"], attributes)

    # # Schedule the initial event creation
    # await entity.async_create_events()

    return True

async def _handle_sensor_state_change(entity_id, old_state, new_state):
    if not started:
        if new_state is not None:
            started = True
            sensor_attributes = new_state.attributes   

            _LOGGER.info("Sensor entity %s is available. Configuring...", entity_id)
            _LOGGER.error(sensor_attributes)
