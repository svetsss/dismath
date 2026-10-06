# Построение рисунка паросочетания для лабораторной работы №9.

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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


def dashed_line(
    draw: ImageDraw.ImageDraw,
    points: tuple,
    fill: str,
    width: int = 4,
    dash: int = 14,
) -> None:
    # Рисует пунктирный отрезок.
    (x1, y1), (x2, y2) = points
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    if length == 0:
        return

    for start in range(0, int(length), dash * 2):
        end = min(start + dash, length)
        start_ratio = start / length
        end_ratio = end / length
        segment = (
            x1 + (x2 - x1) * start_ratio,
            y1 + (y2 - y1) * start_ratio,
            x1 + (x2 - x1) * end_ratio,
            y1 + (y2 - y1) * end_ratio,
        )
        draw.line(segment, fill=fill, width=width)


def draw_matching(
    left: set,
    right: set,
    kept: list,
    removed: list,
    matching: list,
    output: Path,
) -> None:
    # Рисует двудольный граф и выделяет найденное паросочетание.
    width, height = 1600, 1200
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    positions = {}

    for x, group in ((300, sorted(left)), (1300, sorted(right))):
        gap = 940 / max(1, len(group) - 1)
        for index, vertex in enumerate(group):
            positions[vertex] = (x, 150 + index * gap)

    matching_edges = {tuple(sorted(edge)) for edge in matching}
    for u, v in kept:
        is_matching = tuple(sorted((u, v))) in matching_edges
        color = "#D83A3A" if is_matching else "#B4BECC"
        draw.line(
            (positions[u], positions[v]),
            fill=color,
            width=10 if is_matching else 4,
        )

    for u, v in removed:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        offset = 100 if x1 < width / 2 else -100
        middle = ((x1 + x2) / 2 + offset, (y1 + y2) / 2)
        dashed_line(draw, ((x1, y1), middle), "#E59A3A", 5)
        dashed_line(draw, (middle, (x2, y2)), "#E59A3A", 5)

    node_font = get_font(30, bold=True)
    for vertex, (x, y) in positions.items():
        draw.ellipse(
            (x - 35, y - 35, x + 35, y + 35),
            fill="#E8F1FA",
            outline="#204A73",
            width=5,
        )
        label = str(vertex)
        box = draw.textbbox((0, 0), label, font=node_font)
        label_position = (
            x - (box[2] - box[0]) / 2,
            y - (box[3] - box[1]) / 2 - 2,
        )
        draw.text(label_position, label, fill="#102A43", font=node_font)

    title_font = get_font(40, bold=True)
    title = "Максимальное паросочетание двудольного графа"
    box = draw.textbbox((0, 0), title, font=title_font)
    title_position = ((width - (box[2] - box[0])) / 2, 35)
    draw.text(title_position, title, fill="#102A43", font=title_font)

    legend = "красные рёбра — найденное максимальное паросочетание"
    draw.text((300, 1140), legend, fill="#475569", font=get_font(24))
    image.save(output)
