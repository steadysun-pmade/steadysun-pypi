from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from geojson import Point
from pydantic import FiniteFloat, NonNegativeFloat, StrictStr, field_validator
from pydantic_geojson import PointModel

from ._pvsystem_models import PVSystemExpertParams, PVType, TypeCheckingBaseModel
from .steadysun_api import SteadysunAPI


class PVSystem(TypeCheckingBaseModel):
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
    def convert_enum(cls, v, field):
        enum_class = cls.model_fields[field.field_name].annotation
        if isinstance(v, enum_class):
            return v
        return enum_class.from_value(v)

    @classmethod
    def from_steadyweb_config(cls, steadyweb_pv_config: dict):
        expert_fields = PVSystemExpertParams.model_fields.keys()
        expert_params = PVSystemExpertParams(**{field: steadyweb_pv_config.pop(field) for field in expert_fields})
        return cls(**steadyweb_pv_config, expert_params=expert_params)

    @classmethod
    def from_uuid(cls, uuid):
        steadyweb_pv_config = SteadysunAPI().get(f"pvsystem/{uuid}/")
        return PVSystem.from_steadyweb_config(steadyweb_pv_config)

    @classmethod
    def create_new(  # pylint:disable=too-many-arguments
        cls,
        name: StrictStr,
        location: Tuple[FiniteFloat, FiniteFloat],
        pdc0: NonNegativeFloat,
        orientation: NonNegativeFloat = 180,
        inclination: NonNegativeFloat = 30,
    ):
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
        return PVSystem.from_steadyweb_config(new_pvsystem_config)

    def _to_steadyweb_dict(self):
        model_dict = self.model_dump(mode="json")
        expert_params_dict = model_dict.pop("expert_params")
        return {**model_dict, **expert_params_dict}

    def save_changes(self):
        steadyweb_patch_config = self._to_steadyweb_dict()
        return SteadysunAPI().patch(f"pvsystem/{str(self.uuid)}/", data=steadyweb_patch_config)

    def delete(self):
        """Delete the pvsystem (WARNING: this action is irreversible)"""
        return SteadysunAPI().delete(f"pvsystem/{str(self.uuid)}/")


def get_pvsystem_uuids():
    """Get all your pvsystems (accessible with the given token)"""
    response = SteadysunAPI().get_list("pvsystem/", page_limit=100, get_all_pages=True)
    uuids_name_dict = {pv_details["uuid"]: pv_details["name"] for pv_details in response.get("results", [])}
    return uuids_name_dict
