import board
import displayio
import terminalio

from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from circuitpython_grid_template_areas import Layout

# Setup Display
display = board.DISPLAY
root = displayio.Group()
display.root_group = root

# Set display background to white
bg = displayio.Group()
root.append(bg)
bg_bitmap = displayio.Bitmap(display.width, display.height, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0xFFFFFF
bg_tilegrid = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
bg.append(bg_tilegrid)

# Create Group to hold layout
main_group = displayio.Group()
root.append(main_group)

# UI Template Design:
#       +-------------------------------------------+
#       |                   title                   |
#       |-------------------------------------------|
#       |           |             header            |
#       |  sidebar  |-------------------------------|
#       |           |   day   |    day    |   day   |
#       +-------------------------------------------+

# Area names ending in "*" create individual iterable cells
# Repeated names without "*" merge into one rectangular area

TEMPLATE = [
    ["title", "title", "title", "title"],
    ["sidebar", "header", "header", "header"],
    ["sidebar", "day*", "day*", "day*"],
]

# Generate layout 
layout = Layout(template=TEMPLATE, size=(display.width, display.height))

# Create variables for each area
title_area = layout["title"]
header_area = layout["header"]
sidebar_area = layout["sidebar"]
day_areas = layout["day"]

# Add content to title area
title_area.add(Rect(x=0, y=0, width=title_area.width, height=title_area.height - 2, fill=0x000000))
title_area.center(label.Label(font=terminalio.FONT, text="Grid Template Areas", color=0xFFFFFF))

# Add content to header area
header_area.add(Rect(x=2, y=0, width=header_area.width, height=header_area.height, fill=0x808080))
header_area.center(label.Label(font=terminalio.FONT, text="Hello, world!", color=0x000000)) 

# Add content to sidebar area
sidebar_area.add(Rect(x=0, y=0, width=sidebar_area.width, height=sidebar_area.height, outline=0x000000))
sidebar_area.center(label.Label(font=terminalio.FONT, text=f"{sidebar_area.name}\nw:{sidebar_area.width}\nh:{sidebar_area.height}", color=0x000000))

# Add content to repeated day areas
day_names = ["Mon", "Tue", "Wed"]
for area, text in zip(day_areas, day_names):
    day_label = label.Label(font=terminalio.FONT, text=text, color=0x000000)
    area.center(day_label)

# Append layout to main group
main_group.append(layout.make_grid_layout())

display.refresh() # For e-ink displays, do not refresh display inside loop

while True:
    # display.refresh() # For non e-ink displays
    pass