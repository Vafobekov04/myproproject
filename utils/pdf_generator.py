import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors


class PDFGenerator:
    """Generate professional PDF documents for orders with complete details"""
    
    def __init__(self):
        self.documents_dir = "documents"
        if not os.path.exists(self.documents_dir):
            os.makedirs(self.documents_dir)
        
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom styles for professional formatting"""
        self.title_style = ParagraphStyle(
            'DocumentTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=6,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'DocHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#374151'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        self.normal_style = ParagraphStyle(
            'Normal',
            parent=self.styles['BodyText'],
            fontSize=10,
            leading=12,
            textColor=colors.HexColor('#111827')
        )
        
        self.small_style = ParagraphStyle(
            'Small',
            parent=self.styles['BodyText'],
            fontSize=9,
            textColor=colors.HexColor('#4b5563')
        )
    
    def _create_header(self):
        """Create professional document header"""
        story = []
        company_info = "ООО «Система продаж» | www.sales-system.ru | +7 (999) 000-00-01"
        story.append(Paragraph(company_info, self.small_style))
        story.append(Spacer(1, 0.2*cm))
        return story
    
    def _create_order_info_table(self, order_data, client_data, employee_name=""):
        """Create order and client information table"""
        table_data = [
            [
                f"<b>Заказ №</b> {order_data.get('order_id', 'N/A')}",
                f"<b>Дата:</b> {order_data.get('order_date', 'N/A')}",
                f"<b>Статус:</b> {self._translate_status(order_data.get('status', 'N/A'))}"
            ],
            [
                f"<b>Клиент:</b> {client_data.get('full_name', 'N/A')}",
                f"<b>Телефон:</b> {client_data.get('phone', 'N/A')}",
                f"<b>Email:</b> {client_data.get('email', 'N/A')}"
            ],
            [
                f"<b>Адрес:</b> {client_data.get('address', 'N/A')}",
                f"<b>Менеджер:</b> {employee_name}",
                ""
            ]
        ]
        
        table = Table(table_data, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#111827')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        return table
    
    def _create_items_table(self, order_items):
        """Create professional items table with products"""
        if not order_items:
            return Paragraph("<i>Нет товаров в заказе</i>", self.small_style)
        
        table_data = [['№', 'Товар', 'Кол-во', 'Цена', 'Сумма']]
        total = 0
        
        for idx, item in enumerate(order_items, 1):
            product_name = item.get('product_name', 'N/A')
            qty = item.get('quantity', 0)
            price = float(item.get('price', 0))
            subtotal = float(item.get('subtotal', 0))
            total += subtotal
            
            table_data.append([
                str(idx),
                product_name,
                f"{qty} шт.",
                f"{price:,.2f} ₽",
                f"{subtotal:,.2f} ₽"
            ])
        
        # Add totals row
        table_data.append(['', '', '', '<b>ИТОГО:</b>', f'<b>{total:,.2f} ₽</b>'])
        
        table = Table(table_data, colWidths=[1*cm, 7*cm, 2*cm, 2.5*cm, 2.5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, 0), 1, colors.HexColor('#2563eb')),
            ('GRID', (0, 1), (-1, -2), 0.5, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f9fafb')]),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            ('ALIGN', (3, 1), (-1, -2), 'RIGHT'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#dbeafe')),
            ('ALIGN', (0, -1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('TOPPADDING', (0, -1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
            ('GRID', (0, -1), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        
        return table
    
    def _translate_status(self, status):
        """Translate order status to Russian"""
        statuses = {
            'New': 'Новый',
            'Processing': 'В обработке',
            'Completed': 'Завершён',
            'Cancelled': 'Отменён'
        }
        return statuses.get(status, status)
    
    def generate_contract(self, order_data, client_data, order_items, employee_name=""):
        """Generate professional contract PDF"""
        filename = self._get_filename("Contract")
        filepath = os.path.join(self.documents_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
        story = []
        
        story.extend(self._create_header())
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph("КОНТРАКТ", self.title_style))
        story.append(Spacer(1, 0.3*cm))
        
        story.append(self._create_order_info_table(order_data, client_data, employee_name))
        story.append(Spacer(1, 0.4*cm))
        
        story.append(Paragraph("<b>Товары и услуги:</b>", self.heading_style))
        story.append(self._create_items_table(order_items))
        story.append(Spacer(1, 0.4*cm))
        
        story.append(Paragraph(
            "<b>Условия контракта:</b><br/>"
            "1. Продавец обязуется предоставить товары/услуги надлежащего качества.<br/>"
            "2. Покупатель обязуется произвести оплату в установленный срок.<br/>"
            "3. Контракт вступает в силу с момента подписания обеими сторонами.<br/>"
            "4. Все спорные вопросы решаются в соответствии с действующим законодательством.",
            self.normal_style
        ))
        
        story.append(Spacer(1, 0.5*cm))
        
        today = datetime.now().strftime('%d.%m.%Y')
        story.append(Paragraph(f"<b>Дата составления:</b> {today}", self.small_style))
        
        doc.build(story)
        return filepath
    
    def generate_invoice(self, order_data, client_data, order_items, employee_name=""):
        """Generate professional invoice PDF"""
        filename = self._get_filename("Invoice")
        filepath = os.path.join(self.documents_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
        story = []
        
        story.extend(self._create_header())
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph("СЧЁТ-ФАКТУРА", self.title_style))
        story.append(Spacer(1, 0.3*cm))
        
        story.append(self._create_order_info_table(order_data, client_data, employee_name))
        story.append(Spacer(1, 0.4*cm))
        
        story.append(Paragraph("<b>Перечень товаров:</b>", self.heading_style))
        story.append(self._create_items_table(order_items))
        story.append(Spacer(1, 0.3*cm))
        
        total = sum(float(item.get('subtotal', 0)) for item in order_items)
        story.append(Paragraph(
            f"<b>Сумма к оплате:</b> {total:,.2f} ₽",
            ParagraphStyle('Total', parent=self.styles['Normal'], fontSize=12, textColor=colors.HexColor('#dc2626'))
        ))
        
        story.append(Spacer(1, 0.5*cm))
        
        today = datetime.now().strftime('%d.%m.%Y')
        story.append(Paragraph(f"<b>Дата счёта:</b> {today}", self.small_style))
        
        doc.build(story)
        return filepath
    
    def generate_receipt(self, order_data, client_data, order_items, employee_name=""):
        """Generate professional receipt PDF"""
        filename = self._get_filename("Receipt")
        filepath = os.path.join(self.documents_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
        story = []
        
        story.extend(self._create_header())
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph("КВИТАНЦИЯ", self.title_style))
        story.append(Spacer(1, 0.3*cm))
        
        story.append(self._create_order_info_table(order_data, client_data, employee_name))
        story.append(Spacer(1, 0.4*cm))
        
        story.append(Paragraph("<b>Полученные товары:</b>", self.heading_style))
        story.append(self._create_items_table(order_items))
        story.append(Spacer(1, 0.3*cm))
        
        total = sum(float(item.get('subtotal', 0)) for item in order_items)
        story.append(Paragraph(
            f"<b>Сумма платежа:</b> {total:,.2f} ₽",
            ParagraphStyle('Total', parent=self.styles['Normal'], fontSize=12, textColor=colors.HexColor('#059669'))
        ))
        
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(
            "Настоящей квитанцией подтверждается получение вышеуказанных товаров в полном объёме.",
            self.small_style
        ))
        
        today = datetime.now().strftime('%d.%m.%Y')
        story.append(Paragraph(f"<b>Дата получения:</b> {today}", self.small_style))
        
        doc.build(story)
        return filepath
    
    def generate_act(self, order_data, client_data, order_items, employee_name=""):
        """Generate professional act of completion PDF"""
        filename = self._get_filename("Act")
        filepath = os.path.join(self.documents_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
        story = []
        
        story.extend(self._create_header())
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph("АКТ ВЫПОЛНЕННЫХ РАБОТ", self.title_style))
        story.append(Spacer(1, 0.3*cm))
        
        story.append(self._create_order_info_table(order_data, client_data, employee_name))
        story.append(Spacer(1, 0.4*cm))
        
        story.append(Paragraph("<b>Выполненные работы/поставленные товары:</b>", self.heading_style))
        story.append(self._create_items_table(order_items))
        story.append(Spacer(1, 0.3*cm))
        
        total = sum(float(item.get('subtotal', 0)) for item in order_items)
        story.append(Paragraph(
            f"<b>Стоимость работ:</b> {total:,.2f} ₽",
            ParagraphStyle('Total', parent=self.styles['Normal'], fontSize=12, textColor=colors.HexColor('#0891b2'))
        ))
        
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(
            "<b>Акт составлен:</b><br/>"
            "Настоящим актом подтверждается, что работы (услуги) выполнены в полном объёме "
            "и надлежащего качества. Обе стороны согласны с содержанием настоящего акта.",
            self.small_style
        ))
        
        today = datetime.now().strftime('%d.%m.%Y')
        story.append(Paragraph(f"<b>Дата составления:</b> {today}", self.small_style))
        
        doc.build(story)
        return filepath
    
    def generate_check(self, order_data, client_data, order_items, employee_name=""):
        """Generate professional check PDF"""
        filename = self._get_filename("Check")
        filepath = os.path.join(self.documents_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
        story = []
        
        story.extend(self._create_header())
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph("ЧЕК", self.title_style))
        story.append(Spacer(1, 0.3*cm))
        
        story.append(self._create_order_info_table(order_data, client_data, employee_name))
        story.append(Spacer(1, 0.4*cm))
        
        story.append(Paragraph("<b>Покупка:</b>", self.heading_style))
        story.append(self._create_items_table(order_items))
        story.append(Spacer(1, 0.3*cm))
        
        total = sum(float(item.get('subtotal', 0)) for item in order_items)
        story.append(Paragraph(
            f"<b>ИТОГО К ОПЛАТЕ:</b> {total:,.2f} ₽",
            ParagraphStyle('Total', parent=self.styles['Normal'], fontSize=12, textColor=colors.HexColor('#7c3aed'))
        ))
        
        now = datetime.now().strftime('%d.%m.%Y %H:%M')
        story.append(Paragraph(f"<b>Дата и время:</b> {now}", self.small_style))
        
        doc.build(story)
        return filepath
    
    def generate_pdf(self, document_type, order_data, client_data, order_items, employee_name=""):
        """Generate PDF based on document type"""
        generators = {
            'Contract': self.generate_contract,
            'Invoice': self.generate_invoice,
            'Receipt': self.generate_receipt,
            'Act': self.generate_act,
            'Check': self.generate_check,
        }
        
        generator = generators.get(document_type)
        if not generator:
            raise ValueError(f"Unknown document type: {document_type}")
        
        return generator(order_data, client_data, order_items, employee_name)
    
    def _get_filename(self, doc_type):
        """Generate unique filename for PDF"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{doc_type}_{timestamp}.pdf"
