import board
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
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
#       | panel (temp)        | (wind)              |
#       |---------------------+---------------------|
#       | (rain)              | (humid)             |
#       |-------------------------------------------|
#       |    stats*   |     stats*    |   stats*    |
#       +-------------------------------------------+

# Area names ending in "*" create individual iterable cells
# Repeated names without "*" merge into one rectangular area
# Area names above in (brackets) represent a sub-grid layout

# Base Grid Template Layout
TEMPLATE = [
    ["title", "title", "title"],
    ["panel", "panel", "panel"],
    ["panel", "panel", "panel"],
    ["panel", "panel", "panel"],
    ["stats*", "stats*", "stats*"],
]

# Generate layout 
layout = Layout(template=TEMPLATE, size=(display.width, display.height))

title_area = layout["title"]
panel_area = layout["panel"]
stats_area = layout["stats"]

# Append layout to main group with debug overlay
main_group.append(layout.make_grid_layout())

title_area.center(label.Label(terminalio.FONT, text="Subgrid Example Layout", color=0x000000))
stats_area[0].place(label.Label(terminalio.FONT, text="10:12am", color=0x000000, line_spacing=0.9), anchor=(0, 1), offset=(2, 0))
stats_area[1].place(label.Label(terminalio.FONT, text="Playing next:", color=0x000000), anchor=(0.5, 0), offset=(0, 2))
stats_area[1].place(label.Label(terminalio.FONT, text="Yellow Submarine", color=0x000000), anchor=(0.5, 1))
stats_area[2].place(label.Label(terminalio.FONT, text="Battery: 86%", color=0x000000), anchor=(1, 1), offset=(-2, 0))


# Subgrid Template Layout
SUBGRID_TEMPLATE = [
    ["sub_temp", "sub_wind"],
    ["sub_rain", "sub_humid"]
]

# Apply an internal grid to a parent Area
sublayout = panel_area.make_subgrid(SUBGRID_TEMPLATE, debug_labels=0x808080, debug_outline=0x808080)

# Add text and graphics to sublayout areas
sublayout["sub_temp"].center(label.Label(terminalio.FONT, text="27C", color=0x000000, scale=2))
sublayout["sub_wind"].center(label.Label(terminalio.FONT, text="14mph", color=0x000000, scale=2))
sublayout["sub_rain"].place(Rect(0, 0, int(sublayout["sub_rain"].width), 8, outline=0x808080), anchor=(1, 1))
sublayout["sub_rain"].place(Rect(0, 0, int(sublayout["sub_rain"].width * 0.16), 8, fill=0x808080), anchor=(0, 1))
sublayout["sub_rain"].center(label.Label(terminalio.FONT, text="16% Chance", color=0x000000, scale=2))
sublayout["sub_humid"].place(Rect(0, 0, int(sublayout["sub_humid"].width), 8, outline=0x808080), anchor=(1, 1))
sublayout["sub_humid"].place(Rect(0, 0, int(sublayout["sub_humid"].width * 0.62), 8, fill=0x808080), anchor=(0, 1))
sublayout["sub_humid"].center(label.Label(terminalio.FONT, text="62%", color=0x000000, scale=2))

display.refresh() # For e-ink displays we do not refresh display inside loop

while True:
    # display.refresh() # For non e-ink displays
    pass