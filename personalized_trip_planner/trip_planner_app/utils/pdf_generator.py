from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import re

# --- Clean display name (no "(Map)" or anything)
def process_text_for_pdf_links(text_segment, destination_city=""):
    pattern = re.compile(r'\[([^\]]+?)\s*\(?([A-Za-z\s,-]*?)?\)?\]')
    def replace_with_display_name_only(match):
        place_name_raw = match.group(1).strip()
        display_place_name = re.sub(r'\*\*(.*?)\*\*', r'\1', place_name_raw)
        display_place_name = re.sub(r'\*(.*?)\*', r'\1', display_place_name)
        display_place_name = re.sub(r'[^a-zA-Z0-9\s.,\-]', '', display_place_name).strip()
        return f'{display_place_name}'
    return pattern.sub(replace_with_display_name_only, text_segment)

def clean_for_reportlab_paragraph(text_input):
    text = str(text_input)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\x20-\x7E]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace('<br/>', '\n')
    return text.strip()

def generate_itinerary_pdf(itinerary_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(name='MainTitle', alignment=TA_CENTER, fontSize=24, leading=28, spaceAfter=20, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='SectionHeading', alignment=TA_LEFT, fontSize=16, leading=18, spaceBefore=20, spaceAfter=10, fontName='Helvetica-Bold', textColor='#34495e'))
    styles.add(ParagraphStyle(name='DayHeading', alignment=TA_LEFT, fontSize=14, leading=16, spaceBefore=15, spaceAfter=5, fontName='Helvetica-Bold', textColor='#0056b3'))
    styles.add(ParagraphStyle(name='SubSectionItemHeading', alignment=TA_LEFT, fontSize=12, leading=14, spaceBefore=8, spaceAfter=3, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NormalText', alignment=TA_LEFT, fontSize=11, leading=13, spaceAfter=2))
    styles.add(ParagraphStyle(name='BulletStyle', parent=styles['NormalText'], leftIndent=0.3 * inch, firstLineIndent=-0.15 * inch, bulletIndent=0.0 * inch, spaceAfter=2, bulletFontName='Helvetica', bulletFontSize=10))
    styles.add(ParagraphStyle(name='TipStyle', parent=styles['NormalText'], alignment=TA_LEFT, fontSize=10, leading=12, spaceBefore=10, spaceAfter=10, backColor='#fff3cd', borderPadding=5, borderColor='#ffeeba', borderWidth=1, borderRadius=5))

    elements = []

    # Title
    elements.append(Paragraph("Personalized Trip Itinerary", styles['MainTitle']))

    # Disclaimer
    elements.append(Paragraph(
        "This itinerary is generated using AI and serves as a suggestion. "
        "Prices are estimates and may vary. Please verify all details before booking.",
        styles['Italic']
    ))
    elements.append(Spacer(1, 0.2 * inch))

    # --- Trip Overview Section ---
    elements.append(Paragraph("Trip Overview", styles['SectionHeading']))

    trip_facts = []
    trip_facts.append(f"• Destination: {itinerary_data.get('destination', 'N/A')}")
    trip_facts.append(f"• Starting Point: {itinerary_data.get('starting_point', 'N/A')}")
    trip_facts.append(f"• Duration: {itinerary_data.get('trip_duration_days', 'N/A')} days")
    trip_facts.append(f"• Budget: ₹{itinerary_data.get('budget', 0.00)}")

    if itinerary_data.get('interests'):
        trip_facts.append("• Interests: " + ", ".join(itinerary_data['interests']))
    if itinerary_data.get('travel_mode_preference'):
        trip_facts.append("• Travel Modes: " + ", ".join(itinerary_data['travel_mode_preference']))
    if itinerary_data.get('accommodation_preference'):
        trip_facts.append("• Accommodation: " + ", ".join(itinerary_data['accommodation_preference']))
    if itinerary_data.get('food_preference'):
        trip_facts.append("• Food Preferences: " + ", ".join(itinerary_data['food_preference']))

    for fact in trip_facts:
        elements.append(Paragraph(fact, styles['BulletStyle']))

    elements.append(Spacer(1, 0.3 * inch))

    # --- Daily Plan Section ---
    elements.append(Paragraph("Daily Plan", styles['SectionHeading']))
    itinerary_content_raw = itinerary_data.get('itinerary_content', 'No itinerary generated.')
    destination_city = itinerary_data.get('destination', '').split(',')[0].strip()
    lines = itinerary_content_raw.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue
        original_line = line
        line = process_text_for_pdf_links(line, destination_city)
        line = clean_for_reportlab_paragraph(line)

        if original_line.startswith('**Day'):
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(Paragraph(line, styles['DayHeading']))
        elif re.match(r'\* \*\*(.*?)\*\*:', original_line):
            match = re.match(r'\* \*\*(.*?)\*\*:(.*)', original_line)
            if match:
                title = match.group(1).strip()
                body = process_text_for_pdf_links(match.group(2).strip(), destination_city)
                body = clean_for_reportlab_paragraph(body)
                elements.append(Paragraph(f'{title}: {body}', styles['SubSectionItemHeading']))
        elif original_line.startswith('*'):
            bullet = line.lstrip('*').strip()
            elements.append(Paragraph(f'• {bullet}', styles['BulletStyle']))
        elif '**Note:**' in original_line or '**Tip:**' in original_line or '**Important Tip:**' in original_line:
            tip_clean = clean_for_reportlab_paragraph(process_text_for_pdf_links(original_line, destination_city))
            elements.append(Paragraph(tip_clean, styles['TipStyle']))
        else:
            elements.append(Paragraph(line, styles['NormalText']))

    # --- Budget Section ---
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("Budget Summary (Estimate)", styles['SectionHeading']))

    budget_section_started = False
    for line in lines:
        if '**Budget Summary' in line:
            budget_section_started = True
            continue
        if not budget_section_started:
            continue

        line = process_text_for_pdf_links(line.strip(), destination_city)
        line = clean_for_reportlab_paragraph(line)

        if not line:
            continue
        elif line.startswith('*'):
            bullet = line.lstrip('*').strip()
            elements.append(Paragraph(f'• {bullet}', styles['BulletStyle']))
        elif line.startswith('**Total:'):
            total = line.replace('**', '').strip()
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(Paragraph(f'<b>{total}</b>', styles['NormalText']))
        elif 'Tip' in line or 'Note' in line:
            elements.append(Paragraph(line, styles['TipStyle']))
        else:
            elements.append(Paragraph(line, styles['NormalText']))

    # --- Footer ---
    elements.append(Spacer(1, 0.4 * inch))
    elements.append(Paragraph("Generated by Personalized Trip Planner using AI.", styles['Italic']))

    doc.build(elements)
    buffer.seek(0)
    return buffer
