import pyglet

list = {
          "class": ('dg_classm32.png', 11, 8),
          "dungeon": ('dg_dungeon32.gif', 10, 9),
          "ground": ('dg_grounds32.gif', 19, 9),
          "monster1": ('dg_monster132.png', 16, 6)
          }

img = {}
grid = {}
sheet = {}

for k in list:
    img[k] = pyglet.resource.image(list[k][0])
    grid[k] = pyglet.image.ImageGrid(img[k], list[k][1], list[k][2])
    sheet[k] = pyglet.image.TextureGrid(grid[k])
