#!/usr/bin/env python3
"""Wiederverwendbarer Rechnungs-Generator für Pre Art of Hair (A4 PDF)."""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

W, H = A4
M = 50
BLACK = HexColor("#141414")
GRAY = HexColor("#7a7a7a")
LINE = HexColor("#d8d8d8")
LOGO = "/home/user/Mein-Projekt/logo_pre.png"

# Fester Rechnungssteller (Stammdaten)
SELLER = [
    "Pre Art of Hair",
    "Inhaberin: Zyhra Pici",
    "Papa-Schmid-Straße 2",
    "80469 München",
    "zp@preartofhair.com",
    "Steuer-Nr.: 184/390/14489",
]
SENDER_LINE = "Pre Art of Hair · Papa-Schmid-Straße 2 · 80469 München"
BANK = ("Qonto", "IBAN: DE31 1001 0123 0705 0302 27", "BIC: QNTODEB2XXX")


def build(data, out):
    c = canvas.Canvas(out, pagesize=A4)

    def spaced(x, y, text, font, size, space, color=BLACK):
        c.setFont(font, size)
        c.setFillColor(color)
        for ch in text:
            c.drawString(x, y, ch)
            x += c.stringWidth(ch, font, size) + space
        return x

    # ---------- Kopf / Logo ----------
    c.drawImage(LOGO, M, H - 94, width=64, height=64, mask="auto",
                preserveAspectRatio=True)
    spaced(M + 78, H - 68, "ART OF HAIR  ·  MÜNCHEN", "Helvetica", 9.5, 2.4, GRAY)

    # Titel + Meta rechts
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(BLACK)
    c.drawRightString(W - M, H - 58, "RECHNUNG")
    c.setFont("Helvetica", 9.5)
    meta = [
        ("Rechnungs-Nr.", data["number"]),
        ("Rechnungsdatum", data["invoice_date"]),
        ("Leistungsdatum", data["service_date"]),
    ]
    my = H - 76
    for label, val in meta:
        c.setFillColor(GRAY)
        c.drawRightString(W - M - 95, my, label)
        c.setFillColor(BLACK)
        c.drawRightString(W - M, my, val)
        my -= 13

    c.setStrokeColor(BLACK)
    c.setLineWidth(1.4)
    c.line(M, H - 120, W - M, H - 120)
    spaced(M, H - 136, SENDER_LINE, "Helvetica", 8, 0.3, GRAY)

    # ---------- Adressblöcke ----------
    top = H - 166

    def block(x, title, lines, align_right=False):
        c.setFont("Helvetica", 8)
        c.setFillColor(GRAY)
        draw = c.drawRightString if align_right else c.drawString
        draw(x, top, title.upper())
        yy = top - 16
        for i, ln in enumerate(lines):
            c.setFont("Helvetica-Bold" if i == 0 else "Helvetica",
                      10.5 if i == 0 else 9.5)
            c.setFillColor(BLACK)
            draw(x, yy, ln)
            yy -= 13

    block(M, "Rechnung an", data["customer"])
    block(W - M, "Rechnungssteller", SELLER, align_right=True)

    # ---------- Leistungstabelle ----------
    ty = top - 110
    col_pos = M + 4
    col_desc = M + 40
    col_unit = W - M - 95
    col_sum = W - M - 4

    c.setFillColor(BLACK)
    c.rect(M, ty, W - 2 * M, 22, fill=1, stroke=0)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(col_pos, ty + 7, "POS.")
    c.drawString(col_desc, ty + 7, "LEISTUNG")
    c.drawRightString(col_unit, ty + 7, "EINZELPREIS")
    c.drawRightString(col_sum, ty + 7, "GESAMT")

    ry = ty - 6
    for i, (desc, sub, unit, total) in enumerate(data["rows"], start=1):
        ry -= 16
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 10)
        c.drawString(col_pos, ry, str(i))
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
    for label, val in [
        ("Nettobetrag", data["net"]),
        ("zzgl. 19 % MwSt.", data["vat"]),
    ]:
        c.setFont("Helvetica", 10)
        c.setFillColor(BLACK)
        c.drawString(sx_label, sy, label)
        c.drawRightString(sx_val, sy, val)
        sy -= 16
    c.setStrokeColor(BLACK)
    c.setLineWidth(1.2)
    c.line(sx_label, sy + 4, sx_val, sy + 4)
    sy -= 12
    c.setFont("Helvetica-Bold", 12.5)
    c.drawString(sx_label, sy, "Gesamtbetrag")
    c.drawRightString(sx_val, sy, data["gross"])

    # ---------- Hinweistext ----------
    ny = sy - 45
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(BLACK)
    c.drawString(M, ny, "Vielen Dank für die gute Zusammenarbeit!")
    ny -= 15
    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor("#444444"))
    for ln in [
        f"Bitte überweisen Sie den Rechnungsbetrag von {data['gross']} innerhalb von 14 Tagen,",
        f"bis zum {data['due_date']}, ohne Abzug auf das unten genannte Konto.",
        f"Verwendungszweck: Rechnungsnummer {data['number']}.",
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
    c.drawString(M + 320, fy - 7, BANK[0])
    c.drawString(M + 320, fy - 17, BANK[1])
    c.drawString(M + 320, fy - 27, BANK[2])

    c.showPage()
    c.save()
    print("OK:", out)


if __name__ == "__main__":
    data = {
        "number": "2026-0803-2",
        "invoice_date": "03.08.2026",
        "service_date": "21.07.2026",
        "due_date": "17.08.2026",
        "customer": [
            "New Flag GmbH",
            "Leopoldstr. 154",
            "80804 München",
        ],
        "rows": [
            ("Styling Event", None, "400,00 €", "400,00 €"),
        ],
        "net": "336,13 €",
        "vat": "63,87 €",
        "gross": "400,00 €",
    }
    build(data, "/home/user/Mein-Projekt/Rechnung_2026-0803-2_NewFlag.pdf")
