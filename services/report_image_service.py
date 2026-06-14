from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def create_report_image(
    report_text,
    output_file="report.png"
):

    lines = report_text.split("\n")

    width = 900

    line_height = 40

    height = (
        len(lines) * line_height
    ) + 100

    image = Image.new(
        "RGB",
        (width, height),
        "white"
    )

    draw = ImageDraw.Draw(
        image
    )

    try:

        font = ImageFont.truetype(
            "DejaVuSans.ttf",
            28
        )

    except:

        font = ImageFont.load_default()

    y = 30

    for line in lines:

        draw.text(
            (30, y),
            line,
            fill="black",
            font=font
        )

        y += line_height

    image.save(
        output_file
    )

    return output_file
