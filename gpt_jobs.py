import requests
import pandas as pd

def jobSearch(course, university):
    api_key = "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"
    endpoint = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = f"""Act as a senior recruiter for Germany and guide about the job opportunities available for me in Germany,
      after studying this course "{course}" from {university}. Also tell me the salary ranges too for each job. 

                Give output in following format""
                [
                    
                        "jobTitle": "",
                        "salaryPerYear": "€"
                    ,
                    
                        "jobTitle": "Investment Manager",
                        "salaryPerYear": "€"
                    ,
                    
                        "jobTitle": "Risk Manager",
                        "salaryPerYear": "€"
                    ,
                    
                        "jobTitle": "Financial Controller",
                        "salaryPerYear": "€"
                    
                ]
                ""

                I just want output as i told you and no extra INFORMATION. Dont generate <tag> in output its for your understanding. Generate output in array of JSON format"""


    def getResp(prompt):
        messages = []
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 300
        }

        
        response = requests.post(endpoint, headers=headers, json=data)

        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print("Error:", response.status_code, response.text)

    return getResp(prompt)

# # Example usage
# related_course_names = related_courses_gpt("artificial intelligence")
# print(related_course_names)
