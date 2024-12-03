from typing import TYPE_CHECKING

from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections import (
    # Component,
    # CompositeSystem,
    # CompositeSystemReference,
    ElementalComposition,
    # InstrumentReference,
    # PureSubstanceComponent,
    # PureSubstanceSection,
    SectionReference,
)
from nomad.metainfo import (
    Datetime,
    MEnum,
    Quantity,
    # SectionProxy,
    SchemaPackage,
    # Package,
    Section,
    # MSection,
    SubSection,
)
from nomad_material_processing.vapor_deposition.pvd.general import PVDSource
from nomad_material_processing.vapor_deposition.pvd.sputtering import SputterDeposition

from nomad_uibk_plugin.schema_packages import UIBKCategory
from nomad_uibk_plugin.schema_packages.sample import UIBKSample

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

from nomad_measurements.utils import merge_sections  # create_archive

m_package = SchemaPackage()


class Target(PVDSource, EntryData):
    """
    Targets have:
    Static
    - Internal ID
        - number s
        - name s
    - Manufacturer s
    - Reseller s
    - Manufacturing date (day/month optional) s
    - Date of arrival (day/month optional) s
    - Composition (Multiple elements, doted, with purity, at% or wt%)(Supplyer values)
    - Thickness
        - Total s
        - Material s
        - Backing plate s
    - Diameter
        - Material s
        - Backing plate s
    - Backing plate (bool) s
    - shape (planar, special) s
    - prior use s

    Changing
    - Impurity (other target in the same process)
    - Usage (Joule of all processes)

    Measurements
    - Photos
    - IFM
    - EDX

    Associations
    - List of all VP a target was used in
    - A chronological list of all processes
    """

    m_def = Section()

    internal_id = Quantity(
        type=int,
        description='The lab ID of the target.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    internal_name = Quantity(
        type=str,
        description=(
            'Common name of the target. ' 'Usually the (simplified) elements and ID'
        ),
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    manufacturer_name = Quantity(
        type=str,
        description='Name of manufacturing company.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    reseller_name = Quantity(
        type=str,
        description='Name of reseller.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    manufacturing_date = Quantity(
        type=Datetime,
        description='Date of manufacturing',
        a_eln=ELNAnnotation(component=ELNComponentEnum.DateTimeEditQuantity),
    )
    acceptance_date = Quantity(
        type=Datetime,
        description='Date when target was first added to the database',
        a_eln=ELNAnnotation(component=ELNComponentEnum.DateEditQuantity),
    )
    'TODO: Use proper types and crate a new category for the GUI.'
    composition = Quantity(
        type=ElementalComposition,
        description='Composition of the target as stated by the manufacturer',
        # a_eln=ELNAnnotation(component=ELNComponentEnum.element),
        repeatable=True,
    )
    thickness_total = Quantity(
        type=float,
        description='Thickness of the target includnig material and backing plate.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
            defaultDisplayUnit='mm',
            label='Total thickness',
        ),
        unit='m',
    )
    thickness_material = Quantity(
        type=float,
        description='Thickness of the target material thickness.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
            defaultDisplayUnit='mm',
            label='Material thickness',
        ),
        unit='m',
    )
    thickness_backing_plate = Quantity(
        type=float,
        description='Thickness of the target includnig material and backing plate.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
            defaultDisplayUnit='mm',
            label='Backing plate thickness',
        ),
        unit='m',
    )
    diameter_material = Quantity(
        type=float,
        description='Diameter of the target material.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
            defaultDisplayUnit='mm',
            label='Material thickness',
        ),
        unit='m',
    )
    diameter_backing_plate = Quantity(
        type=float,
        description='Diameter of the backing plate.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
            defaultDisplayUnit='mm',
            label='Backing plate diameter',
        ),
        unit='mm',
    )
    backing_plate = Quantity(
        type=bool,
        description='Is the target mounted on a backing plate.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    # TODO: How detailed do we want to be here?
    shape = Quantity(
        type=MEnum(['circular', 'rectangular', 'special']),
        description='Shape of the target.',
        default='circular',
        a_eln={'component': 'RadioEnumEditQuantity'},
    )
    prior_use = Quantity(
        type=bool,
        description='The target was in use before being added to NOMAD.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    m_def = Section()
    """
    # TODO: 
    Impurities
    - Date + Target + Joules (linked via process ID?)
    """

    usage = Quantity(
        type=float,
        description='Total of the energy used of the target',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        unit='joule',
    )
    """
    Measurements
    - Photos
    - IFM
    - EDX

    Associations
    - List of all VPs a target was used in
    - A chronological list of all processes
    """


class TargetReference(SectionReference):
    reference = Quantity(type=Target, a_eln=dict(component='ReferenceEditQuantity'))


class Substrate(EntryData):
    """
    - type
    - subtype
    - manufacturer
    - Batch
    - size (x, y, z)
    -
    """

    m_def = Section()

    type = Quantity(
        type=MEnum(['c-Si die', 'glass', 'polyimide']),
        description='Type of substrate material',
        default='',
        a_eln={'component': 'AutocompleteEditQuantity'},
    )
    subtype = Quantity(
        type=str,
        description='Subtype of the substrate.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    batch = Quantity(
        type=str,
        description='Batch ID',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    mountingType = Quantity(
        type=MEnum(['retainers', 'double sided tape', 'retainers FlexPecs Narrow']),
        description='How is the substrate mounted in the chamber?',
        default='',
        a_eln={'component': 'RadioEnumEditQuantity'},
    )

    size_x = Quantity(
        type=float,
        description='Radius or x-dimension of the sample.',
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'mm'},
        unit='meter',
    )
    size_y = Quantity(
        type=float,
        description='Y-dimension of the sample.',
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'mm'},
        unit='meter',
    )

    size_z = Quantity(
        type=float,
        description='Height of the sample.',
        a_eln={'component': 'NumberEditQuantity', 'defaultDisplayUnit': 'mm'},
        unit='meter',
    )


class SubstrateReference(SectionReference):
    reference = Quantity(type=Substrate, a_eln=dict(component='ReferenceEditQuantity'))


class Operator(EntryData):
    author = Quantity(
        type=str,  ## < ?
        description='Authors/Operators',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,  # AuthorEditQuantity?
        ),
    )


class OperatorReference(SectionReference):
    reference = Quantity(type=Operator, a_eln=dict(component='ReferenceEditQuantity'))


class PSU(EntryData):
    """
    static
    - NOMAD internal ID
    - Manufacturer
    - Reseller
    - Model
    - Serial Number
    - prior use
    - [DC only, RF, Pulsed]

    variable
    - Operating Hours
    - Operating Joules

    time based
    - Setpoint type [W, V, A]
    - Setpoint value
    - RF settings
    - Pulsed settingss
        - Frequency
        - pulse reverse time
    """

    m_def = Section()

    internal_id = Quantity(
        type=int,
        description='NOMAD ID of the PSU',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        a_display={'visible': False},
    )
    manufacturer_name = Quantity(
        type=str,
        description='Name of manufacturing company.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    reseller_name = Quantity(
        type=str,
        description='Name of reseller.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        description='Name of reseller.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    serial = Quantity(
        type=str,
        description='Name of reseller.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    installation_date = Quantity(
        type=Datetime,
        description='',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateEditQuantity,
        ),
    )
    DC_capability = Quantity(
        type=bool,
        description='',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    rf_capability = Quantity(
        type=bool,
        description='',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    pulsed_capability = Quantity(
        type=bool,
        description='',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    prior_use = Quantity(
        type=bool,
        description='The PSU was in use before being added to NOMAD.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )

    operating_hours = Quantity(
        type=int,
        description='NOMAD ID of the PSU',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        unit='hour',
    )
    operating_joules = Quantity(
        type=int,
        description='NOMAD ID of the PSU',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        unit='joule',
    )
    m_def = Section()
    setpoint_type = Quantity(
        type=MEnum(['W', 'V', 'A']),
        description='',
        default='W',
        a_eln={'component': 'RadioEnumEditQuantity'},
    )
    setpoint_value = Quantity(
        type=float,
        description='',
    )
    m_def = Section()
    # RF settings
    m_def = Section()
    # Pulsed settings
    pulse_frequency = Quantity(
        type=int,
        description='',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
            defaultDisplayUnit='kHz',
            label='Pulse frequency',
        ),
        unit='Hz',
    )
    pulse_reverse_time = Quantity(
        type=int,
        description='',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
            defaultDisplayUnit='ms',
            label='Pulse reverse time',
        ),
        unit='s',
    )


class PsuReference(SectionReference):
    reference = Quantity(type=PSU, a_eln=dict(component='ReferenceEditQuantity'))


class PressureGauge(EntryData):
    """
    static

    time based
    - pressure
    """

    internal_id = Quantity(
        type=int,
        description='NOMAD ID of the PSU',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        a_display={'visible': False},
    )
    internal_name = Quantity(
        type=str,
        description='Internal name',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity, label='Internal name'
        ),
    )
    manufacturer_name = Quantity(
        type=str,
        description='Name of manufacturing company.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    reseller_name = Quantity(
        type=str,
        description='Name of reseller.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    model = Quantity(
        type=str,
        description='Name of reseller.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    serial = Quantity(
        type=str,
        description='Name of reseller.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    installation_date = Quantity(
        type=Datetime,
        description='',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.DateEditQuantity,
        ),
    )
    pressure = Quantity(
        type=float,
        description='',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
            defaultDisplayUnit='mBar',
            label='Pressure',
        ),
        unit='Pa',
    )


class PressureGaugeReference(SectionReference):
    reference = Quantity(type=PSU, a_eln=dict(component='ReferenceEditQuantity'))


class MassFlowController(EntryData):
    """
    static
    - Type
    - Medium [Ar, O2, N2]
    ...

    time based
    - mass flow
    """

    pass


class SputterParameters(ArchiveSection):
    """
    static
    - Operator (multiple) (->Operator)
    - samples (multiple) (-> UIBKSample)
        - ids
            - internal
            - external (multiple)
                - partner
                - ID
        - Substrate (->Substrate)
    - Installed targets (multiple)(->Target)
    - Installed PSUs (multiple) (-> PSU)
    - sample distance_to_source
    - Comment
    - LN² (bool)

    time based
    - timestamp
    - PSU(n) -> Target(n)
    - Setpoint type [W, V, A]
    - Setpoint Value
    - Pressure gauge (multiple) (->PressureGauge)
    - sample rotation speed
    """

    test = Quantity(type=str)


class UIBKSputterDeposition(SputterDeposition, EntryData):
    m_def = Section(
        categories=[UIBKCategory],
        label='Sputter Deposition',
    )

    data_file = Quantity(
        type=str,
        description='Path to the data file',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.FileEditQuantity,
        ),
    )

    samples = SubSection(section_def=UIBKSample, repeats=True)

    target = SubSection(section_def=TargetReference, repeats=True)

    parameters = SubSection(section_def=SputterParameters)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """Update the data from the data file if it is not already set"""

        from nomad_uibk_plugin.filereader.sputterreader import read_sputter_csv

        # if self.data is None and self.data_file is not None:
        if self.data_file is not None:
            with archive.m_context.raw_file(self.data_file) as file:
                sputter_entry = read_sputter_csv(file, logger)
                merge_sections(self, sputter_entry, logger)

        super().normalize(archive, logger)


m_package.__init_metainfo__()
