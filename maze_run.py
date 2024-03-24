from maze_main import Maze
import random
import time


def maze_run():

    nx, ny = 20, 15
    # Maze entry position
    ix, iy = 0,0
    cx, cy = 10,11

    maze = Maze(nx, ny, cx,cy,ix, iy)
    maze.add_begin_end = True
    maze.add_treasure = False
    maze.make_maze()

    # a = maze.cell_at(1,2)
    # b = maze.cell_at(0,0).walls['W']

    # self.cell_at(x, y).walls['S']

    maze.write_svg('C:/Users/user/Documents/Chain/Solana Hackathon 2024/solamaze_web/public/images/img0.svg')

    directions = ["E", "W", "S", "N"]

    x=0
    buffer = 5
    while x < buffer:
        time.sleep(0.5)
        # if x == buffer-1:
        #     x=0
        x += 1
        random_direction = random.choice(directions)
        print(x)
        print(random_direction)
        maze.update_maze(random_direction)
        maze.write_svg('C:/Users/user/Documents/Chain/Solana Hackathon 2024/solamaze_web/public/images/img%s.svg'% str(x))


# maze.write_svg('maze3_solution.svg', solution=True)



