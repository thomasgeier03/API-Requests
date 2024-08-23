import csv

def read_csv_act(file_path):
    result = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            split = row.get('User Activities').split(',')
            if len(split) > 2:
                activity = {
                    split[4].replace('"', '').replace('{', '').strip(),
                    split[5].replace('"', '').replace('}', '').strip(),
                    split[7].replace('"', '').replace('}', '').strip()
                }
                result.append(activity)
        return result

def read_csv_user(file_path):
    result = set()
    with open(file_path, 'r') as file:
        reader = file.readlines()
        for row in reader:
            if row.__contains__('Users'):
                split = row.split('/')
                result.add(split[5].replace('"', '').replace(',', '').replace('}', '').strip())
        return list(result)

try:
    activities = read_csv_act('output/activities.csv')
    users = read_csv_user('output/users.csv')
    for activity in activities:
        for user in users:
            if activity.__contains__(user):
                if len(activity) > 1:
                    print('Activity:', activity)
except FileNotFoundError:
    print("No data available. Run the main function first.")