from contextlib import contextmanager
from typing import ClassVar

from .constants import PATH_NAME_PREFIX, PATH_SEARCH_PREFIX
from .utils import detach, etree_tostring
from .wrappers import Dict


def _select_xpath_unique_selector(element):
    # identifiers = ("name", "uuid")
    identifiers = ("uuid", "name")
    for i in identifiers:
        value = element.get(i)
        if value:
            return i, value
    return None, None


def mk_xpath_selector(key, value):
    return f"[@{key}='{value}']"


def xpath_unique_selector(element):
    key, value = _select_xpath_unique_selector(element)
    if key:
        return mk_xpath_selector(key, value)
    # text = element.text.strip()
    # if text:
    #     return "[text()='{}']".format(text)
    return ""


def get_element_xpath(element, unambiguous=False):
    """
    This function return the xpath of an element relatively
    to the root. e.g. /config/devices/...

    unambiguous: Ensure that every possible node
        of the path uses its identifier
    """
    parts = []
    elements = [element, *list(element.iterancestors())]
    selector_ok = False
    for el in elements:
        tag = el.tag
        if not selector_ok or unambiguous:
            selector = xpath_unique_selector(el)
            if selector:
                selector_ok = True
                tag += selector
        parts.append(tag)
    return "/" + "/".join(parts[::-1])


def dump_element(element, pretty=True):
    return etree_tostring(element, pretty_print=pretty).decode()


def find_by_attr(tree, key, value):
    if not isinstance(value, str) or "'" in value:
        return None
    xpath = f"{PATH_SEARCH_PREFIX}//*[@{key} = '{value}']"
    return tree.xpath(xpath)


def find_by_name(tree, object_name):
    return find_by_attr(tree, "name", object_name)


def find_by_uuid(tree, uuid):
    return find_by_attr(tree, "uuid", uuid)


# this will consider all tags:
#   member, translation-address, ... be cautious using it
def find_references(tree, object_name, tag="*"):
    if not isinstance(tag, str):
        # Combine a list of tag into one
        # //*[self::tag1 or self::tag2]
        # //(tag1|tag2)
        tag = "({})".format("|".join(tag))
    if not isinstance(object_name, str) or "'" in object_name:
        return []
    return tree.xpath(
        f"{PATH_SEARCH_PREFIX}//{tag}[text() = '{object_name}']",
    )


def find_ancestor(element, tag):
    return next((x for x in element.iterancestors() if x.tag == tag), None)


class ConfigElement:
    def __init__(self, el, config=None, xpath=None):
        if config is None:
            config = Config(list(el.iterancestors())[-1])
        if xpath is None:
            xpath = get_element_xpath(el)
        self._el = el
        self._config = config
        self._xpath = xpath

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.xpath.replace(PATH_NAME_PREFIX, "")

    def dumps(self, pretty=False):
        return etree_tostring(self._el, pretty_print=pretty).decode()

    @property
    def element(self):
        return self._el

    @property
    def attrib(self):
        return self._el.attrib

    @property
    def name(self):
        return self._el.attrib.get("name")

    @property
    def config(self):
        return self._config

    @property
    def entry(self):
        e = find_ancestor(self._el, "entry")
        return self._wrap_element(e)

    @property
    def parent(self):
        e = self._el.getparent()
        if e is None:
            return None
        return self._wrap_element(e)

    @contextmanager
    def as_dict(self):
        d = Dict(self._el)
        try:
            yield d
        finally:
            new_element = d.element()
            parent = self._el.getparent()
            if parent:
                parent.replace(self._el, new_element)
            self._el = new_element
            self._set_xpath()

    def xpath(self, search=None):
        if search:
            e = self._el.xpath(search)
            return self._wrap_element(e)
        return self._xpath

    def _set_xpath(self, unambiguous=True):
        self._xpath = self.get_xpath(unambiguous=unambiguous)

    def get_xpath(self, unambiguous=True):
        return get_element_xpath(self._el, unambiguous=unambiguous)

    def _wrap_element(self, element):
        if element is None:
            return None
        return ConfigElement(element, self.config)

    def get_references(self):
        references = find_references(self.config.tree, self.name)
        return [self._wrap_element(e) for e in references]

    def remove(self):
        detach(self._el)


class Config:
    # Singleton like: Always return the same Config object for the same tree
    __instances: ClassVar = {}

    def __new__(cls, config_tree, *args, **kwargs):
        instance = cls.__instances.get(config_tree)
        if not instance:
            instance = object.__new__(cls)
            cls.__instances[config_tree] = instance
        return instance

    def __init__(self, config_tree):
        if config_tree.tag != "config":
            raise Exception("Wront tree, root must be <config>")
        detach(config_tree)
        self._tree = config_tree

    # def __str__(self):
    #     return etree_tostring(self._tree).decode()

    def dumps(self, pretty=False):
        return etree_tostring(self._tree, pretty_print=pretty).decode()

    @property
    def tree(self):
        return self._tree

    def _mk_config_el(self, el):
        return ConfigElement(el, self)

    def find_by_name(self, name):
        res = find_by_name(self._tree, name)
        return [self._mk_config_el(x) for x in res]

    def find_by_uuid(self, name):
        res = find_by_uuid(self._tree, name)
        return [self._mk_config_el(x) for x in res]
