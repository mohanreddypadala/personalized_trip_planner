from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import blue # For link color
import re
import urllib.parse 

# --- Helper function to process AI-generated text and create ReportLab-compatible links ---
def process_text_for_pdf_links(text_segment, destination_city=""):
    """
    Converts [Place (City)] patterns into clickable ReportLab <link> tags, 
    with nested <font color="blue"> tags for visual distinction.
    """
    pattern = re.compile(r'\[([^\]]+?)\s*\(?([A-Za-z\s,-]*?)?\)?\]')

    def replace_with_pdf_link_markup(match):
        place_name_raw = match.group(1).strip()
        city = match.group(2).strip() if match.group(2) else destination_city
        city_for_url = city.split(',')[0].strip() if city else ""

        maps_query = urllib.parse.quote_plus(f"{place_name_raw}, {city_for_url}")
        maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}" 

        # Clean place name for display, removing internal markdown
        display_place_name = re.sub(r'\*\*(.*?)\*\*', r'\1', place_name_raw)
        display_place_name = re.sub(r'\*(.*?)\*', r'\1', display_place_name)
        
        # ReportLab <link> tag for the MAP (Primary Link)
        link_text_with_color = f'<font color="blue">{display_place_name}</font>'
        link_markup = f'<link href="{maps_url}">{link_text_with_color}</link>'
        
        if "hotel" in place_name_raw.lower() or "resort" in place_name_raw.lower() or "guesthouse" in place_name_raw.lower() or "stay" in place_name_raw.lower() or "inn" in place_name_raw.lower():
            booking_query = urllib.parse.quote_plus(f"{place_name_raw} {city_for_url} hotel booking")
            booking_url = f"https://www.google.com/search?q={booking_query}"
            
            # Using <font size="8"> and explicit color for the secondary link.
            book_link_tag = f'<link href="{booking_url}"><font color="blue">Book</font></link>'
            # Return the primary link, plus the secondary booking link text.
            return (f'{link_markup} <font size="8">( {book_link_tag} )</font>')
        else:
            return link_markup
    
    processed_text_segment = pattern.sub(replace_with_pdf_link_markup, text_segment)
    return processed_text_segment


# --- Helper to clean string for ReportLab Paragraph (strips non-RML tags) ---
def clean_plain_text_for_paragraph(text_input):
    text = str(text_input)

    # 1. Clean non-ASCII characters and escape ampersands.
    text = re.sub(r'[^\x20-\x7E]', '', text) 
    text = text.replace('&', '&') 

    # 2. Convert markdown bold/italic to RML (Must happen before tag stripping)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text) # Markdown bold
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)    # Markdown italic

    # 3. Aggressively strip ALL HTML tags NOT EXPLICITLY ALLOWED
    allowed_tags = ['b', 'i', 'font', 'link', 'br']
    
    def filter_unallowed_tags(match):
        tag_content = match.group(0) 
        tag_name_match = re.match(r'</?([a-z]+)\b[^>]*>', tag_content, re.IGNORECASE)
        if tag_name_match and tag_name_match.group(1).lower() in allowed_tags:
            return tag_content # Keep the tag if it's allowed
        else:
            return '' # Remove unallowed tag

    text = re.sub(r'<[^>]+>', filter_unallowed_tags, text, flags=re.IGNORECASE)


    # 4. Final cleanup for malformed tags (Crucial for closing tags)
    text = text.replace('</b>>', '</b>')
    text = text.replace('</i>>', '</i>')
    text = text.replace('</link>>', '</link>')
    text = re.sub(r'<br\s*/?>', '<br/>', text)

    # 5. Normalize whitespace and line breaks
    text = text.replace('\n', '<br/>')
    text = re.sub(r'\s*<br/>\s*', '<br/>', text)
    text = re.sub(r'\s*<b>\s*', '<b>', text)
    text = re.sub(r'\s*</b>\s*', '</b>', text)
    text = text.replace('* ', '• ') # Convert markdown list stars to bullets

    return text.strip() 


# ===========================================================================
# MAIN PDF GENERATION FUNCTION
# ===========================================================================

def generate_itinerary_pdf(structured_itinerary_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define custom styles
    styles.add(ParagraphStyle(name='MainTitle', parent=styles['h1'], alignment=TA_CENTER, fontSize=24, leading=28, spaceAfter=20, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='SectionHeading', parent=styles['h2'], alignment=TA_LEFT, fontSize=16, leading=18, spaceBefore=20, spaceAfter=10, fontName='Helvetica-Bold', textColor='#34495e'))
    styles.add(ParagraphStyle(name='DayHeading', parent=styles['h3'], alignment=TA_LEFT, fontSize=14, leading=16, spaceBefore=15, spaceAfter=5, fontName='Helvetica-Bold', textColor='#0056b3'))
    styles.add(ParagraphStyle(name='SubSectionItemHeading', parent=styles['Normal'], alignment=TA_LEFT, fontSize=12, leading=14, spaceBefore=8, spaceAfter=3, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NormalText', parent=styles['Normal'], alignment=TA_LEFT, fontSize=11, leading=13, spaceAfter=2))
    styles.add(ParagraphStyle(name='BulletStyle', parent=styles['NormalText'], leftIndent=0.3 * inch, firstLineIndent=-0.15 * inch, bulletIndent=0.0 * inch, spaceAfter=2, bulletFontName='Helvetica', bulletFontSize=10,))
    styles.add(ParagraphStyle(name='TipStyle', parent=styles['NormalText'], alignment=TA_LEFT, fontSize=10, leading=12, spaceBefore=10, spaceAfter=10, backColor='#fff3cd', borderPadding=5, borderColor='#ffeeba', borderWidth=1, borderRadius=5))


    elements = []

    # --- Project Info / Disclaimer at the Top ---
    elements.append(Paragraph("Personalized Trip Itinerary", styles['MainTitle']))

    # Disclaimer - content is now directly from the input data, cleaned.
    disclaimer_text = "This itinerary is generated using AI and serves as a suggestion. Prices are estimates and may vary. Please verify all details before booking."
    elements.append(Paragraph(disclaimer_text, styles['Italic']))
    elements.append(Spacer(1, 0.2 * inch))

    # --- Trip Overview Section (FIXED: Accessing top-level keys correctly) ---
    elements.append(Paragraph("<b>Trip Overview</b>", styles['SectionHeading']))

    # *** FIX IS HERE: Accessing the injected top-level keys ***
    elements.append(Paragraph(f"• Destination: {structured_itinerary_data.get('destination', 'N/A')}", styles['BulletStyle']))
    elements.append(Paragraph(f"• Starting Point: {structured_itinerary_data.get('starting_point', 'N/A')}", styles['BulletStyle']))
    elements.append(Paragraph(f"• Duration: {structured_itinerary_data.get('trip_duration_days', 'N/A')} days", styles['BulletStyle']))
    elements.append(Paragraph(f"• Budget: ₹{structured_itinerary_data.get('budget', 0.00)}", styles['BulletStyle']))

    # Keep preference lists if they exist:
    if structured_itinerary_data.get('interests'):
        elements.append(Paragraph("• Interests: " + ", ".join(structured_itinerary_data['interests']), styles['BulletStyle']))
    if structured_itinerary_data.get('travel_mode_preference'):
        elements.append(Paragraph("• Travel Modes: " + ", ".join(structured_itinerary_data['travel_mode_preference']), styles['BulletStyle']))
    if structured_itinerary_data.get('accommodation_preference'):
        elements.append(Paragraph("• Accommodation: " + ", ".join(structured_itinerary_data['accommodation_preference']), styles['BulletStyle']))
    if structured_itinerary_data.get('food_preference'):
        elements.append(Paragraph("• Food Preferences: " + ", ".join(structured_itinerary_data['food_preference']), styles['BulletStyle']))

    elements.append(Spacer(1, 0.3 * inch))

    # --- Daily Plan Section ---
    elements.append(Paragraph("<b>Daily Plan</b>", styles['SectionHeading']))

    # Add notes before days from the structured data
    if structured_itinerary_data["notes_before_days"]:
        full_note_text = "\n".join(structured_itinerary_data["notes_before_days"])
        cleaned_note = clean_plain_text_for_paragraph(full_note_text)
        elements.append(Paragraph(cleaned_note, styles['TipStyle']))
        elements.append(Spacer(1, 0.15 * inch))

    # Check if 'days' list is empty before iterating
    if not structured_itinerary_data["days"]:
        elements.append(Paragraph("No itinerary generated.", styles['NormalText']))
    else:
        for day_data in structured_itinerary_data["days"]: # Iterate through structured days
            elements.append(Spacer(1, 0.2 * inch)) # Spacer before each day's content
            
            # Day Heading (e.g., "Day 1: Arrival in Munich & Bavarian Charm")
            day_heading_text = f"Day {day_data['day_number']}: {day_data['theme']}"
            elements.append(Paragraph(day_heading_text, styles['DayHeading']))

            # Travel Section
            if day_data["sections"]["Travel"]:
                travel_links_rml = process_text_for_pdf_links(day_data["sections"]["Travel"], structured_itinerary_data.get('destination', ''))
                cleaned_travel = clean_plain_text_for_paragraph(travel_links_rml)
                elements.append(Paragraph(f'<b>Travel:</b> {cleaned_travel}', styles['SubSectionItemHeading']))

            # Accommodation Section
            if day_data["sections"]["Accommodation"]:
                accomm_links_rml = process_text_for_pdf_links(day_data["sections"]["Accommodation"], structured_itinerary_data.get('destination', ''))
                cleaned_accommodation = clean_plain_text_for_paragraph(accomm_links_rml)
                elements.append(Paragraph(f'<b>Accommodation:</b> {cleaned_accommodation}', styles['SubSectionItemHeading']))

            # Food Section
            if day_data["sections"]["Food"]:
                elements.append(Paragraph('<b>Food:</b>', styles['SubSectionItemHeading']))
                for meal in day_data["sections"]["Food"]:
                    meal_links_rml = process_text_for_pdf_links(meal["details"], structured_itinerary_data.get('destination', ''))
                    meal_details_clean = clean_plain_text_for_paragraph(meal_links_rml)
                    
                    if meal["type"] != "Generic":
                        elements.append(Paragraph(f'• <b>{meal["type"]}:</b> {meal_details_clean}', styles['BulletStyle']))
                    else: # For generic food items
                        elements.append(Paragraph(f'• {meal_details_clean}', styles['BulletStyle']))

            # Activities Section
            if day_data["sections"]["Activities"]:
                elements.append(Paragraph('<b>Activities:</b>', styles['SubSectionItemHeading']))
                for activity in day_data["sections"]["Activities"]:
                    activity_links_rml = process_text_for_pdf_links(activity["details"], structured_itinerary_data.get('destination', ''))
                    activity_details_clean = clean_plain_text_for_paragraph(activity_links_rml)
                    elements.append(Paragraph(f'• {activity_details_clean}', styles['BulletStyle']))

            elements.append(Spacer(1, 0.15 * inch)) # Small spacer after sections for current day


    # --- Budget Summary Section ---
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("<b>Budget Summary (Estimate)</b>", styles['SectionHeading']))

    budget_summary = structured_itinerary_data["budget_summary"]
    
    if budget_summary["items"]:
        for item in budget_summary["items"]:
            cleaned_item = clean_plain_text_for_paragraph(item)
            elements.append(Paragraph(cleaned_item, styles['BulletStyle']))
        
    if budget_summary["total"]:
        cleaned_total = clean_plain_text_for_paragraph(budget_summary["total"])
        elements.append(Paragraph(f'<b>{cleaned_total}</b>', styles['NormalText'])) # Make total bold
    
    if budget_summary["tips"]:
        for tip in budget_summary["tips"]:
            cleaned_tip = clean_plain_text_for_paragraph(tip)
            elements.append(Paragraph(cleaned_tip, styles['TipStyle']))


    # --- Footer ---
    elements.append(Spacer(1, 0.4 * inch))
    elements.append(Paragraph("Generated by Personalized Trip Planner using AI.", styles['Italic']))

    doc.build(elements)
    buffer.seek(0)
    return buffer