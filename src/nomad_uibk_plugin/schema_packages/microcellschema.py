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

from typing import TYPE_CHECKING

import plotly.graph_objects as go
from nomad.config import config
from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
)
from nomad.datamodel.metainfo.basesections import (
    # Collection,
    CompositeSystem,
    CompositeSystemReference,
    # Entity,
    Measurement,
)
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

from nomad_uibk_plugin.schema_packages import UIBKCategory
from nomad_uibk_plugin.schema_packages.XRFschema import XRFResult

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

configuration = config.get_plugin_entry_point(
    'nomad_uibk_plugin.schema_packages:microcellschema',
)
m_package = SchemaPackage(name='microcellschema')


class Image(ArchiveSection):
    m_def = Section(label_quantity='file_name')

    file_name = Quantity(type=str, a_eln=dict(component='StringEditQuantity'))


class MicroscopeMeasurement(Measurement):
    """ "Base class for microscope measurements."""

    images = SubSection(section_def=Image, label_quantity='file_name', repeats=True)


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


class UIBKSample(CompositeSystem, EntryData, PlotSection):
    """
    Represents a sample.
    """

    m_def = Section(
        categories=[UIBKCategory],
        label='Sample',
        a_eln=ELNAnnotation(
            lane_width='600px',
        ),
        a_template=dict(
            measurement_identifiers=dict(),
        ),
    )

    # Measurements on whole sample
    xrf_measurement = SubSection(section_def=XRFResult)
    ifm_measurement = SubSection(section_def=IFMResult)

    # def get_microcell_positions(self):
    #     if self.microcells:
    #         list_of_positions = [microcell.position for microcell in self.microcells]
    #         x_values = [position[0] for position in list_of_positions]
    #         y_values = [position[1] for position in list_of_positions]
    #         return x_values, y_values
    #     else:
    #         return None, None

    def plot(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        from nomad.search import MetadataPagination, search

        query = {
            'section_defs.definition_qualified_name:all': [
                'nomad_uibk_plugin.schema_packages.microcellschema.MicroCell'
            ],
            'entry_references.target_entry_id:all': [archive.metadata.entry_id],
        }
        search_result = search(
            owner='all',
            query=query,
            pagination=MetadataPagination(page_size=1),
            user_id=archive.metadata.main_author.user_id,
        )
        references = []
        x_values = []
        y_values = []
        if search_result.pagination.total > 0:
            for result in search_result.data:
                entry_id = result['entry_id']
                upload_id = result['upload_id']
                reference = f'../../../{upload_id}/entry/id/{entry_id}'
                x, y = None, None
                for quantity in result['search_quantities']:
                    if quantity['path_archive'] == 'data.position.x':
                        x = quantity['float_value']
                    elif quantity['path_archive'] == 'data.position.y':
                        y = quantity['float_value']
                references.append(reference)
                x_values.append(x)
                y_values.append(y)
            logger.info(f'Found {len(references)} microcells')

        # Plotting the microcell positions
        fig = go.Figure(
            data=go.Scatter(
                x=x_values,
                y=y_values,
                mode='markers',
                marker=dict(color='#2A4CDF'),
                customdata=references,
                hovertemplate='<a href="%{customdata}">Link</a><extra></extra>',
            )
        )
        fig.update_layout(
            title='Sample Overview',
            template='plotly_white',
            hovermode='closest',
            dragmode='zoom',
        )
        plot_json = fig.to_plotly_json()
        plot_json['config'] = dict(scrollZoom=False)
        self.figures.append(
            PlotlyFigure(
                label='Sample Overview',
                figure=plot_json,
            )
        )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.figures = []
        self.plot(archive, logger)

        # x_values, y_values = self.get_microcell_positions()
        # if x_values and y_values:
        #     if len(x_values) == len(y_values):
        #         figure = px.scatter(x=x_values, y=y_values)
        #         figure.update_layout(
        #             title='MicroCell Overview',
        #             xaxis_title='X',
        #             yaxis_title='Y',
        #             showlegend=False,
        #         )

        #         self.figures = []
        #         self.figures.append(
        #             PlotlyFigure(
        #                 label='MicroCell Overview', figure=figure.to_plotly_json()
        #             )
        #         )
        #     else:
        #         logger.warn('Unequal number of x and y values in microcell positions')
        # else:
        #     logger.warn('No microcell positions found')


class UIBKSampleReference(CompositeSystemReference):
    """
    A section containing a reference to a sample.
    """

    m_def = Section(label_quantity='sample_id')
    reference = Quantity(
        type=UIBKSample,
        description='Reference to the sample',
        a_eln=ELNAnnotation(component='ReferenceEditQuantity', label='Sample'),
    )


class MicroCellPosition(ArchiveSection):
    """
    Represents the position of a microcell on the sample.
    For now its a unitless quantity starting at the top left of the sample.
    """

    m_def = Section()

    x = Quantity(
        type=float,
        description='X position of the microcell on the sample',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    y = Quantity(
        type=float,
        description='Y position of the microcell on the sample',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        super().normalize(archive, logger)


class MicroCell(CompositeSystem, EntryData):
    """
    Represents a microcell on the sample.
    """

    m_def = Section(categories=[UIBKCategory], label='MicroCell')

    position = SubSection(
        section_def=MicroCellPosition,
        description='Position (x,y) of the microcell on the sample',
    )

    sample = SubSection(
        section_def=UIBKSampleReference, description='Reference to the sample'
    )

    # Measurements on microcell level
    ebic_measurement = SubSection(section_def=EBICResult)
    sem_measurement = SubSection(section_def=SEMResult)
    iv_measurement = SubSection(section_def=IVResult)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger'):
        super().normalize(archive, logger)


m_package.__init_metainfo__()
