import sys

from rdflib import Graph


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def load_graph(graph_file) -> Graph:
    graph = Graph()
    graph.parse(graph_file, format="turtle")
    return graph
