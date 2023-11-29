from typing import Optional, Union, Any


class Device:
    """Convert dictionary into a device object.

    >>> Device

    """

    def __init__(self, dictionary: dict):
        """Set dictionary keys as attributes of Device object.

        Args:
            dictionary: Takes the input dictionary as an argument.
        """
        self.mac_address: Optional[str] = None
        self.ipv4_address: Optional[str] = None
        self.name: Optional[str] = None
        self.last_activity: Optional[str] = None
        self.status: Optional[str] = None
        self.allocation: Optional[str] = None
        self.connection_type: Optional[str] = None
        self.connection_speed: Optional[Union[float, Any]] = None
        self.mesh_client: Optional[str] = None
        for key in dictionary:
            setattr(self, key, dictionary[key])
