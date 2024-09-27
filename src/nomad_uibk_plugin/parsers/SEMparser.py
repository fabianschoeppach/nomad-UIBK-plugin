from typing import TYPE_CHECKING

from nomad.config import config
from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Quantity
from nomad.parsing.parser import MatchingParser
from nomad_measurements.utils import create_archive

from nomad_uibk_plugin.schema_packages.SEMschema import SEM

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

configuration = config.get_plugin_entry_point('nomad_uibk_plugin.parsers:semparser')


class RawFileSEMData(EntryData):
    """
    Section for an SEM data file.
    """

    measurement = Quantity(
        type=SEM,
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
        ),
    )


class XRFParser(MatchingParser):
    """
    Parser for matching SEM files and creating instances of SEM.
    """

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        logger.info('SEMParser.parse')
        data_file = mainfile.split('/')[-1]
        entry = SEM.m_from_dict(SEM.m_def.a_template)
        entry.data_file = data_file
        file_name = f'{"".join(data_file.split(".")[:-1])}.archive.json'
        archive.data = RawFileSEMData(
            measurement=create_archive(entry, archive, file_name)
        )
        archive.metadata.entry_name = f'{data_file} data file'
