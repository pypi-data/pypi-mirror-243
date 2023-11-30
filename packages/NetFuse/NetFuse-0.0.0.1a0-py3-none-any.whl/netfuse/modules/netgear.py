from typing import List

from pynetgear import Device, Netgear

from netfuse.config import settings, ValidationError
from netfuse.logger import LOGGER


def attached_devices() -> List[Device]:
    """Get all attached devices in a Netgear router.

    Returns:
        List[Device]:
        List of device objects.
    """
    if not settings.router_pass:
        raise ValidationError(
            "\n\nrouter_pass\n  Input should be a valid string "
            f"[type=string_type, input_value={settings.router_pass}, input_type={type(settings.router_pass)}]"
        )
    netgear = Netgear(password=settings.router_pass)
    if devices := netgear.get_attached_devices():
        return devices
    else:
        LOGGER.error("Unable to get attached devices.")
