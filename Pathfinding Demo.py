# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 09:52:07 2021

@author: Cillomir (Joel Leckie)
"""

# Import the pygame module & the key commands from pygame.locals
import pygame
from pygame.locals import (KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE)

# Initialize the pygame module
pygame.init()

# *****~~~~****~~~***~~**~ SYSTEM VARIABLES ~**~~***~~~****~~~~*****
# Define the colors to be used
black, white, gray = (0, 0, 0), (255, 255, 255), (150, 150, 150)
green = (0, 255, 0)
# Set the display mode to fit the full available screen size
screen = pygame.display.set_mode()


# Define a function to print text to the screen in size 48 font
def pg_print(text, color, pos_x, pos_y):
    font_type = pygame.font.SysFont(None, 48)
    font_text = font_type.render(text, True, color)
    screen.blit(font_text, (pos_x, pos_y))


# *****~~~~****~~~***~~**~ PATHFINDING VARIABLES ~**~~***~~~****~~~~*****
# Define some walls that will provide obstacles on the grid, using grid notation (Nodes)
All_Walls = [[1, 1], [1, 2], [1, 3], [4, 5], [5, 5], [6, 5]]
# Declare a list of neighbouring nodes using grid notation: left, right, up, and down
neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # left, right, up, down


# Define what it means to add the neighbouring cells to the current node and return the result
def add_neighbour(cur, neigh):
    return [cur[0] + neigh[0], cur[1] + neigh[1]]


# Declare variables to allow the user to move the selector based on keyboard commands
move_x = move_y = 0
# Declare the size, in pixels, for each node on the map
Node = 96
# Declare the spacing, in pixels, between each grid node on the map
Spacing = 2
# Declare a list holding the starting point, in pixels, for the map grid
# Grid_Start[0] & Grid_Start[1] are one node offset from the screens edge
Grid_Start = [96, 96]
# Declare a variable for how many nodes away from the selector to highlight
Speed = 3
# Declare the starting position for the selector square in grid notation
cur_pos = [0, 0]
# Declare the width and height of the grid to be displayed
Grid_Width = 8
Grid_Height = 8

# *****~~~~****~~~***~~**~ MAP GRID ~**~~***~~~****~~~~*****
# Start an empty list to hold the grid nodes
Grid_Nodes = []
# Start a loop to generate a node for each unit wide and each unit high
for width in range(0, Grid_Width):
    for height in range(0, Grid_Height):
        # Add the generated node into the grid list
        Grid_Nodes.append([width, height])


def map_update():
    # Run another loop, now to draw the grid onto the screen
    for x in range(0, Grid_Width):
        for y in range(0, Grid_Height):
            # search the list of walls previously defined
            if [x, y] not in All_Walls:
                # Define a formula to place each generated node based on its generated coordinates
                node_x = (x * (Node + Spacing)) + Grid_Start[0]
                node_y = (y * (Node + Spacing)) + Grid_Start[1]
                # Draw a gray rectangle on the screen for each grid node generated
                pygame.draw.rect(screen, gray, (node_x, node_y, Node, Node))


# *****~~~~****~~~***~~**~ LEGAL MOVES ~**~~***~~~****~~~~*****
# Define a class to check what nodes to highlight as legal moves for the selector
def legal_moves(position):
    # Create an open list of nodes to check and a closed list of nodes already checked
    open_list = [position]
    closed_list = []        
    # Start the loop to check valid neighbouring nodes so long as there are nodes in the open list
    while len(open_list) != 0:
        # Check the first node on the open list and add it to the closed list
        pos_check = open_list.pop(0)
        closed_list.append(pos_check)
        # Loop to generate the four neighbouring nodes of the node that is being checked
        for x in range(0, len(neighbours)):
            # Generate a new node based on the neighbouring nodes (left, right, up, down)
            new_pos = add_neighbour(pos_check, neighbours[x])
            # Measure the distance, in absolutes, from the current node to the new node
            distance = abs(position[0] - new_pos[0]) + abs(position[1] - new_pos[1])
            # Ensure the distance is within the allowable range
            if distance > Speed:
                pass
            # Ensure the new node is still within the grid parameters
            elif 0 <= new_pos[0] < Grid_Width and 0 <= new_pos[1] < Grid_Height:
                # Check that the new node is not classified as a wall
                if new_pos not in All_Walls:
                    # Check that the new node has not already been populated or been previously checked
                    if new_pos not in all_new and new_pos not in closed_list:
                        all_new.append(new_pos)
                        open_list.append(new_pos)
    # Highlight the squares within range and label their coordinates
    for x in range(0, len(all_new)):
        node_x = (all_new[x][0] * (Node + Spacing)) + Grid_Start[0]
        node_y = (all_new[x][1] * (Node + Spacing)) + Grid_Start[1]
        label_x = (all_new[x][0] * (Node + Spacing)) + Grid_Start[0] + 16
        label_y = (all_new[x][1] * (Node + Spacing)) + Grid_Start[1] + 32
        pygame.draw.rect(screen, green, (node_x, node_y, Node, Node))
        pg_print(str(all_new[x]), black, label_x, label_y)


# *****~~~~****~~~***~~**~ SELECTOR ~**~~***~~~****~~~~*****
# Create a sprite group to hold the selector for future collision checks
All_Selector = pygame.sprite.Group()


# Create a sprite (green square) that acts as a main character placeholder
class Selector(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Give the selector a surface the same size as the grid nodes
        self.image = pygame.Surface([Node, Node])
        # Fill the selector surface in black
        self.image.fill(black)
        # Define a rectangle around the surface and place it at the starting grid node
        self.rect = self.image.get_rect(topleft=(Grid_Start[0], Grid_Start[1]))
        # Define the selectors grid notation based on the selectors starting position
        self.move_x = self.move_y = 0
        self.node = [
            (self.rect.topleft[0] - Grid_Start[0]) / (Node + Spacing), 
            (self.rect.topleft[1] - Grid_Start[1]) / (Node + Spacing)]
        # Add the selector sprite to the All_Selector sprite group
        All_Selector.add(self)

    def update(self):
        # Check if the user has moved the selector horizontally
        if self.move_x != 0:
            self.node[0] += self.move_x
            # Check if the new selector node is valid
            if self.node not in All_Walls:
                pass
            # If the new node is a wall, return it to where it was
            else:
                self.node[0] -= self.move_x
        # Check if the user has moved the selector vertically
        if self.move_y != 0:
            self.node[1] += self.move_y
            # Check if the new selector node is valid
            if self.node not in All_Walls:
                pass
            # If the new node is a wall, return it to where it was
            else:
                self.node[1] -= self.move_y
        # Check if the new node is outside the grid parameters
        # If so, move the selector to the opposite side of the grid
        if self.node[0] < 0:
            self.node[0] = Grid_Width - 1
        if self.node[0] > (Grid_Width - 1):
            self.node[0] = 0
        if self.node[1] < 0:
            self.node[1] = Grid_Height - 1
        if self.node[1] > (Grid_Height - 1):
            self.node[1] = 0
        # Return the move commands back to 0
        self.move_x = self.move_y = 0
        # Define a formula to place each selector based on its grid node
        node_x = (self.node[0] * (Node + Spacing)) + Grid_Start[0]
        node_y = (self.node[1] * (Node + Spacing)) + Grid_Start[1]
        # Reposition the selector based on the new node coordinates
        self.rect.topleft = (node_x, node_y)
        # Update the global variable of the selectors current position
        # Ensure to convert the node from a float to an integer
        global cur_pos
        cur_pos = [int(self.node[0]), int(self.node[1])]


# Declare an object to represent the selector class
selector = Selector()

# *****~~~~****~~~***~~**~ RUNNING PROGRAM ~**~~***~~~****~~~~*****
running = True
while running:
    # Fill the screen, the background surface, in white
    screen.fill(white)    
    # *****~~~~****~~~***~~**~ SYSTEM EVENTS ~**~~***~~~****~~~~*****
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # ***---***---***-- KEYBOARD COMMANDS --***---***---***
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                selector.move_x = -1
            elif event.key == K_RIGHT:
                selector.move_x = 1
            elif event.key == K_UP:
                selector.move_y = -1
            elif event.key == K_DOWN:
                selector.move_y = 1
            if event.key == K_ESCAPE:
                running = False
    # *****~~~~****~~~***~~**~ DRAW VISUALS ~**~~***~~~****~~~~*****
    map_update()
    All_Selector.draw(screen)
    All_Selector.update()
    all_new = []
    legal_moves(cur_pos)
    pygame.display.update()
# Close the pygame module when the loop ends and the system closes
pygame.quit()
