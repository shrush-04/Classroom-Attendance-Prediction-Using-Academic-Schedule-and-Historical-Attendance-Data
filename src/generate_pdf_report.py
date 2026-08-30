"""
generate_pdf_report.py
Converts report/project_report.md into a professional PDF report (report/project_report.pdf)
using ReportLab. Supports basic markdown features like headers, lists, tables, code blocks,
and page numbering.
"""
import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

BASE_DIR = r"d:\Data_Science_attendence_project"
MD_PATH  = os.path.join(BASE_DIR, "report", "project_report.md")
PDF_PATH = os.path.join(BASE_DIR, "report", "project_report.pdf")


class NumberedCanvas(canvas.Canvas):
    """Canvas that adds page numbers and running headers/footers dynamically."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Skip header and footer on cover page (Page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0F3C78"))
        
        # Running Header
        self.drawString(54, 750, "Student Attendance Analysis and Prediction System")
        self.setStrokeColor(colors.HexColor("#00B4D8"))
        self.setLineWidth(0.5)
        self.line(54, 742, letter[0] - 54, 742)

        # Running Footer
        self.line(54, 48, letter[0] - 54, 48)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(54, 32, "⚠ CONFIDENTIAL — For Academic Evaluation Only")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()


def parse_markdown(md_text):
    """
    Parses a subset of Markdown to ReportLab Flowables.
    Handles:
    - Headings (# , ## , ### )
    - Blockquotes (> )
    - Bullet lists (* , - , numbered)
    - Tables (|...|...|)
    - Preformatted blocks / horizontal lines
    - Plain paragraphs
    """
    styles = getSampleStyleSheet()

    # Define custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0F3C78"),
        alignment=1, # Center
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0F3C78"),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#00B4D8"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#333333"),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    quote_style = ParagraphStyle(
        'Quote',
        parent=body_style,
        leftIndent=20,
        rightIndent=20,
        fontName='Helvetica-Oblique',
        textColor=colors.HexColor("#8B0000"),
        backColor=colors.HexColor("#FFF0F0"),
        borderColor=colors.HexColor("#8B0000"),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=10
    )

    table_cell_header = ParagraphStyle(
        'TableCellHeader',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.white,
        spaceAfter=0
    )

    table_cell_body = ParagraphStyle(
        'TableCellBody',
        parent=body_style,
        spaceAfter=0
    )

    flowables = []
    lines = md_text.split('\n')
    i = 0
    in_table = False
    table_rows = []

    while i < len(lines):
        line = lines[i].rstrip()
        
        # Check for horizontal rules or blank lines
        if not line:
            if in_table:
                # Build and add the accumulated table
                flowables.append(build_table(table_rows, table_cell_header, table_cell_body))
                flowables.append(Spacer(1, 10))
                table_rows = []
                in_table = False
            else:
                flowables.append(Spacer(1, 6))
            i += 1
            continue

        if line.startswith("---"):
            if in_table:
                flowables.append(build_table(table_rows, table_cell_header, table_cell_body))
                table_rows = []
                in_table = False
            flowables.append(Spacer(1, 10))
            i += 1
            continue

        # Header 1 (Doc Title or Major Section)
        if line.startswith("# "):
            title = line[2:]
            # Check if this is the very first title for title page
            if not flowables:
                flowables.append(Spacer(1, 100))
                flowables.append(Paragraph(title, title_style))
                flowables.append(Spacer(1, 20))
            else:
                flowables.append(Paragraph(title, h1_style))
            i += 1
            continue

        # Header 2
        if line.startswith("## "):
            header = line[3:]
            # If starting major sections after cover/abstract, insert PageBreak or large spaces
            if header.startswith("1. ") or header.startswith("Table of Contents"):
                flowables.append(PageBreak())
            flowables.append(Paragraph(header, h1_style))
            i += 1
            continue

        # Header 3
        if line.startswith("### ") or line.startswith("#### "):
            prefix_len = 4 if line.startswith("### ") else 5
            header = line[prefix_len:]
            flowables.append(Paragraph(header, h2_style))
            i += 1
            continue

        # Blockquote (Synthetic notice)
        if line.startswith("> "):
            quote_lines = []
            while i < len(lines) and (lines[i].startswith("> ") or not lines[i].strip()):
                if lines[i].startswith("> "):
                    quote_lines.append(lines[i][2:])
                else:
                    quote_lines.append("")
                i += 1
            quote_text = "<br/>".join(quote_lines)
            quote_text = clean_inline_md(quote_text)
            flowables.append(Paragraph(quote_text, quote_style))
            flowables.append(Spacer(1, 6))
            continue

        # Bullet lists
        if line.startswith("- ") or line.startswith("* ") or re.match(r"^\d+\.\s+", line):
            # Parse bullet line
            match = re.match(r"^(\d+\.\s+|- |- )", line)
            prefix = match.group(0)
            bullet_char = "&bull; " if "-" in prefix or "*" in prefix else prefix
            
            bullet_lines = [bullet_char + clean_inline_md(line[len(prefix):])]
            i += 1
            
            # Check if consecutive bullet lines exist
            while i < len(lines) and (lines[i].lstrip().startswith("- ") or lines[i].lstrip().startswith("* ") or re.match(r"^\s*\d+\.\s+", lines[i])):
                sub_line = lines[i].lstrip()
                sub_match = re.match(r"^(\d+\.\s+|- |- )", sub_line)
                sub_prefix = sub_match.group(0)
                sub_bullet_char = "&bull; " if "-" in sub_prefix or "*" in sub_prefix else sub_prefix
                bullet_lines.append(sub_bullet_char + clean_inline_md(sub_line[len(sub_prefix):]))
                i += 1
            
            for b_line in bullet_lines:
                flowables.append(Paragraph(b_line, bullet_style))
            flowables.append(Spacer(1, 6))
            continue

        # Table parsing
        if line.startswith("|"):
            in_table = True
            # Check if this is the separator line |---|---|
            if "---" in line:
                i += 1
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            table_rows.append(cells)
            i += 1
            continue

        # Plain Paragraph
        if in_table:
            # We hit a non-table line, so compile and write the table first
            flowables.append(build_table(table_rows, table_cell_header, table_cell_body))
            flowables.append(Spacer(1, 10))
            table_rows = []
            in_table = False
        
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].startswith("-") and not lines[i].startswith("|") and not lines[i].startswith(">") and not lines[i].startswith("---"):
            para_lines.append(lines[i].strip())
            i += 1
        
        para_text = " ".join(para_lines)
        para_text = clean_inline_md(para_text)
        
        # Special check for Cover page metadata Table lookalikes
        if para_text.startswith("Department**") or para_text.startswith("**Department**"):
            # Cover page metadata block
            meta_style = ParagraphStyle(
                'CoverMeta',
                parent=body_style,
                fontSize=11,
                leading=16,
                alignment=1, # Center
                textColor=colors.HexColor("#333333")
            )
            flowables.append(Paragraph(para_text, meta_style))
        else:
            flowables.append(Paragraph(para_text, body_style))
            flowables.append(Spacer(1, 4))

    # Flush final table if open
    if in_table and table_rows:
        flowables.append(build_table(table_rows, table_cell_header, table_cell_body))

    return flowables


def clean_inline_md(text):
    """Replaces inline markdown tags with HTML tags for Paragraph styling."""
    # Bold: **text** or __text__
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.*?)__", r"<b>\1</b>", text)
    
    # Italic: *text*
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    
    # Code: `code`
    text = re.sub(r"`(.*?)`", r"<font face='Courier' color='#0F3C78'><b>\1</b></font>", text)
    
    # Links: [text](url) -> text
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    
    # To prevent ReportLab paraparser XML errors, escape raw '<', '>', '&' characters
    # that are not part of our allowed HTML tags: <b>, </b>, <i>, </i>, <br/>, <font ...>, </font>
    # We do this by temporary placeholders
    text = text.replace("<br/>", "___BR___")
    text = text.replace("<b>", "___B_START___").replace("</b>", "___B_END___")
    text = text.replace("<i>", "___I_START___").replace("</i>", "___I_END___")
    
    # Protect font tags using regex
    font_pattern = re.compile(r"<font\s+(.*?)>")
    font_matches = font_pattern.findall(text)
    for idx, match in enumerate(font_matches):
        text = text.replace(f"<font {match}>", f"___FONT_START_{idx}___")
    text = text.replace("</font>", "___FONT_END___")
    
    # Now escape raw &, <, >
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    
    # Restore tags
    text = text.replace("___BR___", "<br/>")
    text = text.replace("___B_START___", "<b>").replace("___B_END___", "</b>")
    text = text.replace("___I_START___", "<i>").replace("___I_END___", "</i>")
    for idx, match in enumerate(font_matches):
        text = text.replace(f"___FONT_START_{idx}___", f"<font {match}>")
    text = text.replace("___FONT_END___", "</font>")
    
    return text


def build_table(rows, header_style, body_style):
    """Builds a formatted ReportLab Table from row data."""
    if not rows:
        return Spacer(1, 1)

    table_data = []
    # Determine the number of columns
    num_cols = max(len(r) for r in rows)
    
    for r_idx, row in enumerate(rows):
        formatted_row = []
        # Pad row to match max columns
        while len(row) < num_cols:
            row.append("")
        for cell in row:
            clean_cell = clean_inline_md(cell)
            if r_idx == 0:
                formatted_row.append(Paragraph(clean_cell, header_style))
            else:
                formatted_row.append(Paragraph(clean_cell, body_style))
        table_data.append(formatted_row)

    # Simple column width allocation based on number of columns
    col_widths = [letter[0] - 108] # Available width
    if num_cols > 1:
        # Check if 1st col should be narrower or columns should be equal
        if num_cols == 2:
            col_widths = [150, letter[0] - 108 - 150]
        elif num_cols == 3:
            col_widths = [120, 100, letter[0] - 108 - 220]
        else:
            col_widths = [(letter[0] - 108) / num_cols] * num_cols

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    t_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F3C78")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#0F3C78")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]

    # Zebra striping for body rows
    for row_idx in range(1, len(rows)):
        if row_idx % 2 == 0:
            t_style.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor("#F9FBFD")))
            
    t.setStyle(TableStyle(t_style))
    return t


def main():
    if not os.path.isfile(MD_PATH):
        print(f"Error: Markdown file not found at {MD_PATH}")
        return

    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    print("Parsing project_report.md...")
    story = parse_markdown(md_text)

    print(f"Generating PDF at {PDF_PATH}...")
    # Margins: 0.75 inch (54 points) all around, except top margin is slightly larger to accommodate running header
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=54
    )

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF Generation complete!")


if __name__ == "__main__":
    main()
