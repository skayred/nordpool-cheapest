import logging
import voluptuous as vol
from functools import partial
from datetime import timedelta, datetime

from homeassistant.helpers.event import async_track_state_change, async_call_later

from .finder import CheapestFinder

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nordpool-cheapest"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: {
            vol.Required("name", default="Hourly Event"): str,
            vol.Required("nordpool", default="sensor.nordpool_kwh_fi_eur_3_10_024"): str,
            vol.Required("timezone", default="Europe/Helsinki"): str,
            vol.Required("events"): [
                {
                    vol.Required("name"): str,
                    vol.Required("calendar"): str,
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
    handle_sensor_state_change = partial(_handle_sensor_state_change, config, hass)

    # Listen for state changes of the sensor entity
    async_track_state_change(
        hass, nordpool, handle_sensor_state_change
    )

    _LOGGER.info("Waiting for sensor entity: %s", nordpool)

    return True

async def _handle_sensor_state_change(config, hass, entity_id, old_state, new_state):
    if new_state is not None:
        if "is_configured" not in config[DOMAIN]:
            config[DOMAIN]["is_configured"] = True

            async_call_later(hass, seconds_until(), lambda x: (await _run_daily_task(hass, config, new_state.attributes)).__anext__())

            _LOGGER.info("Sensor entity %s is available. Configuring...", entity_id)

def seconds_until():
    """Calculate the number of seconds until 14:00."""
    now = datetime.now()
    target_time = now.replace(hour=15, minute=45, second=0, microsecond=0)
    if now > target_time:
        # Target time has already passed, schedule for the next day
        target_time = target_time + timedelta(days=1)
    time_diff = target_time - now
    return time_diff.total_seconds()

async def _run_daily_task(hass, config, sensor_attributes):
    """Perform the daily task at 14:00."""
    _LOGGER.info("Running daily task at 14:00")
    entity = CheapestFinder(hass, config[DOMAIN]["events"], config[DOMAIN]["timezone"], sensor_attributes)
    await entity.async_create_events()

    nordpool = config[DOMAIN]["nordpool"]
    attrs = hass.states.get(nordpool).attributes

    async_call_later(hass, seconds_until(), lambda: _run_daily_task(hass, config, attrs))
