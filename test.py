import csv

def read_csv_act(file_path):
    result = set()
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            split = row.get('User Activities').split(',')
            if len(split) > 2:
                print(split[4])
                result.add(split[4].replace('"', '').replace(',', '').replace('}', ''))
        return list(result)

def read_csv_user(file_path):
    result = set()
    with open(file_path, 'r') as file:
        reader = file.readlines()
        for row in reader:
            if row.__contains__('displayName'):
                split = row.split(':')
                result.add(split[1].replace('"', '').replace(',', '').replace('}', '').strip())
        return list(result)

try:
    activities = read_csv_act('output/activities.csv')
    users = read_csv_user('output/users.csv')
    print("Activities User:")
    for activity in activities:
        print(activity)
    print("\nUsers:")    
    for user in users:
        print(user)
    
except FileNotFoundError:
    print("No data available. Run the main function first.")