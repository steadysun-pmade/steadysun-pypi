"""This module defines the `PVSystem` class for representing and managing photovoltaic (PV) systems.

With the `PVSystem` class, users can create new PV system configurations, retrieve existing ones by UUID,
and modify or delete them as needed. It also provides methods to convert and validate PV system configurations,
including expert parameters. A helper function is also provided to get the UUIDs of all available systems.

Classes:
    PVSystem: A class representing a photovoltaic system, allowing operations such as creation, update, and deletion.

Functions:
    get_pvsystem_uuids(): Retrieves all your PV system UUIDs and names from Steadyweb API
"""

from datetime import datetime
from typing import Dict, List, Tuple
from uuid import UUID

from geojson import Point
from pydantic import FiniteFloat, NonNegativeFloat, StrictStr, field_validator
from pydantic_geojson import PointModel

from steadysun.models._utils import TypeCheckingBaseModel
from steadysun.models.pvsystem import PVSystemExpertParams, PVType
from steadysun.steadysun_api import SteadysunAPI


class PVSystem(TypeCheckingBaseModel):
    """Dataclass to represent a photovoltaic (PV) system with various configuration parameters.

    Attributes:
        uuid (UUID): Unique identifier for the PV system.
        title (StrictStr): Title of the PV system.
        name (StrictStr): Name of the PV system.
        location (PointModel): Geolocation of the PV system.
        altitude (NonNegativeFloat): Altitude of the PV system (default is 0).
        pv_type (PVType): Type of the PV system (default is fixed).
        requested_fields (List[int]): List of requested fields for the system.
        expert_params (PVSystemExpertParams): Expert parameters for advanced configurations.
    """

    uuid: UUID
    title: StrictStr
    name: StrictStr
    location: PointModel
    altitude: NonNegativeFloat = 0
    pv_type: PVType = PVType.fixed
    requested_fields: List[int]  # FIXME
    expert_params: PVSystemExpertParams

    @field_validator("pv_type", mode="before")
    @classmethod
    def _convert_enum(cls, v, field) -> PVType:
        """Validates and converts the PV type value to its enum representation."""
        enum_class = cls.model_fields[field.field_name].annotation
        if isinstance(v, enum_class):
            return v
        return enum_class.from_value(v)

    @classmethod
    def _from_steadyweb_config(cls, steadyweb_pv_config: dict):
        """Creates a PVSystem instance from a Steadyweb configuration.

        Args:
            steadyweb_pv_config (dict): Configuration data for the PV system from Steadyweb.

        Returns:
            PVSystem: An instance of the PVSystem class.
        """
        expert_fields = PVSystemExpertParams.model_fields.keys()
        expert_params = PVSystemExpertParams(**{field: steadyweb_pv_config.pop(field) for field in expert_fields})
        return cls(**steadyweb_pv_config, expert_params=expert_params)

    @classmethod
    def from_uuid(cls, uuid):
        """Retrieves a PVSystem instance based on its UUID from the Steadyweb API.

        Args:
            uuid (UUID): The unique identifier of the PV system.

        Returns:
            PVSystem: An instance of the PVSystem class.
        """
        steadyweb_pv_config = SteadysunAPI().get(f"pvsystem/{uuid}/")
        return PVSystem._from_steadyweb_config(steadyweb_pv_config)

    @classmethod
    def create_new(  # pylint:disable=too-many-arguments
        cls,
        name: StrictStr,
        location: Tuple[FiniteFloat, FiniteFloat],
        pdc0: NonNegativeFloat,
        orientation: NonNegativeFloat = 180,
        inclination: NonNegativeFloat = 30,
    ):
        """Creates a new PVSystem on Steadyweb with the provided parameters.

        Args:
            name (StrictStr): Name of the PV system.
            location (Tuple[FiniteFloat, FiniteFloat]): Geolocation of the PV system (longitude, latitude).
            pdc0 (NonNegativeFloat): Peak power of the PV system (in  W).
            orientation (NonNegativeFloat): Orientation of the PV system in degrees (default is 180).
            inclination (NonNegativeFloat): Inclination of the PV system in degrees (default is 30).

        Returns:
            PVSystem: The newly created PVSystem instance.
        """
        config = {
            "title": name,
            "name": name,
            "location": Point(location),
            "installation_date": str(datetime.now().date()),
            "pv_type": 2,
            "arrays": [
                {
                    "pvmodules_pdc0": pdc0,
                    "orientation": orientation,
                    "inclination": inclination,
                }
            ],
            "requested_fields": [1, 13],
        }
        new_pvsystem_config = SteadysunAPI().post("pvsystem/", data=config)
        return PVSystem._from_steadyweb_config(new_pvsystem_config)

    def _to_steadyweb_dict(self) -> dict:
        """Converts the PVSystem instance to a dictionary compatible with the Steadyweb API.

        Returns:
            dict: A dictionary representation of the PVSystem object suitable for sending to the Steadyweb API.
        """
        model_dict = self.model_dump(mode="json")
        expert_params_dict = model_dict.pop("expert_params")
        return {**model_dict, **expert_params_dict}

    def save_changes(self) -> dict:
        """Saves changes made to the PVSystem by sending an updated configuration to the Steadyweb API.

        Returns:
            dict: The response from the Steadyweb API after patching the PV system.
        """
        steadyweb_patch_config = self._to_steadyweb_dict()
        return SteadysunAPI().patch(f"pvsystem/{str(self.uuid)}/", data=steadyweb_patch_config)

    def delete(self):
        """Deletes the PVSystem from the Steadyweb API. This action is irreversible.

        Returns:
            dict: The response from the Steadyweb API after deletion.
        """
        return SteadysunAPI().delete(f"pvsystem/{str(self.uuid)}/")


def get_pvsystem_uuids() -> Dict[str, str]:
    """Retrieves all your PV system UUIDs and names.

    Returns:
        dict: A dictionary mapping PV system UUIDs to their corresponding names.
    """
    response = SteadysunAPI().get_list("pvsystem/", page_limit=100, get_all_pages=True)
    uuids_name_dict = {pv_details["uuid"]: pv_details["name"] for pv_details in response.get("results", [])}
    return uuids_name_dict
