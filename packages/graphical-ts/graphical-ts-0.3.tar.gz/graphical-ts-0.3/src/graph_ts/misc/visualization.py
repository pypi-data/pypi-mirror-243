
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.colors as colors
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from yfiles_jupyter_graphs import GraphWidget
import networkx as nx
import numpy as np
from netgraph import Graph as vis_ng
from netgraph import InteractiveGraph as vis_ig
import plotly.tools as tls
import seaborn as sns
import pandas as pd


from pathlib import Path
import skimage.io as sio
import plotly.express as px

def is_binary(series):
    return set(series.unique()).issubset([0, 1])

def is_categorical(series):
    # Check if the series data type is not integer or string
    if not (pd.api.types.is_integer_dtype(series) or pd.api.types.is_string_dtype(series)):
        return False

    unique_values = series.unique()
    num_unique_values = len(unique_values)

    # Check if the number of unique values is between 2 and 9
    if 1 < num_unique_values < 10:
        # Special case: If there are exactly 2 unique values and they are 0 and 1, it's not categorical
        if num_unique_values == 2 and set(unique_values) == {0, 1}:
            return False
        else:
            return True
    else:
        return False

def visualize_binary_series_with_bars(ax, series, color):
    # Plot bars only for the '1' values in the binary series
    ones = series[series == 1]
    ax.bar(ones.index, ones, width=1.0, color=color, align='center', alpha=0.6)
    
def visualize_categorical(series, ax):
    # Get the series index and unique series values
    unique_values = series.unique()
    
    # Create a color map and assign a unique color to each category
    colors = plt.cm.viridis(np.linspace(0, 1, len(unique_values)))
    color_map = {val: colors[i] for i, val in enumerate(unique_values)}

    # Create a grid for the heatmap
    num_values = len(unique_values)
    series_length = len(series)

    # Set the labels for the y-axis and x-axis
    ax.set_yticks(np.arange(num_values))
    ax.set_yticklabels(unique_values)

    # Color each cell based on the category
    for idx, value in enumerate(series):
        value_index = np.where(unique_values == value)[0][0]
        ax.add_patch(plt.Rectangle((idx, value_index), 1, 1, color=color_map[value]))

    # Set the limits and invert the y-axis to have the first category on top
    ax.set_xlim(0, series_length)
    ax.set_ylim(0, num_values)
    
def series_to_heatmat(series):
    unique_values = series.unique()
    cent = len(unique_values) // 2 + 0.5
    
    cols = [(i+1 - cent)*(series==v) for i, v in enumerate(unique_values)]
    
    mat = np.vstack(cols)
    return mat

def ts_go(df, type_ref={}, fig_width=1200, fig_height=600, with_graph=None, save_path='./temp.png', pos=None, g_ratio=0.2, **kwargs):

    n_var = len(df.columns)
    n_cols = 1 if with_graph is None else 2
    specs = None if with_graph is None else [[{'rowspan': n_var}, {}]] + [[None, {}]] * (n_var - 1)
    column_widths = None if with_graph is None else [g_ratio, 1-g_ratio]
    fig = make_subplots(rows=len(df.columns), cols=n_cols, 
                        shared_xaxes=True, 
                        vertical_spacing=0.02, 
                        specs=specs, 
                        column_widths=column_widths)


    for i, column in enumerate(df.columns):
        col = 1 if with_graph is None else 2
        if is_categorical(df[column]) or type_ref.get(column, None) == 'categorical':
            fig.add_trace(go.Heatmap(z=series_to_heatmat(df[column]), colorscale='RdBu', zmid=0), row=i+1, col=col)
            
        elif is_binary(df[column]) or type_ref.get(column, None) == 'binary':
            fig.add_trace(go.Heatmap(z=(-0.5*np.array(np.ones(len(df))==df[column]))[None, :], colorscale='RdBu', zmid=0), row=i+1, col=col)
        else:
            fig.add_trace(go.Scatter(x=df.index, y=df[column], name=column, mode='lines'), row=i+1, col=col)
        fig.update_yaxes(title_text=column, row=i+1, col=1)
        
    if with_graph:
        _, ax = plt.subplots()
        _, fig_path = graph_ng(with_graph, pos=pos, ax=ax, save_fig=save_path, **kwargs)
        img =sio.imread(fig_path);
        figm= px.imshow(img);
        fig.add_trace(figm.data[0], row=1, col=1)
        fig.update_xaxes(showticklabels=False, row=1, col=1)
        fig.update_yaxes(title=None, showticklabels=False, row=1, col=1)
        # fig.update_layout(title=None, margin=dict(l=0, r=0, t=0, b=0), row=1, col=1)

    fig.update_traces(dict(showscale=False,
                            coloraxis=None), selector={'type':'heatmap'})
    fig.update_layout(
        width=fig_width, 
        height=fig_height, 
        
        margin=dict(l=40, r=10, t=10, b=10)  # Adjust these values as desired
    )
    
    fig.show()

def ts_mpl(df, fig_width=15, fig_height=5, with_graph=None, g_ratio=0.2, 
           type_ref={},
           cat_ref=None,
           save_path='./temp.png', 
           pos=None, 
           markersize=None,
           linestyle='-',
           marker=None,
           
           **nx_opts):
    
    color_cycle = plt.cm.plasma(np.linspace(0.1, 0.9, 10))  # Using the 'tab10' colormap for 10 distinct colors
    color_iter = iter(color_cycle)
    n_var = len(df.columns)
    n_cols = 1 if with_graph is None else 2
    plt.figure(figsize=(fig_width, fig_height))
    gs = gridspec.GridSpec(n_var, n_cols, width_ratios=[g_ratio, 1-g_ratio] if with_graph else [1])

    ax = None
    
    columns = np.ravel([[f'r_{col}',col] for col in df.columns])
    
    i = 0
    for col in columns:
        if col not in df.columns: 
            continue
        
        
        if with_graph:
            ax = plt.subplot(gs[i, 1], sharex=ax)
        else:
            ax = plt.subplot(gs[i, 0], sharex=ax)
        
        if col[:2] == 'r_' or type_ref.get(col, None) == 'binary' or is_binary(df[col]):
            visualize_binary_series_with_bars(ax, df[col], "red")
        else:
            if is_categorical(df[col]) or type_ref.get(col, None) == 'categorical':
                visualize_categorical(df[col], ax)
            else:
                mask = ~np.isnan(df[col])
                line, = ax.plot(df.index[mask], df[col][mask], linestyle=":", linewidth=0.8, color=next(color_iter))
                # ax.plot(x,y, color=line.get_color(), lw=1.5)
                # ax.plot(df.index, interpolated, linestyle=':', color='gray')
                ax.plot(df.index, df[col], linestyle=linestyle, marker=marker, label=col, markersize=markersize, color=line.get_color())
                
                

        ax.set_ylabel(col)
        ax.margins(x=0)
        if i == n_var - 1:
            ax.set_xlabel('Time')
            break
        else: 
            plt.setp(ax.get_xticklabels(), visible=False)
            
        i += 1

    if with_graph:
        ax = plt.subplot(gs[0, 0], rowspan=n_var)
        nx.draw(with_graph, pos=pos, ax=ax, **nx_opts)
        ax.set_title('Network Graph')
        ax.axis('off')

    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()


def graph_yf(graph):
    colorscale = 'Hot'  # Choose the colorscale
    color_vals = np.array(graph.lags)
    sampled_colors = colors.sample_colorscale(colorscale, color_vals/np.linalg.norm(color_vals))
    generated_colors = {lag: color for lag, color in zip(color_vals, sampled_colors)}
    

    nodes2id = {}
    yf_nodes = []
    for i, n in enumerate(graph.nodes):
        nodes2id[n] = i
        yf_nodes.append(dict(id=i, properties=dict(yf_label=n, data=graph.nodes[n])))
        
    yf_edges = []
    for i, (u, v, lag) in enumerate(graph.edges(keys=True)):
        yf_edges.append(dict(id=i, start=nodes2id[u], end=nodes2id[v], properties=dict(lag=lag)))
        
    def e_color_mapping(index, element):
        return generated_colors[element['properties']['lag']]
    
    def n_color_mapping(index, element):
        return '#AAAAAA'
    
    def n_scale_mapping(index, element):
        return 0.5
    
    w = GraphWidget()
    w.set_nodes(yf_nodes)
    w.set_edge_color_mapping(e_color_mapping)
    w.set_node_color_mapping(n_color_mapping)
    w.set_node_scale_factor_mapping(n_scale_mapping)
    w.set_edges(yf_edges)
    w.directed = True
    return w




def graph_nx(pgv, pos=None, ax=None, color='#3232aa'):
    if pos is None:
        pos = nx.shell_layout(pgv) 
        
    if ax == None:
        ax=plt.gca()
        
    nx.draw(
        pgv, pos, ax=ax, edge_color='black', width=1, linewidths=1,
        node_size=800, node_color=color, alpha=0.6,
        labels={node: node for node in pgv.nodes()}
    )
    
    nx.draw_networkx_edge_labels(
        pgv, pos, 
        ax=ax,
        edge_labels={(u, v): k for (u, v, k) in pgv.edges(keys=True) if u!=v},
        font_color=color
    )
    nx.draw_networkx_edge_labels(
        pgv, pos, 
        ax=ax,
        edge_labels={(u, v): k for (u, v, k) in pgv.edges(keys=True) if u==v},
        label_pos=10,
        font_color=color
    )
    ax.set_axis_off()
    return pos


def graph_ng(pgv, pos=None, ax=None, color='#323266', scl=0.6, save_fig=None):
    if pos is None:
        pos = {k: (x*scl, y*scl) for k, (x,y) in nx.shell_layout(pgv).items()}
        
    edge_labels = {(u, v): k for (u, v, k) in pgv.edges(keys=True)}
    
    vis_ng(list(edge_labels.keys()), 
           edge_labels=edge_labels, 
           edge_label_position=0.5, 
           arrows=True, 
           ax=ax, 
           node_labels=True,
           node_size=5,
           node_layout=pos,
           edge_color=color,
           edge_layout='straight',
           edge_width=1.5
           )

    if save_fig is not None:
        plt.savefig(save_fig, dpi=300, format='png', bbox_inches='tight')
        return pos, str(Path(save_fig).resolve())
    
    return pos
    
