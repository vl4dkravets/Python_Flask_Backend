import json
from urllib.request import urlopen
import math
from bs4 import BeautifulSoup


def get_jobs_from_page(page_number):
    url = f"https://jobs.github.com/positions.json?full_time=true&part_time=true&page={page_number}:"

    response = urlopen(url)
    source = response.read()
    data = json.loads(source)

    return data


def combine_jobs(pages_of_jobs):
    # combine all the lists of dictionaries => each dictionary is a separate description of a job
    all_jobs = []

    for page in range(1, pages_of_jobs + 1):
        # get jobs from page number
        x = get_jobs_from_page(page)

        # concatenate list of jobs from the page to the list of jobs from all the pages
        all_jobs += x

    return all_jobs


def num_of_jobs_available():
    url = "https://jobs.github.com/positions"
    response = urlopen(url)
    source = response.read()

    soup = BeautifulSoup(source, "lxml")
    specific_div_elem = soup.find("div", attrs={"class": "inner"})
    h1 = specific_div_elem.find("h1")

    # Splits the text into separate words => thus, it removes spaces & newlines
    text = h1.string.split()

    # Fifth word from the string the number we need
    val = text[5]

    if val.isdigit():
        return int(val)
    else:
        # in case of faulty conversion
        return 0


def get_the_jobs():
    jobs = num_of_jobs_available()
    JOBS_PER_PAGE = 50

    # count the number of pages it'll take to go through the num of jobs found
    pages = math.ceil(jobs / JOBS_PER_PAGE)

    list_with_jobs = combine_jobs(pages)

    return list_with_jobs