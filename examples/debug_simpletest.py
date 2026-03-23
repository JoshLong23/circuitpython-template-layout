import board
import displayio

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
#       | title               +                     |
#       |-------------------------------------------|
#       | sidebar   | header        +               |
#       |     +     |-------------------------------|
#       |           | day +   | day +    | day +    |
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

# Append layout to main group with debug overlay
main_group.append(layout.make_grid_layout(debug=True))

# debug=True expands to:
#   debug_fill=False        # if True grayscale fill applied to each area
#   debug_labels=True       # defaults to black if True
#   debug_outline=True      # defaults to black if True
#   debug_centers=0x808080  # defaults to black if True
#   debug_grid=0x808080     # defaults to black if True

display.refresh() # For e-ink displays we do not refresh display inside loop

while True:
    # display.refresh() # For non e-ink displays
    pass