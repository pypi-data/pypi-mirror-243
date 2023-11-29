import subprocess
import time
from typing import Union, Dict, List

from netsync.config import settings, SupportedSystems
from netsync.logger import LOGGER
from netsync.modules import att


def parse_host_file() -> Dict[Union[int, str], Union[List[str], str]]:
    """Parse the host file and convert the host entries into key-value pairs.

    Returns:
        Dict[Union[int, str], List[str]]:
        Returns a dictionary of parsed hosts file information.
    """
    host_entries = {}
    with open(settings.etc_hosts) as file:
        for idx, line in enumerate(file):
            # Yield comments and empty lines with an integer as key
            if not line.strip():
                host_entries[idx] = None
                continue
            if line.startswith('#'):
                host_entries[idx] = line.rstrip()
                continue
            # Split the line into columns (fields)
            fields = line.split()
            # Extract IP address and hostnames
            ip_address = fields[0]
            hostnames = fields[1:]
            hostnames = ' '.join(hostnames).split(',')  # rejoin as string and split by comma (,)
            hostnames = list(map(str.strip, hostnames))  # strip individual hostnames and make a list
            if host_entries.get(ip_address):
                host_entries[f"{ip_address}_DUPLICATE{idx}"] = hostnames
            else:
                host_entries[ip_address] = hostnames
    return host_entries


def update_host_file(host_entries: Dict) -> None:
    """Update the hosts entry file, with all the devices currently connected to the router.

    Args:
        host_entries: Data that has to be dumped into the hosts file.
    """
    with open(settings.etc_hosts, 'w') as file:
        for key, value in host_entries.items():
            if value is None:
                file.write("\n")
                continue
            if isinstance(key, int):
                file.write(f"{value}\n")
                continue
            key = key.split('_')[0]
            if isinstance(value, list):
                file.write(f"{key}\t{', '.join(value)}\n")
                continue
            file.write(f"{key}\t{value}\n")


def flush_dns_cache() -> None:
    """Flushes the DNS cache."""
    for cmd in settings.flush_dns:
        result = subprocess.run(cmd, shell=True)
        if result.returncode:
            LOGGER.error("Failed to clear DNS cache")
            break
    else:
        LOGGER.info("Finished updating hosts file in %.2fs", time.time() - settings.start)


def dump(model: SupportedSystems) -> None:
    """Dumps all devices' hostname and IP addresses into the hosts file."""
    if model == SupportedSystems.att:
        get_attached_devices = att.get_attached_devices
    else:
        raise EnvironmentError(
            "Not supported yet"
        )
    host_entries = parse_host_file()
    for device in get_attached_devices():
        if device.ipv4_address:
            host_entries[device.ipv4_address] = f"{device.name}"
        else:
            LOGGER.error(device.__dict__)
    update_host_file(host_entries)
    flush_dns_cache()
