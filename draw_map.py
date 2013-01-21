#!/usr/bin/python

import math, sys
from PIL import Image, ImageDraw

HEX_RADIUS = 50
TARGET_FILE = '/home/stas/settlers.jpg'

def make_hex(center):
  return [(center[0] + HEX_RADIUS * math.cos(math.radians(angle)),
           center[1] + HEX_RADIUS * math.sin(math.radians(angle)))
          for angle in [0, 60, 120, 180, 240, 300]]

def make_layer(center, layer):
  layer_list = list()
  if layer == 0:
    layer_list.append(center)
    return layer_list

  angle_list = [30, 90, 150, 210, 270, 330]
  hex_x, hex_y = center[0], center[1] - 2 * layer * HEX_RADIUS
  for angle in angle_list:
    for i in range(layer):
      hex_x += 2 * HEX_RADIUS * math.cos(math.radians(angle))
      hex_y += 2 * HEX_RADIUS * math.sin(math.radians(angle))
      layer_list.append((hex_x, hex_y))
  return layer_list

def draw_text(draw, center, string):
  width, height = draw.textsize(string)
  draw.text((center[0] - width / 2, center[1] - height / 2),
            string,
            fill='black')

def draw_map(tiles=None):
  if tiles is None:
    tiles = range(19)

  center, layer = (0, 0), 0
  max_tile, tile_count = max(tiles), 0
  hex_centers = {}

  while tile_count < max_tile:
    layer_tiles = make_layer(center, layer)
    for (i, tile) in enumerate(layer_tiles):
      hex_centers[tile_count] = tile
      tile_count += 1
    layer += 1

  neighbors = {}
  for tile in tiles:
    def dist(x):
      return round(math.sqrt(math.pow(x[0] - hex_centers[tile][0], 2) +
                                 math.pow(x[1] - hex_centers[tile][1], 2)) /
                       (2 * HEX_RADIUS))
    neighbors[tile] = [ x for x in tiles
                        if x != tile and dist(hex_centers[x]) == 1 ]
    print 'Tile', (tile + 1), 'neighbors', [ x + 1 for x in neighbors[tile] ]

  all_vertices = list()
  for tile in hex_centers.values():
    all_vertices.extend(make_hex(tile))
  map_width = int(max([x[1] for x in all_vertices]) -
                  min([x[1] for x in all_vertices])) + 100
  map_height = int(max([x[0] for x in all_vertices]) -
                   min([x[0] for x in all_vertices])) + 100
  
  map_image = Image.new('RGB', (map_width, map_height), 'white')
  map_draw = ImageDraw.Draw(map_image)

  for tile in tiles:
    adjusted_center = (hex_centers[tile][0] + map_width / 2,
                       hex_centers[tile][1] + map_height / 2)
    map_draw.polygon(make_hex(adjusted_center), outline='black')
    draw_text(map_draw, adjusted_center, str(tile + 1))

  del map_draw
  map_image.save(TARGET_FILE, 'png')

if __name__ == "__main__":
  draw_map()
