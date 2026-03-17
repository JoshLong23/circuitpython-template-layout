import displayio
from adafruit_display_shapes.line import Line
from adafruit_displayio_layout.layouts.grid_layout import GridLayout

from .displayio_backend import place_areas_into_grid, draw_layout_debug


class SizedGroup(displayio.Group):
    def __init__(self, width, height, x=0, y=0, scale=1):
        super().__init__(x=x, y=y, scale=scale)
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


class Area:
    def __init__(
        self,
        name,
        col,
        row,
        col_span,
        row_span,
        width,
        height,
        center_x,
        center_y,
        group,
    ):
        self.name = name
        self.col = col
        self.row = row
        self.col_span = col_span
        self.row_span = row_span
        self.width = width
        self.height = height
        self.center_x = center_x
        self.center_y = center_y
        self.group = group

    def add(self, *items):
        for item in items:
            self.group.append(item)

    def append(self, item):
        self.group.append(item)

    def remove(self, item):
        self.group.remove(item)

    def clear(self):
        while len(self.group):
            self.group.pop()

    def place(self, item, anchor=(0.5, 0.5), offset=(0, 0)):
        ax, ay = anchor

        x = int(self.center_x + (ax - 0.5) * self.width) + offset[0]
        y = int(self.center_y + (ay - 0.5) * self.height) + offset[1]

        if hasattr(item, "anchor_point"):
            item.anchor_point = (ax, ay)
            item.anchored_position = (x, y)
        else:
            if hasattr(item, "width"):
                x -= int(item.width * ax)
            if hasattr(item, "height"):
                y -= int(item.height * ay)
            item.x = x
            item.y = y

        self.group.append(item)

    def center(self, item):
        self.place(item, anchor=(0.5, 0.5))

    def make_subgrid(
            self, 
            template,
            debug=False,
            debug_fill=False,
            debug_outline=False, 
            debug_labels=False, 
            debug_centers=False, 
            debug_grid=False,
            **grid_kwargs
    ):
        sublayout = Layout(template, (self.width, self.height))

        grid = GridLayout(
            x=0,
            y=0,
            width=self.width,
            height=self.height,
            grid_size=sublayout.grid_size,
            cell_padding=0,
            **grid_kwargs
        )
        sublayout.place_into(grid)
        self.group.append(grid)

        if not debug == False:
            debug_fill=False
            debug_outline=True 
            debug_labels=True 
            debug_centers=0x808080
            debug_grid=0x808080

        # Draw col/row grid
        if not debug_grid == False or type(debug_grid) == int:
            if isinstance(debug_grid, int):
                color = debug_grid
            else:
                color = 0x808080
            
            grid_row_pos = []
            grid_col_pos = []
            for area in sublayout.all():
                # Use GridLayout math to calculate row height and col width
                right = int((area.col + area.col_span) * self.width / sublayout.cols)
                bottom = int((area.row + area.row_span) * self.height / sublayout.rows)

                if bottom not in grid_row_pos:
                    grid_row_pos.append(bottom)
                
                if right not in grid_col_pos:
                    grid_col_pos.append(right)
            
            for r in grid_row_pos:
                grid.append(Line(x0=0, x1=self.width, y0=r, y1=r, color=color))
            for c in grid_col_pos:
                grid.append(Line(x0=c, x1=c, y0=0, y1=self.height, color=color))
        
        draw_layout_debug(
            sublayout, 
            fill=debug_fill, 
            outline=debug_outline, 
            labels=debug_labels, 
            center_mark=debug_centers
        )  
        return sublayout

    @property
    def left(self):
        return self.center_x - self.width // 2

    @property
    def right(self):
        return self.left + self.width

    @property
    def top(self):
        return self.center_y - self.height // 2

    @property
    def bottom(self):
        return self.top + self.height


class Areas:
    def __init__(self, singles, repeats):
        self.singles = singles
        self.repeats = repeats

    def __getitem__(self, name):
        if name in self.singles:
            return self.singles[name]
        if name in self.repeats:
            return self.repeats[name]
        raise KeyError("Unknown area name: {}".format(name))

    def all(self):
        out = list(self.singles.values())
        for group in self.repeats.values():
            out.extend(group)
        return out

    def names(self):
        out = list(self.singles.keys())
        out.extend(self.repeats.keys())
        return out


class Placement:
    def __init__(self, col, row, col_span, row_span):
        self.col = col
        self.row = row
        self.col_span = col_span
        self.row_span = row_span


def _is_empty_cell(cell):
    return cell is None or cell == "."


def _is_split_name(name):
    return str(name).endswith("*")


def _normalize_name(name):
    name = str(name)
    return name[:-1] if name.endswith("*") else name


def placement_from_coords(name, coords):
    min_r = min(r for r, _ in coords)
    max_r = max(r for r, _ in coords)
    min_c = min(c for _, c in coords)
    max_c = max(c for _, c in coords)

    expected = set()
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            expected.add((r, c))

    if coords != expected:
        raise ValueError(
            "Area '{}' is not a rectangle. It must form a solid block.".format(name)
        )

    return Placement(
        col=min_c,
        row=min_r,
        col_span=max_c - min_c + 1,
        row_span=max_r - min_r + 1,
    )


def template_grid_size(template):
    if not template or not template[0]:
        raise ValueError(
            "Template must be a non-empty rectangular grid with at least one row and one column."
        )

    cols = len(template[0])
    for r, row in enumerate(template):
        if len(row) != cols:
            raise ValueError(
                "Row {} has {} cols; expected {}.".format(r, len(row), cols)
            )

    return cols, len(template)


def template_areas(template):
    cols, rows = template_grid_size(template)

    merged_coords = {}
    repeated_placements = {}

    for r in range(rows):
        for c in range(cols):
            cell = template[r][c]

            if _is_empty_cell(cell):
                continue

            raw_name = str(cell)
            name = _normalize_name(raw_name)

            if _is_split_name(raw_name):
                repeated_placements.setdefault(name, []).append(
                    Placement(col=c, row=r, col_span=1, row_span=1)
                )
            else:
                merged_coords.setdefault(name, set()).add((r, c))

    overlap = set(merged_coords) & set(repeated_placements)
    if overlap:
        raise ValueError(
            "These names are used as both merged and repeated: {}".format(sorted(overlap))
        )

    merged = {}
    for name, coords in merged_coords.items():
        merged[name] = placement_from_coords(name, coords)

    return merged, repeated_placements


def _build_areas(template, layout_size):
    cols, rows = template_grid_size(template)
    merged, repeated = template_areas(template)

    layout_w, layout_h = layout_size

    single_areas = {}
    repeated_areas = {}

    for name, p in merged.items():
        # Use GridLayout math to calculate row height and col width
        left = int(p.col * layout_w / cols)
        right = int((p.col + p.col_span) * layout_w / cols)
        top = int(p.row * layout_h / rows)
        bottom = int((p.row + p.row_span) * layout_h / rows)

        area_w = right - left
        area_h = bottom - top

        single_areas[name] = Area(
            name=name,
            col=p.col,
            row=p.row,
            col_span=p.col_span,
            row_span=p.row_span,
            width=area_w,
            height=area_h,
            center_x=area_w // 2,
            center_y=area_h // 2,
            group=SizedGroup(area_w, area_h),
        )

    for name, placements in repeated.items():
        repeated_areas[name] = []

        for p in placements:
            # Use GridLayout math to calculate row height and col width
            left = int(p.col * layout_w / cols)
            right = int((p.col + p.col_span) * layout_w / cols)
            top = int(p.row * layout_h / rows)
            bottom = int((p.row + p.row_span) * layout_h / rows)

            area_w = right - left
            area_h = bottom - top

            repeated_areas[name].append(
                Area(
                    name=name,
                    col=p.col,
                    row=p.row,
                    col_span=p.col_span,
                    row_span=p.row_span,
                    width=area_w,
                    height=area_h,
                    center_x=area_w // 2,
                    center_y=area_h // 2,
                    group=SizedGroup(area_w, area_h),
                )
            )

    return cols, rows, Areas(single_areas, repeated_areas)


class Layout:
    def __init__(self, template, size):
        cols, rows, areas = _build_areas(template, size)
        self.template = template
        self.width, self.height = size
        self.cols = cols
        self.rows = rows
        self.areas = areas

    def __getitem__(self, name):
        return self.areas[name]

    @property
    def grid_size(self):
        return (self.cols, self.rows)

    def all(self):
        return self.areas.all()

    def place_into(self, grid_layout):
        place_areas_into_grid(grid_layout, self.areas)
        return grid_layout

    def debug(self, **kwargs):
        draw_layout_debug(self.areas, **kwargs)
        return self
        
    def names(self):
        return self.areas.names()
    
    """
    fill=False,
    outline=False,
    labels=True,
    center_mark=False,
    center_mark_color=0x808080,
    """

    def make_grid_layout(
        self,
        *, 
        x=0, 
        y=0, 
        cell_padding=0,
        debug=False,
        debug_fill=False,
        debug_outline=False, 
        debug_labels=False, 
        debug_centers=False, 
        debug_grid=False, 
        **kwargs
    ):
        grid = GridLayout(
            x=x,
            y=y,
            width=self.width,
            height=self.height,
            grid_size=self.grid_size,
            cell_padding=cell_padding,
            **kwargs
        )
        self.place_into(grid)
        
        if not debug == False:
            debug_fill=False
            debug_outline=True 
            debug_labels=True 
            debug_centers=0x808080
            debug_grid=0x808080

        # Draw col/row grid
        if not debug_grid == False or type(debug_grid) == int:
            if isinstance(debug_grid, int):
                color = debug_grid
            else:
                color = 0x808080
            
            grid_row_pos = []
            grid_col_pos = []
            for area in self.areas.all():
                # Use GridLayout math to calculate row height and col width
                right = int((area.col + area.col_span) * self.width / self.cols)
                bottom = int((area.row + area.row_span) * self.height / self.rows)

                if bottom not in grid_row_pos:
                    grid_row_pos.append(bottom)
                
                if right not in grid_col_pos:
                    grid_col_pos.append(right)
            
            for r in grid_row_pos:
                grid.append(Line(x0=0, x1=self.width, y0=r, y1=r, color=color))
            for c in grid_col_pos:
                grid.append(Line(x0=c, x1=c, y0=0, y1=self.height, color=color))
        
        draw_layout_debug(
            self.areas, 
            fill=debug_fill, 
            outline=debug_outline, 
            labels=debug_labels, 
            center_mark=debug_centers, 
            **kwargs
        )
        return grid