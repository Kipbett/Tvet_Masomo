from openai import OpenAI
from utils import ai_api_key

client = OpenAI(api_key= ai_api_key)

curriculum_file = client.files.create(
    file=open("C:\Users\KONZA\Desktop\COPY\CYCLE 2\Enyth Rono\DONE & DUSTED\Computer Science level 6\OS\PDF\UNDERSTAND ARTICICIAL INTELLIGENCE CONCEPTS.pdf", "rb"),
    purpose="assist"
)

occupational_file = client.files.create(
    file=open("C:\Users\KONZA\Desktop\COPY\CYCLE 2\Enyth Rono\DONE & DUSTED\Computer Science level 6\OS\PDF\UNDERSTAND ARTICICIAL INTELLIGENCE CONCEPTS.pdf", "rb"),
    purpose="assist"
)

# Step 2: Use both uploaded files in the request
response = client.responses.create(
    model="gpt-5",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Analyze the curriculum and occupational standard and generate a summary of the key points.",
                },
                {
                    "type": "input_file",
                    "file_id": curriculum_file.id,
                },
                {
                    "type": "input_file",
                    "file_id": occupational_file.id,
                },
            ],
        },
    ]
)

print(response.output_text)