import csv

def read_csv_act(file_path):
    result = set()
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            split = row.get('User Activities').split(',')
            if len(split) > 2:
                list = split[4]
                result.add(list)
        return result

def read_csv_user(file_path):
    result = set()
    with open(file_path, 'r') as file:
        reader = file.readlines()
        for row in reader:
            if row.__contains__('displayName'):
                list = row.split(':')
                result.add(list[1].replace('"', '').replace(',', '').replace('}', '').strip())
    return result

try:
    activities = read_csv_act('output/activities.csv')
    users = read_csv_user('output/users.csv')
    for user in users:
        print(user)
except FileNotFoundError:
    print("No data available. Run the main function first.")