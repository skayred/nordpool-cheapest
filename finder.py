import logging
from datetime import timedelta, datetime
from functools import reduce
import pytz

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nordpool-cheapest"

class CheapestFinder(Entity):
    def __init__(self, events, tz, nordpool):
        self._events = events
        self._tz = tz
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

        _LOGGER.info("Sums:")
        _LOGGER.info(sums)

        idx = 0
        val = float('inf')
        for i, sum in enumerate(sums):
            if sum < val:
                val = sum
                idx = i

        _LOGGER.info("Cheapest sum was %s for index %s", val, idx)

        return idx

    async def async_create_events(self):
        prices = self.nordpool["today"] + self.nordpool["tomorrow"]
        tz = pytz.timezone(self._tz)

        utc_dt = datetime.now(tz=pytz.utc)
        local = tz.normalize(utc_dt)
        
        for event in self._events:
            _LOGGER.error(event)

            title = event["name"]
            calendar = event["calendar"]
            event_start = event["start_hour"]
            event_end = event["end_hour"]
            event_length = event["length"]

            # data = {
            #     "title": title,
            #     "start": (event_start - event_length).isoformat(),
            #     "end": event_end.isoformat(),
            # }

            today = datetime.now().date()
            datetime(today.year, today.month, today.day, 0, 0)

            if event_end <= event_start:
                event_end = event_end + 24

            if local.hour < event_start:
                # still eligible for today - maybe for multiday
                _LOGGER.info("Checking the cheapest prices for %s (%s) for TODAY between %s and %s, length %s", title, calendar, event_start, event_end, event_length)
                event_start = event_start + self.cheapest_start(event_length, prices[event_start:event_end])
            else:
                # check tomorrow in that case
                _LOGGER.info("Checking the cheapest prices for %s (%s) for TOMORROW between %s and %s, length %s", title, calendar, event_start, event_end, event_length)
                event_start = event_start + self.cheapest_start(event_length, prices[24+event_start:max(24+event_end, 47)])

            start = datetime(local.year, local.month, local.day, 0, 0, 0, 0) + timedelta(hours = event_start)
            end = start + timedelta(hours = event_length)

            _LOGGER.info("Best time found: %s..%s", start, end)

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
