from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.datamodel.data import EntryDataCategory
from nomad.metainfo.metainfo import Category
from pydantic import Field


class UIBKCategory(EntryDataCategory):
    """
    A category for all measurements defined in the UIBK nomad plugin.
    """

    m_def = Category(label='UIBK', categories=[EntryDataCategory])

class MySchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_uibk_plugin.schema_packages.mypackage import m_package

        return m_package


mypackage = MySchemaPackageEntryPoint(
    name='MyPackage',
    description='Schema package defined using the new plugin mechanism.',
)

class XRFSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_uibk_plugin.schema_packages.XRFschema import m_package

        return m_package

xrfschema = XRFSchemaPackageEntryPoint(
    name='XRFSchema',
    description='XRF Schema package defined using the new plugin mechanism.',
)