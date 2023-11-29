import math


def db_to_percent(rssi: int, perfect_rssi: int = -20, worst_rssi: int = -85) -> int:
    """Convert signal strength as decibels to percentage for wireless connections.

    This function is licensed under GPL v2. See source code for more info.

    Args:
        rssi: signal strength in decibels
        perfect_rssi: the value to use for a perfect connection. *Default is -20*.
        worst_rssi: the value to use for the worst connection. *Default is -85*.

    Return:
        signal strength as a percentage
    """
    # Copyright(c) 2003 - 2006 Intel Corporation. All rights reserved.

    # 802.11 status code portion of this file from ethereal-0.10.6:
    # Copyright 2000, Axis Communications AB
    # Ethereal - Network traffic analyzer
    # By Gerald Combs <gerald@ethereal.com>
    # Copyright 1998 Gerald Combs

    # Contact Information:
    # Intel Linux Wireless <ilw@linux.intel.com>
    # Intel Corporation, 5200 N.E. Elam Young Parkway, Hillsboro, OR 97124-6497

    # Source adapted from:
    # https://github.com/torvalds/linux/blob/18d46e76/drivers/net/wireless/intel/ipw2x00/ipw2200.c#L4276

    signal_quality = (
        100 * (perfect_rssi - worst_rssi) * (perfect_rssi - worst_rssi)
        - (perfect_rssi - rssi)
        * (15 * (perfect_rssi - worst_rssi) + 62 * (perfect_rssi - rssi))
    ) / ((perfect_rssi - worst_rssi) * (perfect_rssi - worst_rssi))

    if signal_quality > 100:
        return 100
    elif signal_quality < 1:
        return 0

    return math.ceil(signal_quality)
