
from typing import Literal
class Person:

    def __init__(
        self,
        user_id: str,
        name: str,
        gender: str,
        bio: str = "",
        privacy: Literal["public", "private"] = "public",
    ):
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.bio = bio
        self.privacy = privacy

    def __str__(self) -> str:
        #Human-readable representation for printing.
        return f"{self.name} ({self.user_id}) - {self.privacy} profile"

    def __repr__(self) -> str:
        #More technical representation, useful for debugging.
        return (
            f"Person(user_id={self.user_id!r}, name={self.name!r}, "
            f"gender={self.gender!r}, privacy={self.privacy!r})"
        )

    def __eq__(self, other: object) -> bool:
        #Equality based on unique user_id.
        if not isinstance(other, Person):
            return False
        return self.user_id == other.user_id

    def __hash__(self) -> int:

        #Allows Person objects to be used as vertices in a set or dictionary,
        #e.g., inside a graph adjacency list.

        return hash(self.user_id)

if __name__ == "__main__":
    mamamia = Person("u001", "MamaMia", "Female", "Travel enthusiast", "public")
    bobby = Person("u002", "BobbyTheGreat", "Male", "Coffee enthusiast", "private")

    print(mamamia)
    print(bobby)
