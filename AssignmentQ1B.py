
from typing import Optional, List
class Product:
    #Entity class representing a baby shop product.
    def __init__(self, product_id: str, name: str, category: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def __repr__(self) -> str:
        return (
            f"Product(product_id={self.product_id!r}, name={self.name!r}, "
            f"category={self.category!r}, price={self.price!r}, stock={self.stock!r})"
        )

    def __str__(self) -> str:
        return f"[{self.product_id}] {self.name} ({self.category}) - RM{self.price:.2f}, Stock: {self.stock}"



class Node:
    #seperate chaining buckets

    def __init__(self, product: Product, next_node: Optional['Node'] = None):
        self.product = product
        self.next = next_node


class HashTable:
    # hash table using separate chaining (linked lists) for collisions."""

    def __init__(self, size: int = 1031):
        # prime-sized default is often a good starting point
        self.size = size
        self.buckets: List[Optional[Node]] = [None] * size
        self.count = 0

    def _hash(self, key: str) -> int:
        #compute a bucket index for a string key.
        return abs(hash(key)) % self.size

    def insert(self, product: Product) -> None:
        #insert product
        idx = self._hash(product.product_id)
        node = Node(product, self.buckets[idx])  # prepend for O(1)
        self.buckets[idx] = node
        self.count += 1

    def search(self, product_id: str) -> Optional[Product]:
        """Search for a product by its product_id. Return Product or None."""
        idx = self._hash(product_id)
        node = self.buckets[idx]
        while node is not None:
            if node.product.product_id == product_id:
                return node.product
            node = node.next
        return None

    def remove(self, product_id: str) -> bool:
        """Remove a product by id. Return True if removed, False if not found."""
        idx = self._hash(product_id)
        prev = None
        node = self.buckets[idx]
        while node is not None:
            if node.product.product_id == product_id:
                if prev is None:
                    # removing head of chain
                    self.buckets[idx] = node.next
                else:
                    prev.next = node.next
                self.count -= 1
                return True
            prev = node
            node = node.next
        return False

    def display_all(self) -> None:
        """Print all stored products (useful for debugging / inspection)."""
        print("\n Baby Shop Inventory:")
        for i, node in enumerate(self.buckets):
            while node:
                print(f" - {node.product}")
                node = node.next

    def __len__(self) -> int:
        return self.count


# --- Question 2: Build baby shop storage and insert sample records ---
if __name__ == "__main__":
    # choose a small table size for demonstration so collisions are visible
    inventory = HashTable(size=11)

    # Pre-defined baby shop products (you can change / extend these)
    sample_products = [
        Product("BB001", "Pampers Diapers M-Size", "Diapers", 45.90, 100),
        Product("BB002", "Huggies Baby Wipes", "Baby Care", 12.50, 200),
        Product("BB003", "Philips Avent Feeding Bottle", "Feeding", 59.90, 50),
        Product("BB004", "Johnson's Baby Lotion", "Baby Care", 14.90, 80),
        Product("BB005", "MamyPoko Pants XL", "Diapers", 49.90, 60),
        # Add a couple more to force collisions in the small table
        Product("BB006", "Tommee Tippee Spoon Set", "Feeding", 9.90, 120),
        Product("BB007", "Mustela Baby Wash", "Baby Care", 39.90, 40),
    ]

    # Insert sample products
    for p in sample_products:
        inventory.insert(p)

    print("✅ Records inserted successfully!")
    print("Total items:", len(inventory))

    # Search example
    pid = "BB003"
    found = inventory.search(pid)
    if found:
        print("\n🔍 Found:", found)
    else:
        print(f"\n Product {pid} not found.")

    # Remove example
    pid_remove = "BB002"
    removed = inventory.remove(pid_remove)
    print(f"\n🗑️ Removed {pid_remove}:", removed)
    print("Total items after removal:", len(inventory))

    # Display all items
    inventory.display_all()


    miss = "BB999"
    print("\nSearching for non-existent product (should be None):", inventory.search(miss))
