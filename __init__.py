import logging
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

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
