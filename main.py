import csv
import svgwrite
import base64


CARD_WIDTH = 900
CARD_HEIGHT = 1200

card_template = 'templates/MemberTemplate.svg'

# csv data: first_name, last_name, csh_username, major, class_year, status
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

        with open(card_template, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        background_image = f"data:image/svg+xml;base64,{encoded}"

        # Card background
        drawing.add(
            drawing.rect(
                insert=(0, 0),
                size=(CARD_WIDTH, CARD_HEIGHT),
                fill="#f5f5f5",
                rx=15,
                ry=15
            )
        )

        # Background template
        drawing.add(
            drawing.image(
                href=background_image, 
                insert=(0, 0), 
                size=(CARD_WIDTH,CARD_HEIGHT)
            )
        )

        # Profile image
        # drawing.add(
        #     drawing.image(
        #         href=row["photo"],
        #         insert=(20, 40),
        #         size=(80, 100)
        #     )
        # )

        # Name
        drawing.add(
            drawing.text(
                row["first_name"],
                insert=(120, 70),
                font_size=20,
                font_weight="bold"
            )
        )

        # Title
        drawing.add(
            drawing.text(
                row["major"],
                insert=(120, 100),
                font_size=14,
                fill="gray"
            )
        )

        # ID number
        drawing.add(
            drawing.text(
                f"name: {row['csh_username']}",
                insert=(120, 130),
                font_size=14
            )
        )

        # Rotated vertical label
        # drawing.add(
        #     drawing.text(
        #         row['status'],
        #         insert=(330, 180),
        #         transform="rotate(-90,330,180)",
        #         font_size=14,
        #         fill="#444"
        #     )
        # )

        drawing.save()