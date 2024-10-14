from nomad.datamodel.data import EntryData  #ArchiveSection,
from nomad.datamodel.metainfo.basesections import (
    CompositeSystem,  #CompositeSystemReference
)
from nomad.metainfo import Section


class UIBKSample(CompositeSystem, EntryData):
    m_def = Section()