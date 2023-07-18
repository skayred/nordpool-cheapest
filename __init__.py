import logging
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

from sensor import CheapestHoursTracker

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nordpool-cheapest"

EVENT_SCHEMA = cv.schema_with_slug_keys(
    {
        cv.Required(CONF_NAME): cv.string,
        cv.Required("start_hour"): cv.positive_int,
        cv.Required("end_hour"): cv.positive_int,
        cv.Required("length"): cv.positive_int,
    }
)

CONFIG_SCHEMA = cv.schema_with_slug_keys(
    cv.positive_int,
    {
        cv.Optional(CONF_NAME): cv.string,
        cv.Required("events"): cv.ensure_list(EVENT_SCHEMA),
        cv.Required("nordpool"): cv.string,
    },
)

async def async_setup(hass, config):
    """Set up the Hourly Calendar Event component."""
    _LOGGER.error("Initial")
    entities = []

    _LOGGER.error("Nordpool reading")

    sensor_state = hass.states.get(cfg.get("nordpool"))
    attributes = sensor_state.attributes

    hass.data.setdefault(DOMAIN, {})

    for entity_id, cfg in config[DOMAIN].items():
        name = cfg.get(CONF_NAME, entity_id)
        events = cfg["events"]

        entity = CheapestHoursTracker(entity_id, name, events, attributes)
        entities.append(entity)

        # Schedule the initial event creation
        await entity.async_create_events()

    return True

async def async_setup_entry(hass, entry):
    """Set up the Hourly Calendar Event entry."""
    # Retrieve and store the configuration options from the entry
    title = entry.data.get("title")
    events = entry.data.get("events")

    # Perform setup tasks based on the configuration options
    # ...

    # Store any information that needs to be accessed later
    hass.data[DOMAIN][entry.entry_id] = {
        "title": title,
        "events": events,
    }

    return True

async def async_unload_entry(hass, entry):
    """Unload the Hourly Calendar Event entry."""
    # Perform cleanup tasks for the entry
    # ...

    # Remove stored information
    if entry.entry_id in hass.data[DOMAIN]:
        del hass.data[DOMAIN][entry.entry_id]

    return True
