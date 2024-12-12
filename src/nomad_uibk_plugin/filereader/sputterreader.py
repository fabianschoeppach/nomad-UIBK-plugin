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

from datetime import datetime
from typing import TYPE_CHECKING, TextIO

import numpy as np
import pandas as pd
from pint import errors

from nomad_uibk_plugin.schema_packages.basesections import (
    Current,
    GasFlow,
    Power,
    Pressure,
    Voltage,
)
from nomad_uibk_plugin.schema_packages.sputtering import (
    Atmosphere,
    TargetReference,
    UIBKSputterDeposition,
    ureg,
)
from nomad_uibk_plugin.utils import find_reference_by_id

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger


def read_sputter_deposition(
    file_obj: 'TextIO', archive: 'EntryArchive' = None, logger: 'BoundLogger' = None
) -> UIBKSputterDeposition:
    """
    Read the sputter deposition data from a .csv file and return an instance of
    UIBKSputterDeposition.

    Parameters:
        file_obj: A file-like object containing the sputter CSV data.
        logger: A logger instance for logging errors or warnings.
    """

    # Read metadata and time series data
    metadata, dataframe = read_csv_file(file_obj, logger)

    # Create a new UIBKSputterDeposition instance
    deposition = UIBKSputterDeposition(
        name=metadata.get('Process Name', ['Untitled Process'])[0],
        datetime=metadata.get('Start Time', None),
        description=metadata.get('Comment', None),
        distance_to_target=metadata.get('Distance Target Substrate', None),
        substrate_rotation=metadata.get('Substrate Retainer Speed', None),
    )

    # Parse atmosphere
    deposition.atmosphere = Atmosphere(
        pressure=Pressure(
            value=dataframe['Pressure'],
            time=dataframe['time'],
            set_value=[metadata.get('Process Pressure Pfeiffer', np.nan)],
        ),
        Ar=GasFlow(
            value=dataframe['Ar_Flow'],
            time=dataframe['time'],
            set_value=[metadata.get('Ar set point', np.nan)],
        ),
        O2=GasFlow(
            value=dataframe['O2'],
            time=dataframe['time'],
            set_value=[metadata.get('O2 set point', np.nan)],
        ),
        N2=GasFlow(
            value=dataframe['N2'],
            time=dataframe['time'],
            set_value=[metadata.get('N2 set point', np.nan)],
        ),
    )

    # Parse target references
    deposition.target_left, deposition.target_right = parse_target_references(
        metadata, dataframe, archive, logger
    )

    return deposition


def read_csv_file(
    file_obj: 'TextIO', logger: 'BoundLogger'
) -> tuple[dict, pd.DataFrame]:
    """
    Read the metadata and time series data from a CSV file and return them as
    a dictionary and a pandas DataFrame, respectively.
    """

    # Split sections

    metadata = {}
    start_line_time_series = None

    for num, raw_line in enumerate(file_obj):
        line = raw_line.strip()

        # skip commented lines and empty lines
        if line.startswith('%') or line.startswith('#'):
            continue
        if not line:
            continue

        # detect end of metadata
        if 'END_OF_PARAMETERS' in line:
            start_line_time_series = num + 1
            break

        # write metadata to dictionary
        key, *values = line.split(',')
        values = [v.strip() for v in values if v.strip()]
        if len(values) > 0:
            if len(values) == 2:  # noqa: PLR2004
                # try parsing data as quanitity (number + unit)
                try:
                    number = float(values[0])
                    unit = values[1]
                    unit = unit.replace('mBar', 'millibar')
                    unit = unit.replace('sccm', 'cm^3/minute')
                    unit = ureg(unit)
                    metadata[key.strip()] = number * unit
                except (ValueError, errors.UndefinedUnitError):
                    metadata[key.strip()] = values
            else:
                metadata[key.strip()] = values

    # construct time series dataframe
    if start_line_time_series is None:
        logger.error('No time series data found in file.')
        return None
    else:
        file_obj.seek(0)
        raw_df = pd.read_csv(file_obj, skiprows=range(start_line_time_series))

        # drop rows with all NaN values and rows starting with '%'
        dataframe = raw_df.dropna(how='all')
        dataframe = dataframe[~dataframe['Time_Stamp'].str.startswith('%')]

        # convert to datetime and calculate time in seconds
        dataframe['Time_Stamp'] = pd.to_datetime(
            dataframe['Time_Stamp'], format='%Y-%m-%d_%H:%M:%S.%f'
        )
        dataframe['time'] = (
            dataframe['Time_Stamp'] - dataframe['Time_Stamp'].iloc[0]
        ).dt.total_seconds()

        # convert quanitites with proper units

    # Clean up metadata
    if 'Start Time' in metadata:
        metadata['Start Time'] = datetime.strptime(
            metadata['Start Time'][0], '%Y-%m-%d_%H-%M'
        )

    # Comment
    if 'Comment' in metadata:
        metadata['Comment'] = ','.join(metadata['Comment'])

    return metadata, dataframe


def parse_target_references(
    metadata: dict,
    dataframe: pd.DataFrame,
    archive: 'EntryArchive',
    logger: 'BoundLogger',
) -> tuple[TargetReference, TargetReference]:
    """
    Parse the target references from the metadata and time series data and return
    them as TargetReference instances.

    Parameters:
        metadata: A dictionary containing the metadata.
        dataframe: A pandas DataFrame containing the time series data.
        archive: The archive containing the metadata.
        logger: A logger instance for logging errors or warnings.

    Returns:
        A tuple of TargetReference instances for the left and right target.
    """

    # For now: Left = 1, Right = 2
    # TODO: Reading which target is left and which is right from metadata

    target_left = None
    target_right = None

    # Left target
    target_left_id = metadata.get('Target Left', [None])[0]
    target_left = TargetReference(
        reference=find_reference_by_id(target_left_id, 'Target', archive, logger),
        power=Power(value=dataframe['P1_Watt'], time=dataframe['time']),
        voltage=Voltage(value=dataframe['P1_Ampere'], time=dataframe['time']),
        current=Current(value=dataframe['P1_Voltage'], time=dataframe['time']),
    )
    setpoint = metadata.get('Setpoint 1', None)
    if setpoint:
        if setpoint.dimensionality == ureg.W.dimensionality:
            target_left.power.set_value = [setpoint]
        elif setpoint.dimensionality == ureg.A.dimensionality:
            target_left.current.set_value = [setpoint]
        elif setpoint.dimensionality == ureg.V.dimensionality:
            target_left.voltage.set_value = [setpoint]
    if any(s.lower() for s in metadata.get('Power Supply 1 Type', [])):
        target_left.mode = 'DC Pulsed'
        target_left.pulse_frequency = metadata.get('Frequency 1', None)
        target_left.pulse_reverse_time = metadata.get('Pulse Reverse Time 1', None)
    else:
        target_left.mode = 'DC Continuous'

    # Right target
    target_right_id = metadata.get('Target Right', [None])[0]
    target_right = TargetReference(
        reference=find_reference_by_id(target_right_id, 'Target', archive, logger),
        power=Power(value=dataframe['P2_Watt'], time=dataframe['time']),
        voltage=Voltage(value=dataframe['P2_Ampere'], time=dataframe['time']),
        current=Current(value=dataframe['P2_Voltage'], time=dataframe['time']),
    )
    setpoint = metadata.get('Setpoint 2', None)
    if setpoint:
        if setpoint.dimensionality == ureg.W.dimensionality:
            target_right.power.set_value = [setpoint]
        elif setpoint.dimensionality == ureg.A.dimensionality:
            target_right.current.set_value = [setpoint]
        elif setpoint.dimensionality == ureg.V.dimensionality:
            target_right.voltage.set_value = [setpoint]
    if any(s.lower() for s in metadata.get('Power Supply 2 Type', [])):
        target_right.mode = 'DC Pulsed'
        target_right.pulse_frequency = metadata.get('Frequency 2', None)
        target_right.pulse_reverse_time = metadata.get('Pulse Reverse Time 2', None)
    else:
        target_right.mode = 'DC Continuous'

    return target_left, target_right
