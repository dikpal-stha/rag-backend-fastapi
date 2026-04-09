from models.schemas import BookingDetails
from services.rag import llm_generate
from services.memory import save_booking_details, get_booking_details, clear_booking_details
from services.booking_db import save_booking_to_sql

def detect_intent(message: str) -> str:
    prompt = f"""
    Is the message about booking an interview?

    Return only one word:
    booking
    or
    general

    Message:
    {message}
    """
    response = llm_generate(prompt, max_new_tokens=10).strip().lower()
    # print("INTENT RAW", response)

    if "booking" in response:
        return "booking"
    return "general"


def extract_email(message: str) -> str:
    prompt = f"""
    Extract the email address from the message.
    If none found, return null.

    Message:
    {message}
    """

    response = llm_generate(prompt).strip()

    if "@" in response:
        return response
    return None


def extract_name(message: str) -> str:
    prompt = f"""
    Extract the person's name from the message.
    If none found, return null.

    Message:
    {message}
    """

    response = llm_generate(prompt).strip()

    if response.lower() == "null" or response == "":
        return None

    return response


def extract_date(message: str) -> str:
    prompt = f"""
    Extract only the date mentioned in this message.
    If no date is mentioned, return only: null

    Message:
    {message}
    """

    response = llm_generate(prompt).strip()

    if response.lower() == "null" or response == "":
        return None

    return response


def extract_time(message: str) -> str:
    prompt = f"""
    Extract only the time mentioned in this message.
    If no time is mentioned, return only: null

    Message:
    {message}
    """

    response = llm_generate(prompt).strip()

    if response.lower() == "null" or response == "":
        return None

    return response


def extract_booking_details(message: str):
    intent = detect_intent(message)
    
    if intent != "booking":
        return BookingDetails(intent = "general")
    
    return BookingDetails(
        intent = "booking",
        name = extract_name(message),
        email = extract_email(message),
        date = extract_date(message),
        time = extract_time(message)
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





    



