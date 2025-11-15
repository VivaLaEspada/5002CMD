import threading
import time

def factorial(n):
    """Iterative factorial"""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def compute_factorial(n, results, index):
    """
    worker for each thread.
    records its own start and end timestamps (time.time_ns()).
    """
    start = time.time_ns()
    factorial(n)
    end = time.time_ns()
    results[index] = (start, end)

def multithread_test():
    numbers = [50, 100, 200]   # the factorial sizes
    rounds = 10
    chosen_times = []      # times actually used (assignment method or fallback)
    fallback_times = []    # always-recorded overall start->end (for diagnostics)

    print("Running multithreaded test: computing", numbers, "for", rounds, "rounds.\n")

    for r in range(1, rounds + 1):
        results = [None] * len(numbers)
        threads = []

        # Create thread objects
        for i, n in enumerate(numbers):
            t = threading.Thread(target=compute_factorial, args=(n, results, i))
            threads.append(t)

        # record overall start just before starting the threads (for robust fallback)
        overall_start = time.time_ns()

        # Start threads
        for t in threads:
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()

        # Record overall end right after all threads finished
        overall_end = time.time_ns()

        # Extract per-thread timestamps
        thread_starts = [res[0] for res in results]
        thread_ends = [res[1] for res in results]

        # Assignment-specified formula:
        # Time_Elapsed = End_Time_Of_Thread_Finished_Last – Start_Time_Of_Thread_That_Started_First
        min_thread_start = min(thread_starts)
        max_thread_end = max(thread_ends)
        assignment_elapsed = max_thread_end - min_thread_start

        # Fallback (robust) overall elapsed
        overall_elapsed = overall_end - overall_start

        # Choose the assignment elapsed unless it's zero (or absurdly small),
        # then fall back to overall_elapsed.
        # (We still keep both numbers for transparency.)
        used_elapsed = assignment_elapsed if assignment_elapsed > 0 else overall_elapsed

        chosen_times.append(used_elapsed)
        fallback_times.append(overall_elapsed)

        # print round summary
        print(f"Round {r}:")
        print(f"  Assignment elapsed (max thread end - min thread start): {assignment_elapsed} ns")
        print(f"  Overall elapsed (start before threads -> end after join)   : {overall_elapsed} ns")
        # per-thread durations for debugging/inspection
        for i, n in enumerate(numbers):
            s, e = results[i]
            print(f"    Thread for {n}! -> start {s}, end {e}, duration {e - s} ns")
        print(f"  -> Used elapsed for round {r}: {used_elapsed} ns\n")

    # Summary
    avg_used = sum(chosen_times) // len(chosen_times)
    avg_fallback = sum(fallback_times) // len(fallback_times)

    print("=== Summary ===")
    print("Times used per round (ns):")
    for i, t in enumerate(chosen_times, start=1):
        print(f"  Round {i}: {t} ns")
    print(f"\nAverage (used values): {avg_used} ns")
    print(f"Average (overall fallback values): {avg_fallback} ns")

if __name__ == "__main__":
    multithread_test()
