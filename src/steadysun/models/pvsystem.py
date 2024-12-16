from typing import List, Optional

from pydantic import field_validator

from steadysun.models._utils import EnumIntStr, TypeCheckingBaseModel


class ModuleTechnology(EnumIntStr):
    """PV - Module technology types"""

    standard = 1
    bifacial = 2


class ModuleMaterial(EnumIntStr):
    """PV - Module material types"""

    monosi = 1
    cigs = 2
    asi = 3
    cdte = 4
    xsi = 5
    multisi = 6
    polysi = 7


class Racking(EnumIntStr):
    """PV - Racking types"""

    open_rack = 1
    close_mount = 2
    insulated_back = 3


class PVType(EnumIntStr):
    """PV - PV system types"""

    fixed = 1
    single_axis = 2
    double_axis = 3


class ModuleType(EnumIntStr):
    """PV - Module types"""

    glass_polymer = 1
    glass_glass = 2


class TimestampInterval(EnumIntStr):
    """PV - Timestamp intervals"""

    left = 1
    right = 2
    centered = 3


class DecompositionModel(EnumIntStr):
    """PV - Decomposition models"""

    disc = 1
    dirindex = 2
    engerer2 = 3


class TranspositionModel(EnumIntStr):
    """PV - Transposition models"""

    haydavies = 1


class SpectralModel(EnumIntStr):
    """PV - Spectral models"""

    yes = 1
    no = 2


class AoiModel(EnumIntStr):
    """PV - Angle-of-incidence models."""

    ashrae = 1
    sapm = 2


class Array(TypeCheckingBaseModel):
    """Represents an array of PV modules in a PV system."""

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
        """Convert a value to its corresponding enum type."""
        enum_class = cls.model_fields[field.field_name].annotation
        if isinstance(v, enum_class):
            return v
        return enum_class.from_value(v)


class TrackerConfig(TypeCheckingBaseModel):
    """Configuration for a tracker system."""

    max_angle: float
    backtrack: bool
    gcr: float
    slope_azimuth: float
    slope_tilt: float


class BifacialConfig(TypeCheckingBaseModel):
    """Configuration for a bifacial PV system."""

    bifaciality: float
    gcr: float
    pvrow_height: float
    pvrow_width: float


class InverterParameters(TypeCheckingBaseModel):
    """Parameters for an inverter in a PV system."""

    pdc0: float
    eta_inv_nom: float  # FIXME check nom vs norm (get vs patch)


class Irradiances(TypeCheckingBaseModel):
    """Irradiance-related parameters for a PV system."""

    timestamp_interval: TimestampInterval
    decomposition_model: DecompositionModel
    transposition_model: TranspositionModel
    spectral_model: SpectralModel
    aoi_model: AoiModel
    albedo: float
    self_shading: bool


class LossesParameters(TypeCheckingBaseModel):
    """Losses parameters for a PV system."""

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
    """Expert-level configuration parameters for a PV system."""

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
