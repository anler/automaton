# -*- coding: utf-8 -*-
from __future__ import print_function

import pygraphviz as g

from automaton import nodes as r
from automaton.state_machine import to_state_machine


regex = r.Choice(
    r.Constant('a'),
    r.Concat(
        r.Repeat(r.Constant('b')),
        r.Constant('c')
    )
)


def main():
    print(regex)
    st = to_state_machine(regex)

    graph = g.AGraph(directed=True, strict=False)

    for node, edge in st:
        target_node = st[node, edge]
        if type(target_node) is r.Null:
            continue
        graph.add_node(node)
        graph.add_edge(node, target_node, label=edge)
    print(graph.string())
    graph.layout()
    graph.draw('output.png')


if __name__ == "__main__":
    main()
