from time import sleep
import requests
import json
import sys
import time

def main(input_file_url, output_file_url, eval_file_url):

    username = "viktor-we"
    token = "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"

    input_file = open(input_file_url,"r+")
    input = input_file.read()
    input_file.close()
    urls = input.split('\n')

    urls_count = len(urls)

    addresses = set()

    start_time_current_hour = time.time()

    for url in urls:
        url_splitted = url.split('/')
        owner = str(url_splitted[-2])
        repo = str(url_splitted[-1])

        index = 1
        max = 50
        commits_per_page = 100
        full_response = True

        print(f"Now scanning {owner}/{repo} - {urls.index(url)}/{urls_count}")

        while index <= max and full_response:
            url_commits = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page={commits_per_page}&page={index}"
            response = requests.get(url_commits, auth=(username,token))

            response_parsed = response.json()

            if response.text.startswith("{\"message\""):
                print("API Calls exceeded for " + username)
                print("Waiting for limit clearing")

                current_time = time.time()
                time_to_wait = 60 * 60 - (current_time - start_time_current_hour) + 5

                sleep(time_to_wait)

                start_time_current_hour = time.time()
                break

            for commit in response_parsed:
                if commit["commit"]["verification"]["verified"]:
                    if commit["commit"]["committer"]["name"] != "GitHub":
                        addresses.add(commit["commit"]["author"]["email"] + "\n") 

            index += 1

            if len(response_parsed) < 100:
                full_response = False


    output_file = open(output_file_url, "w")
    output_file.writelines(addresses)
    output_file.close()

    eval_file = open(eval_file_url, "w")
    eval_file.write(str(len(addresses)))
    eval_file.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
