import subprocess
import time
from typing import Union, Dict, List

import click

from netfuse.config import settings, ValidationError
from netfuse.logger import LOGGER
from netfuse.modules import att, netgear


def parse_host_file(filepath) -> Dict[Union[int, str], Union[List[str], str]]:
    """Parse the host file and convert the host entries into key-value pairs.

    Args:
        filepath: Host file that matches FQDN with server IPs hosting a specific domain.

    Returns:
        Dict[Union[int, str], List[str]]:
        Returns a dictionary of parsed hosts file information.
    """
    host_entries = {}
    with open(filepath) as file:
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


def update_host_file(host_entries: Dict, output_file: str, dry_run: bool) -> None:
    """Update the hosts entry file, with all the devices currently connected to the router.

    Args:
        host_entries: Data that has to be dumped into the hosts file.
        output_file: Host file that matches FQDN with server IPs hosting a specific domain.
        dry_run: Prints the information instead of writing to hosts file.
    """
    if dry_run:
        for key, value in host_entries.items():
            if value is None:
                print()
                continue
            if isinstance(key, int):
                print(value)
                continue
            key = key.split('_')[0]
            if isinstance(value, list):
                print(f"{key}\t{', '.join(value)}")
                continue
            print(f"{key}\t{value}")
        return
    with open(output_file, 'w') as file:
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


def dump(dry_run: bool, filepath: str, output: str, module: Union[att, netgear]) -> None:
    """Dumps all devices' hostname and IP addresses into the hosts file."""
    host_entries = parse_host_file(filepath)
    for device in module.attached_devices():
        if device.ipv4_address:
            host_entries[device.ipv4_address] = device.name
        else:
            LOGGER.warning("%s [%s] does not have an IP address", device.name, device.mac_address)
    update_host_file(host_entries, output, dry_run)
    if output == settings.etc_hosts:
        flush_dns_cache()


@click.command()
@click.pass_context
@click.option("-m", "--model", required=False, help="Source model that's either 'att' or 'netgear'")
@click.option("-d", "--dry", required=False, is_flag=True, help="Dry run without updating the hosts file")
@click.option("-p", "--path", required=False, default=settings.etc_hosts,
              help=f"Path for the hosts file, defaults to: {settings.etc_hosts}")
@click.option("-o", "--output", required=False, default=settings.etc_hosts,
              help=f"Output filepath to write the updated entries, defaults to: {settings.etc_hosts}")
def main(*args, model: str, dry: bool = False, path: str = None, output: str = None):
    mapped = {"att": att, "netgear": netgear}
    if model in mapped.keys():
        dump(dry_run=dry, filepath=path, output=output, module=mapped[model])
    else:
        raise ValidationError(
            "\n\nmodel\n  Input should be 'att' or 'netgear' "
            f"[type=string_type, input_value={model}, input_type={type(model)}]\n"
        )


if __name__ == '__main__':
    main()
