import requests
import pandas as pd

def related_courses_gpt(course_name):
    api_key = "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"
    endpoint = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = f"""Given the course name <tag>{course_name}</tag>, generate a concise list of 20 related course keywords. These keywords should represent real university course topics that are often associated with or are extensions of the given course. For instance, if the course name is "{course_name}", suitable keywords might include 'machine learning', 'data analytics', 'artificial intelligence', etc. Please provide the keywords in a simple list format, without additional explanation or sentences.
            Also no need to generate keywords which has course_name included in it>
            for example:  course_name: finance.
            the outputs "Investment analysis, Financial accounting, Risk management, Financial markets" are good outputs but "Personal finance, Corporate finance, International finance" are bad outputs since they already have course_name: finance in it."""

    def getResp(prompt):
        messages = []
        messages.append({"role": "user", "content": prompt})
        # Data payload
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 300
        }

        # Send request
        response = requests.post(endpoint, headers=headers, json=data)

        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print("Error:", response.status_code, response.text)

    return getResp(prompt)

# # Example usage
# related_course_names = related_courses_gpt("artificial intelligence")
# print(related_course_names)
