from nomad.config.models.plugins import ParserEntryPoint
from pydantic import Field


class MyParserEntryPoint(ParserEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from nomad_ubik_plugin.parsers.myparser import MyParser

        return MyParser(**self.dict())


myparser = MyParserEntryPoint(
    name='MyParser',
    description='Parser defined using the new plugin mechanism.',
    mainfile_name_re='.*\.myparser',
)

# class XRFParserEntryPoint(ParserEntryPoint):
#     parameter: int = Field(0, description='Custom configuration parameter')

#     def load(self):
#         from nomad_ubik_plugin.parsers.XRFparser import XRFParser

#          return XRFParser(**self.dict())


# xrfparser = XRFParserEntryPoint(
#     name='XRFParser',
#     description='XRF Parser defined using the new plugin mechanism.',
#     mainfile_name_re='.*\.xrfparser',
# )
