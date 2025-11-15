from time import perf_counter_ns
import random
from typing import Optional, List

# --- Configuration ---
N = 100_000      # number of products (dataset size)
M = 1_000        # number of searches per category per round
ROUNDS = 10      # how many rounds to run
HT_SIZE = 131071 # hash table bucket count (prime-ish)
random.seed(42)  # deterministic sampling across runs

#product entity
class Product:
    def __init__(self, product_id: str, name: str):
        self.product_id = product_id
        self.name = name
    def __repr__(self):
        return f"Product({self.product_id})"

# separate chaining
class Node:
    def __init__(self, product: Product, next_node: Optional['Node'] = None):
        self.product = product
        self.next = next_node

class HashTable:
    def __init__(self, size: int = HT_SIZE):
        self.size = size
        self.buckets: List[Optional[Node]] = [None] * size
        self.count = 0

    def _hash(self, key: str) -> int:
        return abs(hash(key)) % self.size

    def insert(self, product: Product) -> None:
        idx = self._hash(product.product_id)
        node = Node(product, self.buckets[idx])
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


#linear search on array
def linear_search(arr: List[Product], product_id: str) -> Optional[Product]:
    for p in arr:
        if p.product_id == product_id:
            return p
    return None

# Build dataset and data structures

print(f"Config: N={N:,}, M={M:,}, ROUNDS={ROUNDS}, HashTable size={HT_SIZE}")

# Create products
products = [Product(f"P{i:06d}", f"Product #{i}") for i in range(N)]

# Create and build hash table and array
ht = HashTable(size=HT_SIZE)
arr: List[Product] = []

t0 = perf_counter_ns()
for p in products:
    ht.insert(p)
t1 = perf_counter_ns()
ht_build_ns = t1 - t0

t0 = perf_counter_ns()
for p in products:
    arr.append(p)
t1 = perf_counter_ns()
arr_build_ns = t1 - t0

print(f"Build times (ns): HashTable={ht_build_ns:,}, Array append={arr_build_ns:,}\n")

# run the rounds

rounds_results = []

for r in range(1, ROUNDS + 1):
    # Prepare keys: M existing, M missing
    existing_keys = random.sample([p.product_id for p in products], M)
    missing_keys = [f"X{random.randint(N, N*10):06d}" for _ in range(M)]

    # HashTable -> existing
    t0 = perf_counter_ns()
    for key in existing_keys:
        _ = ht.search(key)
    t1 = perf_counter_ns()
    ht_existing_total = t1 - t0

    # Array -> existing
    t0 = perf_counter_ns()
    for key in existing_keys:
        _ = linear_search(arr, key)
    t1 = perf_counter_ns()
    arr_existing_total = t1 - t0

    # HashTable -> missing
    t0 = perf_counter_ns()
    for key in missing_keys:
        _ = ht.search(key)
    t1 = perf_counter_ns()
    ht_missing_total = t1 - t0

    # Array -> missing
    t0 = perf_counter_ns()
    for key in missing_keys:
        _ = linear_search(arr, key)
    t1 = perf_counter_ns()
    arr_missing_total = t1 - t0

    # Save round
    rounds_results.append({
        "round": r,
        "ht_existing_ns": ht_existing_total,
        "arr_existing_ns": arr_existing_total,
        "ht_missing_ns": ht_missing_total,
        "arr_missing_ns": arr_missing_total
    })

    # Print per-round results
    print(
        f"Round {r:2d}: "
        f"HT(existing)={ht_existing_total:,} ns, ARR(existing)={arr_existing_total:,} ns, "
        f"HT(missing)={ht_missing_total:,} ns, ARR(missing)={arr_missing_total:,} ns"
    )

# Compute averages and summary

def average(key: str) -> float:
    return sum(d[key] for d in rounds_results) / len(rounds_results)

avg_ht_existing = average("ht_existing_ns")
avg_arr_existing = average("arr_existing_ns")
avg_ht_missing = average("ht_missing_ns")
avg_arr_missing = average("arr_missing_ns")

print("\nAverages over rounds (ns):")
print(f"  HashTable existing avg: {avg_ht_existing:,.0f} ns")
print(f"  Array existing    avg: {avg_arr_existing:,.0f} ns")
print(f"  HashTable missing avg: {avg_ht_missing:,.0f} ns")
print(f"  Array missing     avg: {avg_arr_missing:,.0f} ns\n")

ratio_existing = avg_arr_existing / avg_ht_existing if avg_ht_existing > 0 else float('inf')
ratio_missing = avg_arr_missing / avg_ht_missing if avg_ht_missing > 0 else float('inf')

print(f"Speedup (Array / Hash) existing ~ {ratio_existing:.1f}x (higher means array slower)")
print(f"Speedup (Array / Hash) missing  ~ {ratio_missing:.1f}x (higher means array slower)")

print(f"\nCounts sanity check: HashTable stored {ht.count}, Array stored {len(arr)}")




