from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.datamodel.data import EntryDataCategory
from nomad.metainfo.metainfo import Category
from pydantic import Field


class UIBKCategory(EntryDataCategory):
    """
    A category for all measurements defined in the UIBK nomad plugin.
    """

    m_def = Category(label='UIBK', categories=[EntryDataCategory])


class XRFSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_uibk_plugin.schema_packages.XRFschema import m_package

        return m_package


xrfschema = XRFSchemaPackageEntryPoint(
    name='XRFSchema',
    description='XRF Schema package defined using the new plugin mechanism.',
)


class SputteringSchemaEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_uibk_plugin.schema_packages.sputtering import m_package

        return m_package


sputtering = SputteringSchemaEntryPoint(
    name='Sputtering',
    description='Schema entry point for sputter deposition.',
)


# class MicroCellSchemaPackageEntryPoint(SchemaPackageEntryPoint):
#     def load(self):
#         from nomad_uibk_plugin.schema_packages.microcellschema import m_package

#         return m_package


# microcellschema = MicroCellSchemaPackageEntryPoint(
#     name='MicroCellSchema',
#     description='MicroCell Schema package defined using the new plugin mechanism.',
# )


class SampleSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_uibk_plugin.schema_packages.sample import m_package

        return m_package


sample = SampleSchemaPackageEntryPoint(
    name='sample',
    description='Sample Schema package defined using the new plugin mechanism.',
)
