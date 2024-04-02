# This is the main function to construct the maze

import random

class Cell:

    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    delta = {'W': (-1, 0), 'E': (1, 0), 'S': (0, 1), 'N': (0, -1)}

    def __init__(self, x, y):

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def __repr__(self):

        return f'({self.x}, {self.y})'

    def has_all_walls(self):

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):


        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:


    def __init__(self, nx, ny,  cx, cy, ix=0, iy=0):


        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.cx, self.cy = cx, cy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

        self.add_begin_end = False
        self.add_treasure = False
        self.treasure_x = random.randint(0, self.nx - 1)
        self.treasure_y = random.randint(0, self.ny - 1)


        self.excluded_walls = [((nx - 1, ny), (nx, ny)),
                               ((0, 0), (0, 1))]


        self.solution = None

    def cell_at(self, x, y):
        return self.maze_map[x][y]

    def __str__(self):

        maze_rows = ['-' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def update_maze(self,movement):

        success_move = 0
        goal = 0
        if movement == 'N' and not self.cell_at(self.cx, self.cy).walls['N']:
             self.cy -= 1
             success_move = 1
        if movement == 'S' and not self.cell_at(self.cx, self.cy).walls['S']:
             self.cy += 1
             success_move = 1
        if movement == 'E' and not self.cell_at(self.cx, self.cy).walls['E']:
             self.cx += 1
             success_move = 1
        if movement == 'W' and not self.cell_at(self.cx, self.cy).walls['W']:
             self.cx -= 1
             success_move = 1
        if self.cy == self.ny-1 and self.cx == self.nx-1:
            goal = 1

        return success_move, goal

    def write_svg(self, filename):

        aspect_ratio = self.nx / self.ny
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx

        def write_wall(f, x1, y1, x2, y2):

            if ((x1, y1), (x2, y2)) in self.excluded_walls:
                # print(f'Excluding wall at {((x1, y1), (x2, y2))}')
                return
            sx1, sy1, sx2, sy2 = x1 * scx, y1 * scy, x2 * scx, y2 * scy
            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                  .format(sx1, sy1, sx2, sy2), file=f)

        def add_cell_rect(f, x, y, colour):
            pad = 5
            print(f'<rect x="{scx * x + pad}" y="{scy * y + pad}" width="{scx - 2 * pad}"'
                  f' height="{scy - 2 * pad}" style="fill:{colour}" />', file=f)

        def add_cell_rect_small(f, x, y, colour):
                pad = 10
                print(f'<rect x="{scx * x + pad}" y="{scy * y + pad}" width="{scx - 2 * pad}"'
                      f' height="{scy - 2 * pad}" style="fill:{colour}" />', file=f)


        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                  .format(width + 2 * padding, height + 2 * padding,
                          -padding, -padding, width + 2 * padding, height + 2 * padding),
                  file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #aca788;\n    stroke-linecap: round;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)

            for x in range(self.nx):
                for y in range(self.ny):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x, y + 1, x + 1, y + 1
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = x + 1, y, x + 1, y + 1
                        write_wall(f, x1, y1, x2, y2)


            for x in range(self.nx):
                write_wall(f, x, 0, x + 1, 0)
            for y in range(self.ny):
                write_wall(f, 0, y, 0, y + 1)



            if self.add_begin_end:
                add_cell_rect(f, 0, 0, 'green')
                add_cell_rect(f, self.nx - 1, self.ny - 1, 'red')
                add_cell_rect_small(f, self.cx, self.cy, 'yellow')

            print('</svg>', file=f)



    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        neighbours = []
        for direction, (dx, dy) in Cell.delta.items():
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours


    def make_maze(self):

        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)

        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:

                current_cell = cell_stack.pop()
                continue


            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell

            if (current_cell.x == self.nx - 1) and \
                    (current_cell.y == self.ny - 1):
                self.solution = cell_stack.copy()
                self.solution.append(next_cell)
            nv += 1