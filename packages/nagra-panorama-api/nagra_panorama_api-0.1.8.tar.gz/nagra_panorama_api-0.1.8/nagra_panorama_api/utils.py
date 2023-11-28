# import defusedxml.lxml
import urllib.parse

import xmltodict
from diff_match_patch import diff_match_patch
from lxml import etree  # nosec B410

# Safe XML parsing with custom options (solution of the author)
# https://github.com/tiran/defusedxml/issues/102
# Nb: From issue #33, defusedxml.lxml should be depracted by the author.
# PARSER = etree.Parser(remove_blank_text=True, resolve_entities=False)
# LOOKUP = etree.ElementDefaultClassLookup(defusedxml.lxml.RestrictedElement)
# PARSER.set_element_class_lookup(LOOKUP)

# https://stackoverflow.com/questions/3310614/remove-whitespaces-in-xml-string


def etree_fromstring(string, remove_blank_text=True):
    parser = etree.XMLParser(remove_blank_text=remove_blank_text)
    return etree.XML(string, parser=parser)


def etree_tostring(element, pretty_print=False):
    return etree.tostring(element, pretty_print=pretty_print)


def parse_response(response):
    if isinstance(response, (str, bytes)):
        # Nb: We should use defusedxml library but it doesn't support
        # Removing blank spaces
        response = etree_fromstring(response)
    data = response.xpath("/response/result/*")
    for d in data:
        detach(d)
    return data


def detach(e):
    parent = e.getparent()
    if parent is not None:
        parent.remove(e)
    return e


def delete_nat_membership(
    client,
):
    pass


def delete_policy_membership(element):
    entry = element.entry
    # TODO: Check type
    element.remove()  # Remove element from tree
    print(element.dumps(True))
    with entry.as_dict() as d:
        d.target.negate = "no"
        d["destination-hip"].member = "any"
    print(element.dumps(True))

    # client.update(e.xpath, e.dumps())
    # client.create(e.xpath, e.dumps())


def map_dicts(a, b):
    """
    Combine values from b with the value in a having the same key.
    """
    for uuid, u in a.items():
        r = b.get(uuid)
        if r is None:
            continue
        yield u, r


def extend_element(dest, elements):
    """
    Only add element that are not already in the destination
    element.extend(...) is causing duplicates entries because
    the merge is not controlled
    """
    children = {c.tag for c in dest.getchildren()}
    for e in elements:
        if e.tag in children:
            continue
        dest.append(e)
    return dest


def el2dict(e):
    return xmltodict.parse(etree_tostring(e))


# =============================================
# Utility function to compare the changes between configurations
# Nb: native difflib is too slow

# Using xmldiff.main.diff_trees gives false positives (can be filtered) and is very slow
# also, deepdiff.DeepDiff(el2dict(xml1), el2dict(xml2)).to_json() xpath is not able to use attributes to identify entries
# eval(re.findall(".*entry'\]\[\d+\]", diff["dictionary_item_added"][0])[0], {"root": y})


def _diff_patch(text1, text2):
    dmp = diff_match_patch()
    patches = dmp.patch_make(text1, text2)
    return urllib.parse.unquote(dmp.patch_toText(patches))


def diff_patch(xml1, xml2):
    if not isinstance(xml1, str):
        xml1 = etree_tostring(xml1).decode()
    if not isinstance(xml2, str):
        xml2 = etree_tostring(xml2).decode()
    return _diff_patch(xml1, xml2)
