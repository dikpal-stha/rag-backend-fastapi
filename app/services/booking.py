import json
import re
from app.models.schemas import BookingDetails
from app.services.rag import llm_generate
from app.services.memory import save_booking_details, get_booking_details, clear_booking_details
from app.services.booking_db import save_booking_to_sql

def keyword_booking_intent(message: str) -> bool:
    msg = message.lower()
    keywords = ["book", "booking", "schedule", "reschedule", "cancel", "interview"]
    return any(word in msg for word in keywords)

def extract_email_rule(message: str):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message)
    return match.group(0) if match else None

def extract_time_rule(message: str):
    match = re.search(r'\b\d{1,2}(:\d{2})?\s?(AM|PM|am|pm)\b', message)
    return match.group(0) if match else None

# date validation to stop llm hallunication
def validate_date(date: str, message: str):
    if not date:
        return None

    if any(word in message.lower() for word in date.lower().split()):
        return date

    return None


# Booking details extraction using LLM
def extract_booking_details_llm(message: str):
    prompt = f"""
        Extract booking information from the message.

        Return ONLY valid JSON in this exact format:
        {{
        "intent": "booking" or "general",
        "name": null or string,
        "email": null or string,
        "date": null or string,
        "time": null or string
        }}

        Rules:
        - If the message is about booking, scheduling, rescheduling, or cancelling an interview, intent = "booking"
        - Otherwise intent = "general"
        - Do not invent information
        - If a field is not explicitly present, return null
        - Return only JSON

        Message:
        {message}
    """
    response = llm_generate(prompt, max_new_tokens=100).strip()

    try:
        data = json.loads(response)
        return data
    except Exception:
        return {
            "intent": "general",
            "name": None,
            "email": None,
            "date": None,
            "time": None
        }


def extract_booking_details(message: str):
    if not keyword_booking_intent(message):
        return BookingDetails(intent="general")

    email = extract_email_rule(message)
    time = extract_time_rule(message)
    data = extract_booking_details_llm(message)
    date = validate_date(data.get("date"), message)
    

    return BookingDetails(
        intent = data.get("intent", "booking"),
        name = data.get("name"),
        email = email or data.get("email"),
        date = date,
        time = time or data.get("time")
    )


def get_missing_fields(details: BookingDetails) -> list:
    fields = ["name", "email", "date", "time"]

    return [field for field in fields if getattr(details, field) is None]


def generate_missing_fields_response(missing_fields: list) -> str:
    if not missing_fields:
        return ""

    if len(missing_fields) == 1:
        fields_text = missing_fields[0]
    
    elif len(missing_fields) == 2:
        fields_text = f"{missing_fields[0]} and {missing_fields[1]}"

    else:
        fields_text = ",".join(missing_fields[:-1])
        fields_text += f", and {missing_fields[-1]}"

    return f"Please provide your {fields_text} to complete the booking."


# Merge old and new bookingdetails
def merge_booking_details(old_details: BookingDetails, new_details: BookingDetails) -> BookingDetails:
    
    return BookingDetails(
        intent = "booking",
        name = new_details.name or old_details.name,
        email= new_details.email or old_details.email,
        date = new_details.date or old_details.date,
        time = new_details.time or old_details.time
    )


# main booking handler
def handle_booking_request(message: str, user_id: str):
    new_details = extract_booking_details(message)
    old_details = get_booking_details(user_id)

    if new_details.intent != "booking" and old_details is None:
        return {"intent": "general"}
    
    # get and merge old details if any
    if old_details is not None:
        details = merge_booking_details(old_details, new_details)
    else:
        details = new_details

    # save to redis
    save_booking_details(user_id, details)

    #check missing fields
    missing_fields = get_missing_fields(details)

    if missing_fields:
        return {
            "intent": "booking",
            "complete": False,
            "response": generate_missing_fields_response(missing_fields),
            "details": details 
        }
    
    # save only if all details are extracted
    save_booking_to_sql(details)
    clear_booking_details(user_id)

    return {
        "intent": "booking",
        "complete": True,
        "response": "Your interview booking has been recorded successfully!",
        "details": details
    }





    



