from generate_test_data import generate_data
from log_parameter import log   
from datetime import date, datetime
import time
import csv
import os
import wandb 


wandb.login(key = os.getenv("wandbKey"))

generate_data()
project_data = {}
with open('fake-data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    headers = next(csv_reader)

    for header in headers:
        project_data[header] = []

    for row in csv_reader:
        for i, value in enumerate(row):
            project_data[headers[i]].append(float(value))

curr_date = datetime.now()
curr_time = time.mktime(curr_date.timetuple())
for my_param in project_data:
    log(project_data, my_param, "test3", curr_time, 1000)

