from decimal import Decimal
from offline.graph_project.data_structures import Graph, Node, Edge
from offline.graph_project import data_sources

"""
Used to generate the prices of each asset
Hot take: edges don't really matter for this.  They are unfinished for MIR
"""


class TerraPriceGraph:
    ust_node = Node("uusd", Decimal(1.0))
    luna_price_in_ust = None

    def build_terra_luna_graph(self, graph: Graph):
        """
        Build a doubly linked unweighted graph of all assets.  Prices are normalized to UST
        """

        nodes = set()

        # build luna terra graph
        response = data_sources.get_terra_prices()

        luna = Node("luna", 1)

        for line in response:
            node = Node(line["denom"], Decimal(line["amount"]))

            if node.denom == "uusd":
                self.ust_node.amount = Decimal(1.0)
                self.luna_price_in_ust = Decimal(node.amount)
            else:
                node.edges.add(Edge(node, self.ust_node))
                self.ust_node.edges.add(Edge(self.ust_node, node))

            nodes.add(node)

        for node in nodes:
            if node.denom != "uusd":
                node.amount = node.amount / self.luna_price_in_ust

        luna.amount = self.ust_node.amount
        nodes.add(luna)

        graph.nodes |= nodes

    def build_anc_graph(self, graph):
        """
        Get the price of ANC in UST
        Add it to the graph
        """
        nodes = set()

        response = data_sources.get_anc_prices()
        anchor_price = response['second']['data']['AnchorBorrowerDistributionAPYs'][0]['ANCPrice']

        anchor = Node("anc", anchor_price)
        anchor.edges.add(Edge(anchor, self.ust_node))
        self.ust_node.edges.add(Edge(self.ust_node, anchor))

        nodes.add(anchor)

        graph.nodes |= nodes

    def build_mir_graph(self, graph):
        nodes = set()

        response = data_sources.get_mirror_prices()
        for line in response['assets']:
            node = Node(denom=line["symbol"], amount=line["prices"]["price"])
            nodes.add(node)

        graph.nodes |= nodes

    def build(self):
        graph = Graph()
        self.build_terra_luna_graph(graph)
        self.build_anc_graph(graph)
        self.build_mir_graph(graph)
        return graph


if __name__ == "__main__":
    builder = TerraPriceGraph()
    graph = builder.build()
    pass
