import argparse
import logging
import datetime
import pprint
import requests

logging.basicConfig(filename='errors.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def downloadData(url):
    """Downloads the data"""
    csvData = requests.get(url)
    # print(csvData.text)

    return csvData.text

def dtConvert(fieldname):
    formatted = r'%d/%m/%Y'
    converted = (datetime.datetime.strptime(fieldname, formatted))

    return converted

def processData(file_content):
    url_result = {}

    rows = file_content.split('\n')
    linenum = 0
    for row in rows:
        cells = row.split(",")
        linenum += 1

        try:
            if len(cells) == 3:

                url_result[int(cells[0])] = (cells[1], dtConvert(cells[2]))

        except(ValueError):
            logging.error(f'Error processing line # {linenum} for ID #{cells[0]}')


    # pprint.pprint(url_result)

    return url_result

def displayPerson(id, personData):
    print(f'from dislpayPerson: {personData[id]}')

def main(url):
    print(f"Running main with URL = {url}")
    downloadData(url)
    processData(downloadData(url))

    a = 0

    while a == 0:

        get_id = int(input('Enter an ID:'))

        if get_id >= 1:

            try:
                displayPerson(get_id, processData(downloadData(url)))

            except(KeyError):
                print('No user found with that id')
        else:
            a = 1

if __name__ == "__main__":
    """Main entry point"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)

    # url = "https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv"
    # main(url)



