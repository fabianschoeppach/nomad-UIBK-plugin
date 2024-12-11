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

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger


def find_reference_by_id(
    target_id: str, target_type: str, archive: 'EntryArchive', logger: 'BoundLogger'
) -> str:
    """
    Extracts the target references from the metadata.

    Parameters:
        target_id: The ID of the target.
        target_type: The type of the target.
        archive: The archive containing the metadata.
        logger: The logger object.

    Returns:
        A reference to the target.
    """

    from nomad.search import search

    if target_id is None or target_type is None or archive is None:
        logger.warning('Target ID, target type, or archive not provided.')
        return None

    # search for target entry in database
    search_result = search(
        owner='all',
        query={
            'results.eln.sections:any': [target_type],
            'results.eln.lab_ids:any': [target_id],
        },
        user_id=archive.metadata.main_author.user_id,
    )

    # Logger checks
    if not search_result.data:
        logger.warning(f'{target_type} entry with {target_id} not found in database.')
        return None
    else:
        if len(search_result.data) > 1:
            logger.warning(
                f'Multiple {target_type} entries found for ID {target_id}.'
                f'Using the first one.'
            )

        # create reference string
        entry_id = search_result.data[0]['entry_id']
        upload_id = search_result.data[0]['upload_id']

        return f'../uploads/{upload_id}/archive/{entry_id}#data'
