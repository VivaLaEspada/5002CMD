from AssignmentQ2B import Person
from AssignmentQ2A import DirectedGraph
def create_people():
    mamamia=Person("u001", "Mamamia", "Female", "Travel lover", "public")
    bobby=Person("u002", "Bobby", "Male", "Coffee enthusiast", "private")
    charlie=Person("u003", "Charlie", "Other", "Tech geek", "public")
    diana=Person("u004", "Diana", "Female", "Fitness fan", "public")
    ethan=Person("u005", "Ethan", "Male", "Restless Gambler", "private")

    return [mamamia, bobby, charlie, diana, ethan]
def build_social_media_graph():
    graph = DirectedGraph[Person]()
    # Load people
    people = create_people()
    # add everyone as vertices
    for p in people:
        graph.addVertex(p)
    #create following edges
    graph.addEdge(people[0], people[1])
    graph.addEdge(people[0], people[2])
    graph.addEdge(people[1], people[3])
    graph.addEdge(people[2], people[0])
    graph.addEdge(people[3], people[4])
    graph.addEdge(people[4], people[1])
    return graph, people

if __name__ == "__main__":
    graph, people = build_social_media_graph()
    # Show outgoing edges and who each person follows
    print("=== FOLLOWING LIST ===")
    for p in people:
        print(f"{p.name} follows:")
        neighbours = graph.listOutgoingAdjacentVertex(p)
        for n in neighbours:
            print("  →", n.name)
        print()
