# -*- coding: utf-8 -*-
"""Generate an automaton diagram for the given regular expression.

Currently only the following operators are supported: | and * son you can use regular expressions
such as: (a|b)c or ((a|b))*
"""
from __future__ import print_function
import argparse

import pygraphviz as g

from automaton.parser import parse
from automaton.nodes import Null
from automaton.state_machine import to_state_machine


def draw_state_machine(state_machine, output):
    graph = g.AGraph(directed=True, strict=False)

    for node, edge in state_machine:
        target_node = state_machine[node, edge]
        if type(target_node) is Null:
            continue
        graph.add_node(node)
        graph.add_edge(node, target_node, label=edge)
    graph.layout(prog='circo')
    graph.draw(output)


def alphabet(regex):
    return "{%s}" % ", ".join(str(i) for i in regex.alphabet())


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('regex', help='The regular expression')
    parser.add_argument('-o', '--output-filename', default='output.png',
                        help="Output file name. Default 'output.png'")

    args = parser.parse_args()

    regex = parse(args.regex).regex()
    state_machine = to_state_machine(regex)

    print(u"Regular Expression:", regex)
    print(u"Regular Expression Alphabet (∑):", alphabet(regex))

    draw_state_machine(state_machine, output=args.output_filename)


if __name__ == "__main__":
    main()
