"""Console script for esp_serial_find."""

import argparse
import logging
import os
import sys
import plistlib
import multiprocessing
import time
from typing import Dict, List, Tuple

from esp_serial_find.esp_serial_find import find_serial_and_path, find_subtree_paths

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def find_one_device(base_path, device):
    devices = []
    try:
        manufacturer = None
        with open(os.path.join(base_path, device, "manufacturer"), "r") as f:
            manufacturer = f.read().strip()

        if manufacturer == "Espressif":
            with open(os.path.join(base_path, device, "serial"), "r") as f:
                serial_number = f.read().strip()
            tty_path = find_tty_path(device)
            if tty_path:
                for tty in tty_path:
                    devices.append((serial_number, tty))
    except IOError:
        pass  # Ignore files and directories that can't be read
    return devices

def find_one_device_worker(base_path, devices, device):
    devices += find_one_device(base_path, device)

def find_usb_devices(vendor_name):
    manager = multiprocessing.Manager()
    devices = manager.list()
    base_path = "/sys/bus/usb/devices/"
    with multiprocessing.Pool(3) as pool:
        for device in os.listdir(base_path):
            pool.apply_async(find_one_device_worker, (base_path, devices, device))
        pool.close()
        time.sleep(0.1)
        pool.terminate()
    return devices


def find_tty_path(device):
    ttys = []
    tty_base_path = f"/sys/bus/usb/devices/{device}/"
    for subdir in os.listdir(tty_base_path):
        try:
            for subsubdir in os.listdir(os.path.join(tty_base_path, subdir)):
                if subsubdir.startswith("tty"):
                    ttys += [
                        f"/dev/{ttyname}" for ttyname in os.listdir(os.path.join(tty_base_path, subdir, subsubdir))
                    ]
        except:
            pass
    return ttys


def main():
    """Main entrypoint."""

    argparser = argparse.ArgumentParser()

    argparser.add_argument("--verbose", "-v", action="store_true", help="Print verbose output")

    # if provided a serial number, only print the path for that serial number
    argparser.add_argument(
        "--serial",
        "-s",
        type=str,
        default=None,
        help="Print the path for the given serial number",
    )

    argparser.add_argument(
        "--prefer-tty",
        "-t",
        action="store_true",
        help="Prefer the tty device over the cu device",
    )

    args = argparser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    serial_and_path = None
    if sys.platform.startswith("linux"):
        serial_and_path = find_usb_devices("Espressif")
        logging.info(f"{serial_and_path = }")

    if sys.platform.startswith("darwin"):
        # read the plist
        plist = os.popen("ioreg -i -t -r -c AppleUSBACMData -l -a").read()
        data: List = plistlib.loads(plist.encode())
        paths = find_subtree_paths(data)

        logging.info("Found {} ESP32 devices".format(len(paths)))

        serial_and_path: List[Tuple[str, str]] = [
            (
                path[-2].get("USB Serial Number"),
                path[-1]
                .get("IORegistryEntryChildren")[0]
                .get("IODialinDevice" if args.prefer_tty else "IOCalloutDevice"),
            )
            for path in paths
        ]

    if args.serial:
        # find the path for the given serial number
        serial = args.serial
        path_device = None
        for serial, path in serial_and_path:
            if serial == args.serial:
                path_device = path
                break

        # if the serial number was not found, print an error
        if not path_device:
            logging.error("Serial number {} not found".format(args.serial))
            exit(1)
        else:
            print(path_device)
            exit(0)

    for serial, path in serial_and_path:
        print("{} {}".format(serial, path))


if __name__ == "__main__":
    main()  # pragma: no cover
