import imaplib
import email
from bs4 import BeautifulSoup
import datetime
import pandas as pd


def fetch_emails_last_48_hours_to_excel(email_address, app_password):
    """Fetch all emails from the last 48 hours and save them to an Excel file."""
   
    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_address, app_password)
    mail.select('inbox')

    # Get date 48 hours ago
    date_48hrs_ago = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime('%d-%b-%Y')

    # Search for all emails SINCE that date
    result, data = mail.search(None, f'(UNSEEN SINCE {date_48hrs_ago})')
    # result, data = mail.search(None, )
    if result != 'OK':
        print("No emails found.")
        return

    emails_data = []

    for num in reversed(data[0].split()):
        result, msg_data = mail.fetch(num, '(RFC822)')
        if result != 'OK':
            continue

        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)

        sender = email.utils.parseaddr(email_message['From'])[1]
        subject = email_message['Subject']
        date = email_message['Date']

        # Convert email date to local time
        try:
            email_date = email.utils.parsedate_to_datetime(date)
            email_date_local = email_date.astimezone().strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            email_date_local = date

        # Extract the body content
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" in content_disposition:
                    continue

                if content_type in ['text/plain', 'text/html']:
                    try:
                        content = part.get_payload(decode=True).decode()
                        if content_type == 'text/html':
                            soup = BeautifulSoup(content, 'html.parser')
                            content = soup.get_text()
                        body += content.strip() + "\n"
                    except:
                        continue
        else:
            try:
                content = email_message.get_payload(decode=True).decode()
                soup = BeautifulSoup(content, 'html.parser')
                body = soup.get_text().strip()
            except:
                body = ""

        # Store extracted info
        emails_data.append({
            "Sender Email": sender,
            "Subject": subject,
            "Email Body": body.strip(),
            "Received Time": email_date_local
        })

    # Save to Excel
    df = pd.DataFrame(emails_data)
    df.to_excel("emails_last_48_hours.xlsx", index=False)
    print("✅ Emails saved to 'emails_last_48_hours.xlsx' successfully!")

    mail.close()
    mail.logout()

    return emails_data


# === Usage ===
email_address = 'bot_tc@zillious.com'
app_password = 'vmrvocnqvmeawuhq'  # Replace with your actual app password

mail_data = fetch_emails_last_48_hours_to_excel(email_address, app_password)

# Prevent window from closing
# input("Press Enter to exit...")

print(mail_data)








# data = mail_data[0]['Email Body']
data = 'Please provide Delhi to Mumbai for 2 dec and return on 4 december'
soup = BeautifulSoup(data, "html.parser")
plain_text = soup.get_text()
print(plain_text)

import ollama
import json
import re

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

    response = ollama.chat(
        model='mistral',
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







'''
import ollama
import json
import re

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

    response = ollama.chat(
        model='mistral',
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['message']['content']

    try:
        # Try to extract a JSON list using a regex that matches from [ to ]
        json_match = re.search(r'\[\s*\{.*?\}\s*\]', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)

        # Fallback: try to match a single object if the list wasn't returned
        json_match = re.search(r'\{.*?\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return [json.loads(json_str)]  # Wrap single object in a list

        # If nothing matched, return None
        print("⚠️ No valid JSON found in the response:\n", content)
        return None

    except json.JSONDecodeError as e:
        print("⚠️ JSON decode error:", e)
        print("⚠️ Raw response content:\n", content)
        return None

print(extract_travel_info_ollama(plain_text))
'''