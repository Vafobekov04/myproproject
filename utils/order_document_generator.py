import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class OrderDocumentGenerator:
    """Generate professional order documents with complete information"""

    def __init__(self):
        self.documents_dir = "documents"
        if not os.path.exists(self.documents_dir):
            os.makedirs(self.documents_dir)

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.font_name = "Helvetica"
        self.bold_font_name = "Helvetica-Bold"

        self._setup_fonts()

        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_fonts(self):
        """Try to load Cyrillic fonts from project fonts folder or system fonts"""
        candidates = [
            (
                os.path.join(self.base_dir, "fonts", "DejaVuSans.ttf"),
                os.path.join(self.base_dir, "fonts", "DejaVuSans-Bold.ttf"),
                "DejaVuSans",
                "DejaVuSans-Bold",
            ),
            (
                os.path.join(self.base_dir, "fonts", "Arial.ttf"),
                os.path.join(self.base_dir, "fonts", "Arial Bold.ttf"),
                "Arial",
                "Arial-Bold",
            ),
            (
                r"C:\Windows\Fonts\DejaVuSans.ttf",
                r"C:\Windows\Fonts\DejaVuSans-Bold.ttf",
                "DejaVuSans",
                "DejaVuSans-Bold",
            ),
            (
                r"C:\Windows\Fonts\arial.ttf",
                r"C:\Windows\Fonts\arialbd.ttf",
                "Arial",
                "Arial-Bold",
            ),
        ]

        for regular_path, bold_path, regular_name, bold_name in candidates:
            try:
                if os.path.exists(regular_path):
                    pdfmetrics.registerFont(TTFont(regular_name, regular_path))
                    self.font_name = regular_name
                if os.path.exists(bold_path):
                    pdfmetrics.registerFont(TTFont(bold_name, bold_path))
                    self.bold_font_name = bold_name
                if os.path.exists(regular_path) or os.path.exists(bold_path):
                    return
            except Exception:
                continue

    def _setup_styles(self):
        """Setup professional document styles"""
        self.header_style = ParagraphStyle(
            "Header",
            parent=self.styles["Heading1"],
            fontSize=16,
            textColor=colors.HexColor("#1f2937"),
            spaceAfter=4,
            fontName=self.bold_font_name,
        )

        self.title_style = ParagraphStyle(
            "DocumentTitle",
            parent=self.styles["Heading2"],
            fontSize=24,
            textColor=colors.HexColor("#1a202c"),
            spaceAfter=12,
            alignment=1,
            fontName=self.bold_font_name,
        )

        self.section_title = ParagraphStyle(
            "SectionTitle",
            parent=self.styles["Heading2"],
            fontSize=12,
            textColor=colors.white,
            spaceAfter=8,
            fontName=self.bold_font_name,
        )

        self.normal = ParagraphStyle(
            "Normal",
            parent=self.styles["BodyText"],
            fontSize=10,
            leading=12,
            textColor=colors.HexColor("#2d3748"),
            fontName=self.font_name,
        )

        self.small = ParagraphStyle(
            "Small",
            parent=self.styles["BodyText"],
            fontSize=9,
            leading=11,
            textColor=colors.HexColor("#4a5568"),
            fontName=self.font_name,
        )

    def _p(self, text, style=None):
        return Paragraph(str(text).replace("\n", "<br/>"), style or self.normal)

    def _create_company_header(
        self,
        company_name="ООО 'Система продаж'",
        phone="+7 (999) 000-00-01",
        email="info@sales-system.ru",
        website="www.sales-system.ru",
        logo_text="[место для логотипа]",
        document_number=None,
    ):
        story = []
        document_number = document_number or datetime.now().strftime("%Y-%m-%d-%H%M%S")

        header_data = [
            [
                self._p(
                    f"<b>{company_name}</b><br/>"
                    f"{logo_text}<br/>"
                    f"<font size=9>Телефон: {phone}</font><br/>"
                    f"<font size=9>Email: {email}</font><br/>"
                    f"<font size=9>Сайт: {website}</font>",
                    self.normal,
                ),
                self._p(
                    f"<b>ДОКУМЕНТ № {document_number}</b><br/>"
                    f"<font size=9>Дата: {datetime.now().strftime('%d.%m.%Y')}</font><br/>"
                    f"<font size=9>Время: {datetime.now().strftime('%H:%M')}</font>",
                    self.normal,
                ),
            ]
        ]

        header_table = Table(header_data, colWidths=[8 * cm, 8 * cm])
        header_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (0, 0), "LEFT"),
                    ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (-1, -1), self.font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#2d3748")),
                    ("GRID", (0, 0), (-1, -1), 0, colors.white),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        story.append(header_table)
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph("_" * 100, self.small))
        story.append(Spacer(1, 0.3 * cm))
        return story

    def _create_document_title(self):
        return [Paragraph("ЗАКАЗ КЛИЕНТА", self.title_style), Spacer(1, 0.5 * cm)]

    def _create_section_header(self, title):
        section_table = Table([[self._p(title, self.section_title)]], colWidths=[16 * cm])
        section_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#2d3748")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTNAME", (0, 0), (-1, -1), self.bold_font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return [section_table, Spacer(1, 0.2 * cm)]

    def _create_client_info_section(self, client_data):
        story = self._create_section_header("ИНФОРМАЦИЯ О КЛИЕНТЕ")

        data = [
            [self._p("Код клиента:", self.normal), self._p(client_data.get("client_id", "N/A"))],
            [self._p("Наименование:", self.normal), self._p(client_data.get("full_name", "N/A"))],
            [self._p("Телефон:", self.normal), self._p(client_data.get("phone", "N/A"))],
            [self._p("Email:", self.normal), self._p(client_data.get("email", "N/A"))],
            [self._p("Адрес:", self.normal), self._p(client_data.get("address", "N/A"))],
        ]

        table = Table(data, colWidths=[4 * cm, 12 * cm])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7fafc")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                    ("FONTNAME", (0, 0), (-1, -1), self.font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 0.5 * cm))
        return story

    def _create_order_info_section(self, order_data, employee_name=""):
        story = self._create_section_header("ИНФОРМАЦИЯ О ЗАКАЗЕ")

        order_id = order_data.get("order_id", "N/A")
        order_date = order_data.get("order_date", "N/A")
        status = self._translate_status(order_data.get("status", "N/A"))

        data = [
            [self._p("Номер заказа:", self.normal), self._p(order_id), self._p("Дата создания:", self.normal), self._p(order_date)],
            [self._p("Статус:", self.normal), self._p(status), self._p("Менеджер:", self.normal), self._p(employee_name or "N/A")],
        ]

        table = Table(data, colWidths=[3.5 * cm, 5.5 * cm, 3.5 * cm, 5.5 * cm])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7fafc")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                    ("FONTNAME", (0, 0), (-1, -1), self.font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 0.5 * cm))
        return story

    def _create_order_items_section(self, order_items):
        story = self._create_section_header("СОСТАВ ЗАКАЗА")

        if not order_items:
            story.append(Paragraph("Нет товаров в заказе", self.normal))
            story.append(Spacer(1, 0.5 * cm))
            return story

        data = [[
            self._p("№", self.small),
            self._p("Наименование товара", self.small),
            self._p("Категория", self.small),
            self._p("Кол-во", self.small),
            self._p("Цена", self.small),
            self._p("Сумма", self.small),
        ]]

        for idx, item in enumerate(order_items, 1):
            data.append([
                self._p(idx),
                self._p(item.get("product_name", "N/A")),
                self._p(item.get("category_name", "N/A")),
                self._p(f"{item.get('quantity', 0)} шт."),
                self._p(f"{float(item.get('price', 0)):.2f} ₽"),
                self._p(f"{float(item.get('subtotal', 0)):.2f} ₽"),
            ])

        table = Table(data, colWidths=[0.8 * cm, 5.5 * cm, 3 * cm, 1.8 * cm, 2.4 * cm, 2.5 * cm], repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d3748")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), self.bold_font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (0, -1), "CENTER"),
                    ("ALIGN", (3, 1), (-1, -1), "RIGHT"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 0.5 * cm))
        return story

    def _create_financial_section(self, total_amount, discount=0):
        story = self._create_section_header("ФИНАНСОВАЯ ИНФОРМАЦИЯ")

        discount_amount = (total_amount * discount / 100) if discount > 0 else 0
        final_amount = total_amount - discount_amount

        data = [
            [self._p("Общая стоимость товаров:", self.normal), self._p(f"{total_amount:,.2f} ₽")],
            [self._p(f"Размер скидки ({discount}%):", self.normal), self._p(f"- {discount_amount:,.2f} ₽")],
            [self._p("ИТОГОВАЯ СУММА К ОПЛАТЕ:", self.normal), self._p(f"{final_amount:,.2f} ₽", self.header_style)],
        ]

        table = Table(data, colWidths=[10 * cm, 6 * cm])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -2), colors.HexColor("#f7fafc")),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#dbeafe")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (-1, -1), self.font_name),
                    ("FONTNAME", (0, -1), (-1, -1), self.bold_font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("TEXTCOLOR", (0, -1), (-1, -1), colors.HexColor("#1e40af")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 0.5 * cm))
        return story

    def _create_payment_section(self, payment_method="Не указано", payment_date=None, payment_status="Ожидает оплаты"):
        story = self._create_section_header("ИНФОРМАЦИЯ ОБ ОПЛАТЕ")

        data = [
            [self._p("Способ оплаты:", self.normal), self._p(payment_method), self._p("Статус оплаты:", self.normal), self._p(payment_status)],
            [self._p("Дата оплаты:", self.normal), self._p(payment_date or "Не оплачено"), self._p("", self.normal), self._p("", self.normal)],
        ]

        table = Table(data, colWidths=[3.5 * cm, 5.5 * cm, 3.5 * cm, 5.5 * cm])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7fafc")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                    ("FONTNAME", (0, 0), (-1, -1), self.font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 0.5 * cm))
        return story

    def _create_delivery_section(self, delivery_method="Не указано", delivery_address="", delivery_date=""):
        story = self._create_section_header("ИНФОРМАЦИЯ О ДОСТАВКЕ")

        data = [
            [self._p("Способ доставки:", self.normal), self._p(delivery_method)],
            [self._p("Адрес доставки:", self.normal), self._p(delivery_address or "Не указан")],
            [self._p("Дата доставки:", self.normal), self._p(delivery_date or "Не указана")],
        ]

        table = Table(data, colWidths=[4 * cm, 12 * cm])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7fafc")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                    ("FONTNAME", (0, 0), (-1, -1), self.font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 0.5 * cm))
        return story

    def _create_notes_section(self, notes=""):
        story = self._create_section_header("ПРИМЕЧАНИЯ")
        story.append(Paragraph(notes or "Дополнительные комментарии отсутствуют", self.normal))
        story.append(Spacer(1, 0.5 * cm))
        return story

    def _create_signature_section(self):
        story = self._create_section_header("ПОДПИСИ СТОРОН")

        data = [
            [
                self._p("<b>Менеджер:</b><br/><br/>______________________", self.normal),
                self._p("<b>Клиент:</b><br/><br/>______________________", self.normal),
            ],
            [
                self._p("Подпись и расшифровка", self.small),
                self._p("Подпись и расшифровка", self.small),
            ],
        ]

        table = Table(data, colWidths=[8 * cm, 8 * cm])
        table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
                    ("FONTNAME", (0, 0), (-1, -1), self.font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 0.5 * cm))
        story.append(Paragraph(f"<b>Дата подписания:</b> {datetime.now().strftime('%d.%m.%Y')}", self.normal))
        return story

    def _translate_status(self, status):
        statuses = {
            "New": "Новый",
            "Processing": "В обработке",
            "Completed": "Завершён",
            "Cancelled": "Отменён",
        }
        return statuses.get(status, status)

    def generate_order_document(
        self,
        order_data,
        client_data,
        order_items,
        employee_name="",
        payment_info=None,
        delivery_info=None,
        notes="",
        organization_info=None,
    ):
        filename = self._get_filename("Order")
        filepath = os.path.join(self.documents_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            topMargin=1 * cm,
            bottomMargin=1 * cm,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
        )

        organization_info = organization_info or {}

        story = []
        story.extend(
            self._create_company_header(
                company_name=organization_info.get("company_name", "ООО 'Система продаж'"),
                phone=organization_info.get("phone", "+7 (999) 000-00-01"),
                email=organization_info.get("email", "info@sales-system.ru"),
                website=organization_info.get("website", "www.sales-system.ru"),
                logo_text=organization_info.get("logo_text", "[место для логотипа]"),
                document_number=organization_info.get("document_number"),
            )
        )
        story.extend(self._create_document_title())
        story.extend(self._create_client_info_section(client_data))
        story.extend(self._create_order_info_section(order_data, employee_name))
        story.extend(self._create_order_items_section(order_items))

        total = sum(float(item.get("subtotal", 0)) for item in order_items)
        discount = organization_info.get("discount", 0)
        story.extend(self._create_financial_section(total, discount))

        if payment_info:
            story.extend(
                self._create_payment_section(
                    payment_info.get("method", "Не указано"),
                    payment_info.get("date"),
                    payment_info.get("status", "Ожидает оплаты"),
                )
            )

        if delivery_info:
            story.extend(
                self._create_delivery_section(
                    delivery_info.get("method", "Не указано"),
                    delivery_info.get("address"),
                    delivery_info.get("date"),
                )
            )

        story.extend(self._create_notes_section(notes))
        story.extend(self._create_signature_section())

        doc.build(story)
        return filepath

    def _get_filename(self, doc_type):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{doc_type}_{timestamp}.pdf"