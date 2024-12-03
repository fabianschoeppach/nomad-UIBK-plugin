from typing import TYPE_CHECKING

from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.metainfo import Quantity
from nomad.parsing.parser import MatchingParser
from nomad_measurements.utils import (
    create_archive,
    get_entry_id_from_file_name,
    get_reference,
)

from nomad_uibk_plugin.schema_packages.sputtering import UIBKSputterDeposition

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger


class RawFileSputterData(EntryData):
    """
    Section for a sputter deposition data file.
    """

    measurement = Quantity(
        type=UIBKSputterDeposition,
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
        ),
    )


class SputterParser(MatchingParser):
    """
    Parser for matching sputter deposition files and creating instances of
    SputterDeposition.
    """

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        logger.info('SputterParser.parse')
        filename = mainfile.split('/')[-1]
        # entry = UIBKSputterDeposition.m_from_dict(
        #     UIBKSputterDeposition.m_def.a_template
        # )
        entry = UIBKSputterDeposition()
        entry.data_file = filename
        archive_name = f'{"".join(filename.split(".")[:-1])}.archive.json'
        archive.data = RawFileSputterData(
            measurement=get_reference(
                archive.metadata.upload_id,
                get_entry_id_from_file_name(archive_name, archive),
            )
        )
        create_archive(entry, archive, archive_name)
