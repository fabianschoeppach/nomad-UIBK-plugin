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
    #  MEnum,
    Datetime,
    Quantity,
    #  Package,
    Section,
    # MSection,
    SubSection,
    #  SectionProxy,
)
from nomad_material_processing.vapor_deposition.pvd.general import PVDSource
from nomad_material_processing.vapor_deposition.pvd.sputtering import SputterDeposition

from nomad_uibk_plugin.schema_packages import UIBKCategory
from nomad_uibk_plugin.schema_packages.sample import UIBKSample


class Target(PVDSource, EntryData):
    """
    Targets have:
    Static
    - Internal ID
        - number
        - name
    - Manufacturer
    - Reseller
    - Manufacturing date (day optional)
    - Date of arrival (day/month optional)
    - Composition (Multiple elements, doted, with purity, at% or wt%)(Supplyer values)
    - Thickness
        - Total
        - Material
        - Backing plate
    - Diameter
        - Material
        - Backing plate
    - Backing plate (bool)
    - shape (planar, special)

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

    internal_id = Quantity(
        type=int,
        description='The lab ID of the target.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    internal_name = Quantity(
        type=str,
        description='Common name of the target. Usually the (simplified) elements and ID',
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
        a_eln=ELNAnnotation(component=ELNComponentEnum.DateTimeEditQuantity),
    )
    'TODO: Use proper types and crate a new category for the GUI.'
    composition = Quantity(
        type=ElementalComposition,
        description='Composition of the target as stated by the manufacturer',
        a_eln=ELNAnnotation(component=ELNComponentEnum.element),
        repeatable=True,
    )
    thickness_total = Quantity(
        type=float,
        description='Thickness of the target includnig material and backing plate.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        unit='mm',
    )
    thickness_material = Quantity(
        type=float,
        description='Thickness of the target material thickness.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        unit='mm',
    )
    thickness_backing_plate = Quantity(
        type=float,
        description='Thickness of the target includnig material and backing plate.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        unit='mm',
    )
    diameter_material = Quantity(
        type=float,
        description='Thickness of the target material thickness.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
        ),
        unit='mm',
    )
    diameter_backing_plate = Quantity(
        type=float,
        description='Thickness of the target includnig material and backing plate.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity,
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
    shape = Quantity(
        type=str,
        description='Shape of the target surface.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity,
        ),
    )
    prior_use = Quantity(
        type=bool,
        description='The target was in use before being added to NOMAD.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.BoolEditQuantity,
        ),
    )
    """
    Impurities
    - Date + Target + Joules (linked via process ID?)
    """
    """
    Usage
    - Sum of energy for the target.

    - pre sputter time (shutter)
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
    - List of all VP a target was used in
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

    pass


class Operator(EntryData):
    """
    - NOMAD internal ID
    - c-number
        - student
        - employee
    - Name
    - NOMAD user name (for API upload?)
    - Token (API upload?)
    """

    pass


class PSU(EntryData):
    """
    static
    - NOMAD internal ID
    - Manufacturer
    - Model
    - Serial Number
    - Operating Hours
    - Operating Joules
    - prior use
    - [DC only, RF, Pulsed]

    time based
    - Setpoint type [W, V, A]
    - Setpoint value
    - RF settings
    - Pulsed settings
        - Frequency
        - pulse reverse time
    """

    pass


class PressureGauge(EntryData):
    """
    static

    time based
    - pressure
    """

    pass


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
    - Installed PSUs (multiple)
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

    pass


class UIBKSputterDeposition(SputterDeposition, EntryData):
    m_def = Section(
        categories=[UIBKCategory],
        label='Sputter Deposition',
    )

    samples = SubSection(section_def=UIBKSample, repeats=True)

    target = SubSection(section_def=TargetReference, repeats=True)

    parameter = SubSection()
