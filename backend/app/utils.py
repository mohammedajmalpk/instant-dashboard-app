from fastapi import HTTPException


def clean_validate_html(html_data):
    """
        data cleaning and validation
        - remove unwanted strings from generated html
        - validate the html_data
        - return cleaned and validated html
    """
    html_data = html_data.replace('```html', '')
    html_data = html_data.replace('```', '')
    html_data = html_data.strip()

    if not ('<!DOCTYPE' in html_data or '<html' in html_data):
        raise HTTPException(status_code=500, detail="AI didn't generate a valid html. please try again")
    return html_data

def extract_numeric_values(obj):
    """
        - calculate the total from the json data
    """
    numbers = []
    if isinstance(obj, dict):
        for value in obj.values():
            numbers.extend(extract_numeric_values(value))
    elif isinstance(obj, list):
        for item in obj:
            numbers.extend(extract_numeric_values(item))
    elif isinstance(obj, (int, float)):
        numbers.append(obj)
    return numbers