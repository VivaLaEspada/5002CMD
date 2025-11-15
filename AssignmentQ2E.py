
from typing import Dict, Generic, List, Optional, Set, TypeVar, Literal
import sys

T = TypeVar('T')


# Person entity (Q2)
class Person:
    """Represents a social-media user."""
    def __init__(self, user_id: str, name: str, gender: str = "", bio: str = "", privacy: Literal["public", "private"] = "public"):
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.bio = bio
        # privacy: "public" or "private"
        if privacy not in ("public", "private"):
            raise ValueError("privacy must be 'public' or 'private'")
        self.privacy = privacy

    def __repr__(self) -> str:
        return f"Person(user_id={self.user_id!r}, name={self.name!r}, privacy={self.privacy!r})"

    def __str__(self) -> str:
        return f"{self.name} ({self.user_id})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Person):
            return False
        return self.user_id == other.user_id

    def __hash__(self) -> int:
        return hash(self.user_id)

# Directed Graph (Q1)

class DirectedGraph(Generic[T]):

    def __init__(self) -> None:
        self._adj: Dict[T, Set[T]] = {}

    # --- required operations ---
    def addVertex(self, v: T) -> None:
        if v not in self._adj:
            self._adj[v] = set()

    def addEdge(self, src: T, dst: T) -> None:
        # auto-add missing vertices
        if src not in self._adj:
            self._adj[src] = set()
        if dst not in self._adj:
            self._adj[dst] = set()
        self._adj[src].add(dst)

    def listOutgoingAdjacentVertex(self, v: T) -> List[T]:
        neighbors = self._adj.get(v)
        if neighbors is None:
            return []
        return list(neighbors)

    # --- helpful extras ---
    def removeEdge(self, src: T, dst: T) -> bool:
        if src not in self._adj:
            return False
        if dst in self._adj[src]:
            self._adj[src].remove(dst)
            return True
        return False

    def hasVertex(self, v: T) -> bool:
        return v in self._adj

    def vertices(self) -> List[T]:
        return list(self._adj.keys())

    def __str__(self) -> str:
        lines = []
        for v, nbrs in self._adj.items():
            nbr_list = [str(x) for x in nbrs]
            lines.append(f"{v} -> {nbr_list}")
        return "\n".join(lines)



# Sample data creation (Q3 & Q4)

def create_sample_graph() -> (DirectedGraph[Person], List[Person]):
    graph: DirectedGraph[Person] = DirectedGraph()

    # Create 7 sample people (between 5 and 10)
    alice = Person("u001", "Alice", "Female", "Travel lover and photographer.", "public")
    bob = Person("u002", "Bob", "Male", "Coffee enthusiast and dev.", "private")
    charlie = Person("u003", "Charlie", "Other", "Tech geek, open-source fan.", "public")
    diana = Person("u004", "Diana", "Female", "Fitness coach.", "public")
    ethan = Person("u005", "Ethan", "Male", "Gamer and streamer.", "private")
    fiona = Person("u006", "Fiona", "Female", "Food blogger.", "public")
    george = Person("u007", "George", "Male", "Home chef.", "public")

    people = [alice, bob, charlie, diana, ethan, fiona, george]

    # Add vertices
    for p in people:
        graph.addVertex(p)

    # Make follow relationships (directed): (who follows whom)
    # Alice follows Bob and Charlie
    graph.addEdge(alice, bob)
    graph.addEdge(alice, charlie)
    # Bob follows Diana
    graph.addEdge(bob, diana)
    # Charlie follows Alice (mutual with Alice->Charlie not required)
    graph.addEdge(charlie, alice)
    # Diana follows Ethan and Fiona
    graph.addEdge(diana, ethan)
    graph.addEdge(diana, fiona)
    # Ethan follows Bob
    graph.addEdge(ethan, bob)
    # Fiona follows George
    graph.addEdge(fiona, george)
    # George follows no one (example)

    return graph, people



# Utility helpers
def find_person_by_name(people: List[Person], name: str) -> Optional[Person]:
    for p in people:
        if p.name.lower() == name.lower():
            return p
    return None


def list_followers(graph: DirectedGraph[Person], target: Person) -> List[Person]:
    # incoming edges: find all vertices that have 'target' in their outgoing set
    followers: List[Person] = []
    for v in graph.vertices():
        nbrs = graph.listOutgoingAdjacentVertex(v)
        if target in nbrs:
            followers.append(v)
    return followers

# Menu-driven program (Question 5)


def print_menu():
    print("\n=== Social Media Menu ===")
    print("1. Display all users' names")
    print("2. View a user's full profile (ignore privacy)  [Mandatory]")
    print("3. View the list of accounts a user follows (outgoing)")
    print("4. View the list of followers of a user (incoming)")
    print("5. Add a new user profile")
    print("6. Follow someone (user X follows user Y)")
    print("7. Unfollow someone (user X unfollows user Y)")
    print("8. View a user's profile (respect privacy)  [Optional feature]")
    print("9. Show full graph (debug)")
    print("0. Exit")


def prompt_new_person() -> Person:
    print("\nEnter new user details:")
    user_id = input("User ID (unique): ").strip()
    name = input("Name: ").strip()
    gender = input("Gender: ").strip()
    bio = input("Biography: ").strip()
    while True:
        privacy = input("Privacy ('public' or 'private'): ").strip().lower()
        if privacy in ("public", "private"):
            break
        print("Invalid privacy value. Enter 'public' or 'private'.")
    return Person(user_id, name, gender, bio, privacy)


def menu(graph: DirectedGraph[Person], people: List[Person]) -> None:
    # maintain people list in sync with graph (so adding new users works)
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        # 1. Display all users' names
        elif choice == "1":
            print("\nAll users:")
            if not people:
                print(" (none)")
            for p in people:
                print(" -", p.name)

        # 2. View full profile ignoring privacy
        elif choice == "2":
            name = input("Enter user name: ").strip()
            person = find_person_by_name(people, name)
            if not person:
                print("User not found.")
            else:
                print("\n--- Full Profile (privacy ignored--) ---")
                print(f"User ID : {person.user_id}")
                print(f"Name    : {person.name}")
                print(f"Gender  : {person.gender}")
                print(f"Bio     : {person.bio}")
                print(f"Privacy : {person.privacy}")

        # 3. View the list of accounts a user follows (outgoing)
        elif choice == "3":
            name = input("Enter user name: ").strip()
            person = find_person_by_name(people, name)
            if not person:
                print("User not found.")
            else:
                following = graph.listOutgoingAdjacentVertex(person)
                print(f"\n{person.name} follows ({len(following)}):")
                if not following:
                    print(" (none)")
                for f in following:
                    print(" ->", f.name)

        # 4. View list of followers (incoming edges)
        elif choice == "4":
            name = input("Enter user name: ").strip()
            person = find_person_by_name(people, name)
            if not person:
                print("User not found.")
            else:
                followers = list_followers(graph, person)
                print(f"\nFollowers of {person.name} ({len(followers)}):")
                if not followers:
                    print(" (none)")
                for f in followers:
                    print(" <-", f.name)

        # 5. Add a new user profile (optional)
        elif choice == "5":
            new_person = prompt_new_person()
            # ensure unique user_id and name
            if any(p.user_id == new_person.user_id for p in people):
                print("A user with that ID already exists. Aborting.")
            elif any(p.name.lower() == new_person.name.lower() for p in people):
                print("A user with that name already exists. Aborting.")
            else:
                people.append(new_person)
                graph.addVertex(new_person)
                print(f"Added user: {new_person}")

        # 6. Follow someone (user X follows user Y)
        elif choice == "6":
            name_x = input("Enter follower's name (X): ").strip()
            name_y = input("Enter follower's name (Y): ").strip()
            x = find_person_by_name(people, name_x)
            y = find_person_by_name(people, name_y)
            if not x or not y:
                print("One or both users not found.")
            else:
                graph.addEdge(x, y)
                print(f"{x.name} now follows {y.name}.")

        # 7. Unfollow someone
        elif choice == "7":
            name_x = input("Enter follower's name (X): ").strip()
            name_y = input("Enter follower's name (Y): ").strip()
            x = find_person_by_name(people, name_x)
            y = find_person_by_name(people, name_y)
            if not x or not y:
                print("One or both users not found.")
            else:
                removed = graph.removeEdge(x, y)
                if removed:
                    print(f"{x.name} unfollowed {y.name}.")
                else:
                    print(f"{x.name} was not following {y.name}.")

        # 8. View profile with privacy respected (optional)
        elif choice == "8":
            name = input("Enter user name: ").strip()
            person = find_person_by_name(people, name)
            if not person:
                print("User not found.")
            else:
                print("\n--- Profile (privacy respected++) ---")
                print(f"Name : {person.name}")
                if person.privacy == "public":
                    print(f"User ID: {person.user_id}")
                    print(f"Gender : {person.gender}")
                    print(f"Bio    : {person.bio}")
                else:
                    print("(private profile - other details hidden)")

        # 9. Show full graph (debug)
        elif choice == "9":
            print("\nGraph adjacency (debug):")
            print(graph)

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    g, people_list = create_sample_graph()
    menu(g, people_list)
