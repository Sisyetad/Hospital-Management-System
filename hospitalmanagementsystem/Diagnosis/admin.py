from django.contrib import admin
from django.urls import path, reverse
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils.html import format_html
from django.conf import settings
from pathlib import Path
from threading import Timer

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from .models import DiagnosisModel


@admin.register(DiagnosisModel)
class DiagnosisAdmin(admin.ModelAdmin):
    exclude = ['medication', 'diagnosis_name', 'related_symptomes', 'clinical_notes']
    readonly_fields = ('history_tools',)

    def history_tools(self, obj):
        if not obj or not obj.pk:
            return "Save and continue editing to view history PDF."

        preview_url = reverse('admin:diagnosis_history_preview', args=[obj.pk])
        download_url = reverse('admin:diagnosis_history_pdf', args=[obj.pk]) + '?download=1'
        return format_html(
            '<a class="button" href="{}">View History PDF</a>\n'
            '<a class="button" href="{}">Download PDF</a>',
            preview_url,
            download_url,
        )
    history_tools.short_description = "Diagnosis History"

    def get_readonly_fields(self, request, obj=None):
        # Hide the history widget on add form to avoid reverse errors
        if not obj:
            return tuple(f for f in self.readonly_fields if f != 'history_tools')
        return self.readonly_fields

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:diagnosis_id>/history/preview/',
                 self.admin_site.admin_view(self.history_preview_view),
                 name='diagnosis_history_preview'),
            path('<int:diagnosis_id>/history/pdf/',
                 self.admin_site.admin_view(self.history_pdf_view),
                 name='diagnosis_history_pdf'),
        ]
        return custom_urls + urls

    def history_preview_view(self, request, diagnosis_id: int):
        if not request.user.is_staff:
            return HttpResponseForbidden("Staff access required")

        obj = get_object_or_404(DiagnosisModel, pk=diagnosis_id)
        pdf_url = reverse('admin:diagnosis_history_pdf', args=[obj.pk])
        download_url = pdf_url + '?download=1'
        back_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.pk])

        overview = {
            'Diagnosis ID': obj.pk,
            'Diagnosis Name': getattr(obj, 'diagnosis_name', None) or '-',
            'Severity Level': getattr(obj, 'severity_level', None),
            'Status': getattr(obj, 'diagnosis_status', None),
            'Visibility': 'Visible' if getattr(obj, 'visibility', False) else 'Hidden',
            'Patient': str(getattr(obj, 'patient', '-')),
            'Doctor': str(getattr(obj, 'doctor', '-')) if getattr(obj, 'doctor', None) else '-',
            'Branch': str(getattr(obj, 'branch', '-')) if getattr(obj, 'branch', None) else '-',
            'Created': getattr(obj, 'created_at', None),
            'Updated': getattr(obj, 'updated_at', None),
        }

        return render(request, 'admin/diagnosis_history_preview.html', {
            'title': f'Diagnosis History #{obj.pk}',
            'overview': overview,
            'pdf_url': pdf_url,
            'download_url': download_url,
            'back_url': back_url,
        })

    def history_pdf_view(self, request, diagnosis_id: int):
        if not request.user.is_staff:
            return HttpResponseForbidden("Staff access required")

        obj = get_object_or_404(DiagnosisModel, pk=diagnosis_id)
        history_queryset = obj.history.all().order_by('-history_date')

        if not history_queryset.exists():
            # Return an empty PDF with a message
            pdf_path = self._build_empty_pdf(diagnosis_id)
        else:
            pdf_path = self._build_history_pdf(history_queryset, diagnosis_id)

        inline = request.GET.get('download') != '1'
        response = FileResponse(pdf_path.open('rb'), content_type='application/pdf')
        disposition = 'inline' if inline else 'attachment'
        response['Content-Disposition'] = f'{disposition}; filename=diagnosis_{diagnosis_id}_history.pdf'
        return response

    def _pdf_target_path(self, diagnosis_id: int) -> Path:
        media_root = Path(getattr(settings, 'MEDIA_ROOT') or (settings.BASE_DIR / 'media'))
        target_dir = media_root / 'diagnosis_history'
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir / f'diagnosis_{diagnosis_id}_history.pdf'

    def _build_history_pdf(self, history_queryset, diagnosis_id: int) -> Path:
        pdf_path = self._pdf_target_path(diagnosis_id)
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        elements = [
            Paragraph(f"Diagnosis History #{diagnosis_id}", styles['Title']),
            Spacer(1, 12),
            Paragraph("Most recent first", styles['Normal']),
            Spacer(1, 12)
        ]

        # Render each history record as a readable card
        for record in history_queryset:
            header_text = f"{record.history_date.strftime('%Y-%m-%d %H:%M')} — {record.get_history_type_display()}"
            elements.append(Paragraph(header_text, styles['Heading3']))

            meta_rows = [
                ['Severity', str(record.severity_level)],
                ['Status', str(record.diagnosis_status)],
                ['Visibility', 'Visible' if record.visibility else 'Hidden'],
                ['Modified By', str(record.history_user) if record.history_user else '-'],
                ['Reason', record.history_change_reason or '-'],
            ]

            meta_table = Table(meta_rows, colWidths=[100, None])
            meta_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            elements.append(meta_table)
            elements.append(Spacer(1, 8))

            long_rows = [
                ['Diagnosis Name', Paragraph(record.diagnosis_name or '-', styles['BodyText'])],
                ['Symptoms', Paragraph(record.related_symptomes or '-', styles['BodyText'])],
                ['Clinical Notes', Paragraph(record.clinical_notes or '-', styles['BodyText'])],
                ['Medication', Paragraph(record.medication or '-', styles['BodyText'])],
            ]

            content_table = Table(long_rows, colWidths=[120, None])
            content_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ]))
            elements.append(content_table)
            elements.append(Spacer(1, 18))

        doc.build(elements)

        self._schedule_pdf_cleanup(pdf_path)
        return pdf_path

    def _build_empty_pdf(self, diagnosis_id: int) -> Path:
        pdf_path = self._pdf_target_path(diagnosis_id)
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
        elements = [Paragraph("No history records available.", styles['Title'])]
        doc.build(elements)
        self._schedule_pdf_cleanup(pdf_path)
        return pdf_path

    def _schedule_pdf_cleanup(self, pdf_path: Path, ttl_seconds: int = 300):
        def _cleanup():
            try:
                pdf_path.unlink(missing_ok=True)
            except Exception:
                pass

        timer = Timer(ttl_seconds, _cleanup)
        timer.daemon = True
        timer.start()
