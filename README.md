# circuitpython_grid_template_areas

A CircuitPython layout helper inspired by CSS Grid Template Areas in order to reduce UI development iterations.

Originally developed for use on displays such as Adafruit's MagTag and other e-ink/e-paper displays where layouts cannot be refreshed regularly, making visual development and alignment of graphical elements challenging.

## Features

- Named areas from a template grid
- Merged rectangular areas
- Repeated iterable areas using `*`
- Easy placement helpers
- Optional debug overlays
- Subgrid support

## Files

- `lib/circuitpython_grid_template_areas/` - library code
- `examples/` - demo scripts

## Basic idea/example

To create a layout like this:

```
+-------------------------------------------+
|                   title                   |
|-------------------------------------------|
|           |             header            |
|  sidebar  |-------------------------------|
|           |   day   |    day    |   day   |
+-------------------------------------------+
```

Create a template like:

```python
TEMPLATE = [
    ["title", "title", "title", "title"],
    ["sidebar", "header", "header", "header"],
    ["sidebar", "day*", "day*", "day*"],
]
```

Creates a 4 column x 3 row grid where:

- Row 1 all cells are merged and named `title`
- Row 2 cells in column 2, 3 and 4 are merged and named `header`
- Row 3 cells in column 2, 3 and 4 are seperate and iterable e.g. `day[0]` `day[1]` `day[2]`
- Row 2 and 3 in Column 1 are merged and named `sidebar`

A `layout` is created using:

```python
layout = Layout(template=TEMPLATE, size=(display.width, display.height))
```

Areas within the layout can now be accessed via:

```python
layout["title"]
layout["header"]
layout["sidebar"]
layout["day"][0]
layout["day"][1]
layout["day"][2]
```

For each Area you can access it's:

- `name` (Area name)
- `col` (Column that the Area starts in)
- `row` (Row that the Area starts in)
- `col_span` (Number of columns the Area spans)
- `row_span` (Number of rows the Area spans)
- `width` (Width of the Area)
- `height` (Height of the Area)
- `center_x` (Pixels from Area left edge to center of the Area)
- `center_y` (Pixels from Area top edge to center of the Area)
- `group` (Area's displayio Group)

Elements such as text, shapes or images can be added or removed from each Area's displayio Group using the following:

- `.add(*items)`
- `.append(item)`
- `.remove(item)`
- `.clear()`
- `.place(item, anchor=(0.5, 0.5), offset=(0, 0))`
- `.center(item)`

Areas can also become subgrids by using `.make_subgrid()`. See `examples/subgrid_simpletest.py` for an example.
