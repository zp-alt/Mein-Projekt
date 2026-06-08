#!/usr/bin/env python3
"""Erzeugt die Rechnung als PDF (A4) für Pre Art of Hair."""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

OUT = "/home/user/Mein-Projekt/Rechnung_2026-0608_Hoedl.pdf"
W, H = A4
M = 50
BLACK = HexColor("#141414")
GRAY = HexColor("#7a7a7a")
LINE = HexColor("#d8d8d8")

c = canvas.Canvas(OUT, pagesize=A4)


def spaced(x, y, text, font, size, space, color=BLACK):
    c.setFont(font, size)
    c.setFillColor(color)
    for ch in text:
        c.drawString(x, y, ch)
        x += c.stringWidth(ch, font, size) + space
    return x


# ---------- Kopf / Wortmarke ----------
spaced(M, H - 62, "PRE", "Helvetica-Bold", 34, 6)
spaced(M, H - 80, "ART OF HAIR  ·  MÜNCHEN", "Helvetica", 9, 2.2, GRAY)

# Rechnungstitel + Meta rechts
c.setFont("Helvetica-Bold", 24)
c.setFillColor(BLACK)
c.drawRightString(W - M, H - 58, "RECHNUNG")
c.setFont("Helvetica", 9.5)
meta = [
    ("Rechnungs-Nr.", "2026-0608"),
    ("Rechnungsdatum", "08.06.2026"),
    ("Leistungsdatum", "08.06.2026"),
]
my = H - 76
for label, val in meta:
    c.setFillColor(GRAY)
    c.drawRightString(W - M - 95, my, label)
    c.setFillColor(BLACK)
    c.drawRightString(W - M, my, val)
    my -= 13

# Trennlinie
c.setStrokeColor(BLACK)
c.setLineWidth(1.4)
c.line(M, H - 120, W - M, H - 120)

# Absenderzeile
spaced(M, H - 136, "Pre Art of Hair · Papa-Schmid-Straße 2 · 80469 München",
       "Helvetica", 8, 0.3, GRAY)

# ---------- Adressblöcke ----------
top = H - 166


def block(x, title, lines, align_right=False):
    c.setFont("Helvetica", 8)
    c.setFillColor(GRAY)
    draw = c.drawRightString if align_right else c.drawString
    draw(x, top, title.upper())
    yy = top - 16
    for i, ln in enumerate(lines):
        c.setFont("Helvetica-Bold" if i == 0 else "Helvetica", 10.5 if i == 0 else 9.5)
        c.setFillColor(BLACK)
        draw(x, yy, ln)
        yy -= 13


block(M, "Rechnung an", [
    "Benedikt Hödl",
    "Landrat-Krug-Str. 5",
    "94447 Plattling",
    "benhoedl@web.de",
])
block(W - M, "Rechnungssteller", [
    "Pre Art of Hair",
    "Inhaberin: Zyhra Pici",
    "Papa-Schmid-Straße 2",
    "80469 München",
    "zp@preartofhair.com",
    "Steuer-Nr.: 184/390/14489",
], align_right=True)

# ---------- Leistungstabelle ----------
ty = top - 110
col_pos = M + 4
col_desc = M + 40
col_unit = W - M - 95
col_sum = W - M - 4

# Kopfzeile (schwarzer Balken)
c.setFillColor(BLACK)
c.rect(M, ty, W - 2 * M, 22, fill=1, stroke=0)
c.setFillColor(HexColor("#ffffff"))
c.setFont("Helvetica-Bold", 8.5)
c.drawString(col_pos, ty + 7, "POS.")
c.drawString(col_desc, ty + 7, "LEISTUNG")
c.drawRightString(col_unit, ty + 7, "EINZELPREIS")
c.drawRightString(col_sum, ty + 7, "GESAMT")

rows = [
    ("1", "Strähnen ganzer Kopf – Neukunde",
     "inkl. Glossing und Epres Haarbonding", "330,00 €", "330,00 €"),
    ("2", "Haarschnitt – Neukunde", None, "110,00 €", "110,00 €"),
]

ry = ty - 6
for pos, desc, sub, unit, total in rows:
    ry -= 16
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 10)
    c.drawString(col_pos, ry, pos)
    c.drawString(col_desc, ry, desc)
    c.drawRightString(col_unit, ry, unit)
    c.drawRightString(col_sum, ry, total)
    if sub:
        ry -= 12
        c.setFillColor(GRAY)
        c.setFont("Helvetica", 8.5)
        c.drawString(col_desc, ry, sub)
    ry -= 6
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(M, ry, W - M, ry)

# ---------- Summen ----------
sy = ry - 22
sx_label = W - M - 150
sx_val = W - M - 4
for label, val, bold in [
    ("Nettobetrag", "369,75 €", False),
    ("zzgl. 19 % MwSt.", "70,25 €", False),
]:
    c.setFont("Helvetica", 10)
    c.setFillColor(BLACK)
    c.drawString(sx_label, sy, label)
    c.drawRightString(sx_val, sy, val)
    sy -= 16

# Gesamtbetrag mit Linie
c.setStrokeColor(BLACK)
c.setLineWidth(1.2)
c.line(sx_label, sy + 4, sx_val, sy + 4)
sy -= 12
c.setFont("Helvetica-Bold", 12.5)
c.drawString(sx_label, sy, "Gesamtbetrag")
c.drawRightString(sx_val, sy, "440,00 €")

# ---------- Hinweistext ----------
ny = sy - 45
c.setFont("Helvetica-Bold", 9.5)
c.setFillColor(BLACK)
c.drawString(M, ny, "Vielen Dank für Ihren Besuch und Ihr Vertrauen!")
ny -= 15
c.setFont("Helvetica", 9)
c.setFillColor(HexColor("#444444"))
for ln in [
    "Bitte überweisen Sie den Rechnungsbetrag von 440,00 € innerhalb von 14 Tagen,",
    "bis zum 22.06.2026, ohne Abzug auf das unten genannte Konto.",
    "Verwendungszweck: Rechnungsnummer 2026-0608.",
]:
    c.drawString(M, ny, ln)
    ny -= 13

# ---------- Fußzeile ----------
fy = 70
c.setStrokeColor(LINE)
c.setLineWidth(0.8)
c.line(M, fy + 18, W - M, fy + 18)
c.setFont("Helvetica-Bold", 8)
c.setFillColor(BLACK)
c.drawString(M, fy + 4, "Pre Art of Hair")
c.drawString(M + 180, fy + 4, "Steuer")
c.drawString(M + 320, fy + 4, "Bankverbindung")
c.setFont("Helvetica", 7.5)
c.setFillColor(GRAY)
c.drawString(M, fy - 7, "Inhaberin Zyhra Pici")
c.drawString(M, fy - 17, "zp@preartofhair.com")
c.drawString(M + 180, fy - 7, "Steuer-Nr.:")
c.drawString(M + 180, fy - 17, "184/390/14489")
c.drawString(M + 320, fy - 7, "Qonto")
c.drawString(M + 320, fy - 17, "IBAN: DE31 1001 0123 0705 0302 27")
c.drawString(M + 320, fy - 27, "BIC: QNTODEB2XXX")

c.showPage()
c.save()
print("OK:", OUT)
