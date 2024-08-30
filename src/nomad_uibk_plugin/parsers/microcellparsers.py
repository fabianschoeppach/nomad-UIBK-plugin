import os
from typing import (
    TYPE_CHECKING,
)

from nomad.config import config
from nomad.datamodel import EntryArchive
from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.datamodel.metainfo.basesections import Entity
from nomad.metainfo import Quantity
from nomad.parsing.parser import MatchingParser
from nomad_measurements.utils import (
    create_archive,
    get_entry_id_from_file_name,
    get_reference,
)

from nomad_uibk_plugin.schema_packages.microcellschema import (
    UIBKSample,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger


configuration = config.get_plugin_entry_point(
    'nomad_uibk_plugin.parsers:ifmparser',
)


def parse_filename(file_name: str) -> dict:
    """ """

    microcell_coordinates = (0, 0)

    file_name_particles = file_name.split('_')
    for particle in file_name_particles:
        if '-' in particle:
            if len(particle.split('-')) == 2:  # noqa: PLR2004
                microcell_coordinates = tuple(map(int, particle.split('-')))

    sample_id = name = file_name_particles[0]

    return {
        'name': name,
        'sample_id': sample_id,
        'microcell_coordinates': microcell_coordinates,
    }


class RawFile(EntryData):
    """
    Section which contains any raw data file.
    """

    processed_archive = Quantity(
        type=Entity,
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
        ),
    )


class EBICParser(MatchingParser):
    """
    Parser for matching EBIC files.
    """

    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        if logger:
            logger.info('EBICParser.parse executed')
        else:
            print('EBICParser.parse executed')

        # handle file name
        # .volumes/fs/staging/Tp/TpW_A6wmQbuia_oVdwLqng/raw/20231115_A1_2m.tiff
        mainfile_split = os.path.basename(mainfile).split('.')
        mainfile_name, mainfile_ext = mainfile_split[0], mainfile_split[-1]
        # details = parse_filename(mainfile_name)

        # case decision based on file extension
        if mainfile_ext in ['tif', 'tiff']:
            entry = UIBKSample()
            archive.metadata.entry_name = f'{mainfile_name} data file'

            # create archive and reference the raw data file to it
            filename = f'{mainfile_name}.archive.json'
            entry_id = get_entry_id_from_file_name(filename, archive)
            archive.data = RawFile(
                processed_archive=get_reference(archive.metadata.upload_id, entry_id)
            )
            create_archive(entry, archive, filename)

        elif logger:
            logger.warn(f'File extension {mainfile_ext} not supported')
        else:
            print(f'File extension {mainfile_ext} not supported')


class IFMParser(MatchingParser):
    """
    Parser for matching IFM files.
    """

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        if logger:
            logger.info('IFMParser.parse executed')
        else:
            print('IFMParser.parse executed')

        # case decision based on file extension
        # .volumes/fs/staging/Tp/TpW_A6wmQbuia_oVdwLqng/raw/20231115_A1_2m.tiff
        mainfile_split = os.path.basename(mainfile).split('.')
        mainfile_name, mainfile_ext = mainfile_split[0], mainfile_split[-1]

        if mainfile_ext in ['tif', 'tiff']:
            # data_file = mainfile_name
            # entry = UIBKSample.m_from_dict(UIBKSample.m_def.a_template)
            entry = UIBKSample()
            # entry.ifm_measurement = IFMResult()
            # entry.ifm_measurement.data_file = file_name
            # file_name = f'{"".join(file_name.split(".")[:-1])}.archive.json'
            # archive.data = RawFileTIFF(
            #     measurement=create_archive(entry, archive, file_name)
            # )
            archive.metadata.entry_name = f'{mainfile_name} data file'

            # create archive and reference the raw data file to it
            filename = f'{mainfile_name}.archive.json'
            entry_id = get_entry_id_from_file_name(filename, archive)
            archive.data = RawFile(
                processed_archive=get_reference(archive.metadata.upload_id, entry_id)
            )
            create_archive(entry, archive, filename)

        elif logger:
            logger.warn(f'File extension {mainfile_ext} not supported')
        else:
            print(f'File extension {mainfile_ext} not supported')
