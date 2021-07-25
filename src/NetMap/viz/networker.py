from NetMap import ( go, nx, DATAFRAME, GRAPH, 
                     SCATTER, LAYOUT, FIGURE )

def genEdge(G: GRAPH, pos: dict) -> tuple:
    """Function to Generate Edge and Edge data coordinates"""
    edge_x, edge_y, xtext, ytext = [], [], [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        xtext.append((x0+x1)/2)
        ytext.append((y0+y1)/2)
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    return edge_x, edge_y, xtext, ytext

def genEdgeTrace(x: list, y: list) -> SCATTER:
    """Function to Generate Edge Traces"""
    return go.Scatter(
            x=x, y=y,
            line={'width': 0.8, 'color': 'cornflowerblue'},
            hoverinfo='none',
            mode='lines'
    )

def genEdgeText(G: GRAPH) -> list:
    "Function to Clean and Pull Text for Edge Data"
    return list(map(lambda x: x.replace('\n', ''), [ f"Tweet: {G.edges[edge]['full_text']}" for edge in G.edges()]))

def genEdgeTextTrace(xtext: list, ytext: list, text: list ) -> SCATTER:
    """Function to Generate Edge Text Traces"""
    return go.Scatter(
            x=xtext, y=ytext,
            mode='markers',
            text=text,
            opacity=0
    )

def genNodeColor(node: str) -> str:
    """Function to decide node color for mapping"""
    if node.startswith("#"):
        return 'yellow'
    else:
        return 'purple'

def genNode(G: GRAPH, pos: dict) -> tuple:
    """Function to Generate Node Coordinates"""
    node_x, node_y, node_color = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_color.append(genNodeColor(node=node))

    return node_x, node_y, node_color

def genNodeTrace(x: list, y: list, node_color: list, nodes: list) -> SCATTER:
    """Function to Generate Node Trace"""
    return go.Scatter(
        x=x, y=y,
        mode='markers',
        text=nodes,
        hoverinfo='text',
        marker={'color': node_color},
        opacity=0.7
    )

def genLayout(title: str) -> LAYOUT:
    """Function to Generate Layout"""
    return go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=title,
        titlefont_size=16,
        showlegend=False,
        width=1400,
        height=1600,
        hovermode='closest',
        margin={
            'b':20, 'l':5, 'r':5, 't':40
        },
        xaxis={
            'showgrid': False,
            'zeroline': False,
            'showticklabels': False
        },
        yaxis={
            'showgrid': False,
            'zeroline': False,
            'showticklabels': False
        }
    )

def genFigure(data: list, layout: LAYOUT) -> FIGURE:
    """Function to generate Figure"""
    return go.Figure(data=data, layout=layout)


class Web:
    """Object to Generate Network Visualization"""
    def __init__(self, data: DATAFRAME, title: str ):

        self.title = title
        self.data = data                        # this should be dynamic eventually, to allow for different graphs
        self.G = nx.from_pandas_edgelist(data, 'tweet_user_name', 'search_query', # current case shows hashtags to accounts
                                                ['full_text', 'tweet_user_location'])
        self.pos = nx.spring_layout(self.G)

    def genEdges(self):
        """Function to generate all edge data and text"""
        # generate all coordinates for edges and text
        self.edge_x, self.edge_y, self.xtext, self.ytext = genEdge(G=self.G, pos=self.pos)
        self.edgeText = genEdgeText(G=self.G)
        # generate traces for edges and text
        self.edgeTrace = genEdgeTrace(x=self.edge_x, y=self.edge_y)
        self.edgeTextTrace = genEdgeTextTrace(xtext=self.xtext, ytext=self.ytext, text=self.edgeText)

    def genNodes(self):
        """Function to generate all Node coordinates and data"""
        # generate node data
        self.node_x, self.node_y, self.node_color = genNode(G=self.G, pos=self.pos)
        # generate node trace
        self.nodeTrace = genNodeTrace(x=self.node_x, y=self.node_y,
                                      node_color=self.node_color, nodes=list(self.G.nodes))

    def genFigure(self):
        """Function to generate layout and figure"""
        # generate layout and figure
        self.layout = genLayout(title=self.title)
        self.figure = genFigure(data=[self.edgeTrace, 
                                      self.nodeTrace, 
                                      self.edgeTextTrace], 
                                layout=self.layout)
    
    def generate(self):
        """Function to Generate Visual Web"""
        self.genEdges()
        self.genNodes()
        self.genFigure()        