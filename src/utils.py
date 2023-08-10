import csv

from src.api_hh_class import HeadHunterAPI


def write_csv(name_csv_file, api):
    keys = api[0].keys()
    with open(f'{name_csv_file}.csv', 'w', encoding='utf-8', newline='') as file:
        file_writer = csv.DictWriter(file, keys)
        file_writer.writeheader()
        file_writer.writerows(api)



