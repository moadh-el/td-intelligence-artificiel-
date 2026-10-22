
import time
import matplotlib.pyplot as plt
import algorithms
from game import create_board


def benchmark(board, algorithm, **options):
    start = time.perf_counter()
    result = algorithm(board, **options)
    duration = time.perf_counter() - start

    return {
        "algorithm": algorithm.__name__,
        "move": result["move"],
        "score": result["score"],
        "nodes": result["nodes_explored"],
        "time": duration,
        "options": options,
    }


def run_experiments():
    board = create_board()
    results = []

    for depth in range(1, 6):
        results.append(benchmark(board, algorithms.minimax, depth=depth))

    for depth2 in range(1, 6):
        results.append(benchmark(board, algorithms.alphabeta, depth=depth2))

    for simulations in [100, 500, 1000, 2000]:
        results.append(benchmark(board, algorithms.mcts, num_simulations=simulations))

    return results


def print_results(results):
    print("Algorithm       Configuration       Move   Nodes   Time (s)")
    print("-" * 62)

    for result in results:
        options = result["options"]

        if "depth" in options:
            configuration = "Depth " + str(options["depth"])
        else:
            configuration = str(options["num_simulations"]) + " simulations"

        print(f"{result['algorithm']:<15} {configuration:<20} {str(result['move']):<7} {result['nodes']:<8} {result['time']:.6f}")


def draw_plots(results):

    minimax = [r for r in results if r["algorithm"] == "minimax"]
    alphabeta = [r for r in results if r["algorithm"] == "alphabeta"]
    mcts = [r for r in results if r["algorithm"] == "mcts"]

    depths = [r["options"]["depth"] for r in minimax]
    minimax_nodes = [r["nodes"] for r in minimax]
    alphabeta_nodes = [r["nodes"] for r in alphabeta]

    plt.figure()
    plt.plot(depths, minimax_nodes , label="Minimax")
    plt.plot(depths, alphabeta_nodes, label="Alpha-Beta")
    plt.xlabel("Search depth")
    plt.ylabel("Nodes explored")
    plt.title("Minimax and Alpha-Beta")
    plt.legend()

    simulations = [r["options"]["num_simulations"] for r in mcts]
    times = [r["time"] for r in mcts]

    plt.figure()
    plt.plot(simulations, times, label="MCTS")
    plt.xlabel("Number of simulations")
    plt.ylabel("Time (seconds)")
    plt.title("MCTS execution time")
    plt.legend()

    plt.show()

results = run_experiments()
print_results(results)
draw_plots(results)
