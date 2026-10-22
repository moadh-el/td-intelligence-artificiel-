"""Run the Pokémon search exercise."""

import matplotlib

try:
    import tkinter  # noqa: F401
except ModuleNotFoundError:
    # Keep the search exercise runnable on Python installations without Tk.
    matplotlib.use("Agg")
    INTERACTIVE = True
else:
    matplotlib.use("TkAgg")
    INTERACTIVE = True
import matplotlib.pyplot as plt
from pokemon_game import (
    draw_map,
    generate_map,
    path_to_actions,
    visualize_path,
)
from search import generate_random_path, breadth_first_search, depth_first_search

# Using a fixed seed gives every student the same example.
# Replace it with None to generate a different map on each execution.
MAP_SEED = 1
PATH_SEED = 10


def main() -> None:
    """Generate a map and demonstrate the path visualization."""
    game_map, start, goal = generate_map(
        rows=10,
        columns=14,
        tree_probability=0.25,
        seed=MAP_SEED,
    )

    print(f"Initial state: {start}")
    print(f"Goal state:    {goal}")

    # First display the randomly generated initial map.
    # Close this window to continue to the animation.
    draw_map(
        game_map,
        start,
        goal,
        show=INTERACTIVE,
    )

    # Generate a random valid example path.
    random_path = generate_random_path(
        game_map,
        start,
        goal,
        seed=PATH_SEED,
    )

    print("\nRandom example path:")
    print(random_path)

    print("\nCorresponding actions:")
    print(path_to_actions(random_path))

    print(f"\nPath cost: {len(random_path) - 1}")

    # Execute BFS and DFS so their results are displayed as well.
    bfs_path = breadth_first_search(game_map, start, goal)
    dfs_path = depth_first_search(game_map, start, goal)

    print("\nBFS result:")
    print(bfs_path)
    print("BFS actions:")
    print(path_to_actions(bfs_path))
    print(f"BFS path cost: {len(bfs_path) - 1}")

    print("\nDFS result:")
    print(dfs_path)
    print("DFS actions:")
    print(path_to_actions(dfs_path))
    print(f"DFS path cost: {len(dfs_path) - 1}")

    # Save all search results in a simple text file next to this program.
    with open("search_results.txt", "w", encoding="utf-8") as results_file:
        results_file.write(f"Initial state: {start}\n")
        results_file.write(f"Goal state: {goal}\n\n")

        results_file.write("RANDOM PATH\n")
        results_file.write(f"Path: {random_path}\n")
        results_file.write(f"Actions: {path_to_actions(random_path)}\n")
        results_file.write(f"Path cost: {len(random_path) - 1}\n\n")

        results_file.write("BREADTH-FIRST SEARCH (BFS)\n")
        results_file.write(f"Path: {bfs_path}\n")
        results_file.write(f"Actions: {path_to_actions(bfs_path)}\n")
        results_file.write(f"Path cost: {len(bfs_path) - 1}\n\n")

        results_file.write("DEPTH-FIRST SEARCH (DFS)\n")
        results_file.write(f"Path: {dfs_path}\n")
        results_file.write(f"Actions: {path_to_actions(dfs_path)}\n")
        results_file.write(f"Path cost: {len(dfs_path) - 1}\n")

    # Animate the trainer walking along the generated path.
    if INTERACTIVE:
        animation = visualize_path(
            game_map,
            start,
            goal,
            random_path,
            interval=300,
            repeat=False,
        )
        animation.save("random_path.gif", writer="pillow")
        # Keep a reference to the animation until the window is closed.
        _ = animation
        plt.show()
if __name__ == "__main__":
    main()
