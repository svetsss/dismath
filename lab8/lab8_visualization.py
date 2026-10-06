# Построение схем транспортной сети для лабораторной работы №8.

from math import atan2, cos, sin
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


POSITIONS = {
    "S": (110, 450),
    "p": (330, 120),
    "d": (420, 410),
    "a": (300, 720),
    "k": (850, 120),
    "c": (990, 410),
    "b": (930, 720),
    "T": (1390, 450),
}

LABEL_OFFSETS = {
    ("S", "p"): (-35, -15),
    ("S", "d"): (0, -30),
    ("S", "a"): (-30, 20),
    ("p", "k"): (0, -32),
    ("p", "b"): (90, 45),
    ("a", "d"): (-48, 0),
    ("a", "k"): (-50, -55),
    ("a", "b"): (0, 28),
    ("d", "k"): (-10, -22),
    ("d", "c"): (0, -32),
    ("k", "T"): (0, -30),
    ("c", "T"): (0, -30),
    ("c", "b"): (36, 0),
    ("b", "T"): (0, 28),
}


def get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    # Загружает доступный шрифт для рисунка.
    candidates = [
        (
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
            if bold
            else "/System/Library/Fonts/Supplemental/Arial.ttf"
        ),
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple,
    end: tuple,
    color: str,
    width: int = 5,
    radius: int = 38,
) -> None:
    # Рисует направленную дугу между границами двух вершин.
    angle = atan2(end[1] - start[1], end[0] - start[0])
    start_point = (start[0] + radius * cos(angle), start[1] + radius * sin(angle))
    end_point = (end[0] - radius * cos(angle), end[1] - radius * sin(angle))
    draw.line((start_point, end_point), fill=color, width=width)

    arrow_size = 18
    left = (
        end_point[0] - arrow_size * cos(angle - 0.55),
        end_point[1] - arrow_size * sin(angle - 0.55),
    )
    right = (
        end_point[0] - arrow_size * cos(angle + 0.55),
        end_point[1] - arrow_size * sin(angle + 0.55),
    )
    draw.polygon((end_point, left, right), fill=color)


def draw_network(
    edge_list: list,
    output: Path,
    title: str,
    flow: Optional[dict] = None,
    source_side: Optional[set] = None,
    cut_edges: Optional[list] = None,
) -> None:
    # Рисует транспортную сеть с ёмкостями или найденным потоком.
    image = Image.new("RGB", (1500, 900), "white")
    draw = ImageDraw.Draw(image)
    title_font = get_font(40, bold=True)
    node_font = get_font(30, bold=True)
    edge_font = get_font(24, bold=True)
    cut_set = {(u, v) for u, v, _ in (cut_edges or [])}

    for u, v, capacity in edge_list:
        is_cut_edge = (u, v) in cut_set
        color = "#D83A3A" if is_cut_edge else "#718096"
        draw_arrow(
            draw,
            POSITIONS[u],
            POSITIONS[v],
            color,
            width=9 if is_cut_edge else 5,
        )
        midpoint = (
            (POSITIONS[u][0] + POSITIONS[v][0]) / 2,
            (POSITIONS[u][1] + POSITIONS[v][1]) / 2,
        )
        dx, dy = LABEL_OFFSETS.get((u, v), (0, -22))
        label = f"{flow[u, v]}/{capacity}" if flow is not None else str(capacity)
        box = draw.textbbox((0, 0), label, font=edge_font)
        x = midpoint[0] + dx - (box[2] - box[0]) / 2
        y = midpoint[1] + dy - (box[3] - box[1]) / 2
        background = (
            x - 6,
            y - 3,
            x + box[2] - box[0] + 6,
            y + box[3] - box[1] + 3,
        )
        draw.rounded_rectangle(background, 5, fill="white")
        draw.text((x, y), label, fill=color, font=edge_font)

    for node, (x, y) in POSITIONS.items():
        if source_side is None:
            fill = "#E8F1FA"
        else:
            fill = "#DFF2E1" if node in source_side else "#FDE7D8"
        draw.ellipse(
            (x - 38, y - 38, x + 38, y + 38),
            fill=fill,
            outline="#204A73",
            width=5,
        )
        box = draw.textbbox((0, 0), node, font=node_font)
        node_position = (
            x - (box[2] - box[0]) / 2,
            y - (box[3] - box[1]) / 2 - 2,
        )
        draw.text(node_position, node, fill="#102A43", font=node_font)

    box = draw.textbbox((0, 0), title, font=title_font)
    title_position = ((1500 - (box[2] - box[0])) / 2, 25)
    draw.text(title_position, title, fill="#102A43", font=title_font)

    legend = (
        "красные дуги — минимальный разрез; подписи — поток/ёмкость"
        if flow is not None
        else "подписи — пропускные способности"
    )
    draw.text((70, 850), legend, fill="#475569", font=get_font(22))
    image.save(output)
