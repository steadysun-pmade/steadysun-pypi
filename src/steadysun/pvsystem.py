from typing import Union

from ._steadysun_api import SteadysunAPI


def get_pvsystem_list():
    """Get all your pvsystems (accessible with the given token)"""
    return SteadysunAPI().get("pvsystem/")


def get_pvsystem_config(site_uuid: str):
    """Get the configuration of the requested pvsystem"""
    return SteadysunAPI().get(f"pvsystem/{site_uuid}/")


def create_pvsystem(config: Union[dict, str]):
    """Create a new pvsystem with the given configuration"""
    return SteadysunAPI().post("pvsystem/", data=config)


def patch_pvsystem_config(site_uuid: str, config: Union[dict, str]):
    """Patch some parameters of a pvsystem configuration"""
    return SteadysunAPI().patch(f"pvsystem/{site_uuid}/", data=config)


def delete_pvsystem(site_uuid: str):
    """Delete the selected pvsystem (WARNING: this action is irreversible)"""
    return SteadysunAPI().delete(f"pvsystem/{site_uuid}/")
