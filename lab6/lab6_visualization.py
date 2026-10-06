# Построение рисунков для лабораторной работы №6.

from math import cos, pi, sin
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


def normalized_edges(edges: list) -> set:
    # Приводит неориентированные рёбра к единому виду.
    return {tuple(sorted(edge)) for edge in edges}


def circular_layout(
    labels: list,
    size: int,
    radius_fraction: float = 0.39,
) -> dict:
    # Располагает вершины равномерно по окружности.
    center = size / 2
    radius = size * radius_fraction
    return {
        label: (
            center + radius * cos(-pi / 2 + 2 * pi * index / len(labels)),
            center + radius * sin(-pi / 2 + 2 * pi * index / len(labels)),
        )
        for index, label in enumerate(labels)
    }


def get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    # Загружает доступный шрифт для подписей.
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


def draw_graph(
    labels: list,
    edges: list,
    output: Path,
    title: str,
    label_prefix: str = "",
    highlighted: Optional[list] = None,
) -> None:
    # Рисует граф и при необходимости выделяет выбранные рёбра.
    size = 1500 if len(labels) <= 12 else 1900
    image = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(image)
    positions = circular_layout(labels, size)
    highlighted_edges = normalized_edges(highlighted or [])

    for left, right in normalized_edges(edges):
        is_highlighted = (left, right) in highlighted_edges
        color = "#D84A4A" if is_highlighted else "#8190A5"
        width = 10 if is_highlighted else (3 if len(labels) > 12 else 5)
        draw.line((positions[left], positions[right]), fill=color, width=width)

    radius = 42 if len(labels) <= 12 else 35
    node_font = get_font(30 if len(labels) <= 12 else 22, bold=True)
    for label in labels:
        x, y = positions[label]
        draw.ellipse(
            (x - radius, y - radius, x + radius, y + radius),
            fill="#E8F1FA",
            outline="#204A73",
            width=5,
        )
        text = f"{label_prefix}{label}"
        box = draw.textbbox((0, 0), text, font=node_font)
        text_position = (
            x - (box[2] - box[0]) / 2,
            y - (box[3] - box[1]) / 2 - 2,
        )
        draw.text(text_position, text, fill="#102A43", font=node_font)

    title_font = get_font(42, bold=True)
    box = draw.textbbox((0, 0), title, font=title_font)
    title_position = ((size - (box[2] - box[0])) / 2, 28)
    draw.text(title_position, title, fill="#102A43", font=title_font)
    image.save(output)
