import os
import csv

def save_csv(csv_file, data):
    if os.path.exists(csv_file):
        # Open the CSV file in append mode ('a') if it exists
        with open(csv_file, 'a', newline='', encoding="utf-8") as file:
            fieldnames = data.keys()
            print(data)
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            try:
                writer.writerow(data)
            except:
                pass
        print(f'Data has been appended to {csv_file}')
    else:
        # If the file doesn't exist, create it and write headers along with the data
        with open(csv_file, 'w', newline='', encoding="utf-8") as file:
            fieldnames = data.keys()
            print(data)
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data)
        print(f'Data has been written to {csv_file}')


