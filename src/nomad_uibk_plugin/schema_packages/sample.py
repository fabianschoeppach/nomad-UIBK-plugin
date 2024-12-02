from typing import TYPE_CHECKING

import plotly.graph_objects as go
from nomad.datamodel.data import (
    EntryData,  # ArchiveSection,
)
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections import (
    CompositeSystem,
    CompositeSystemReference,
)
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger


m_package = SchemaPackage()


class MicroCell(CompositeSystem):
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


class MicroCellArray(CompositeSystem):
    cells = SubSection(section_def=MicroCell, repeats=True)

    create_array = Quantity(
        type=bool,
        default=False,
        a_eln=ELNAnnotation(component=ELNComponentEnum.BoolEditQuantity),
    )

    array_x = Quantity(
        type=int,
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )

    array_y = Quantity(
        type=int,
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        if self.create_array:
            for x in range(1, self.array_x + 1):
                for y in range(1, self.array_y + 1):
                    self.cells.append(
                        MicroCell(x=x, y=y, name=f'Cell {str(x)} {str(y)}')
                    )
            self.create_array = False


class UIBKSample(CompositeSystem, EntryData, PlotSection):
    m_def = Section()

    arrays = SubSection(section_def=MicroCellArray, repeats=True)

    def plot(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        x_values, y_values = self.list_microcell_positions(
            archive.data.arrays[0], logger
        )
        fig = go.Figure(
            data=go.Scatter(
                x=x_values,
                y=y_values,
                mode='markers',
                marker=dict(color='#2A4CDF', size=10),
            )
        )
        annotations = []
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            annotations.append(
                dict(
                    x=x,
                    y=y,
                    # text=f'<a href="{url}">MicroCell {int(x)}-{int(y)}</a>',
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-20,
                )
            )
        fig.update_layout(
            title='Sample Overview',
            template='plotly_white',
            # hovermode='closest',
            dragmode=False,
            annotations=annotations,
            # clickmode='event+select',
        )
        plot_json = fig.to_plotly_json()
        plot_json['config'] = dict(
            scrollZoom=False,
        )
        self.figures.append(
            PlotlyFigure(
                label='Sample Overview',
                figure=plot_json,
            )
        )

    def list_microcell_positions(self, array, logger: 'BoundLogger'):
        x_values, y_values = [], []
        for cell in array.cells:
            x_values.append(cell.x)
            y_values.append(cell.y)
        return x_values, y_values

        # x_values = list(range(1, array.array_x + 1))
        # y_values = list(range(1, array.array_y + 1))
        # x_values, y_values = zip(
        #     *product(range(1, array.array_x + 1), range(1, array.array_y + 1))
        # )
        # return x_values, y_values

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        self.figures = []
        self.plot(archive, logger)


class UIBKSampleReference(CompositeSystemReference):
    """
    Reference section to an UIBK sample.
    """

    reference = Quantity(
        type=UIBKSample,
        description='Reference to an UIBK sample',
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
            label='Link to Sample',
        ),
    )


m_package.__init_metainfo__()
