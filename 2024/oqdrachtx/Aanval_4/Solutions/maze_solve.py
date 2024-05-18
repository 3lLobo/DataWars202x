"""
This solution walks every possible path by visiting a node once. It will shortcut if the current steps taken are longer than an already known possible solution.

It reads in a maze from text file where a target, startpoint and wall character can be defined for parsing the maze; It should not matter if the maze is not a perfect rectangle.

For getting a path set past some nodes see the solution of creating multiple target and endpoints; like it was the case for this challenge.
"""


class Node:
    def __init__(self, t: int, x: int, y: int) -> None:
        self.t: int = t
        self.x: int = x
        self.y: int = y

    @staticmethod
    def get_node_types():
        class node_types:
            START = 0
            TARGET = 1
            WALL = 2
            PATH = 3

        return node_types


class Path:
    def __init__(self, *nodes) -> None:
        self.nodes: list[Node] = []
        self.seen: dict[int, bool] = {}

        # the start node is included in the path, the first step should not count; start at -1.
        self.steps: int = -1

        for node in nodes:
            self.add_node(node)

    def add_node(self, node: Node) -> None:
        """
        Adds the given node to this path.

        Args:
            node (Node): the node to add.
        """
        self.nodes.append(node)
        self.seen[id(node)] = True
        self.steps += 1

    def has_node(self, node: Node) -> bool:
        """
        Checks to see if the node is already present in this path.

        Args:
            node (Node): the node to search for.

        Returns:
            bool: True if the node exists; False if it doesn't
        """
        if self.seen.get(id(node), None) is None:
            return False
        return True

    def copy(self) -> "Path":
        """
        Create a copy of this path.

        Returns:
            Path: a new path with the same steps taken as this path.
        """
        return Path(*self.nodes)


class Maze:
    def __init__(
        self, maze_as_text: list[str], start: str, end: str, wall: str
    ) -> None:
        node_types = Node.get_node_types()

        self.node_map: dict[str, int] = {
            wall: node_types.WALL,
            start: node_types.START,
            end: node_types.TARGET,
        }

        self.maze: list[list[Node]] = self.parse(maze_as_text=maze_as_text)
        self.start_node: Node = self.get_from_maze(Node.get_node_types().START)
        self.target_node: Node = self.get_from_maze(Node.get_node_types().TARGET)
        self.shortest_solution = None

    def get_from_maze(self, node_type: int) -> Node:
        """
        get a node with given type from the maze list.

        if a lookup is done for a node_type that exists multiple times the first occurence is returned (L->R, T->D);

        Args:
            node_type (int): what node type to look for.

        Raises:
            LookupError: this error is thrown if the node does not exist in the maze.

        Returns:
            Node: the node with the requested node type.
        """
        for row in self.maze:
            for node in row:
                if node.t == node_type:
                    return node

        raise LookupError(f"Can't find node of {node_type}...")

    def parse(self, maze_as_text: list[str]) -> list[list[Node]]:
        """
        parse the maze from text to an array of nodes.

        Args:
            maze_as_text (list[str]): the result from file.readlines()

        Returns:
            list[list[Node]]: 2d array of nodes.
        """
        maze: list[list[Node]] = []

        for y, row in enumerate(maze_as_text):
            maze_row: list[Node] = []
            row.strip("\n")
            for x, char in enumerate(row):
                maze_row.append(
                    Node(self.node_map.get(char, Node.get_node_types().PATH), x, y)
                )
            maze.append(maze_row)

        return maze

    def solve(self, path: Path = None, from_node: Node = None) -> Path | None:
        """
        tries to solve the maze using the given path and start node.

        to solve the maze all neighboring nodes of the current node are checked for valid next_nodes that we can walk to.
        if multiple possible paths exist this function is called again to check out the next path;

        Args:
            path (Path, optional): the current path for this solution. Defaults to None.
            from_node (Node, optional): the current node we are at for this solution. Defaults to None.

        Returns:
            Path | None: returns an Path object with the least amount of steps; or None if no path is available.
        """

        if path is None:
            path = Path()

        if from_node is None:
            from_node = self.start_node

        current_node: Node = from_node
        while current_node != self.target_node:
            if (
                self.shortest_solution is not None
                and self.shortest_solution.steps < path.steps
            ):
                # this path takes more stepts than the current shortest solution; break
                break

            x: int = current_node.x
            y: int = current_node.y

            path.add_node(node=current_node)
            path_has_next: bool = False
            for nx, ny in [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]:
                try:
                    node: Node = self.maze[ny][nx]
                except IndexError:
                    continue

                if node == self.target_node:
                    path.add_node(node=node)

                    if (
                        self.shortest_solution is None
                        or path.steps < self.shortest_solution.steps
                    ):
                        self.shortest_solution = path

                    return self.shortest_solution

                if node.t == Node.get_node_types().WALL:
                    # a wall is no valid node.
                    continue

                if path.has_node(node=node):
                    # we've already been here.
                    continue

                if path_has_next:
                    # this is a valid node; but we already have a valid node to visit; branch out to solve that path first.
                    self.solve(path=path.copy(), from_node=node)
                    continue

                # first node found that is a valid next_node
                next_node: Node = node
                path_has_next = True

            # if no next node is found, this is a dead end;
            if not path_has_next:
                return self.shortest_solution

            current_node = next_node

        return self.shortest_solution

    def draw(self, path: Path) -> None:
        """
        this function draws the maze in ascii art;

        a wall will be represented by an #; target will be a ?; starting point will be a @, the path will be represented by +.

        Args:
            path (Path): the path to draw in the maze.
        """
        drawing: list[list[str]] = []

        node_types = Node.get_node_types()

        draw_map: dict[int, str] = {
            node_types.WALL: "#",
            node_types.TARGET: "?",
            node_types.START: "@",
        }

        for row in self.maze:
            drawing_row: list[str] = []
            for node in row:
                drawing_row.append(draw_map.get(node.t, " "))
            drawing.append(drawing_row)

        for node in path.nodes:
            if node == self.start_node or node == self.target_node:
                continue

            drawing[node.y][node.x] = "+"

        for row in drawing:
            print("".join(row))


base = "2024/oqdrachtx/Aanval_4/Destroy Deathstar (pt. 1)/"

with open(base + "input.txt") as f:
    maze_as_text: list[str] = f.readlines()

total_steps = 0

for start, target in zip("@abcdefghijkl", "abcdefghijkl$"):
    maze = Maze(maze_as_text=maze_as_text, start=start, end=target, wall="#")
    solution: Path = maze.solve()

    total_steps += solution.steps

    print(f"Solution from {start} to {target}, took {solution.steps} steps.")
    maze.draw(path=solution)
    print()


print("----------------------------------------------------")
print(f"Total steps taken: {total_steps}")
