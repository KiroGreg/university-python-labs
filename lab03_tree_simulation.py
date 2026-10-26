"""
Laboratory Work 3: Orchard Tree Simulation
Analyzes orchard layout to determine dead trees and non-fruitful trees based on distance rules.
"""


class LessThan1(Exception):
    pass


def find_possible_non_fruitful(N, dead_trees):
    """Takes field size and dead tree coordinates, returns possible non-fruitful trees within 30m."""
    possible_non_fruitful = []
    for dead_coords in dead_trees:
        for col_item in range(max(0, dead_coords[0] - 3), min(N, dead_coords[0] + 4)):
            for row_item in range(max(0, dead_coords[1] - 3), min(N, dead_coords[1] + 4)):
                if abs(col_item - dead_coords[0]) + abs(row_item - dead_coords[1]) <= 3 and \
                        ([col_item, row_item] not in possible_non_fruitful) and \
                        ([col_item, row_item] not in dead_trees):
                    possible_non_fruitful.append([col_item, row_item])
    return possible_non_fruitful


def find_non_fruitful_trees(N, possible_non_fruitful, dead_trees):
    """Checks if alive trees have neighboring alive trees within 30m."""
    non_fruitful = {}
    for possible_non_fruit in possible_non_fruitful:
        has_alive_nearby = False
        for col_item in range(max(0, possible_non_fruit[0] - 3), min(N, possible_non_fruit[0] + 4)):
            for row_item in range(max(0, possible_non_fruit[1] - 3), min(N, possible_non_fruit[1] + 4)):
                if (abs(col_item - possible_non_fruit[0]) + abs(row_item - possible_non_fruit[1]) <= 3) and \
                        ([col_item, row_item] not in dead_trees) and ([col_item, row_item] != possible_non_fruit):
                    has_alive_nearby = True
                    break
            if has_alive_nearby:
                break
        if not has_alive_nearby:
            if possible_non_fruit[0] not in non_fruitful:
                non_fruitful[possible_non_fruit[0]] = []
            non_fruitful[possible_non_fruit[0]].append(possible_non_fruit[1])
    return non_fruitful


def main():
    """Main execution function for orchard analysis."""
    try:
        N = int(input("Enter orchard field size (positive integer): "))
        if N <= 1:
            raise LessThan1
        dead_trees = []
        while True:
            x_y = input("Enter dead tree coordinates [row col] (leave empty to finish): ")
            if not x_y:
                break
            else:
                row, col = map(int, x_y.split())
            if 0 < row <= N and 0 < col <= N:
                dead_trees.append([row - 1, col - 1])
            else:
                raise IndexError

        possible_non_fruitful = find_possible_non_fruitful(N, dead_trees)
        non_fruit = find_non_fruitful_trees(N, possible_non_fruitful, dead_trees)
        length = sum(len(iter_list) for iter_list in non_fruit.values())

    except ValueError:
        print("Error: Invalid input format.")
    except LessThan1:
        print("Error: Field size must be greater than 0.")
    except IndexError:
        print("Error: Coordinates out of field range.")
    except KeyboardInterrupt:
        print("\nProgram aborted.")
    else:
        print("\nAnalysis completed successfully.")
        print(f"Total dead trees: {len(dead_trees)}")
        print(f"Total alive but non-fruitful trees: {length}")
        print("Locations of non-fruitful trees by row:")
        if non_fruit:
            for row_idx, cols in non_fruit.items():
                print(f"Row {row_idx + 1}: {', '.join(str(c + 1) for c in cols)}")
        else:
            print("No non-fruitful trees found.")


if __name__ == '__main__':
    main()
