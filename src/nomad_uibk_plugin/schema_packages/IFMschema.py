#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from typing import (
    TYPE_CHECKING,
)

from nomad.datamodel.data import EntryData  # ArchiveSection
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections import Entity, SectionReference
from nomad.datamodel.metainfo.eln import ELNAnalysis, ELNMeasurement
from nomad.datamodel.metainfo.workflow import Link
from nomad.metainfo import Datetime, MEnum, Quantity, SchemaPackage, Section, SubSection
from nomad_measurements.utils import (
    create_archive,
    get_entry_id_from_file_name,
    get_reference,
    merge_sections,
)
from pint import UnitRegistry

from nomad_uibk_plugin.schema_packages import UIBKCategory

if TYPE_CHECKING:
    from nomad.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

ureg = UnitRegistry()

m_package = SchemaPackage()


class IFMMeasurement(ELNMeasurement):
    """
    IFM Measurement entry.
    """

    m_def = Section(
        categories=[UIBKCategory],
        label='IFM Measurement',
    )

    image_file = Quantity(
        type=str,
        description='File containing the microscopy image.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )

    metadata_file = Quantity(
        type=str,
        description='File containing the measurement metadata.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )

    # Metadata Quantities
    start_time = Quantity(
        type=Datetime,
        description='The date and time when this process was started.',
        a_eln=dict(label='start time'),  # component='DateTimeEditQuantity'
    )

    end_time = Quantity(
        type=Datetime,
        description='The date and time when this process was finished.',
        a_eln=dict(label='end time'),
    )

    exposure_time = Quantity(
        type=float,
        description='Exposure time of the image.',
        unit='second',
        a_eln=ELNAnnotation(defaultDisplayUnit='µs'),
    )

    device = Quantity(
        type=str,
        description='Device used for the measurement.',
        a_eln=dict(label='measurement device'),
    )

    magnification = Quantity(
        type=float,
        description='Magnification used for the measurement.',
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        Read the metadata file and extract information from it.
        """
        super().normalize(archive, logger)
        self.method = 'IFM Measurement'

        if self.metadata_file is not None:
            logger.info('Metadata file recognized. Parsing...')

            from nomad_uibk_plugin.filereader.IFMreader import read_ifm_xml

            with archive.m_context.raw_file(self.metadata_file) as file:
                measurement = read_ifm_xml(file, archive, logger)
                merge_sections(self, measurement, logger)


class IFMModel(Entity, EntryData):
    """
    Model for the automated image analysis.
    """

    m_def = Section(
        categories=[UIBKCategory],
        label='IFM Model',
    )

    file = Quantity(
        type=str,
        description='File containing the data.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )

    # Metadata Quantities
    type = Quantity(
        type=MEnum('binary', 'classification'), description='Type of the model.'
    )

    number_of_layers = Quantity(
        type=int,
        description='Number of layers in the model.',
    )

    number_of_parameters = Quantity(
        type=int,
        description='Number of parameters in the model.',
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        """
        Read the model file and extract the metadata.
        """
        super().normalize(archive, logger)
        self.method = 'IFM Model'

        if self.file is not None:
            logger.info('Model file recognized. Parsing...')

            from nomad_uibk_plugin.filereader.IFMreader import read_keras_metadata

            with archive.m_context.raw_file(self.file, 'rb') as file:
                model = read_keras_metadata(file, archive, logger)
                merge_sections(self, model, logger)


class IFMAnalysisOutput(EntryData):
    file = Quantity(
        type=str,
        description='File containing the data.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )


class IFMAnalysedImage(IFMAnalysisOutput):
    pass


class IFMExtractedFeatures(IFMAnalysisOutput):
    pass


class ImageReference(SectionReference):
    reference = Quantity(
        type=IFMMeasurement,
        description='Reference to the IFM measurement.',
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
            label='section reference',
        ),
    )


class ModelReference(SectionReference):
    reference = Quantity(
        type=IFMModel,
        description='Reference to the IFM model.',
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
            label='section reference',
        ),
    )


class OutputReference(SectionReference):
    reference = Quantity(
        type=IFMAnalysisOutput,
        description='Reference to the IFM analysis output.',
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
            label='section reference',
        ),
    )


class IFMTwoStepAnalysis(ELNAnalysis):
    """
    Automated image analysis entry.
    """

    m_def = Section(
        categories=[UIBKCategory],
        label='IFM Two Step Analysis',
    )

    inputs = SubSection(
        section_def=ImageReference,
        description='Input data for the automated image analysis.',
        repeats=True,
    )
    outputs = SubSection(
        section_def=OutputReference,
        description='Output data from the automated image analysis.',
        repeats=True,
    )
    model_binary = SubSection(
        section_def=ModelReference,
        description='Model for the automated image analysis.',
    )
    model_classiciation = SubSection(
        section_def=ModelReference,
        description='Model for the automated image analysis.',
    )

    # Execution Quantity
    perform_analysis = Quantity(
        type=bool,
        description=(
            'Check box to trigger the automated image analysis after assigning '
            'the measurement(s) and the two models.'
        ),
        default=False,
        a_eln=ELNAnnotation(component=ELNComponentEnum.BoolEditQuantity),
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        super().normalize(archive, logger)
        self.method = 'IFM Two Step Analysis'

        # workflow linking
        if self.model_binary:
            archive.workflow2.inputs.append(
                Link(name='Binary Model', section=self.model_binary.reference)
            )
        if self.model_classiciation:
            archive.workflow2.inputs.append(
                Link(
                    name='Classification Model',
                    section=self.model_classiciation.reference,
                )
            )

        if self.inputs and self.model_binary and self.model_classiciation:
            logger.info(
                'Two Models found. Ready for IFM Two Step Analysis normalization'
            )

            self.outputs = []
            for input in self.inputs:
                # here we execute Georgs code to extract the defects
                with (
                    archive.m_context.raw_file(
                        input.reference.image_file
                    ) as image_file,
                    archive.m_context.raw_file(
                        self.model_binary.reference.file
                    ) as model_binary,
                    archive.m_context.raw_file(
                        self.model_classiciation.reference.file
                    ) as model_classiciation,
                ):
                    # create paths and names for the csv file and archive file
                    path, filename_with_ext = os.path.split(image_file.name)
                    filename, ext = os.path.splitext(filename_with_ext)
                    csv_path = os.path.join(path, f'{filename}_prediction.csv')
                    csv_archive_name = f'{filename}_prediction.archive.json'

                    if self.perform_analysis and not os.path.exists(csv_path):
                        logger.info('Performing the analysis...')
                        from ifm_image_defect_detection.defectRecognition_toCSV import (
                            defect_recognition,
                        )

                        defect_recognition(
                            image_file.name, model_binary.name, model_classiciation.name
                        )

                        feature_entry = IFMExtractedFeatures(file=csv_path)
                        create_archive(feature_entry, archive, csv_archive_name)

                    output_reference = OutputReference(
                        reference=get_reference(
                            archive.metadata.upload_id,
                            get_entry_id_from_file_name(csv_archive_name, archive),
                        )
                    )
                    self.outputs.append(output_reference)

                    archive.workflow2.outputs.append(
                        Link(
                            name='Extracted Features',
                            section=output_reference.reference,
                        )
                    )

                self.perform_analysis = False


m_package.__init_metainfo__()
