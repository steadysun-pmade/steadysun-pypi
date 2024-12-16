import unittest

from steadysun.models.pvsystem import Array, ModuleMaterial, ModuleTechnology, PVSystemExpertParams, Racking


class TestPVSystem(unittest.TestCase):
    def test_enum_conversion(self):
        # Test Enum conversion
        self.assertEqual(ModuleTechnology.from_value(1), ModuleTechnology.standard)
        self.assertEqual(str(ModuleMaterial.monosi), "monosi")
        self.assertEqual(int(Racking.open_rack), 1)

    def test_array_model(self):
        # Test Array model instantiation
        array = Array(
            id=1,
            pvmodules_pdc0=400,
            orientation=180,
            inclination=25,
            module_technology=ModuleTechnology.standard,
            module_material=ModuleMaterial.monosi,
            racking=Racking.open_rack,
            module_type="glass_polymer",
            power_temp_coeff=-0.4,
        )
        self.assertEqual(array.id, 1)
        self.assertEqual(array.module_technology, ModuleTechnology.standard)
        self.assertEqual(array.module_material, ModuleMaterial.monosi)

    def test_pv_system_expert_params(self):
        # Test PVSystemExpertParams with minimal setup
        pv_system = PVSystemExpertParams(
            installation_date="2025-01-01",
            arrays=[],
        )
        self.assertEqual(pv_system.installation_date, "2025-01-01")
        self.assertEqual(len(pv_system.arrays), 0)
