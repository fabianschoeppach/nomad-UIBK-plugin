import os

import pytest
from nomad.client import normalize_all, parse


@pytest.fixture(params=['QNT20220823_A1_2m.txt'])
def parsed_archive(request):
    """
    Sets up a parsed archive and cleans up afterwards.
    """
    file_path = os.path.join('tests', 'data', request.param)
    archive_from_file = parse(file_path)[0]
    measurement = os.path.join(
        'tests', 'data', '.'.join(request.param.split('.')[:-1]) + '.archive.json'
    )
    assert archive_from_file.data.measurement.m_proxy_value == os.path.abspath(
        measurement
    )
    measurement_archive = parse(measurement)[0]

    yield measurement_archive

    if os.path.exists(measurement):
        os.remove(measurement)


def test_normalize_all(parsed_archive):
    """
    Tests the normalization of data in the archive.
    """
    normalize_all(parsed_archive)

    # checks for different parsers
    if parsed_archive.data.method == 'X-Ray Fluorescence (XRF)':
        # TODO: Add tests specific for XRF method
        pass
