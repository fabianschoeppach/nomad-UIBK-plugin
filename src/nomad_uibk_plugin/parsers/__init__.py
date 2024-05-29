from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class MyParserEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_uibk_plugin.parsers.myparser import MyParser

        return MyParser(**self.dict())


myparser = MyParserEntryPoint(
    name='MyParser',
    description='Parser defined using the new plugin mechanism.',
    mainfile_name_re='.*\.myparser',
)


class XRFParserEntryPoint(ParserEntryPoint):
    """
    XRF Parser plugin entry point.
    """

    def load(self):
        # lazy import to avoid circular dependencies
        from nomad_uibk_plugin.parsers.XRFparser import XRFParser

        return XRFParser(**self.dict())


xrfparser = XRFParserEntryPoint(
    name='XRFParser',
    description='XRF Parser for UIBK .txt files.',
    mainfile_name_re='.*\.txt',
    mainfile_content_re='PositionType\s+Application\s+Sample\s+name\s+Date\s+\n[A-Z0-9-]+\s+Quant\s+analysis',
)
