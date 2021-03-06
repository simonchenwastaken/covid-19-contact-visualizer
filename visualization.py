"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Visualization Module
This module contains the functions that visualize either a degree graph on its own, or a simulation.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
from typing import Any, Tuple
import networkx as nx
from plotly.graph_objs import Scatter, Figure
import plotly.graph_objects as go
from social_graph import Graph


# Degrees visualization
def render_degrees_apart(graph: Graph, init_infected: set[str]) -> None:
    """ Render the degrees visualization given a graph, and the initial set of infected people by
    ID.

    Preconditions:
        - all(not person.infected for person in graph._people.values())
    """
    # Degree calculation
    graph.set_infected(init_infected)
    graph.recalculate_degrees()

    # Converts to nx.Graph
    graph_nx = graph.to_nx_with_degree_colour()

    colours = [graph_nx.nodes[node]['colour'] for node in graph_nx.nodes]
    pos = getattr(nx, 'spring_layout')(graph_nx)

    # put positions of nodes into lists
    x_values, y_values, x_edges, y_edges = determine_positions(pos, graph_nx)
    labels = list(graph_nx.nodes)

    trace3, trace4 = create_scatters((x_edges, y_edges), (x_values, y_values), colours, labels)

    # add these nodes and edges to the figure and show the graph
    data1 = [trace3, trace4]

    fig = Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    fig.show()


def render_simulation_frame(graph: Graph, pos: dict[str, Any], num: int = 0,
                            with_degrees: bool = False) -> go.Frame:
    """Return a plotly Frame given object a graph and the positions of each person and edge on the
    rendered graph.
    """
    if with_degrees:
        graph_nx = graph.to_nx_with_degree_colour()
    else:
        graph_nx = graph.to_nx_with_simulation_colour()

    # create frame
    colours = [graph_nx.nodes[node]['colour'] for node in graph_nx.nodes]
    num_infected = colours.count('rgb(255, 0, 0)')
    x_values, y_values, x_edges, y_edges = determine_positions(pos, graph_nx)
    labels = list(graph_nx.nodes)

    # put positions of edges into lists
    trace3, trace4 = create_scatters((x_edges, y_edges), (x_values, y_values), colours, labels)

    return go.Frame(data=[trace3, trace4], layout={"title": 'Number of People Infected: '
                                                            + str(num_infected) + '/'
                                                            + str(len(graph_nx.nodes))}, name=num)


def update_slider(sliders_dict: dict[str, Any], num: int = 0) -> None:
    """Updates slider_dict for the layout of plotly figure. slider_dict controls the slider on the
    plotly visualization.
    """

    slider_step = {"args": [[num], {"frame": {"duration": 700, "redraw": True},
                                    "mode": "immediate",
                                    "transition": {"duration": 100},
                                    }],
                   "label": 'Week ' + str(num),
                   "method": "animate"}

    sliders_dict["steps"].append(slider_step)


def render_simulation_full(frames: list[go.Frame], sliders_dict: dict, num_nodes: int,
                           num_init_infected: int) -> None:
    """Creates the entire simulation and outputs it for the user.
    """
    fig = Figure(data=frames[0].data,
                 layout=go.Layout(
                     xaxis=dict(range=[0, 5], autorange=True),
                     yaxis=dict(range=[0, 5], autorange=True),
                     title='Number of People Infected: ' + str(num_init_infected) + '/'
                     + str(num_nodes),
                     updatemenus=[dict(
                         type="buttons",
                         buttons=[dict(label="Play",
                                       method="animate",
                                       args=[None, {"frame": {"duration": 700, "redraw": True},
                                                    "fromcurrent": True}]),

                                  dict(label="Pause",
                                       method="animate",
                                       args=[[None], {"frame": {"duration": 0, "redraw": True},
                                                      "mode": "immediate",
                                                      "transition": {"duration": 0}}])
                                  ])],
                     sliders=[sliders_dict]),
                 frames=frames)

    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    fig.show()


def create_scatters(edges: Tuple[list[Any], list[Any]], values: Tuple[list[Any], list[Any]],
                    colours: list[Any], labels: list[Any]) -> tuple[go.Scatter, go.Scatter]:
    """Create the nodes and edges through plotly for the visualization"""

    trace3 = Scatter(x=edges[0],
                     y=edges[1],
                     mode='lines',
                     name='edges',
                     line=dict(width=2,
                               color='rgb(0, 0, 0)'),
                     hoverinfo='none',
                     )

    # create the nodes in plotly
    trace4 = Scatter(x=values[0],
                     y=values[1],
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=50,
                                 color=colours,
                                 line=dict(width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    return trace3, trace4


def determine_positions(pos: dict[str, Any], graph_nx: nx.Graph) -> tuple[list[Any], list[Any],
                                                                          list[Any], list[Any]]:
    """Returns the x and y positions of the edges and nodes."""
    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    return x_values, y_values, x_edges, y_edges


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx', 'social_graph', 'plotly.graph_objs', 'plotly.graph_objects'],
        'max-line-length': 100,
        'disable': ['E1136']
    })
