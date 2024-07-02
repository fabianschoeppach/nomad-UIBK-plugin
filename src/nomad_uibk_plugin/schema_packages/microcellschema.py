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

import plotly.express as px
from nomad.config import config
from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
)
from nomad.datamodel.metainfo.measurements import Sample
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

from nomad_uibk_plugin.schema_packages.XRFschema import XRFResult

configuration = config.get_plugin_entry_point(
    'nomad_uibk_plugin.schema_packages:microcellschema',
)
m_package = SchemaPackage()


class SEMResult(ArchiveSection):
    """ """

    data_file = Quantity(
        type=str,
        description='Path to the SEM image file',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )


class EBICResult(ArchiveSection):
    """ """

    data_file = Quantity(
        type=str,
        description='Path to the EBIC image file',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )


class IVResult(ArchiveSection):
    """ """

    data_file = Quantity(
        type=str,
        description='Path to the IV file',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )


class IFMResult(ArchiveSection):
    """ """

    data_file = Quantity(
        type=str,
        description='Path to the IFM image file',
        a_eln=ELNAnnotation(component=ELNComponentEnum.FileEditQuantity),
    )


class MicroCell(Sample):
    """
    Represents a microcell on the sample.
    """

    position = Quantity(
        type=float,
        shape=[2],
        description='Position of the microcell on the sample',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )

    # Measurements on microcell level
    ebic_measurement = SubSection(section_def=EBICResult)
    sem_measurement = SubSection(section_def=SEMResult)
    iv_measurement = SubSection(section_def=IVResult)

    # def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
    #     super().normalize()


class MySample(Sample, EntryData, PlotSection):
    """
    Represents a sample.
    """

    m_def = Section(
        categories=[],
        label='MicroCell Sample',
        a_eln=ELNAnnotation(
            lane_width='600px',
        ),
        a_template=dict(
            measurement_identifiers=dict(),
        ),
    )

    # MicroCells
    microcells = SubSection(
        section_def=MicroCell,
        description='List of MicroCells on the sample',
        repeats=True,
    )

    # Measurements on whole sample
    xrf_measurement = SubSection(section_def=XRFResult)
    ifm_measurement = SubSection(section_def=IFMResult)

    def get_microcell_positions(self):
        list_of_positions = [microcell.position for microcell in self.microcells]
        x_values = [position[0] for position in list_of_positions]
        y_values = [position[1] for position in list_of_positions]
        return x_values, y_values

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        x_values, y_values = self.list_of_positions()
        figure = px.scatter(x=x_values, y=y_values)
        self.figures = []
        self.figures.append(PlotlyFigure(label='test', figure=figure.to_plotly_json()))


m_package.__init_metainfo__()
