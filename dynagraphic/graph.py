import networkx as nx
from networkx.classes.filters import no_filter
from dynagraphic.node import GdcBioNode
from dynagraphic.edge import GdcBioEdge
from typing import List
from functools import reduce


class GdcDiGraph(nx.DiGraph):
    '''
    Custom method override for nx.DiGraph allowing cleaner node creation
    code and cleaner node dictionaries.

    This data structure underlies some capabilities of GdcBioGraph
    '''
    def add_node(self, node: dict) -> None:
        super().add_node(node.id, **node.data)



class GdcBioGraph():
    def __init__(self, node_list=[], edge_list=[]) -> None:
        self.graph = GdcDiGraph()
        self.nodes = {}
        self.edges = {}
        # Moving to keep subgraph state here instead of node display properties
        self.subgraph_nodes = set() # future use
        self.selected_nodes = set() # future use
        for node in node_list:
            self.add_node(node)
        for edge in edge_list:
            self.add_edge(edge)

    @classmethod
    def from_biodictionary(cls, dictionary: dict):
        '''
        Alternative constructor to build GdcBioGraph instances from 
        the GDC Biodictionary

        Returns a GdcBioGraph object
        '''
        def traverse_links(links: list | dict, lst: list=[]) -> list[str]:
            if isinstance(links, list):
                for link in links:
                    lst = traverse_links(link, lst)
            else:
                if 'subgroup' in links:
                    lst.extend(traverse_links(links['subgroup'], lst))
                else:
                    lst.append(links['target_type'])
            return lst
        node_list = []
        edge_list = []
        for key, node in dictionary.schema.items():
            # build node
            node_id: str = node['id']
            label: str = node['title']
            data = {
                'title': node['title'],
                'category': node['category'],
                'description': node['description'],
                'uniqueKeys': node['uniqueKeys'],
            }
            thisnode = GdcBioNode(node_id=node_id, label=label, data=data)
            thisnode.add_class(node['category'])
            thisnode.add_class('hidden')
            thisnode.add_class('not-selected')
            node_list.append(thisnode)
            # gather outward edges
            edges = [
                GdcBioEdge(source=node_id, target=target)
                for target 
                in traverse_links(node['links'], lst=[])
            ]
            edge_list.extend(edges)
        return cls(node_list, edge_list)

    # Add nodes and edges
    def add_node(self, node: GdcBioNode) -> None:
        # TODO: check that node doesn't already exist
        # node.set_graph(self)
        self.nodes[node.id] = node
        self.graph.add_node(node)

    def add_edge(self, edge: GdcBioEdge) -> None:
        self.edges[edge.id] = edge
        self.graph.add_edge(edge.source, edge.target)
    
    # Manage subgraph
    def node_in_subgraph(self, node_id: str) -> bool:
        return node_id in self.subgraph
        # return self.nodes[node_id].is_standard()

    ######## State-Modifying Actions
    def select_only_node(self, node_id: str) -> None:
        """
        Set node matching node_id to selected, de-select all others
        """
        self.selected_nodes = set([node_id])
    
    def add_node_to_selection(self, node_id: str) -> None:
        """
        Add node matching node_id to set of selected nodes
        """
        self.selected_nodes |= set([node_id])
    
    def select_no_nodes(self) -> None:
        """
        Clear selection so that no nodes are selected
        """
        self.selected_nodes = set()
    
    def add_subgraph_node(self, node_id: str) -> None:
        """
        Add node matching node_id to subgraph
        """
        self.subgraph_nodes |= set()
    
    def remove_subgraph_node(self, node_id: str) -> None:
        """
        Remove node matching node_id from subgraph
        """
        self.subgraph_nodes -= set([node_id])

    def empty_subgraph(self) -> None:
        """
        Reset subgraph so that it is empty
        """
        self.subgraph_nodes = set()

    ######### Render Methods
    # WORKING HERE:
    def render_subgraph(self) -> None:
        """
        Render the subgraph based on current state
        """
        # reset properties on all nodes and edges
        # If one node is selected, set fringe nodes and edges
        # set `selected`` for nodes in selected_nodes
        # create subgraph view for set of subgraph nodes and fringe nodes
        # report cytoscape elements

        # Can I determine a state delta from last render?
        # Would avoid quite so many updates each render cycle
        # main thing is set of subgraph nodes and selected nodes

    def reset_nodes(self) -> None:
        """
        reset properties on all nodes
        """
        
        pass
    
    def set_fringes(self) -> None:
        """
        Set fringe nodes on nodes in selection
        """
        pass

    def set_selected(self) -> None:
        """
        Set selected on nodes in selection
        """
        pass
    
    def render_cytoscape_elements(self) -> list:
        """
        Render ctoscape elements for subgraph
        """
        pass

    # def select_node(self, node_id: str) -> None:
    #     '''
    #     Select node matching node_id
    #     '''
    #     self.nodes[node_id].set_selected()

        # de-select other nodes
        # hide non-subgraph nodes
        # set 'fringe' on fringe nodes and edges
        # 
    
    def deselect_nodes(self) -> None:
        '''
        Deselect all nodes
        '''
        # de-select nodes
        for node_id, node in self.nodes.items():
            node.set_not_selected()
        # blank node details?
        # disable controls that depend on selection

    def set_display_nodes(self, node_id_list: list[str]) -> None:
        '''
        Set list of nodes to 'standard' and hide others
        '''
        for node_id in self.nodes.keys():
            if node_id in node_id_list:
                self.nodes[node_id].set_standard()
            else:
                self.nodes[node_id].set_hidden()
        
        for edge_id, edge in self.edges.items():
            if edge.source in node_id_list and edge.target in node_id_list:
                edge.set_standard()
            else:
                edge.set_hidden()

    def add_display_node(self, node_id: str) -> None:
        '''
        Set node display state to 'standard'
        '''
        # TODO: check if valid
        self.nodes[node_id].set_standard()
        
        # set inward edges to standard if source node is standard
        for src, tgt in self.graph.in_edges(node_id):
            if self.nodes[src].is_standard():
                self.edges[src, tgt].set_standard()
        # set edges out to standard if target is standard
        for src, tgt in self.graph.out_edges(node_id):
            if self.nodes[tgt].is_standard():
                self.edges[src, tgt].set_standard()


    def remove_display_node(self, node_id: str) -> None:
        '''
        Set node display state to 'hidden'
        '''
        # TODO: check if valid
        self.nodes[node_id].set_hidden()
        # self.node_stack.pop()
    
    def toggle_fringes_of_node(self, node_id: str) -> None:
        '''
        Toggle display of fringe nodes attached to node
        '''
        # find potential fringe nodes
        potential_fringe_nodes = set(list(self.graph.predecessors(node_id)))
        # subtract current subgraph nodes
        nodes_in_subgraph = set([
            nid 
            for nid, node 
            in self.nodes.items() 
            if node.is_standard()])
        potential_fringe_nodes -= nodes_in_subgraph
        # save set of current fringe nodes
        current_fringe_nodes = set([
            nid 
            for nid, node 
            in self.nodes.items()
            if node.is_fringe()])
        # hide all current fringe nodes
        for nid in current_fringe_nodes:
            self.nodes[nid].set_hidden()
        # if no potential fringe nodes are in current set
        #     display potential fringe nodes
        if len(potential_fringe_nodes & current_fringe_nodes) == 0:
            for nid in potential_fringe_nodes:
                self.nodes[nid].set_fringe()
                self.edges[(nid, node_id)].set_fringe()


    ######## State Control Functions
    # def update_display_state(self) -> None:
    #     '''
    #     Updates fringe and hidden status for nodes not part of
    #     subgraph
    #     '''
    #     nodes_in_subgraph = set([
    #         node_id 
    #         for node_id, node 
    #         in self.nodes.items() 
    #         if node.is_standard()])
    #     all_nodes = set(self.nodes.keys())
    #     not_in_subgraph = all_nodes - nodes_in_subgraph
    #     # hide ALL non-standard nodes
    #     for node_id in not_in_subgraph:
    #         self.nodes[node_id].set_hidden()
    #     # find fringe nodes and set them
    #     all_predecessors = set(reduce(
    #         lambda i, j: i + j,
    #         [
    #             list(self.graph.predecessors(node_id))
    #             for node_id 
    #             in nodes_in_subgraph
    #         ]))
    #     fringe_nodes = all_predecessors - nodes_in_subgraph
    #     for node_id in fringe_nodes:
    #         self.nodes[node_id].set_fringe()

        # def init_display_graph(self, node_list: List[str]=None) -> None:
        #     '''
        #     Default initialization for display_graph
        #     '''
        #     for node_id in node_list
        #     # node_filter_fn = no_filter
        #     # if node_list is not None:
        #     #     node_filter_fn = lambda node: node in node_list
        #     # self.display_graph = nx.subgraph_view(self.graph, filter_node=node_filter_fn)
    


    ######## View Generation Functions
    # def cyto_edge(self, edge: tuple[str, str]) -> dict:
    #     data_dict = {'data': {'source': edge[0], 'target': edge[1]}}
    #     return data_dict

    # TODO: add functions to calculate the states of 
    # 'NodeDetail' and 'ControlPanel' components

    def get_node_detail(self) -> str:
        '''
        Generate node details based on the graph state
        '''
        # Node detail with one node selected shows details of that node
        #    maybe just data dictionary for now
        # With two or more nodes selected
        #    Lists selected nodes
        pass
    
    def get_control_panel(self) -> list:
        '''
        Generate state of control panel based on the graph state
        '''
        # Delete node button is active only when one or more
        #   nodes are selected
        # Might have a list of control panel components to process
        pass

    def get_cytoscape_elements(self) -> list[dict]:
        # find list of non-hidden nodes
        visible_nodes = [
            node_id 
            for node_id, node 
            in self.nodes.items()
            if node.is_visible()]
        # create sub-graph view
        filter_node_fn = lambda node: node in visible_nodes
        sgv = nx.subgraph_view(self.graph, filter_node=filter_node_fn)
        # report cytoscape elements (nodes + edges)
        cyto_nodes = [self.nodes[node_id].cyto_repr() for node_id in sgv.nodes.keys()]
        cyto_edges = [self.edges[edge_id].cyto_repr() for edge_id in sgv.edges.keys()]
        # if self.display_graph is None:
        #     self.init_display_graph()
        # cyto_nodes = [self.nodes[node_id].cyto_repr() for node_id in self.display_graph.nodes.keys()]
        # cyto_edges = [self.cyto_edge(edge_id) for edge_id, edge_data in self.display_graph.edges.items()]
        # cyto_elements = 
        return cyto_nodes + cyto_edges


    # def set_node_classes(self, node_id: str, class_list: list[str]) -> None:
    #     '''
    #     set list of classes on a node directly
    #     '''
    #     self.nodes[node_id].set_classes(class_list)


    # def get_standard_nodes(self) -> None:
    #     '''
    #     Get list of nodes currently marked as standard
    #     '''