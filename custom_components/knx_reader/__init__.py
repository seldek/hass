"""Custom component for reading values from knx group address"""

import logging
import voluptuous as vol
from homeassistant.components.knx import DATA_KNX
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'knx_reader'

SERVICE_KNX_READ = "read"
SERVICE_KNX_ATTR_ADDRESS = "address"

SERVICE_KNX_READ_SCHEMA = vol.Schema({
    vol.Required(SERVICE_KNX_ATTR_ADDRESS): cv.string,
})

async def async_setup(hass, config):
    """Ensure KNX is there."""

    if DATA_KNX not in hass.data:
        _LOGGER.warning("Setup failed, knx_reader (custom component) cannot find DATA_KNX in hass.data")
        hass.components.persistent_notification.async_create(
            "Setup failed, knx_reader (custom component) cannot find DATA_KNX in hass.data",
            title="KNX-READER")
        return False

    def service_read_from_knx_bus(call):
        """Issue read request to the bus."""
        from xknx.core import ValueReader
        from xknx.knx import Address
        attr_address = call.data.get(SERVICE_KNX_ATTR_ADDRESS)
        knx_address = Address(attr_address)

        value_reader = ValueReader(hass.data[DATA_KNX].xknx, knx_address)
        _LOGGER.warning("Shoul read from KNX bus now")
        yield from value_reader.send_group_read()
        _LOGGER.warning("Not sure if I got a value from KNX bus...")

    hass.services.async_register(
        DOMAIN, SERVICE_KNX_READ,
        service_read_from_knx_bus,
        schema=SERVICE_KNX_READ_SCHEMA)

    return True
