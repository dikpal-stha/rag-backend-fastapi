pip install -r requirements.txt
uvicorn app.main:app --reload

# Example request 

POST /chat/
{
  "user_id": "test_user",
  "query": "How can I get a refund?"
}


Developed and logic-tested in Google Colab and Python environment with Redis Cloud for memory integration.
API is structured for local/server execution via FastAPI.