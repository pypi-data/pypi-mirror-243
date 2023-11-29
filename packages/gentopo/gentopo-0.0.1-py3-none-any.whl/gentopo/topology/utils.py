import os
import re
import json
from datetime import datetime
import networkx as nx
from statistics import mean, median
import matplotlib.pyplot as plt


def positions(graph):
    return nx.circular_layout(graph)


def degree_statistics(graph):
    """Get the statistics of a graph's degrees across nodes.

    Args:
        graph (NetworkX Graph): A generated NetworkX graph.

    Returns:
        dict: A dictionary with min, mean, median, and max
    """
    degrees = [deg for (node, deg) in graph.degree()]
    return {
        "min": min(degrees),
        "mean": mean(degrees),
        "median": median(degrees),
        "max": max(degrees),
    }


def visualize(graph, path=None):
    """
    Draws a circular layout of the graph and defaults to not saving to file.
    """
    fig = plt.figure(figsize=(10, 10))
    topology_visual = nx.draw_networkx(graph, positions(graph))

    if path:
        plt.savefig(f"{path}/diagram.png")


def is_topology_dir(p, d):
    return os.path.isdir(os.path.join(p, d)) and re.search("topology", d) is not None


def create_topology_dir(study_name):
    """
    Create a topology directory with a new id in sequence from previously written directories
    """
    dir_path = f"studies/{study_name}"
    topology_dirs = [d for d in os.listdir(dir_path) if is_topology_dir(dir_path, d)]
    if len(topology_dirs) > 0:
        new_id_num = max([int(id.split("_")[1]) for id in topology_dirs]) + 1
        topology_id = f"topology_{str(new_id_num).zfill(3)}"
    else:
        topology_id = "topology_001"
    os.mkdir(f"studies/{study_name}/{topology_id}")
    return topology_id


def write_topology_json(study_name, topology_id, graph):
    # TODO: needs to reference config file?
    dt = datetime.utcnow()
    topology_metadata = dict(
        id=topology_id,
        created_for=study_name,
        created_at=dt.strftime(format="%Y-%m-%dT%H:%M:%S"),
        omega=nx.smallworld.omega(graph),
        network=nx.node_link_data(graph),
    )
    filename = f"studies/{study_name}/{topology_id}/metadata.json"
    with open(filename, "w") as f:
        f.write(json.dumps(topology_metadata))
        print(f"wrote {filename} to file")
    return topology_metadata
