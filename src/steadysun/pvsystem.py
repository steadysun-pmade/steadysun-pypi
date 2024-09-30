from typing import Union

from ._steadysun_api import SteadysunAPI


def get_pvsystem_list(page_limit: int = 10, get_all_pages: bool = False):
    """Get all your pvsystems (accessible with the given token)"""
    return SteadysunAPI().get_list("pvsystem/", page_limit=page_limit, get_all_pages=get_all_pages)


def get_pvsystem_count():
    """Get the count of your pvsystems (accessible with the given token)"""
    response = SteadysunAPI().get_list("pvsystem/", page_limit=1, get_all_pages=False)
    return response["count"]


def get_pvsystem_uuids():
    """Get all your pvsystems (accessible with the given token)"""
    response = SteadysunAPI().get_list("pvsystem/", page_limit=100, get_all_pages=True)
    uuids = [pv_details["uuid"] for pv_details in response.get("results", [])]
    return uuids


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
