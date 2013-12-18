# -*- coding: utf-8 -*-


def to_state_machine(node):
    automaton = {}
    nodes = set([node])
    visited_nodes = set()

    while True:
        start_node = nodes.pop()
        for edge in node.alphabet():
            end_node = start_node.derive(edge).reduce()
            if end_node and end_node not in visited_nodes:
                visited_nodes.add(end_node)
                nodes.add(end_node)
            automaton[(start_node, edge)] = end_node

        if not nodes:
            break

    return automaton
