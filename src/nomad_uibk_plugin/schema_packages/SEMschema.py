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

from typing import (
    TYPE_CHECKING,
)

from structlog.stdlib import BoundLogger

if TYPE_CHECKING:
    pass

from typing import (
    TYPE_CHECKING,
)

from nomad.config import config
from nomad.datamodel.data import (
    ArchiveSection,
    EntryData,
)
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
)
from nomad.datamodel.metainfo.basesections import (
    Measurement,
)
from nomad.metainfo import Quantity, SchemaPackage, Section
from nomad_measurements import (
    NOMADMeasurementsCategory,
)

if TYPE_CHECKING:
    pass

configuration = config.get_plugin_entry_point(
    'nomad_uibk_plugin.schema_packages:semschema'
)

m_package = SchemaPackage(name='nomad_sem')


class SEMSettings(ArchiveSection):
    """
    Section containing the settings for an SEM measurement.
    """

    pass


class SEM(Measurement, EntryData):
    """
    Section for SEM measurements.
    """

    m_def = Section(
        categories=[NOMADMeasurementsCategory],
        label='Scanning Electron Microscopy (SEM)',
        a_eln=ELNAnnotation(
            lane_width='600px',
        ),
        a_template=dict(measurement_identifiers=dict()),
    )

    data_file = Quantity(
        type=str,
        description='Name of the data file containing the SEM data.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.FileEditQuantity,
        ),
    )

    def normalize(self, archive, logger: BoundLogger) -> None:
        return super().normalize(archive, logger)


m_package.__init_metainfo__()
