#single threading
import time

def factorial(n):
    """iterative factorial function."""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def single_thread_test():
    numbers = [50, 100, 200]   # factorial sizes
    rounds =10
    times =[]       # store elapsed time per round (ns)

    print("Running single-threaded test: computing", numbers, "for", rounds, "rounds.\n")

    for r in range(1, rounds + 1):
        # record start time right before the first calculation
        start_all = time.time_ns()

        # optionally record per-number durations for extra info
        per_number_times = []
        for n in numbers:
            s =time.time_ns()
            factorial(n)
            e =time.time_ns()
            per_number_times.append((n, e - s))

        # record end time after last calculation
        end_all = time.time_ns()
        elapsed = end_all - start_all
        times.append(elapsed)
        # print results for this round
        print(f"Round {r}:")
        print(f"  Total elapsed (50! then 100! then 200!): {elapsed} ns")
        for n, dt in per_number_times:
            print(f"    {n}! duration: {dt} ns")
        print()

    # summary
    avg_time = sum(times) // len(times)
    print("=== Summary (single-threaded) ===")
    for i, t in enumerate(times, start=1):
        print(f"  Round {i}: {t} ns")
    print(f"\nAverage time over {rounds} rounds: {avg_time} ns")

if __name__ == "__main__":
    single_thread_test()
