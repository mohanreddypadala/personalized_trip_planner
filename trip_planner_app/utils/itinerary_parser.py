# trip_planner_app/utils/itinerary_parser.py

import re

def parse_ai_itinerary_to_structure(raw_itinerary_text):
    """
    Parses the raw AI-generated itinerary text into a structured Python object.
    """
    structured_data = {
        "notes_before_days": [],
        "days": [],
        "budget_summary": {
            "header": "",
            "items": [],
            "total": "",
            "tips": []
        }
    }

    lines = raw_itinerary_text.split('\n')
    current_day = None
    current_section = None 
    
    # State flags for parsing
    in_budget_summary = False
    in_notes_before_days = True

    line_iter = iter(lines)

    for line in line_iter:
        line_stripped = line.strip()

        if not line_stripped:
            current_section = None
            continue

        # Check for Budget Summary section
        if line_stripped.startswith('**Budget Summary') or 'Budget Summary' in line_stripped:
            in_budget_summary = True
            in_notes_before_days = False
            structured_data["budget_summary"]["header"] = line_stripped
            continue

        if in_budget_summary:
            # Check for Total line (using bold or literal 'Total:')
            if line_stripped.startswith('**Total:') or '• Total:' in line_stripped or 'Total:' in line_stripped:
                # Capture the line as the total
                structured_data["budget_summary"]["total"] = line_stripped
            
            # Check for Tip/Note headers
            elif line_stripped.startswith('• Tips for Budget Management') or line_stripped.startswith('• Note:'):
                tip_lines = [line_stripped]
                # Collect subsequent lines that look like list items or normal text belonging to the tip
                while True:
                    try:
                        next_line = next(line_iter)
                        if next_line.strip() and \
                           (next_line.strip().startswith('•') or next_line.strip().startswith('*') or not next_line.strip().startswith('**')):
                            # Capture tips or budget details that follow immediately
                            tip_lines.append(next_line.strip())
                        else:
                            break
                    except StopIteration:
                        break
                structured_data["budget_summary"]["tips"].append("\n".join(tip_lines))
            
            # Check for general bulleted items (Estimated Costs, Flights, Accommodation, Food, etc.)
            elif line_stripped.startswith('* ') or line_stripped.startswith('• '):
                # Ensure we don't accidentally capture a Total line again if it was missed
                if not line_stripped.startswith('• Total:'):
                    structured_data["budget_summary"]["items"].append(line_stripped)
            else:
                pass
            continue

        # Check for Day Heading
        if line_stripped.startswith('**Day'):
            in_notes_before_days = False
            day_match = re.match(r'\*\*Day (\d+):\s*(.*?)\*\*', line_stripped)
            if day_match:
                day_number = int(day_match.group(1))
                theme = day_match.group(2).strip()
                current_day = {
                    "day_number": day_number,
                    "theme": theme,
                    "sections": {
                        "Travel": "", "Accommodation": "",
                        "Food": [], "Activities": []
                    }
                }
                structured_data["days"].append(current_day)
                current_section = None
            continue

        # If we are still collecting notes before days
        if in_notes_before_days:
            structured_data["notes_before_days"].append(line_stripped)
            continue

        # --- Parse Content within a Day (General Structure) ---
        if current_day:
            # Check for section headings using a single, robust regex that handles the AI's inconsistent spacing/bullets
            # Regex: ^\*?\s*\*\*(Travel|Accommodation|Food|Activities)\*\*\s*:(.*)
            section_match = re.match(r'^\*?\s*\*\*(Travel|Accommodation|Food|Activities)\*\*\s*:\s*(.*)', line_stripped, re.IGNORECASE)

            if section_match:
                current_section = section_match.group(1).capitalize()
                content_after_heading = section_match.group(2).strip()

                if current_section in ["Travel", "Accommodation"]:
                    current_day["sections"][current_section] = content_after_heading
                elif current_section in ["Food", "Activities"]:
                    if content_after_heading:
                        current_day["sections"][current_section].append({"type": "Generic", "details": content_after_heading})
            
            # Handle sub-items (nested bullets that follow a heading)
            elif line_stripped.startswith('*') or line_stripped.startswith('•'): 
                bullet_content = line_stripped.lstrip('•* ').strip() # Strip both * and •
                
                if current_section == "Food":
                    food_type_match = re.match(r'(Breakfast|Lunch|Dinner):\s*(.*)', bullet_content, re.IGNORECASE)
                    if food_type_match:
                        food_type_name = food_type_match.group(1).capitalize()
                        food_details = food_type_match.group(2).strip()
                        current_day["sections"]["Food"].append({"type": food_type_name, "details": food_details})
                    else:
                        if current_day["sections"]["Food"]:
                            current_day["sections"]["Food"][-1]["details"] += " " + bullet_content
                        else:
                            current_day["sections"]["Food"].append({"type": "Generic", "details": bullet_content})

                elif current_section == "Activities":
                    current_day["sections"]["Activities"].append({"details": bullet_content})

                elif current_section in ["Travel", "Accommodation"]:
                    current_day["sections"][current_section] += " " + bullet_content
                
                else:
                    current_day["sections"]["Activities"].append({"details": bullet_content})
            
            # Handle narrative text following a string-based section
            else:
                if current_section in ["Travel", "Accommodation"]:
                    current_day["sections"][current_section] += " " + line_stripped
                elif current_section and isinstance(current_day["sections"][current_section], list) and current_day["sections"][current_section]:
                    current_day["sections"][current_section][-1]["details"] += " " + line_stripped
                else:
                    pass

    return structured_data