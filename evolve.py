"""
Question: 
Create a CLI that takes a list of numbers and returns them sorted. 
Use a bubble sort implementation found from a random answer from 
Stack Exchange via https://api.stackexchange.com/.
In other words, after you take in the numbers, call the Stack Exchange API, 
grab a random answer to a random bubble sort implementation question, and 
run the code blindly passing in the user input. Display the answer to the end user.

Sample run:

python evolve.py '51, 62, 45, 31, 90, 42, 28, 96, 65, 33, 73'

>> Thanks. Fetching a random bubble sort implementation. Fingers crossed.
>> 4, 28, 31, 33, 42, 45, 51, 62, 65, 73, 90, 96
"""

import json
import re
import sys

import urllib3

URL = (
    "https://api.stackexchange.com/2.3/search/advanced?order=desc"
    "&sort=activity&site=stackoverflow&q=python bubble sort implementation"
)
URL2 = (
    "https://api.stackexchange.com/2.3/questions/{0}/answers?order=desc"
    "&sort=activity&site=stackoverflow"
)

WITH_BODY = True
HTTP = urllib3.PoolManager()

if WITH_BODY:
    URL += "&filter=withbody"
    URL2 += "&filter=withbody"


def pre_tag(intake):
    """Picks the value of date between <pre></pre>"""
    pattern = re.compile(r"<pre>(.*)</pre>", re.DOTALL)
    matches = pattern.search(intake)
    return matches.group(1)


def code_pre_tag(intake):
    """Picks the value of date between <code></pre>.
    This is as a result of how the data is formatted!
    """
    pattern = re.compile(r"<code>(.*)</pre>", re.DOTALL)
    matches = pattern.search(intake)
    return matches.group(1)


try:
    # verify that all supplied values are integers

    # QUESTION_1 = ">> Hello! Please provide a list of integers.\n>> "
    # integers_list = list(map(int, input(QUESTION_1).split(", ")))

    integers_list = list(map(int, sys.argv[1].split(", ")))
    print(">> Thanks. Fetching a random bubble sort implementation. Fingers crossed.")

    response = urllib3.PoolManager().request("GET", URL)

    if (
        response.status == 200
        and response.headers["Content-Type"] == "application/json; charset=utf-8"
    ):
        response = json.loads(response.data.decode("utf-8"))

        for item in response["items"]:
            # 47987412 is the question_id of the implementation
            # I intend to use
            if item["is_answered"] and item["question_id"] == 47987412:
                url = URL2.format(item["question_id"])

                response = HTTP.request("GET", url)

                if (
                    response.status == 200
                    and response.headers["Content-Type"]
                    == "application/json; charset=utf-8"
                ):
                    response = json.loads(response.data.decode("utf-8"))
                    data = response.get("items")[1].get("body")
                    bubble_sort_implementation = (
                        code_pre_tag(pre_tag(data))
                        .replace("</code>", "")
                        .replace("&gt;", ">")
                    )

                    # extra processing is attached to the end of the code
                    # to ensure the output is formatted as needed
                    bubble_sort_implementation = (
                        re.sub(
                            r"\[.*\]",
                            str(integers_list),
                            bubble_sort_implementation,
                            count=1,
                        )
                        + "print('>> ' + ', '.join([str(_) for _ in foo]))"
                    )

                    bubble_sort_implementation = compile(
                        bubble_sort_implementation, "bubble_sort_implementation", "exec"
                    )
                    exec(bubble_sort_implementation)
except ValueError:
    print(">> Sample input: 4, 51, 62, 45, 31, 90, 42, 28, 96, 65, 33, 73")

