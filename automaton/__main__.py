# -*- coding: utf-8 -*-
"""Generate an automaton diagram as a png image for the given regular expression.

Currently only the following operators are supported: (), | and * son you can use regular
expressions such as: (a|b)c or ((a|b))*
"""
from __future__ import print_function
import sys
import argparse

import pygraphviz as g

from automaton.parser import parse, ParseError
from automaton.nodes import Null
from automaton.state_machine import to_state_machine


VALID_LAYOUTS = ('neato', 'dot', 'twopi', 'circo', 'fdp')


def mark_as_accepting_state(graph, node):
    graph_node = graph.get_node(node)
    graph_node.attr[u'color'] = u'blue'
    graph_node.attr[u'label'] = u'λ'


def draw_state_machine(start_node, state_machine, accepting_states, output, layout='circo'):
    graph = g.AGraph(directed=True, strict=False)
    graph.add_node(start_node, label=u'>')
    for node, edge in state_machine:
        target_node = state_machine[node, edge]
        if type(target_node) is Null:
            continue
        if target_node in accepting_states:
            graph.add_node(target_node)
            mark_as_accepting_state(graph, target_node)
        else:
            graph.add_node(target_node, label=u'')
        graph.add_node(node, label=u'')
        if node in accepting_states:
            mark_as_accepting_state(graph, node)
        graph.add_edge(node, target_node, label=edge)
    graph.layout(prog=layout)
    graph.draw(output)


def alphabet(regex):
    return "{%s}" % ", ".join(str(i) for i in regex.alphabet())


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('regex', help='The regular expression')
    parser.add_argument('-o', '--output-filename', default='output.png',
                        help="Output file name. Default 'output.png'")
    parser.add_argument('--layout', choices=VALID_LAYOUTS, default="circo",
                        help="Graph layout. Default is circo.")

    args = parser.parse_args()
    regex_string = args.regex
    output_filename = args.output_filename
    layout = args.layout

    try:
        regex = parse(regex_string).regex()
    except ParseError:
        print("Unsupported regular expression")
        return
    start_node, state_machine, accepting_states = to_state_machine(regex)

    draw_state_machine(start_node, state_machine, accepting_states, output=output_filename,
                       layout=layout)

    print(u"Graph saved as {!r}".format(output_filename))


if __name__ == "__main__":
    sys.exit(main())
