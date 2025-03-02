from google import genai
from config.config import GEMINI_API_KEY
from model.schema import TaskDeadLinePriority, TaskList

client = genai.Client(api_key=GEMINI_API_KEY)
from datetime import datetime
import re, json


def get_task_deadline_and_priority(task_title: str, tasks: TaskList) -> TaskDeadLinePriority:
    today = datetime.today()

    prompt = f'''Extract the deadline-related phrase and urgency level from this task description:
    "{task_title}".
    Today is {today}.
    My existing tasks are {tasks}.
    - Deadline should be in ISO 8601 format (YYYY-MM-DD HH:MM:SS) if mentioned.
    - If the deadline is relative (e.g., 'tomorrow' or 'next week' or 'by today 6 PM', 'tomorrow', 'next Monday'), calculate the actual date-time.
    - If the deadline does not contain exact time, take the ceiling (e.g., 'by tomorrow' becomes (YYYY-MM-DD 23:59:59)).
    - Be more intelligent about the deadline (e.g., breakfast is to be had in the morning, sleep early is to be done at night)
    - If no deadline is found, return null.
    - Determine urgency as 1=High, 2=Medium, or 3=Low.
    - Determine the priority keeping in mind I already have other tasks in hand.

    Respond in JSON format:
    {{
        "deadline": "raw datetime" or "None",
        "priority": 1 or 2 or 3
    }}'''

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    try:
        extracted_data = response.text.strip()
        data = json.loads(re.sub(r"```(?:json)?", "", extracted_data, flags=re.IGNORECASE).strip())  # Convert Gemini response to dictionary
        return TaskDeadLinePriority(deadline=data.get('deadline'), priority=data.get('priority'))
    except Exception as e:
        print(e)
        return TaskDeadLinePriority(deadline=None, priority=2)


#
# test_cases = [
#         "Complete the report by tomorrow 3 PM",
#         "Do laundry next Friday evening",
#         "Submit the project by March 10th, 2 PM",
#         "Write an email in the morning",
#         "No deadline, just whenever",
#     ]
#
# for text in test_cases:
#     print(f"Task: {text}")
#     print(get_task_deadline_and_priority(text))
