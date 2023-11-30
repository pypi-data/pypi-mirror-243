import io
import socket
from collections.abc import Generator

import pandas as pd
import requests

from netfuse.config import settings
from netfuse.logger import LOGGER
from netfuse.modules.squire import Device


def get_network_id() -> str:
    """Get network id from the current IP address."""
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        socket_.connect(("8.8.8.8", 80))
        ip_address = socket_.getsockname()[0]
        network_id = '.'.join(ip_address.split('.')[0:3])
        socket_.close()
    except OSError as error:
        LOGGER.warning(error)
        network_id = "192.168.1"
    return network_id


def generate_dataframe() -> pd.DataFrame:
    """Generate a dataframe using the devices information from router web page.

    Returns:
        pd.DataFrame:
        Devices list as a data frame.
    """
    # pd.set_option('display.max_rows', None)
    try:
        response = requests.get(url=f"http://{get_network_id()}.254/cgi-bin/devices.ha")
    except requests.RequestException as error:
        LOGGER.error(error)
        raise ConnectionError(error.args)
    else:
        if response.ok:
            html_source = response.text
            html_tables = pd.read_html(io.StringIO(html_source))
            return html_tables[0]
        else:
            LOGGER.error("[%s] - %s" % (response.status_code, response.text))


def attached_devices() -> Generator[Device]:
    """Get all devices connected to the router.

    Yields:
        Generator[Device]:
        Yields each device information as a Device object.
    """
    device_info = {}
    dataframe = generate_dataframe()
    if dataframe is None:
        return
    for value in dataframe.values:
        if str(value[0]) == "nan":
            yield Device(device_info)
            device_info = {}
        elif value[0] == "IPv4 Address / Name":
            key = value[0].split('/')
            val = value[1].split('/')
            device_info[settings.format_key(key[0].strip())] = val[0].strip()
            device_info[settings.format_key(key[1].strip())] = val[1].strip()
        else:
            device_info[settings.format_key(value[0])] = value[1]
