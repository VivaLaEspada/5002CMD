from typing import Dict, Generic, Iterable, List, Optional, Set, TypeVar
T = TypeVar('T')
class DirectedGraph(Generic[T]):


    def __init__(self) -> None:
        self._adj: Dict[T, Set[T]] = {}

    def addVertex(self, v: T) -> None:
        #add vertex v. If it already exists, do nothing.
        if v not in self._adj:
            self._adj[v] = set()

    def addEdge(self, src: T, dst: T) -> None:

        # Auto-add vertices for convenience
        if src not in self._adj:
            self._adj[src] = set()
        if dst not in self._adj:
            self._adj[dst] = set()
        self._adj[src].add(dst)

    def listOutgoingAdjacentVertex(self, v: T) -> List[T]:

        #Return a list of outgoing adjacent vertices from v.
        #return empty list if no v

        neighbors = self._adj.get(v)
        if neighbors is None:
            return []
        return list(neighbors)

    def hasVertex(self, v: T) -> bool:
        #check if got vertex or not
        return v in self._adj

    def __str__(self) -> str:
        parts = []
        for v, nbrs in self._adj.items():
            parts.append(f"{v} -> {sorted(nbrs, key=str)}")
        return "\n".join(parts)

if __name__ == "__main__":
    g = DirectedGraph[str]()
    g.addVertex("A")
    g.addVertex("B")
    g.addEdge("A", "B")
    g.addEdge("A", "C")      # auto-adds C
    g.addEdge("B", "C")
    g.addEdge("C", "A")

    print("Outgoing from A:", g.listOutgoingAdjacentVertex("A"))
    print("Outgoing from B:", g.listOutgoingAdjacentVertex("B"))
    print("Outgoing from Z (missing):", g.listOutgoingAdjacentVertex("Z"))

    print("\nFull graph:")
    print(g)