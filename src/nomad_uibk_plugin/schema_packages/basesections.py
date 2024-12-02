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

# from typing import TYPE_CHECKING

from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections import (
    Process,
)
from nomad.metainfo import Quantity, SchemaPackage, SubSection

from nomad_uibk_plugin.schema_packages.sample import UIBKSampleReference

# if TYPE_CHECKING:
#     from nomad.datamodel.datamodel import EntryArchive
#     from structlog.stdlib import BoundLogger

m_package = SchemaPackage()


class UIBKProcess(Process):
    """Base class for UIBK processes which adds sample linking."""

    samples = SubSection(
        section_def=UIBKSampleReference,
        description='Reference to the sample.',
        repeats=True,
    )

    lab_id = Quantity(
        type=str,
        description='The lab ID of the process.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    # def normalize(self, archive: EntryArchive, logger: BoundLogger) -> None:

    #     from nomad.datamodel.context import ServerContext

    #     # TODO: check if statement
    #     if self.samples is None or self.samples == []:

    #         from nomad.search import MetadataPagination, search

    #         query = {'results.eln.lab_ids': self.lab_id}
    #         search_result = search(
    #             owner='all',
    #             query=query,
    #             pagination=MetadataPagination(page_size=1),
    #             user_id=archive.metadata.user_id, # TODO: check if this is correct
    #         )

    #         if search_result.pagination.total > 0:
    #             entry_id = search_result.data[0]['entry_id']
    #             upload_id = search_result.data[0]['upload_id']
    #             self.system = f'../uploads/{upload_id}/archive/{entry_id}#data'
    #             if search_result.pagination.total > 1:
    #                 logger.warn(
    #                     f'Found {search_result.pagination.total} entries with lab_id: '  # noqa: E501
    #                     f'"{self.lab_id}". Will use the first one found.'
    #                 )
    #         else:
    #             logger.warn(f'Found no entries with lab_id: "{self.lab_id}".')
    #     elif self.lab_id is None and len(self.samples) > 0:
    #         self.lab_id = self.samples[0].lab_id
    #     if self.name is None:
    #         self.name = self.lab_id


m_package.__init_metainfo__()
