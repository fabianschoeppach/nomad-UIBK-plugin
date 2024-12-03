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

# import numpy as np
from nomad_uibk_plugin.schema_packages.sputtering import (
    SputterParameters,
    UIBKSputterDeposition,
)

if TYPE_CHECKING:
    from structlog.stdlib import (
        BoundLogger,
    )


def read_sputter_csv(
    file_path: str, logger: 'BoundLogger' = None
) -> UIBKSputterDeposition:
    """
    Read the sputter deposition data from a .csv file and return an instance of
    UIBKSputterDeposition.
    """

    # with open(file_path, 'r') as file:
    #     lines = file.readlines()

    # # Split sections
    # in_metadata = True
    # metadata = {}
    # time_series_lines = []
    # for line in lines:
    #     # skip commented lines
    #     if line.startswith("%") or line.startswith("#"):
    #         continue

    #     line = line.strip()
    #     # skip empty lines
    #     if not line:
    #         continue
    #     if line == "END_OF_PARAMETERS":
    #         in_metadata = False
    #         continue

    #     # Split metadata and time series
    #     if in_metadata:
    #         key, *values = line.split(';')
    #         key = key.strip()
    #         values = [v.strip() for v in values if v.strip()]
    #         metadata[key] = values
    #     else:
    #         time_series_lines.append(line)

    deposition = UIBKSputterDeposition(
        name='TESTTESTTEST',
    )

    # Parse metadata
    # TODO: Implement metadata parsing

    # Parse time series
    # TODO: Implement time series parsing

    deposition.parameters = SputterParameters(test='HUHU!')
    deposition.samples = []

    return deposition
