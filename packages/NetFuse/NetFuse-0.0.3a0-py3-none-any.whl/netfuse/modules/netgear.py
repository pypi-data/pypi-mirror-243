from typing import List

from netfuse.config import settings, ValidationError, Modules
from netfuse.logger import LOGGER


def attached_devices() -> 'List[Modules.pynetgear.Device]':
    """Get all attached devices in a Netgear router.

    Returns:
        List[Device]:
        List of device objects.
    """
    netgear_object = Modules.pynetgear.Netgear
    if not settings.router_pass:
        raise ValidationError(
            "\n\nrouter_pass\n  Input should be a valid string "
            f"[type=string_type, input_value={settings.router_pass}, input_type={type(settings.router_pass)}]\n"
        )
    netgear = netgear_object(password=settings.router_pass)
    if devices := netgear.get_attached_devices():
        return devices
    else:
        LOGGER.error("Unable to get attached devices.")
