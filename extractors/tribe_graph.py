#!/usr/bin/env python3
"""
TRIBE GRAPH EXTRACTION
======================
Network analysis using Python's power.

Fast graph building, community detection, mentor finding.
"""

from typing import Dict, List
from collections import defaultdict
from copy import deepcopy

# Try to import networkx, fallback to simple implementation
try:
    import networkx as nx  # type: ignore[import-untyped]

    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False
    nx = None  # type: ignore[assignment]
    print("⚠️  NetworkX not installed - using simple graph implementation")


def build_tribe_graph(activities: List) -> Dict:
    """
    Build collaboration graph - Python makes this easy.

    Week 4: Deep copy to safe schema (no shared references)
    Week 5: Use appropriate data structures (dict, set)

    Returns:
        Graph representation (dict or NetworkX graph)
    """
    edge_weights: Dict[tuple[str, str], int] = defaultdict(int)
    nodes: set[str] = set()

    # Fast iteration - collect edges
    # Week 4: Create safe copies (no shared references)
    for activity in activities:
        # Deep copy to avoid shared references
        if hasattr(activity, "user_id"):
            user_id = activity.user_id
            target_id = activity.target_user_id
        else:
            # Dict access - create copy
            activity_copy = deepcopy(activity)
            user_id = activity_copy.get("user_id", "")
            target_id = activity_copy.get("target_user_id", "")

        if user_id and target_id and user_id != target_id:
            u1, u2 = sorted([user_id, target_id])  # Undirected
            edge_weights[(u1, u2)] += 1
            nodes.add(u1)
            nodes.add(u2)

    # Build graph structure
    if HAS_NETWORKX:
        G = nx.Graph()
        for (u1, u2), weight in edge_weights.items():
            G.add_edge(u1, u2, weight=weight)
        return G
    else:
        # Simple dict-based graph
        graph = {
            "nodes": list(nodes),
            "edges": [
                {"source": u1, "target": u2, "weight": weight}
                for (u1, u2), weight in edge_weights.items()
            ],
        }
        return graph


def extract_communities(graph) -> List[List[str]]:
    """
    Detect communities - one library call if NetworkX available.
    """
    if HAS_NETWORKX and isinstance(graph, nx.Graph):
        try:
            communities = nx.community.greedy_modularity_communities(graph)
            return [list(comm) for comm in communities]
        except Exception:
            # Fallback to connected components
            communities = nx.connected_components(graph)
            return [list(comm) for comm in communities]
    else:
        # Simple connected components
        edges = graph.get("edges", [])
        node_connections = defaultdict(set)

        for edge in edges:
            u1, u2 = edge["source"], edge["target"]
            node_connections[u1].add(u2)
            node_connections[u2].add(u1)

        # Simple BFS for components
        visited = set()
        communities = []

        for node in graph.get("nodes", []):
            if node in visited:
                continue

            # BFS
            component = []
            queue = [node]
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                component.append(current)
                for neighbor in node_connections.get(current, []):
                    if neighbor not in visited:
                        queue.append(neighbor)

            if len(component) >= 3:  # Minimum community size
                communities.append(component)

        return communities


def find_mentors(graph, users: Dict, top_n: int = 10) -> List[Dict]:
    """
    Find mentor candidates - fast Python operations.

    Uses centrality or connection count.
    """
    if HAS_NETWORKX and isinstance(graph, nx.Graph):
        # Fast centrality calculation
        centrality = nx.degree_centrality(graph)
        candidates = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]

        return [
            {
                "user_id": user_id,
                "centrality": score,
                "connections": graph.degree(user_id),
                "activity_count": users.get(user_id, {}).activity_count
                if hasattr(users.get(user_id, {}), "activity_count")
                else 0,
            }
            for user_id, score in candidates
        ]
    else:
        # Simple: count connections
        edges = graph.get("edges", [])
        connection_count: Dict[str, int] = defaultdict(int)

        for edge in edges:
            connection_count[edge["source"]] += 1
            connection_count[edge["target"]] += 1

        candidates = sorted(connection_count.items(), key=lambda x: x[1], reverse=True)[:top_n]

        return [
            {
                "user_id": user_id,
                "connections": count,
                "activity_count": users.get(user_id, {}).activity_count
                if hasattr(users.get(user_id, {}), "activity_count")
                else 0,
            }
            for user_id, count in candidates
        ]


def find_bridges(graph, communities: List[List[str]]) -> List[Dict]:
    """
    Find users who bridge communities.
    """
    if HAS_NETWORKX and isinstance(graph, nx.Graph):
        # Find betweenness centrality
        betweenness = nx.betweenness_centrality(graph)
        bridges = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]

        return [
            {
                "user_id": user_id,
                "betweenness": score,
                "bridges_communities": len([c for c in communities if user_id in c]),
            }
            for user_id, score in bridges
        ]
    else:
        # Simple: users in multiple communities
        user_communities = defaultdict(set)
        for i, comm in enumerate(communities):
            for user in comm:
                user_communities[user].add(i)

        bridges = [
            {"user_id": user, "communities": len(comms)}
            for user, comms in user_communities.items()
            if len(comms) > 1
        ]

        return sorted(bridges, key=lambda x: x["communities"], reverse=True)[:10]


if __name__ == "__main__":
    # Quick test
    print("TRIBE Graph Extractor - Ready")
    print("Use build_tribe_graph(), extract_communities(), find_mentors()")
