# circuitpython_grid_template_areas

A CircuitPython layout helper inspired by CSS Grid Template Areas.

## What this does

Positioning UI elements in displayio can get messy when working with pixel coordinates.

This library lets you define layouts using named grid areas, similar to CSS grid-template-areas, and then place content into those areas easily.

## Features

- Define layouts using a simple 2D template
- Named areas for easy access
- Merge cells into rectangular areas
- Repeated iterable areas using `*`
- Easy content placement helpers
- Built-in debug overlays
- Subgrid support

## Installation

Copy the library folder to your device:
`lib/circuitpython_grid_template_areas/`

Then import it:

```python
from circuitpython_grid_template_areas import Layout
```

## Running on Hardware

This library does not handle display setup, but it does use displayio to create and handle Groups.

See `examples/simpletest.py` for a complete working example on a displayio-compatible device.

## Quick Start

```python
import terminalio
from adafruit_display_text import label
from circuitpython_grid_template_areas import Layout

TEMPLATE = [
    ["title", "title", "title", "title"],
    ["sidebar", "header", "header", "header"],
    ["sidebar", "day*", "day*", "day*"],
]

layout = Layout(template=TEMPLATE, size=(296, 128))

title = layout["title"]
days = layout["day"]

# Add content
title.center(label.Label(font=terminalio.FONT, text="Quick Start"))

for area in days:
    area.center(label.Label(font=terminalio.FONT, text="Day"))
```

For a complete working hardware example including display setup, see `examples/simpletest.py`.

## Template Syntax

### Named Areas

Cells with the same name are merged in a single rectangular area:

```
["title", "title", "title"]
```

---

### Repeated Areas (`*`)

Names ending in `*` create separate, iterable areas:

```
["day*", "day*", "day*"]
```

Access them like:

```python
for area in layout["day"]:
    area.append(...)
```

To loop through a list of values as well as the list of Areas you can use `zip()` to combine iterables:

```python
day_areas = layout["day"]
day_names = ["Mon", "Tue", "Wed"]

for area, text in zip(day_areas, day_names):
    day_label = label.Label(font=terminalio.FONT, text=text, color=0x000000)
    area.center(day_label)
```

---

### Empty Cells

Use `.` or `None` to create empty cells:

```python
["title", ".", "sidebar"]
```

or

```python
["title", None, "sidebar"]
```

---

### Working with Areas

Each area is an object with a display group and helper methods.

#### Add content

```python
area.add(item)
```

---

### Place content

```python
area.place(item, anchor=(0.5, 0.5), offset=(0, 0))
```

- `anchor` controls alignment (0 = left/top, 1 = right/bottom)
- `offset` shifts in pixels from that anchor point

---

### Center content

```python
area.center(item)
```

---

### Debug Options

Quick debug mode:

```python
layout.make_grid_layout(debug=True)
```

This activates the following options:

- Outlines
- Area name labels
- Area center markers
- Grid lines

Custom debug options:

```python
layout.make_grid_layout(
    debug_fill = True,
    debug_grid = 0x808080,
    debug_labels = True,
    debug_outline = False,
    debug_centers = 0x808080
)
```

---

## Subgrids

You can create a nested layout inside an area.

```python
sublayout = area.make_subgrid([
    ["temp", "wind"],
    ["rain", "humid"]
])
```

Use it like a normal layout:

```python
sublayout["temp"].center(...)
sublayout["wind"].center(...)
```

## Area Properties and Methods

- `area.name` Area name
- `area.col` Column that the Area starts in
- `area.row` Row that the Area starts in
- `area.col_span` Number of columns the Area spans
- `area.row_span` Number of rows the Area spans
- `area.width` Width of the Area
- `area.height` Height of the Area
- `area.top` Pixel position at top of Area
- `area.right` Pixel position at right of Area
- `area.bottom` Pixel position at bottom of Area
- `area.left` Pixel position at left of Area
- `area.center_x` Pixels from Area left edge to center of the Area
- `area.center_y` Pixels from Area top edge to center of the Area
- `area.group` Area displayio Group

Elements such as text, shapes or images can be added or removed from each Area's displayio Group using the following:

- `area.append(item)` Append a single item to an Area
- `area.add(*items)` Append multiple items to an Area
- `area.remove(item)` Remove an item from an Area
- `area.clear()` Clear all items from an Area
- `area.place(item, anchor=(0.5, 0.5), offset=(0, 0))` Position an item in an Area
- `area.center(item)` Center an item in an Area

## Examples

- `examples/simpletest.py` - basic layout usage
- `examples/debug_simpletest.py` - debug overlays
- `examples/subgrid_simpletest.py` - nested layouts

## Rules & Limitations

- Merged areas must form solid rectangles
- Names cannot be both merged and repeated
- Templates must be rectangular (all rows same length)
- Layout size must be explicitly provided

## Status

Early-stage library. API may change.

## Licence

MIT Licence
