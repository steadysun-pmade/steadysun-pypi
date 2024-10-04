from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, field_validator


# pylint: disable=invalid-name
class EnumIntStr(Enum):
    @classmethod
    def from_value(cls, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, int):
            return cls(value)
        if isinstance(value, str):
            return cls[value]
        raise ValueError(f"Invalid value '{value}' for {cls.__name__}")

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value


class ModuleTechnology(EnumIntStr):
    standard = 1
    bifacial = 2


class ModuleMaterial(EnumIntStr):
    monosi = 1
    cigs = 2
    asi = 3
    cdte = 4
    xsi = 5
    multisi = 6
    polysi = 7


class Racking(EnumIntStr):
    open_rack = 1
    close_mount = 2
    insulated_back = 3


class PVType(EnumIntStr):
    fixed = 1
    single_axis = 2
    double_axis = 3


class ModuleType(EnumIntStr):
    glass_polymer = 1
    glass_glass = 2


class TimestampInterval(EnumIntStr):
    left = 1
    right = 2
    centered = 3


class DecompositionModel(EnumIntStr):
    disc = 1
    dirindex = 2
    engerer2 = 3


class TranspositionModel(EnumIntStr):
    haydavies = 1


class SpectralModel(EnumIntStr):
    yes = 1
    no = 2


class AoiModel(EnumIntStr):
    ashrae = 1
    sapm = 2


class TypeCheckingBaseModel(BaseModel):
    class Config:
        validate_assignment = True


class Array(TypeCheckingBaseModel):
    id: int
    pvmodules_pdc0: float
    orientation: float
    inclination: float
    module_technology: ModuleTechnology
    module_material: ModuleMaterial
    racking: Racking
    module_type: ModuleType
    power_temp_coeff: float

    @field_validator("module_technology", "module_material", "racking", "module_type", mode="before")
    @classmethod
    def convert_enum(cls, v, field):
        enum_class = cls.model_fields[field.field_name].annotation
        if isinstance(v, enum_class):
            return v
        return enum_class.from_value(v)


class TrackerConfig(TypeCheckingBaseModel):
    max_angle: float
    backtrack: bool
    gcr: float
    slope_azimuth: float
    slope_tilt: float


class BifacialConfig(TypeCheckingBaseModel):
    bifaciality: float
    gcr: float
    pvrow_height: float
    pvrow_width: float


class InverterParameters(TypeCheckingBaseModel):
    pdc0: float
    eta_inv_nom: float  # FIXME check nom vs norm (get vs patch)


class Irradiances(TypeCheckingBaseModel):
    timestamp_interval: TimestampInterval
    decomposition_model: DecompositionModel
    transposition_model: TranspositionModel
    spectral_model: SpectralModel
    aoi_model: AoiModel
    albedo: float
    self_shading: bool


class LossesParameters(TypeCheckingBaseModel):
    wiring: float
    lid: float
    nameplate_rating: float
    mismatch: float
    soiling: float
    snow: float
    shading: float
    availability: float
    connections: float
    age: float
    aging: float
    aging_auto_compute: bool


class PVSystemExpertParams(TypeCheckingBaseModel):
    installation_date: str
    arrays: List[Array]
    tracker_config: Optional[TrackerConfig] = None
    bifacial_config: Optional[BifacialConfig] = None
    inverter_parameters: Optional[InverterParameters] = None
    irradiances: Optional[Irradiances] = None
    losses_parameters: Optional[LossesParameters] = None
    # horizon ?
    # correction_... ?
    # apply_clearsky_correction ?
    # temperature_model
    # apply_topography_mask
    # autocalibrate
    # pdc0
