from collections import Set


class Node:
    def __init__(self, denom, amount):
        self.denom = denom
        self.amount = amount


class Edge:
    def __init__(self, weight):
        self.weight = weight


class Graph:
    nodes = Set(Node)
