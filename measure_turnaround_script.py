"""
This script should measure the status of the Speechmatics service every
minute for an hour and print the time(s) when the longest turnaround time
was measured in that period in EST in the format HH:MM:SS.

"""

import json
import time
import datetime
import requests

SAMPLES_NO = 60
SAMPLES_INTERVAL_SECONDS = 60

RESPONSE_ITEM_TIMESTAMP = "Time_UTC"
RESPONSE_ITEM_TURNAROUND = "Average_Turnaround_Mins"

API_SCHEMA = "https://"
API_BASE = "api.speechmatics.com"
API_VERSION = "v1.0"
API_NAME = "status"

SAMPLE_ITEM_TIMESTAMP = "timestamp"
SAMPLE_ITEM_TURNAROUND = "turnaround"

EST_HOURS_DIFFERENCE = 5
GMT_FORMAT_LONG = "%a, %d %b %Y %H:%M:%S GMT"
EST_FORMAT_SHORT = "%H:%M:%S"

def get_time_est(time_string_utc):
    """Converts the UCT formatted time string passed as parameter into a EST
    formatted time string and returns it

    """

    utc_tz_object = datetime.datetime.strptime(time_string_utc, GMT_FORMAT_LONG)
    converted_est = utc_tz_object - datetime.timedelta(hours=EST_HOURS_DIFFERENCE)

    return converted_est

def get_turnaround_time():
    """Queries the /status API endpoint and returns the current turnaround time
    and time

    """

    response = requests.get(API_SCHEMA + API_BASE + "/" + API_VERSION + "/" +API_NAME)
    status_json = json.loads(response.text)

    return {SAMPLE_ITEM_TIMESTAMP: str(status_json[RESPONSE_ITEM_TIMESTAMP]), \
            SAMPLE_ITEM_TURNAROUND: str(status_json[RESPONSE_ITEM_TURNAROUND])}

def main():
    """Main function

    Poll RESTful API. When (new) max turnaround is returned, record associated timestamp

    """

    max_turnaround = -1 #not expecting a valid negative time from the API...
    times = []

    print "Computing max turnaround over " + str(SAMPLES_NO) + \
          " samples with a " + str(SAMPLES_INTERVAL_SECONDS) + "s interval..."

    for i in range(0, SAMPLES_NO+1):
        sample = get_turnaround_time()

        print "[" + str(datetime.datetime.now()) + "] Sample " + str(i + 1) + ": " + str(sample)

        if int(sample[SAMPLE_ITEM_TURNAROUND]) > max_turnaround:
            # new max
            max_turnaround = int(sample[SAMPLE_ITEM_TURNAROUND])
            times = []

        if int(sample[SAMPLE_ITEM_TURNAROUND]) == max_turnaround \
        and sample[SAMPLE_ITEM_TIMESTAMP] not in times:
            # record timestamp
            times.append(sample[SAMPLE_ITEM_TIMESTAMP])


        time.sleep(SAMPLES_INTERVAL_SECONDS)


    print "Max turnaround " + str(max_turnaround) + "m observed at (EST):"
    for timestamp in times:
        print get_time_est(timestamp).strftime(EST_FORMAT_SHORT)

    print "Done"

if __name__ == "__main__":
    main()

