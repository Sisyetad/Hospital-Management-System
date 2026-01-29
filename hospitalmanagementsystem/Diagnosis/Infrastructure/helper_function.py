from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from pathlib import Path


def build_history_pdf(history_queryset, pdf_path: Path, diagnosis_id: int):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)

    elements = [
        Paragraph(f"Diagnosis History #{diagnosis_id}", styles['Title']),
        Spacer(1, 12),
        Paragraph("Most recent first", styles['Normal']),
        Spacer(1, 12)
    ]

    table_data = [[
        "Date",
        "Change",
        "Severity",
        "Status",
        "Visibility",
        "Modified By",
        "Reason"
    ]]

    for record in history_queryset:
        table_data.append([
            record.history_date.strftime('%Y-%m-%d %H:%M'),
            record.get_history_type_display(),
            str(record.severity_level),
            str(record.diagnosis_status),
            "Visible" if record.visibility else "Hidden",
            str(record.history_user) if record.history_user else "-",
            record.history_change_reason or "-",
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ]))

    elements.append(table)
    doc.build(elements)
