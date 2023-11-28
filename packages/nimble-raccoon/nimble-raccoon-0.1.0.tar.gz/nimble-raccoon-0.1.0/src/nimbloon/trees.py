"""
Hierarchical tree functions for RACCOON
F. Comitani     @2020-2024
"""

import numpy as np
import pandas as pd

from anytree import Node
from anytree.importer import JsonImporter, DictImporter
from anytree.exporter import JsonExporter

def build_tree(table: pd.DataFrame, out_path=None) -> Node:
    """ Set up a anytree object with useful information on
        the hierarchy of identified classes.

    :param table: one-hot-encoded table of class membership.
    :param out_path: path where output files will be saved
        (includes filename).
    :return: root node of the tree.
    """

    nodes = []

    def find_parent(name, lista=nodes):
        parents = [l for l in lista if l.name == name[:-name[::-1].find('_')-1]]
        parents.append(None)
        return parents[0]

    for col in table.columns:
        nodes.append(Node(col,
                          population=int((~np.isnan(table[col])).sum()),
                          parent=find_parent(col),
                          level=col.count('_'),
                          leaf=None))

    for n in nodes:
        n.leaf = len(n.children) == 0

    if out_path is not None:
        exporter = JsonExporter(indent=2, sort_keys=True)
        with open(out_path, 'w') as handle:
            exporter.write(nodes[0], handle)

    return nodes[0]

def load_tree(file: str) -> Node:
    """ Load an anytree object saved as json.

    :param file: path to input json file.
    :return: root node of the tree.
    """

    importer = JsonImporter(DictImporter(nodecls=Node))
    with open(file, 'r') as handle:
        root = importer.read(handle)

    return root