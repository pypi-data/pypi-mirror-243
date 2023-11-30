from typing import List

# noinspection PyProtectedMember
from multiprocessing.context import TimeoutError
from multiprocessing.pool import ThreadPool


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
    process = ThreadPool(processes=1).apply_async(func=netgear.get_attached_devices)
    try:
        return process.get(60)  # default is 120, we don't want to wait that long
    except TimeoutError:
        raise Error("Failed to get attached devices.")
