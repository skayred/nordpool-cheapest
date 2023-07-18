import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nordpool-cheapest"

# EVENT_SCHEMA = cv.schema_with_slug_keys(
#     {
#         cv.Required(CONF_NAME): cv.string,
#         cv.Required("start_hour"): cv.positive_int,
#         cv.Required("end_hour"): cv.positive_int,
#         cv.Required("length"): cv.positive_int,
#     }
# )

# CONFIG_SCHEMA = cv.schema_with_slug_keys(
#     cv.positive_int,
#     {
#         cv.Optional(CONF_NAME): cv.string,
#         cv.Required("events"): cv.ensure_list(EVENT_SCHEMA),
#         cv.Required("nordpool"): cv.string,
#     },
# )
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional("nordpool", default=3): cv.positive_int,
    }
)



async def async_setup(hass, config):
    """Set up the Hourly Calendar Event component."""
    entities = []

    sensor_state = hass.states.get(cfg.get("nordpool"))
    attributes = sensor_state.attributes

    for entity_id, cfg in config[DOMAIN].items():
        name = cfg.get(CONF_NAME, entity_id)
        events = cfg["events"]

        entity = HourlyCalendarEventEntity(entity_id, name, events, attributes)
        entities.append(entity)

        # Schedule the initial event creation
        await entity.async_create_events()

    if entities:
        hass.data[DOMAIN] = entities

    return True


class HourlyCalendarEventEntity(Entity):
    """Representation of an Hourly Calendar Event."""

    def __init__(self, entity_id, name, events, nordpool):
        """Initialize the Hourly Calendar Event entity."""
        self.entity_id = entity_id
        self._name = name
        self._events = events
        self.nordpool = nordpool

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    async def async_create_events(self):
        """Create calendar events."""
        for event in self._events:
            event_start = timedelta(hours=event["start_hour"])
            event_end = timedelta(hours=event["end_hour"])
            event_length = timedelta(hours=event["length"])

            data = {
                "title": event[CONF_NAME],
                "start": (event_start - event_length).isoformat(),
                "end": event_end.isoformat(),
            }

            _LOGGER.error(data)
            _LOGGER.error("ASYNC!")
            _LOGGER.error(self.nordpool.today)
            # try:
            #     await self.hass.services.async_call(
            #         "calendar", "create_event", data, blocking=True
            #     )
            # except Exception as e:
            #     _LOGGER.error("Error creating calendar event: %s", str(e))
            # else:
            #     _LOGGER.info("Calendar event created: %s", event[CONF_NAME])

        # Schedule the next event creation
        await self.async_schedule_next_events()

    async def async_schedule_next_events(self):
        """Schedule the next event creation."""
        next_event = timedelta(minutes=1)
        await self.async_create_events()
        await self.async_schedule_next_event(next_event)

    async def async_schedule_next_event(self, next_event):
        """Schedule the next event creation."""
        async_call_later(
            self.hass, (next_event - dt_util.utcnow()).total_seconds(), self.async_create_events
        )
