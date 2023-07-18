import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nordpool-cheapest"

async def async_setup(hass, config):
    _LOGGER.error("Initial")
    """Set up the Hourly Calendar Event component."""
    if DOMAIN not in config:
        return True
    
    _LOGGER.error("Nordpool reading")

    for entry_config in config[DOMAIN]:
        title = entry_config.get("name", "Hourly Event")
        events = entry_config["events"]

        # Process the configuration options
        # ...

        _LOGGER.info("Configuring %s with title '%s' and events: %s", DOMAIN, title, events)

        # Perform setup tasks based on the configuration options
        # ...

    return True
