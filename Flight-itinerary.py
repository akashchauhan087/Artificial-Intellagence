from bs4 import BeautifulSoup
import ollama, json, re


# data = mail_data[0]['Email Body']
data = 'Please provide Delhi to Mumbai for 2 dec and return on 4 december'
soup = BeautifulSoup(data, "html.parser")
plain_text = soup.get_text()
print(plain_text)


def extract_travel_info_ollama(user_input):
    prompt = f"""
Given the travel request: "{user_input}", extract the following fields and return ONLY valid JSON (no markdown, no explanation):

- source: iata/airport code (e.g. GOI, BOM, NAG)
- source_city: name of the airport source city
- destination: iata/airport code
- destination_city: name of the airport destination city
- travel_date: in YYYY-MM-DD format (assume current year if not mentioned)
- is_return: true or false
- return_date: in YYYY-MM-DD or null
- adult_count: 1 or adult
- child_count: child/children count or 0
- infant_count: infant count or 0
- total_travel_count: sum of adult, child/children, infant
- preferred career: return the list of preferred career for flight like Indigo, Air Asia, AirAsia India, Air India etc

Strictly return JSON. Do not explain.
"""
    print("============================")
    response = ollama.chat(
        model='phi3:latest',
        # model='mistral',
        # model='deepseek-r1:7b',
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['message']['content']

    try:
        json_str = re.search(r'\{.*\}', content, re.DOTALL).group(0)
        return json.loads(json_str)
    except:
        print("⚠️ Invalid response:\n", content)
        return None

print(extract_travel_info_ollama(plain_text))
print("Query completed")








# import ollama
# import json
# import re

# def extract_travel_info_ollama(user_input):
#     prompt = f"""
# Given the travel request: "{user_input}", extract the following fields and return ONLY valid JSON (no markdown, no explanation):

# - source: iata/airport code (e.g. GOI, BOM, NAG)
# - source_city: name of the airport source city
# - destination: iata/airport code
# - destination_city: name of the airport destination city
# - travel_date: in YYYY-MM-DD format (assume current year if not mentioned)
# - is_return: true or false
# - return_date: in YYYY-MM-DD or null
# - adult_count: 1 or adult
# - child_count: child/children count or 0
# - infant_count: infant count or 0
# - total_travel_count: sum of adult, child/children, infant
# - preferred career: return the list of preferred career for flight like Indigo, Air Asia, AirAsia India, Air India etc

# Strictly return JSON. Do not explain.
# """

#     response = ollama.chat(
#         model='mistral',
#         messages=[{"role": "user", "content": prompt}]
#     )

#     content = response['message']['content']

#     try:
#         # Try to extract a JSON list using a regex that matches from [ to ]
#         json_match = re.search(r'\[\s*\{.*?\}\s*\]', content, re.DOTALL)
#         if json_match:
#             json_str = json_match.group(0)
#             return json.loads(json_str)

#         # Fallback: try to match a single object if the list wasn't returned
#         json_match = re.search(r'\{.*?\}', content, re.DOTALL)
#         if json_match:
#             json_str = json_match.group(0)
#             return [json.loads(json_str)]  # Wrap single object in a list

#         # If nothing matched, return None
#         print("⚠️ No valid JSON found in the response:\n", content)
#         return None

#     except json.JSONDecodeError as e:
#         print("⚠️ JSON decode error:", e)
#         print("⚠️ Raw response content:\n", content)
#         return None

# print(extract_travel_info_ollama(plain_text))
