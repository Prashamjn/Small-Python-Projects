"""
Invoice Generator
------------------
A terminal-based invoice generator that produces clean, modern,
minimal PDF invoices (amounts shown in Indian Rupees, Rs symbol).
"""

import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT_FOLDER = "invoices"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ----------------------------------------------------------------------
# FONTS
# ----------------------------------------------------------------------
# The built-in PDF fonts (Helvetica etc.) do NOT contain a Rupee (₹)
# glyph, so printing it with them renders as a solid black/white box.
# DejaVu Sans includes the Rupee glyph, so we register it and use it
# everywhere money is printed.
#
# To make this work on ANY machine (Windows/Mac/Linux), this script
# first looks for the font bundled in a "fonts" folder placed right
# next to this .py file. Keep the folder structure below intact:
#
#   invoice_generator.py
#   fonts/
#       DejaVuSans.ttf
#       DejaVuSans-Bold.ttf
#
# If the bundled font isn't found, it falls back to common system
# font locations. If none of those work either, it falls back to
# printing "Rs." instead of the "₹" symbol -- so you'll NEVER see a
# black box, worst case you just get "Rs." instead of "₹".

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

FONT_CANDIDATES = [
    # Bundled with this script (recommended, works on every OS)
    (os.path.join(SCRIPT_DIR, "fonts", "DejaVuSans.ttf"),
     os.path.join(SCRIPT_DIR, "fonts", "DejaVuSans-Bold.ttf")),
    # Linux
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    # macOS
    ("/Library/Fonts/Arial Unicode.ttf",
     "/Library/Fonts/Arial Unicode.ttf"),
    # Windows (Arial and Segoe UI both include the Rupee glyph on
    # modern Windows installs)
    ("C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\arialbd.ttf"),
    ("C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\segoeuib.ttf"),
]

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
RUPEE = "Rs. "  # safe fallback used only if no Rupee-capable font is found

for regular_path, bold_path in FONT_CANDIDATES:
    if os.path.exists(regular_path) and os.path.exists(bold_path):
        try:
            pdfmetrics.registerFont(TTFont("InvoiceSans", regular_path))
            pdfmetrics.registerFont(TTFont("InvoiceSans-Bold", bold_path))
            FONT_REGULAR = "InvoiceSans"
            FONT_BOLD = "InvoiceSans-Bold"
            RUPEE = "\u20B9"  # ₹ symbol -- safe to use with this font
            break
        except Exception:
            continue

# ----------------------------------------------------------------------
# THEME
# ----------------------------------------------------------------------
INK = colors.HexColor("#111827")        # near-black text
MUTED = colors.HexColor("#6B7280")      # gray secondary text
ACCENT = colors.HexColor("#4F46E5")     # indigo accent
LINE = colors.HexColor("#E5E7EB")       # light divider
PANEL_BG = colors.HexColor("#F9FAFB")   # very light gray panel


def money(value):
    """Format a number as a rupee amount, e.g. 75000 -> '\u20b975,000.00'"""
    return f"{RUPEE}{value:,.2f}"


# ----------------------------------------------------------------------
# TERMINAL UI HELPERS
# ----------------------------------------------------------------------

def banner(title):
    line = "=" * 46
    print("\n" + line)
    print(title.center(46))
    print(line)


def section(title):
    print(f"\n{title}")
    print("-" * len(title))


def ask(prompt, required=True, default=None):
    while True:
        value = input(f"{prompt}: ").strip()
        if value:
            return value
        if not required:
            return default or ""
        print("  This field can't be empty. Please try again.")


def ask_optional(prompt):
    return input(f"{prompt} (optional): ").strip()


def ask_number(prompt, kind=float, minimum=None):
    while True:
        raw = input(f"{prompt}: ").strip()
        try:
            value = kind(raw)
            if minimum is not None and value < minimum:
                print(f"  Value must be at least {minimum}.")
                continue
            return value
        except ValueError:
            print("  Please enter a valid number.")


def ask_yes_no(prompt, default_yes=True):
    suffix = "Y/n" if default_yes else "y/N"
    while True:
        raw = input(f"{prompt} ({suffix}): ").strip().lower()
        if not raw:
            return default_yes
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  Please answer Y or N.")


def ask_choice(prompt, choices):
    choice_str = "/".join(choices)
    while True:
        raw = input(f"{prompt} ({choice_str}): ").strip().lower()
        for c in choices:
            if raw == c.lower():
                return c
        print(f"  Please choose one of: {choice_str}")


# ----------------------------------------------------------------------
# DATA COLLECTION
# ----------------------------------------------------------------------

def get_business_info():
    section("Business Information")
    return {
        "name": ask("Name"),
        "address": ask_optional("Address"),
        "phone": ask_optional("Phone"),
        "gstin": ask_optional("GSTIN"),
    }


def get_customer_info():
    section("Customer Information")
    return {
        "name": ask("Name"),
        "address": ask_optional("Address"),
        "phone": ask_optional("Phone"),
    }


def get_items():
    section("Items")
    items = []
    index = 1
    while True:
        print(f"\nItem {index}:")
        item_name = ask("  Product / Service name")
        quantity = ask_number("  Quantity", kind=int, minimum=1)
        price = ask_number("  Price per unit (Rs)", kind=float, minimum=0)
        items.append({
            "name": item_name,
            "quantity": quantity,
            "price": price,
            "total": quantity * price,
        })
        index += 1
        if not ask_yes_no("Add another item?", default_yes=False):
            break
    return items


def get_payment_method():
    section("Payment")
    return ask_choice("Payment method", ["UPI", "Cash", "Card"])


# ----------------------------------------------------------------------
# PDF STYLES
# ----------------------------------------------------------------------

def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="BusinessName",
        fontName=FONT_BOLD,
        fontSize=20,
        leading=24,
        textColor=INK,
    ))

    styles.add(ParagraphStyle(
        name="MutedSmall",
        fontName=FONT_REGULAR,
        fontSize=9,
        leading=13,
        textColor=MUTED,
    ))

    styles.add(ParagraphStyle(
        name="InvoiceLabel",
        fontName=FONT_BOLD,
        fontSize=16,
        leading=18,
        textColor=ACCENT,
        alignment=TA_RIGHT,
    ))

    styles.add(ParagraphStyle(
        name="MutedRight",
        fontName=FONT_REGULAR,
        fontSize=9,
        leading=13,
        textColor=MUTED,
        alignment=TA_RIGHT,
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        fontName=FONT_BOLD,
        fontSize=9.5,
        leading=12,
        textColor=MUTED,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="BodyText2",
        fontName=FONT_REGULAR,
        fontSize=10.5,
        leading=15,
        textColor=INK,
    ))

    styles.add(ParagraphStyle(
        name="BodyBold",
        fontName=FONT_BOLD,
        fontSize=11,
        leading=15,
        textColor=INK,
    ))

    styles.add(ParagraphStyle(
        name="TableHeader",
        fontName=FONT_BOLD,
        fontSize=9,
        leading=12,
        textColor=colors.white,
    ))

    styles.add(ParagraphStyle(
        name="TableHeaderRight",
        fontName=FONT_BOLD,
        fontSize=9,
        leading=12,
        textColor=colors.white,
        alignment=TA_RIGHT,
    ))

    styles.add(ParagraphStyle(
        name="TableCell",
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=14,
        textColor=INK,
    ))

    styles.add(ParagraphStyle(
        name="TableCellRight",
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=14,
        textColor=INK,
        alignment=TA_RIGHT,
    ))

    styles.add(ParagraphStyle(
        name="TotalLabel",
        fontName=FONT_REGULAR,
        fontSize=10,
        leading=14,
        textColor=MUTED,
        alignment=TA_RIGHT,
    ))

    styles.add(ParagraphStyle(
        name="GrandTotalLabel",
        fontName=FONT_BOLD,
        fontSize=12,
        leading=16,
        textColor=colors.white,
        alignment=TA_RIGHT,
    ))

    styles.add(ParagraphStyle(
        name="GrandTotalValue",
        fontName=FONT_BOLD,
        fontSize=13,
        leading=17,
        textColor=colors.white,
        alignment=TA_RIGHT,
    ))

    styles.add(ParagraphStyle(
        name="TotalValue",
        fontName=FONT_REGULAR,
        fontSize=10.5,
        leading=14,
        textColor=INK,
        alignment=TA_RIGHT,
    ))

    styles.add(ParagraphStyle(
        name="FooterNote",
        fontName=FONT_BOLD,
        fontSize=11,
        leading=15,
        textColor=INK,
    ))

    return styles


# ----------------------------------------------------------------------
# PDF BUILD
# ----------------------------------------------------------------------

def build_pdf(business, customer, items, payment_method, output_path,
              invoice_number, invoice_date):

    styles = build_styles()
    elements = []

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=42,
        leftMargin=42,
        topMargin=42,
        bottomMargin=42,
        title=f"Invoice {invoice_number}",
    )

    page_width = A4[0] - 84  # minus margins

    # ---------- Header: business block (left) + invoice block (right) ----------
    business_lines = [Paragraph(business["name"], styles["BusinessName"])]
    detail_bits = [x for x in [business.get("address"), business.get("phone")] if x]
    if detail_bits:
        business_lines.append(Spacer(1, 3))
        business_lines.append(Paragraph(" &nbsp;|&nbsp; ".join(detail_bits), styles["MutedSmall"]))
    if business.get("gstin"):
        business_lines.append(Paragraph(f"GSTIN: {business['gstin']}", styles["MutedSmall"]))

    invoice_block = [
        Paragraph("INVOICE", styles["InvoiceLabel"]),
        Spacer(1, 4),
        Paragraph(f"No. {invoice_number}", styles["MutedRight"]),
        Paragraph(f"Date: {invoice_date}", styles["MutedRight"]),
    ]

    header_table = Table(
        [[business_lines, invoice_block]],
        colWidths=[page_width * 0.6, page_width * 0.4],
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(header_table)

    elements.append(Spacer(1, 14))
    elements.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceAfter=0))
    elements.append(Spacer(1, 22))

    # ---------- Bill To / Payment panel ----------
    bill_to_lines = [Paragraph("BILL TO", styles["SectionHeading"])]
    bill_to_lines.append(Paragraph(customer["name"], styles["BodyBold"]))
    for field in (customer.get("address"), customer.get("phone")):
        if field:
            bill_to_lines.append(Paragraph(field, styles["MutedSmall"]))

    payment_lines = [
        Paragraph("PAYMENT METHOD", styles["SectionHeading"]),
        Paragraph(payment_method, styles["BodyBold"]),
    ]

    info_table = Table(
        [[bill_to_lines, payment_lines]],
        colWidths=[page_width * 0.6, page_width * 0.4],
    )
    info_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(info_table)

    elements.append(Spacer(1, 26))

    # ---------- Items table ----------
    header_row = [
        Paragraph("#", styles["TableHeader"]),
        Paragraph("ITEM / SERVICE", styles["TableHeader"]),
        Paragraph("QTY", styles["TableHeaderRight"]),
        Paragraph("RATE", styles["TableHeaderRight"]),
        Paragraph("AMOUNT", styles["TableHeaderRight"]),
    ]

    data = [header_row]
    subtotal = 0.0
    for i, item in enumerate(items, start=1):
        subtotal += item["total"]
        data.append([
            Paragraph(str(i), styles["TableCell"]),
            Paragraph(item["name"], styles["TableCell"]),
            Paragraph(str(item["quantity"]), styles["TableCellRight"]),
            Paragraph(money(item["price"]), styles["TableCellRight"]),
            Paragraph(money(item["total"]), styles["TableCellRight"]),
        ])

    col_widths = [
        page_width * 0.06,
        page_width * 0.44,
        page_width * 0.12,
        page_width * 0.18,
        page_width * 0.20,
    ]

    items_table = Table(data, colWidths=col_widths, repeatRows=1)

    row_styles = [
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TOPPADDING", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 1), (-1, -1), 0.6, LINE),
    ]
    # subtle zebra striping for readability
    for row_idx in range(1, len(data)):
        if row_idx % 2 == 0:
            row_styles.append(("BACKGROUND", (0, row_idx), (-1, row_idx), PANEL_BG))

    items_table.setStyle(TableStyle(row_styles))
    elements.append(items_table)

    elements.append(Spacer(1, 18))

    # ---------- Totals ----------
    totals_rows = [
        [Paragraph("Subtotal", styles["TotalLabel"]), Paragraph(money(subtotal), styles["TotalValue"])],
    ]
    totals_table_top = Table(totals_rows, colWidths=[page_width * 0.75, page_width * 0.25])
    totals_table_top.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(totals_table_top)

    elements.append(Spacer(1, 8))

    grand_total_table = Table(
        [[Paragraph("GRAND TOTAL", styles["GrandTotalLabel"]),
          Paragraph(money(subtotal), styles["GrandTotalValue"])]],
        colWidths=[page_width * 0.75, page_width * 0.25],
    )
    grand_total_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("LEFTPADDING", (0, 0), (0, 0), 14),
        ("RIGHTPADDING", (1, 0), (1, 0), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(grand_total_table)

    elements.append(Spacer(1, 34))
    elements.append(HRFlowable(width="100%", thickness=0.7, color=LINE, spaceAfter=14))

    elements.append(Paragraph("Thank you for your business!", styles["FooterNote"]))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        f"Generated on {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
        styles["MutedSmall"],
    ))

    doc.build(elements)


# ----------------------------------------------------------------------
# MAIN FLOW
# ----------------------------------------------------------------------

def generate_invoice():
    banner("INVOICE GENERATOR")

    try:
        business = get_business_info()
        customer = get_customer_info()
        items = get_items()
        payment_method = get_payment_method()

        subtotal = sum(item["total"] for item in items)

        # ---- Review summary before writing the file ----
        print("\nSummary")
        print("-------")
        print(f"Business : {business['name']}")
        print(f"Customer : {customer['name']}")
        print(f"Items    : {len(items)}")
        print(f"Total    : {money(subtotal)}")
        print(f"Payment  : {payment_method}")

        if not ask_yes_no("\nGenerate Invoice?", default_yes=True):
            print("\nInvoice cancelled.")
            return

        invoice_number = datetime.now().strftime("INV-%Y%m%d-%H%M%S")
        invoice_date = datetime.now().strftime("%d-%m-%Y")
        filename = f"{invoice_number}.pdf"
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        build_pdf(
            business=business,
            customer=customer,
            items=items,
            payment_method=payment_method,
            output_path=output_path,
            invoice_number=invoice_number,
            invoice_date=invoice_date,
        )

        banner("INVOICE CREATED SUCCESSFULLY")
        print(f"Invoice : {invoice_number}")
        print(f"Total   : {money(subtotal)}")
        print(f"Saved   : {os.path.abspath(output_path)}")
        print("=" * 46)

    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\nERROR: {e}")


def main():
    banner("INVOICE GENERATOR")
    print("Type 'exit' to close.")
    print("=" * 46)

    while True:
        command = input("\nPress ENTER to create invoice or type 'exit': ").strip()
        if command.lower() in ("exit", "quit", "q"):
            print("\nGoodbye!")
            break
        generate_invoice()
        print("\nWaiting for next invoice...")


if __name__ == "__main__":
    main()