from typing import Optional, List

# Define Product class (missing from original code)
class Product:
    def __init__(self, product_id: str, name: str):
        self.product_id = product_id
        self.name = name

# Linked list node for bucket
class Node:
    def __init__(self, product: 'Product', next_node: Optional['Node'] = None):
        self.product = product
        self.next = next_node

# Hash Table with separate chaining (linked lists)
class HashTable:
    def __init__(self, size: int = 1031):
        # Use a prime-sized bucket count by default for better distribution.


        self.size = size
        self.buckets: List[Optional[Node]] = [None] * size
        self.count = 0

    def _hash(self, key: str) -> int:
        return abs(hash(key)) % self.size

    def insert(self, product: Product) -> None:
        idx = self._hash(product.product_id)
        node = Node(product, self.buckets[idx])  # prepend for O(1) insert
        self.buckets[idx] = node
        self.count += 1

    def search(self, product_id: str) -> Optional[Product]:
        idx = self._hash(product_id)
        node = self.buckets[idx]
        while node is not None:
            if node.product.product_id == product_id:
                return node.product
            node = node.next
        return None

    def remove(self, product_id: str) -> bool:
        idx = self._hash(product_id)
        prev = None
        node = self.buckets[idx]
        while node is not None:
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
