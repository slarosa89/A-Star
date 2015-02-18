import time,sys
import Tkinter as tk
from random import randint

class Cell():
    def __init__(self,x,y):
        self.H = None
        self.G = 0
        self.F = None
        self.parent = None
        self.color = "white"
        self.x = x
        self.y = y
        self.walked_on = False
        self.start = False
        self.end = False
        self.wall = False


    def update(self):
        if self.walked_on:
            self.color = "yellow"
        if self.start:
            self.color = "green"
        if self.end:
            self.color = "red"
        if self.wall:
            self.color = "black"
        
    def neighbors(self):
        for n in neighbor_cords():
            nx,ny = n
            yield matrix[ny+self.y][nx+self.x]

    def cord(self):
        return (self.y,self.x)

class Matrix():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.start_set = False
        self.end_set = False
        self.solved = False
        self.matrix = [[Cell(col,row) for col in xrange(self.cols)] for row in xrange(rows)]
        
    def maze(self):
        for row in self.matrix:
            for cell in row:
                if cell.y == 0 and cell.x in xrange(0,des_cols):
                    cell.wall = True
                elif cell.x == 0 and cell.y in xrange(0,des_rows):
                    cell.wall = True
                elif cell.y == des_rows-1 and cell.x in xrange(1,des_cols):
                    cell.wall = True
                elif cell.x == des_cols-1 and cell.y in xrange(1,des_rows):
                    cell.wall = True
                elif not any([cell.start,cell.end,cell.wall]) and randint(1,11)>8:
                    cell.wall = True
                cell.update()

    def draw(self):
        for row in matrix:
            for cell in row:
                c.create_rectangle(cell.x*cell_w,cell.y*cell_h,(cell.x+1)*cell_w,(cell.y+1)*cell_h,fill=cell.color)

    def __getitem__(self, key):
        return self.matrix[key]

def onClick(event):
    x, y = event.x, event.y
    px = x/cell_w
    py = y/cell_h
    if not matrix.start_set:
        if not matrix[py][px].wall:
            matrix[py][px].start = True
            matrix.start_set = True
            matrix.start = matrix[py][px]
            matrix.start.update()
            c.create_rectangle(matrix.start.x*cell_w,matrix.start.y*cell_h,(matrix.start.x+1)*cell_w,(matrix.start.y+1)*cell_h,fill=matrix.start.color)
    elif not matrix.end_set:
        if not matrix[py][px].wall and not matrix[py][px].start:
            matrix[py][px].end = True
            matrix.end_set = True
            matrix.end = matrix[py][px]
            matrix.end.update()
            c.create_rectangle(matrix.end.x*cell_w,matrix.end.y*cell_h,(matrix.end.x+1)*cell_w,(matrix.end.y+1)*cell_h,fill=matrix.end.color)

def check_cell(next_cell):
    y,x = next_cell.cord()
    if y < 0 or x < 0:
        return False
    if y > len(matrix.matrix)-1 or x > len(max(matrix,key=len))-1:
        return False
    if matrix[y][x].wall:
        return False
    return True

def neighbor_cords():
    for y in xrange(-1,2):
        for x in xrange(-1,2):
            if not (y,x) == (0,0):
                yield (y,x)

def get_G(cur_cell,next_cell):
    cy,cx = cur_cell.cord()
    ny,nx = next_cell.cord()
    for dy,dx in neighbor_cords():
        if cy+dy == ny and cx+dx == nx:
            if abs(dy+dx) == 1:
                return 10
            else:
                return 14

def get_H(cur_cell,target_cell):
    cy,cx = cur_cell.cord()
    ty,tx = target_cell.cord()
    x_diff = abs(tx-cx)
    y_diff = abs(ty-cy)
    return (x_diff+y_diff)*10

def blocked_corner(cur_cell,neighbor):
    y,x = cur_cell.cord()
    if get_G(cur_cell,neighbor) == 14:
        if  (y-1,x-1) == neighbor.cord():
            if matrix[y-1][x].wall and matrix[y][x-1].wall:
                return True
        if  (y+1,x-1) == neighbor.cord():
            if matrix[y+1][x].wall and matrix[y][x-1].wall:
                return True
        if  (y-1,x+1) == neighbor.cord():
            if matrix[y-1][x].wall and matrix[y][x+1].wall:
                return True
        if  (y+1,x+1) == neighbor.cord():
            if matrix[y+1][x].wall and matrix[y][x+1].wall:
                return True
    return False

def aStar():
    if matrix.start_set and matrix.end_set:
        open_list = {matrix.start:matrix.start.G}
        closed_list = []
        while True:
            if len(open_list) == 0 :
                print "NO PATH"
                sys.exit()
                return False

            cur_cell = min(open_list,key=open_list.get)
            del open_list[cur_cell]
            closed_list.append(cur_cell)

            if matrix.end in closed_list:
                matrix.solved = True
                break
            for neighbor in cur_cell.neighbors():
                if check_cell(neighbor) and neighbor not in closed_list:
                    y,x = neighbor.cord()
                    if neighbor in open_list:
                        if get_G(cur_cell,neighbor)+cur_cell.parent.G < neighbor.G:
                            neighbor.parent = cur_cell
                            neighbor.G = get_G(cur_cell,neighbor) + cur_cell.parent.G
                            neighbor.H = get_H(neighbor,matrix.end)
                            neighbor.F = neighbor.G + neighbor.H
                        else:
                            pass
                    else:
                        neighbor.parent = cur_cell
                        neighbor.G = get_G(cur_cell,neighbor) + neighbor.parent.G
                        neighbor.H = get_H(neighbor,matrix.end)
                        neighbor.F = neighbor.G + neighbor.H
                    if blocked_corner(cur_cell,neighbor):
                        if neighbor == matrix.end:
                            pass
                        else:
                            closed_list.append(neighbor)
                    else:
                        open_list[neighbor] = neighbor.F
                
    if not matrix.solved:
        root.after(1000,aStar)
    else:
        slowdown(draw_path())

def draw_path():
    backwards_path = []
    cur_cell = matrix.end
    while cur_cell != matrix.start:
        cur_cell = cur_cell.parent
        backwards_path.append(cur_cell)

    for cell in reversed(backwards_path):
        cell.walked_on = True
        cell.update()
        c.create_rectangle(cell.x*cell_w,cell.y*cell_h,(cell.x+1)*cell_w,(cell.y+1)*cell_h,fill=cell.color)
        yield 100

def slowdown(iterator):
    try:
        root.after(iterator.next(),slowdown,iterator)
    except StopIteration:
        pass

if __name__ == "__main__":
    win_width = 500
    win_height = 250
    des_cols = 50
    des_rows = 25
    

    cell_w = win_width/des_cols
    cell_h = win_height/des_rows

    matrix = Matrix(des_rows,des_cols)
    matrix.maze()

    root = tk.Tk()
    root.resizable(0,0)
    
    c = tk.Canvas(root,width=win_width,height=win_height,background="gray")
    c.pack()
    c.bind("<Button-1>", onClick)

    matrix.draw()
    
    root.after(1000,aStar)
    root.mainloop()

