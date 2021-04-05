import decimal


class Node:
    def __init__(self, denom: str, amount: decimal):
        self.denom = denom
        self.amount = amount
        self.edges = set()


class Edge:
    def __init__(self, start, end, weight=None):
        self.start = start
        self.to = end
        self.weight = weight


class Graph:
    def __init__(self, *nodes):
        self.nodes = set()
