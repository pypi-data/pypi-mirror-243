"""Main module."""
import argparse
import logging
import os
import plistlib
from typing import Dict, List, Tuple


# traverse the plist and find the ESP32 IOUSBHostInterface
def find_subtree_paths(data) -> List:
    subtree_paths = []

    def traverse(data, path):
        if isinstance(data, list):
            for item in data:
                if traverse(item, path + [item]):
                    subtree_paths.append(path + [item])
        elif isinstance(data, dict):
            if data.get("IOProviderClass") == "IOUSBHostInterface":
                return True
            else:
                if traverse(list(data.values()), path + [data]):
                    subtree_paths.append(path + [data])
        return False

    traverse(data, [])
    return subtree_paths


# find the serial number and path for each ESP32
def find_serial_and_path(subtrees: List) -> Dict:
    serial_and_path = {}
    for subtree in subtrees:
        serial = subtree.get("USB Serial Number")
        path = subtree.get("IORegistryEntryChildren")[0].get("IORegistryEntryName")
        serial_and_path[serial] = path
    return serial_and_path
