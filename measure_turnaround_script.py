
import json
import os
import requests
import requests
import sys
import time


def Get_turnaround_time():
    """
    Queries the /status API endpoint and returns the current turnaround time and
    time
    """
    r = requests.get('api.speechmatics.com/v1.0/status')
    status_json = json.loads(r.text)
    return str(status_json['Time_UTC']), str(status_json['average_turnaround_mins'])

def RUN():
    turnarounds = []
    times=[]
    for i in range(1,60):
      times.append(Get_turnaround_time()[0])
      turnarounds.append(Get_turnaround_time()[1 ])
      
      time.sleep(1)


    max_turnaround_time_element_index_for_use_in_finding_correct_time = int(max(turnarounds))
    print times[max_turnaround_time_element_index_for_use_in_finding_correct_time]

if __name__ == "__main__":
    RUN()
 
