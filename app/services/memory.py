import redis
import json

r = redis.Redis(
    host='redis-18426.c301.ap-south-1-1.ec2.cloud.redislabs.com',
    port=18426,
    decode_responses=True,
    username="default",
    password="GHtDXyjc2yhUhu7SCxubm5Fxpoyj4oQF"
)

# save message
def save_message(user_id: str, role: str, content: str):
    key = f"chat {user_id}"

    message = {
        "role": role,
        "content": content
    }

    r.rpush(key, json.dumps(message))

# Get chat history
def get_history(user_id: str):
    key = f"chat {user_id}"

    messages = r.lrange(key, 0, -1)

    return [json.loads(m) for m in messages]


