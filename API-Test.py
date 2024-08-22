import http.client
import json
import csv
import os
from dotenv import load_dotenv
import SACAccess

# load environment variables
load_dotenv(dotenv_path='api.env')

# Service-Aufruf und Daten in CSV-Datei speichern
def Usersrequest(bearer_token):
    conn = http.client.HTTPSConnection(f"{os.getenv('SACServiceURL')}")
    headers = {
        #'x-csrf-token': f'{xcsrf_token}',
        'x-sap-sac-custom-auth': 'true',
        'Authorization': f'Bearer {bearer_token}'
    }
    conn.request("GET", "/api/v1/scim/Users", headers=headers)
    response = conn.getresponse()
    data = response.read()

    if response.status == 200:
        json_data = json.loads(data.decode("utf-8"))  # Decode and parse the response as JSON
        return json_data
    else:
        raise Exception(f"Failed to get data: {response.status} {data.decode('utf-8')}")


def Activitiesrequest(bearer_token):
    conn = http.client.HTTPSConnection(f"{os.getenv('SACServiceURL')}")
    headers = {
        #'x-csrf-token': f'{xcsrf_token}',
        'x-sap-sac-custom-auth': 'true',
        'Authorization': f'Bearer {bearer_token}'
    }
    conn.request("GET", "/api/v1/audit/activities/exportActivities?pageSize=100", headers=headers)
    response = conn.getresponse()
    data = response.read()

    if response.status == 200:
        return data.decode("utf-8")
    else:
        raise Exception(f"Failed to get data: {response.status} {data.decode('utf-8')}")
    
def Storiesrequest(bearer_token):
    conn = http.client.HTTPSConnection(f"{os.getenv('SACServiceURL')}")
    headers = {
        #'x-csrf-token': f'{xcsrf_token}',
        'x-sap-sac-custom-auth': 'true',
        'Authorization': f'Bearer {bearer_token}'
    }
    conn.request("GET", "/api/v1/stories", headers=headers)
    response = conn.getresponse()
    data = response.read()

    if response.status == 200:
        return json.loads(data.decode("utf-8"))  # Decode and parse the response as JSON
    else:
        raise Exception(f"Failed to get data: {response.status} {data.decode('utf-8')}")
    

# CSV-Datei schreiben
def write_text_to_csv(text_data, csv_filename):
    """
    Write plain text data to a CSV file.

    :param text_data: The plain text data to write to the CSV file.
    :param csv_filename: The name of the CSV file to write to.
    """
    if not text_data:
        raise ValueError("No data to write to CSV")

    lines = text_data.splitlines()
    filepath = os.path.join('output', csv_filename)
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        for line in lines:
            writer.writerow([line])


# Example usage in the main function
def main():
    bearer_token = SACAccess.get_bearer_token()
    #SACAccess.get_xcsrf_token()

    # Activities Request
    json_data = Activitiesrequest(bearer_token)
    write_text_to_csv(json_data, 'activities.csv')

    # Users Request
    json_data = Usersrequest(bearer_token)
    write_text_to_csv(json.dumps(json_data, indent=4), 'users.csv')

    # Stories Request
    json_data = Storiesrequest(bearer_token)
    write_text_to_csv(json.dumps(json_data, indent=4), 'stories.csv')

# Run the main function if the script is executed
if __name__ == '__main__':
    main()