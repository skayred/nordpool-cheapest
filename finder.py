import logging
from datetime import timedelta, datetime
from functools import reduce

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nordpool-cheapest"

class CheapestFinder(Entity):
    def __init__(self, events, nordpool):
        self._events = events
        self.nordpool = nordpool

    @property
    def name(self):
        """Return the name of the entity."""
        return DOMAIN
    
    def cheapest_start(self, length, prices):
        if len(prices) <= length:
            return 0
        
        sums = []
        for i in range(len(prices) - length + 1):
            sums.append(reduce(lambda a, b: a+b, prices[i:length+i]))

        idx = 0
        val = float('inf')
        for i, sum in enumerate(sums):
            if sum < val:
                val = sum
                idx = i

        return idx

    async def async_create_events(self):
        prices = self.nordpool["today"] + self.nordpool["tomorrow"]
        
        for event in self._events:
            _LOGGER.error(event)

            title = event["name"]
            event_start = timedelta(hours=event["start_hour"])
            event_end = timedelta(hours=event["end_hour"])
            event_length = timedelta(hours=event["length"])

            # data = {
            #     "title": title,
            #     "start": (event_start - event_length).isoformat(),
            #     "end": event_end.isoformat(),
            # }

            # _LOGGER.error(data)
            _LOGGER.error("000")
            today = datetime.now().date()
            datetime(today.year, today.month, today.day, 0, 0)

            _LOGGER.error(datetime.now().hour)
            _LOGGER.error(datetime.now())
            _LOGGER.error("111")

            # try:
            #     await self.hass.services.async_call(
            #         "calendar", "create_event", data, blocking=True
            #     )
            # except Exception as e:
            #     _LOGGER.error("Error creating calendar event: %s", str(e))
            # else:
            #     _LOGGER.info("Calendar event created: %s", event[CONF_NAME])

        # Schedule the next event creation
        # await self.async_schedule_next_events()

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
