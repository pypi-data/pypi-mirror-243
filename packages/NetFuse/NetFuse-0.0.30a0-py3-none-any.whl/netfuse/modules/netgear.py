from typing import List

from netfuse.config import settings, ValidationError, MissingRequirement, Error


def attached_devices():
    """Get all attached devices in a Netgear router.

    Returns:
        List[pynetgear.Device]:
        List of device objects.
    """
    try:
        import pynetgear
    except ImportError as err:
        raise MissingRequirement(
            f"\n\n{err.name}\n\tpip install netfuse[netgear]"
        )
    if not settings.router_pass:
        raise ValidationError(
            "\n\nrouter_pass\n\tEnvironment variable should be a valid string "
            f"[type=string_type, input_value={settings.router_pass}, input_type={type(settings.router_pass)}]\n"
        )
    netgear = pynetgear.Netgear(password=settings.router_pass)
    if devices := netgear.get_attached_devices():
        return devices
    else:
        raise Error("Failed to get attached devices.")
