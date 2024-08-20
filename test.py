import csv

def read_csv_act(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            split = row.get('User Activities').split(',')
            if len(split) > 2:
                print(split[4])
        return list(reader)

def read_csv_user(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
        return list(reader)

try:
    #activities = read_csv_act('output/activities.csv')
    users = read_csv_user('output/users.csv')
except FileNotFoundError:
    print("No data available. Run the main function first.")