"""
    Takes in data from a .csv and creates .svg cards from it. 
    csv data: first_name, last_name, csh_username, major, graduation_year (just the yyyy number), status (Member, Alumni, ...)

    Author: Addison Asuncion
    Last Updated: 3/27/2026
"""

import csv
import svgwrite
import base64

GROUPED_COLS_NUM: float = 5.0

CARD_WIDTH = 900
CARD_HEIGHT = 1200

cards_list = []
card_template = 'templates/MemberTemplate.svg'

def main():
    generate_svgs()
    to_one_page()

# generate svgs using data from data.csv
def generate_svgs():
    # csv data: first_name, last_name, csh_username, major, graduation_year (just the yyyy number), status (Member, Alumni, ...)
    with open("data/data.csv") as file:
        reader = csv.DictReader(file)
        num = 0

        for row in reader:
            filename = f"../../../Downloads/csh50th_cards/{row['first_name']}_{row['last_name']}_{row['csh_username']}_{num}.svg"
            num += 1
            cards_list.append(filename)

            drawing = svgwrite.Drawing(filename, size=(CARD_WIDTH, CARD_HEIGHT))
            match (row['status'].lower()):
                case 'alumni':
                    card_template = 'templates/AlumniTemplate.svg'
                case 'member':
                    card_template = 'templates/MemberTemplate.svg'
                case 'relative':
                    card_template = 'templates/RelativeTemplate.svg'
                case 'volunteer':
                    card_template = 'templates/VolunteerTemplate.svg'
                case 'honorary':
                    card_template = 'templates/HonoraryTemplate.svg'
                case 'advisory':
                    card_template = 'templates/AdvisoryTemplate.svg'
                case 'organizer':
                    card_template = 'templates/OrganizerTemplate.svg'
                case 'nonmember':
                    card_template = 'templates/NonmemberTemplate.svg'
                case _:
                    raise Exception("invalid status: " + row['status'])

            # Add a border
            drawing.add(
                drawing.rect(
                    insert=(0, 0), 
                    size=('100%', '100%'), 
                    fill='none', 
                    rx=100, 
                    ry=100,
                    stroke='red', 
                    stroke_width=5))
            
            # Add a line
            drawing.add(
                drawing.rect(
                    insert=("360px", "7.5%"), 
                    size=('200px', '45px'), 
                    fill='red', 
                    rx=20, 
                    ry=20,
                    stroke='red', 
                    stroke_width=5))

            # encode template for embedding into the svg
            with open(card_template, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            background_image = f"data:image/svg+xml;base64,{encoded}"

            # Background template
            drawing.add(
                drawing.image(
                    href=background_image, 
                    insert=(0, 0), 
                    size=(CARD_WIDTH,CARD_HEIGHT)
                )
            )

            # First Name
            drawing.add(
                drawing.text(
                    row["first_name"],
                    insert=(555, 645),
                    font_size=get_font_size(row["first_name"], 161, 6),
                    font_family="Roboto",
                    text_anchor="middle",
                )
            )

            # Last Name
            drawing.add(
                drawing.text(
                    row["last_name"],
                    insert=(555, 785),
                    font_size=get_font_size(row["last_name"], 96, 9),
                    font_family="Roboto",
                    text_anchor="middle",
                )
            )

            # CSH Username
            drawing.add(
                drawing.text(
                    row["csh_username"],
                    insert=(555, 905),
                    font_size=get_font_size(row["csh_username"], 61, 16),
                    font_family="Roboto",
                    text_anchor="middle",
                    font_style='italic',
                    fill="black"
                )
            )

            row['major'] = row['major'].replace('~', ',')
            # Major
            # If there is more than 1 major, split them up into different rows
            if(len(row['major']) > 28 and '/' in row['major']):
                splitMajor = row['major'].split(" / ")
                i = 0
                for major in splitMajor:
                    drawing.add(
                        drawing.text(
                            major,
                            insert=(555, 1030-(50*i)),
                            font_size=get_font_size(splitMajor[0], 48, 20),
                            font_family="Roboto",
                            text_anchor="middle",
                        )
                    )
                    i += 1
            else:
                drawing.add(
                    drawing.text(
                        row['major'],
                        insert=(555, 1015),
                        font_size=get_font_size(row["major"], 48, 20),
                        font_family="Roboto",
                        text_anchor="middle",
                    )
                )

            # Graduation Year
            drawing.add(
                drawing.text(
                    f"Class of {row['graduation_year']}",
                    insert=(555, 1085),
                    font_size=48,
                    font_family="Roboto",
                    text_anchor="middle",
                )
            )

            drawing.save()

# add all svgs to one page
def to_one_page():
    canvas_width, canvas_height = 900*len(cards_list), 1200*len(cards_list)  # enough for stacking vertically
    filename = f"../../../Downloads/combined_csh50th_cards.svg"

    dwg = svgwrite.Drawing(filename, size=(canvas_width, canvas_height))

    # Load SVG files as strings
    for i, file in enumerate(cards_list):
        with open(file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        data_uri = f"data:image/svg+xml;base64,{encoded}"

        col = i % GROUPED_COLS_NUM
        row = i // GROUPED_COLS_NUM

        dwg.add(
            dwg.image(
                href=data_uri,
                insert=((col) * CARD_WIDTH, (row) * CARD_HEIGHT),
                size=(CARD_WIDTH, CARD_HEIGHT)
            )
        )

    dwg.save()

# dynamic font size
def get_font_size(text: str, base_size: int = 161, max_chars: int = 7):
    """
        Dynamically changes the font size based on the length of the given text
        Args:
            text (str): the text to check for
            base_size (int): (default 161) the base font size
            max_chars (int): (default 7) the max number of chars before the font size is changed
        Returns:
            int: the new font size
    """
    if len(text) <= max_chars:
        return base_size
    return base_size * (max_chars / len(text))

if __name__ == "__main__":
    main()