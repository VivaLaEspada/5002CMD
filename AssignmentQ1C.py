from typing import Optional, List
import sys

class Product:

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
    def __init__(self, product: Product, next_node: Optional['Node'] = None):
        self.product = product
        self.next = next_node

class HashTable:
    def __init__(self, size: int = 1031):
        self.size = size
        self.buckets: List[Optional[Node]] = [None] * size
        self.count = 0
    def _hash(self, key: str) -> int:
        return abs(hash(key)) % self.size

    def insert(self, product: Product) -> None:
        # Prevent duplicate product_id: replace existing
        idx = self._hash(product.product_id)
        node = self.buckets[idx]
        while node is not None:
            if node.product.product_id == product.product_id:
                # replace existing product record
                node.product = product
                return
            node = node.next
        # otherwise prepend
        node = Node(product, self.buckets[idx])
        self.buckets[idx] = node
        self.count += 1

    def search(self, product_id: str) -> Optional[Product]:
        idx = self._hash(product_id)
        node = self.buckets[idx]
        while node:
            if node.product.product_id == product_id:
                return node.product
            node = node.next
        return None

    def remove(self, product_id: str) -> bool:
        idx = self._hash(product_id)
        prev = None
        node = self.buckets[idx]
        while node:
            if node.product.product_id == product_id:
                if prev is None:
                    self.buckets[idx] = node.next
                else:
                    prev.next = node.next
                self.count -= 1
                return True
            prev = node
            node = node.next
        return False

    def display_all(self) -> None:
        print("\n Baby Shop Inventory:\n")
        any_item = False
        for node in self.buckets:
            while node:
                print(" -", node.product)
                any_item = True
                node = node.next
        if not any_item:
            print(" (empty)")

    def __len__(self) -> int:
        return self.count


# --- Utility functions for CLI ---

def prompt_product_input(existing_id: Optional[str] = None) -> Product:
    if existing_id:
        product_id = existing_id
        print(f"Editing product {product_id}")
    else:
        product_id = input("Enter Product ID: ").strip()
    name = input("Enter Name: ").strip()
    category = input("Enter Category: ").strip()

    while True:
        price_str = input("Enter Price (e.g. 45.90): ").strip()
        try:
            price = float(price_str)
            break
        except ValueError:
            print("Invalid price. Try again.")

    while True:
        stock_str = input("Enter Stock (integer): ").strip()
        try:
            stock = int(stock_str)
            break
        except ValueError:
            print("Invalid stock. Try again.")

    return Product(product_id, name, category, price, stock)


def cli_insert(inventory: HashTable) -> None:
    pid = input("Product ID to insert: ").strip()
    if not pid:
        print("Product ID cannot be empty.")
        return
    existing = inventory.search(pid)
    if existing:
        print("A product with this ID already exists:")
        print(" ", existing)
        choice = input("Overwrite? (y/N): ").strip().lower()
        if choice != "y":
            print("Insert cancelled.")
            return
        # If overwriting, prompt fields but keep same id
        new_product = prompt_product_input(existing_id=pid)
        inventory.insert(new_product)
        print("Product overwritten.")
        return

    # new insertion
    new_product = prompt_product_input(existing_id=pid)
    inventory.insert(new_product)
    print("Product inserted.")


def cli_search(inventory: HashTable) -> None:
    pid = input("Product ID to search: ").strip()
    if not pid:
        print("Product ID cannot be empty.")
        return
    found = inventory.search(pid)
    if found:
        print("Found:")
        print(" ", found)
    else:
        print("Product not found.")


def cli_edit(inventory: HashTable) -> None:
    pid = input("Product ID to edit: ").strip()
    if not pid:
        print("Product ID cannot be empty.")
        return
    existing = inventory.search(pid)
    if not existing:
        print("Product not found.")
        return
    print("Current:", existing)
    updated = prompt_product_input(existing_id=pid)
    inventory.insert(updated)  # insert replaces existing
    print("Product updated.")


def cli_delete(inventory: HashTable) -> None:
    pid = input("Product ID to delete: ").strip()
    if not pid:
        print("Product ID cannot be empty.")
        return
    confirm = input(f"Are you sure you want to delete {pid}? (y/N): ").strip().lower()
    if confirm != "y":
        print("Delete cancelled.")
        return
    removed = inventory.remove(pid)
    print("Removed:" if removed else "Product not found.")


def print_menu() -> None:
    print("\n=== Baby Shop Inventory CLI ===")
    print("1) Insert product")
    print("2) Search product")
    print("3) Edit product (optional)")
    print("4) Delete product (optional)")
    print("5) List all products")
    print("6) Exit")

def seed_sample_products(inventory: HashTable) -> None:
    sample_products = [
        Product("BB001", "Random Diapers M-Size", "Diapers", 45.90, 100),
        Product("BB002", "Random Baby Wipes", "Baby Care", 12.50, 200),
        Product("BB003", "Random Feeding Bottle", "Feeding", 59.90, 50),
    ]
    for p in sample_products:
        inventory.insert(p)

def main():
    inventory = HashTable(size=101)
    seed_sample_products(inventory)
    print("Sample products loaded. Total:", len(inventory))

    while True:
        print_menu()
        choice = input("Choose an option [1-6]: ").strip()
        if choice == "1":
            cli_insert(inventory)
        elif choice == "2":
            cli_search(inventory)
        elif choice == "3":
            cli_edit(inventory)
        elif choice == "4":
            cli_delete(inventory)
        elif choice == "5":
            inventory.display_all()
        elif choice == "6":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
