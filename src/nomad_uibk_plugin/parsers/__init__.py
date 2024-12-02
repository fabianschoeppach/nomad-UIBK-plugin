from nomad.config.models.plugins import ParserEntryPoint


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
    mainfile_name_re=r'.*\.txt',
    mainfile_content_re=r'PositionType\s+Application\s+Sample\s+name\s+Date\s+\n[A-Z0-9-]+\s+Quant\s+analysis',
)


class SputterParserEntryPoint(ParserEntryPoint):
    """
    Sputter Parser plugin entry point.
    """

    def load(self):
        # lazy import to avoid circular dependencies
        from nomad_uibk_plugin.parsers.sputterparser import SputterParser

        return SputterParser(**self.dict())


sputterparser = SputterParserEntryPoint(
    name='SputterParser',
    description='Parser for UIBK Sputterdeposition .csv log files.',
    mainfile_name_re=r'.*\.csv',
    # mainfile_content_re=r'',
)
