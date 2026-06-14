from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def create_report_image(
    report_text,
    output_file="report.png"
):

    width = 900
    height = 1400

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

    draw.multiline_text(
        (40, 40),
        report_text,
        fill="black",
        font=font,
        spacing=12
    )

    image.save(
        output_file
    )

    return output_file
