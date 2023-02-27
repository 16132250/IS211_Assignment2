import argparse
import logging
import datetime
import pprint
import requests

logging.basicConfig(filename='errors.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def downloadData(url):
    """Downloads the data and returns the contents"""
    csvData = requests.get(url)
    # print(csvData.text)

    return csvData.text

def dtConvert(fieldname):
    """To format the date found in the imported data file"""
    formatted = r'%d/%m/%Y'
    converted = (datetime.datetime.strptime(fieldname, formatted).date())
    formatted_date = converted.strftime('%Y-%m-%d')

    return formatted_date

def processData(file_content):
    """Returns the data in dictionary format"""
    url_result = []

    rows = file_content.split('\n')
    linenum = 0
    for row in rows:
        cells = row.split(",")
        linenum += 1

        try:
            if len(cells) == 3:
                person_data = {
                    'id': int(cells[0]),
                    'name': cells[1],
                    'birthdate': dtConvert(cells[2])
                }
                url_result.append(person_data)

                # url_result[int(cells[0])] = (cells[1], dtConvert(cells[2]))

        except(ValueError):
            logging.error(f'Error processing line # {linenum} for ID #{cells[0]}')


    # pprint.pprint(url_result)

    return url_result

def displayPerson(id, personData):
    """Prints the name and data of the people found in the download"""
    # print(f'from dislpayPerson: {personData[id]}')

    for person in personData:
        if person['id'] == id:
            print(f"Person #{id} is {person['name']} with a birthday of {person['birthdate']}")
            return

    print('No user found with that id')

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
                print('Main: No user found with that id')
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



