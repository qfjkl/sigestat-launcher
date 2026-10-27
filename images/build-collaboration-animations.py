"""Create the illustrated, bilingual workflow GIFs used by the public README."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parent
FONT = "C:/Windows/Fonts/segoeui.ttf"
BOLD = "C:/Windows/Fonts/segoeuib.ttf"
regular = ImageFont.truetype(FONT, 19)
small = ImageFont.truetype(FONT, 15)
bold = ImageFont.truetype(BOLD, 21)
heading = ImageFont.truetype(BOLD, 24)
badge = ImageFont.truetype(BOLD, 15)

CONFIG = {
    "annuaire-fr": ("DE LA QUESTION À LA DÉCISION", "Un travail d’équipe, accompagné par l’agent", [
        ("1", "L’équipe", "pose sa question"), ("2", "Agent annuaire", "prépare une proposition"),
        ("3", "L’équipe", "examine le résultat")]),
    "annuaire-en": ("FROM QUESTION TO DECISION", "A team workflow, supported by the agent", [
        ("1", "The team", "asks a question"), ("2", "Yearbook agent", "prepares a proposal"),
        ("3", "The team", "reviews the result")]),
    "migration-fr": ("DES DONNÉES PRÊTES À L’EMPLOI", "Préparer ensemble un traitement de migration", [
        ("1", "L’équipe", "décrit son besoin"), ("2", "Agent migration", "prépare un traitement"),
        ("3", "Le studio", "vérifie et simule")]),
    "migration-en": ("DATA READY FOR USE", "Preparing a migration workflow together", [
        ("1", "The team", "describes its need"), ("2", "Migration agent", "prepares a workflow"),
        ("3", "The studio", "checks and simulates")]),
}

def render(key, frame):
    kicker, title, cards = CONFIG[key]
    image = Image.new("RGB", (1100, 400), "#edf5f0")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((15, 15, 1085, 385), radius=24, fill="#f8fbf9", outline="#d9e9df", width=2)
    draw.text((48, 39), kicker, font=badge, fill="#287451")
    draw.text((48, 66), title, font=heading, fill="#143d2d")
    phase = (frame // 10) % 3
    for i, (number, label, description) in enumerate(cards):
        x = 45 + i * 354
        active = i == phase
        draw.rounded_rectangle((x, 145, x + 300, 310), radius=18,
                               fill="#ffffff", outline="#3e9c72" if active else "#d8e7df", width=3 if active else 2)
        draw.rounded_rectangle((x + 20, 165, x + 57, 202), radius=11,
                               fill="#d9f2e3" if active else "#eef4f0")
        draw.text((x + 33, 169), number, font=bold, fill="#16664a")
        # Simple pictograms distinguish people from the assistant without
        # pretending to show an actual screen from the platform.
        icon = "#348464" if active else "#91b7a4"
        if i == 1:
            draw.line((x + 255, 165, x + 255, 172), fill=icon, width=3)
            draw.ellipse((x + 252, 162, x + 258, 168), fill=icon)
            draw.rounded_rectangle((x + 239, 172, x + 271, 196), radius=7, outline=icon, width=3)
            draw.ellipse((x + 247, 181, x + 251, 185), fill=icon)
            draw.ellipse((x + 259, 181, x + 263, 185), fill=icon)
        elif i == 2 and key.startswith("migration"):
            draw.rounded_rectangle((x + 238, 166, x + 270, 195), radius=5, outline=icon, width=3)
            draw.line((x + 248, 168, x + 248, 193), fill=icon, width=2)
            draw.line((x + 240, 177, x + 268, 177), fill=icon, width=2)
        else:
            draw.ellipse((x + 246, 164, x + 260, 178), fill=icon)
            draw.rounded_rectangle((x + 239, 181, x + 267, 197), radius=8, fill=icon)
        draw.text((x + 20, 220), label, font=bold, fill="#183d2c")
        draw.text((x + 20, 253), description, font=regular, fill="#587164")
        if i < 2:
            left, right = x + 308, x + 346
            draw.line((left, 226, right, 226), fill="#9abdad", width=3)
            draw.polygon([(right, 226), (right - 8, 220), (right - 8, 232)], fill="#9abdad")
    if phase < 2:
        x = 45 + phase * 354 + 308 + (frame % 10) / 9 * 36
        r = 6 + math.sin((frame % 10) / 9 * math.pi) * 2
        draw.ellipse((x-r, 226-r, x+r, 226+r), fill="#d39b35")
    draw.text((48, 339), "SIGESTAT  ·  Illustration" if key.endswith("fr") else "SIGESTAT  ·  Illustration", font=small, fill="#70867b")
    return image

for name in CONFIG:
    frames = [render(name, frame) for frame in range(30)]
    frames[0].save(ROOT / f"collaboration-{name}.gif", save_all=True, append_images=frames[1:],
                   duration=120, loop=0, optimize=True, disposal=2)
