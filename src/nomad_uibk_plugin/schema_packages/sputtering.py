from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.basesections import SectionReference
from nomad.metainfo import Quantity, Section, SubSection
from nomad_material_processing.vapor_deposition.pvd.general import PVDSource
from nomad_material_processing.vapor_deposition.pvd.sputtering import SputterDeposition

from nomad_uibk_plugin.schema_packages import UIBKCategory
from nomad_uibk_plugin.schema_packages.sample import UIBKSample


class Target(PVDSource, EntryData):
    pass

class TargetReference(SectionReference):
    reference = Quantity(
        type=Target,
        a_eln=dict(component='ReferenceEditQuantity')
    )

class SputterParameters(ArchiveSection):
    pass

class UIBKSputterDeposition(SputterDeposition, EntryData):

    m_def = Section(
        categories=[UIBKCategory],
        label = 'Sputter Deposition',
    )

    samples = SubSection(section_def = UIBKSample, repeats=True)

    target = SubSection(section_def = TargetReference, repeats=True)

    parameter = SubSection()
