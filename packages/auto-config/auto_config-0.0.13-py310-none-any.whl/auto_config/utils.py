from __future__ import annotations

import os
from sys import stdout

import toml
from loguru import logger
from pydantic import ValidationError

from .device import Device
from .field import BaseExtraField, DefaultExtraField
from .generator import AnsibleHostsGenerator, DNSConfigGenerator, SSHHostsGenerator
from .service import Service
from typing import TypeVar

def __wrapper_func_get_devices():
    __get_devices_T = TypeVar("__get_devices_T", bound = BaseExtraField)
    
    
    def get_devices(
        devices_config: list[dict], extra_field_cls: type[__get_devices_T] = BaseExtraField
    ) -> list[Device[__get_devices_T]]:
        devices = []
        for device in devices_config:
            try:
                extra_field_cls.model_validate(device.get("extra", {}))
                devices.append(Device[extra_field_cls].model_validate(device))
            except ValidationError:
                logger.warning(f"device {device} has invalid extra field")
                continue
        return devices
    return get_devices
get_devices = __wrapper_func_get_devices()


def get_services(services_config: list[dict]) -> list[Service]:
    services = []
    for service in services_config:
        services.append(Service.model_validate(service))
    return services


def generate_config(path: str = "~/.config/autoconfig/config.toml", *, log_level="INFO"):
    logger.remove()
    logger.add(stdout, level=log_level)
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    config = toml.load(open(path, "r"))
    devices = get_devices(config["devices"], DefaultExtraField)
    generator = AnsibleHostsGenerator(devices)
    generator.write("~/.config/ansible/hosts")
    generator = SSHHostsGenerator(devices)
    generator.write("~/.ssh/config")
    generator = DNSConfigGenerator(devices)
    generator.write("~/.config/autoconfig/auto-ddns.json")
