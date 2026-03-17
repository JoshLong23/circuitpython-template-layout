import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label


def _random_gray(val):
    return int("{:02X}{:02X}{:02X}".format(val, val, val), 16)


def draw_layout_debug(
    areas,
    *,
    fill=False,
    outline=False,
    labels=False,
    center_mark=False,
):
    col_val = 0
    for area in areas.all():

        if fill:
            color = _random_gray(col_val)
            col_val += 85
            if col_val > 255:
                col_val = 0

            area.append(
                Rect(
                    0,
                    0,
                    area.width,
                    area.height,
                    fill=color,
                )
            )

        if outline:
            if type(outline) == int:
                color = outline
            else:
                color = 0x000000
            area.append(
                Rect(
                    0,
                    0,
                    area.width,
                    area.height,
                    outline=color,
                )
            )

        if labels:
            if type(labels) == int:
                color = labels
            else:
                color = 0x000000
            debug_label = label.Label(
                terminalio.FONT,
                text=area.name,
                color=color,
                background_color=0xFFFFFF if fill else None,
            )
            area.place(debug_label, anchor=(0, 0), offset=(2, 1))
            

        if center_mark:
            if type(center_mark) == int:
                color = center_mark
            else:
                color = 0x000000
            area.center(label.Label(terminalio.FONT, text="+", scale=2, color=color))

def place_areas_into_grid(grid_layout, areas):
    for area in areas.all():
        grid_layout.add_content(
            area.group,
            grid_position=(area.col, area.row),
            cell_size=(area.col_span, area.row_span),
        )