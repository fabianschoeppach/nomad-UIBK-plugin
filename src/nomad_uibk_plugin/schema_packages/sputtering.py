from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.metainfo import Section, SubSection  #Quantity
from nomad_material_processing.vapor_deposition.pvd.general import PVDSource
from nomad_material_processing.vapor_deposition.pvd.sputtering import SputterDeposition

from nomad_uibk_plugin.schema_packages import UIBKCategory
from nomad_uibk_plugin.schema_packages.sample import UIBKSample


class SputterSource(PVDSource, ArchiveSection):
    pass

class SputterParameters(ArchiveSection):
    pass

class UIBKSputterDeposition(SputterDeposition, EntryData):

    m_def = Section(
        categories=[UIBKCategory],
        label = 'Sputter Deposition',
    )

    samples = SubSection(section_def = UIBKSample, repeats=True)