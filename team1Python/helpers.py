# From Team 4

from lxml import etree


def print_element(root, pretty_print=True):
    buf = etree.tostring(
        root,
        encoding='utf-8',
        pretty_print=pretty_print
    )
    print(buf.decode('utf-8'))