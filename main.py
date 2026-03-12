"""
    Takes in data from a .csv and creates .svg cards from it. 
    csv data: first_name, last_name, csh_username, major, graduation_year (just the yyyy number), status (Member, Alumni, ...)

    Author: Addison Asuncion
    Last Updated: 3/12/2026
"""

import csv
import svgwrite
import base64

CARD_WIDTH = 900
CARD_HEIGHT = 1200

card_template = 'templates/MemberTemplate.svg'

# csv data: first_name, last_name, csh_username, major, graduation_year (just the yyyy number), status (Member, Alumni, ...)
with open("data/data.csv") as file:
    reader = csv.DictReader(file)

    for row in reader:
        filename = f"C:/Users/ahasu/Downloads/csh50th_cards/{row['first_name']}_{row['last_name']}_{row['csh_username']}.svg"

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
                card_template = 'templates/NonmemmberTemplate.svg'
            case _:
                raise Exception("invalid status")

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
                font_size=161,
                font_family="Roboto",
                text_anchor="middle",
            )
        )

        # Last Name
        drawing.add(
            drawing.text(
                row["last_name"],
                insert=(555, 785),
                font_size=96,
                font_family="Roboto",
                text_anchor="middle",
            )
        )

        # CSH Username
        drawing.add(
            drawing.text(
                row["csh_username"],
                insert=(555, 905),
                font_size=61,
                font_family="Roboto",
                text_anchor="middle",
                font_style='italic',
                fill="black"
            )
        )

        # Major
        drawing.add(
            drawing.text(
                row['major'],
                insert=(555, 1015),
                font_size=48,
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