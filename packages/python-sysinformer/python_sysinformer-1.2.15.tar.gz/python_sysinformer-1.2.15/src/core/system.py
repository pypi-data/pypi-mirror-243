import os
import platform
import time

import distro

from src.utilities.utils import print_bold_kv, print_title


def get_system_info() -> tuple[str, str, str, str, str, str, str, str, int, str]:
    """
    Retrieves various system information.

    Returns:
        tuple: A tuple containing the following system information:
            - OS type
            - Distribution name (if Linux)
            - Distribution version (if Linux)
            - Hostname
            - System uptime
            - Last boot date
            - Kernel information
            - System architecture
            - Number of users
            - Current date and time
    """
    os_type = platform.system()
    dist = distro.name() if os_type == "Linux" else "UNKNOWN"
    dist_version = (
        platform.freedesktop_os_release().get("VERSION")
        if os_type == "Linux"
        else "UNKNOWN"
    )
    hostname = platform.node()
    kernel_info = platform.uname().release
    architecture = platform.machine()

    try:
        uptime_seconds = time.time() - os.stat("/proc/1").st_ctime
        last_boot_date = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(os.stat("/proc/1").st_ctime)
        )
        days, rem = divmod(uptime_seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, _ = divmod(rem, 60)
        uptime = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"
    except FileNotFoundError:
        uptime = "UNKNOWN"
        last_boot_date = "UNKNOWN"

    try:
        users_nb = len(os.listdir("/home"))
    except FileNotFoundError:
        users_nb = "UNKNOWN"

    current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    return (
        os_type,
        dist,
        dist_version,
        hostname,
        uptime,
        last_boot_date,
        kernel_info,
        architecture,
        users_nb,
        current_date,
    )


def print_system_info() -> None:
    """
    Prints various system information.
    """
    print_title("System Information")  # using the print_title function

    try:
        (
            os_type,
            dist,
            dist_version,
            hostname,
            uptime,
            last_boot_date,
            kernel_info,
            architecture,
            users_nb,
            current_date,
        ) = get_system_info()
    except TypeError as exception:
        print(f"Could not get system info. Error: {exception}")
        return

    print_bold_kv("Hostname", hostname)
    print_bold_kv("OS", f"{os_type} {dist} {dist_version}")
    print_bold_kv("Kernel", kernel_info)
    print_bold_kv("Architecture", architecture)
    print_bold_kv("Uptime", uptime)
    print_bold_kv("Last boot", last_boot_date)
    print_bold_kv("Users (/home)", str(users_nb))
    print_bold_kv("Server datetime", current_date)
