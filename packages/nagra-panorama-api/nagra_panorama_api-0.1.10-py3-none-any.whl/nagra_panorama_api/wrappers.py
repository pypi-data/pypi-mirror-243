import addict
import xmltodict
from lxml.etree import _Element  # nosec B410

from .utils import etree_fromstring, etree_tostring


# This code is safe using lxml
# It will only handle code already parsed
class Dict(addict.Dict):
    def __init__(self, xml=None):
        if isinstance(xml, _Element):
            xml = etree_tostring(xml)
        if isinstance(xml, str):
            if not xml:
                xml = "<entry/>"
            xml = xmltodict.parse(xml)
        return super().__init__(xml)

    def dumps(self):
        return xmltodict.unparse(self, full_document=False)

    def element(self):
        return etree_fromstring(self.dumps())
