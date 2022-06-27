import json
import sys

def main(rr_type, input_file_url, output_file_url, eval_file_url):

    print(f"Now extracting data from {rr_type}")
    
    list_answers = list()
    results_status = dict()

    input_file = open(input_file_url, "r")
    output_file = open(output_file_url, "w")
    eval_file = open(eval_file_url, "w")

    while True:
        line = input_file.readline()
        if not line:
            break
        json_string = json.loads(line)
        if json_string["status"] in results_status:
            results_status[json_string["status"]] +=1
        else:
            results_status[json_string["status"]] = 1
        if json_string["status"] == "NOERROR":
            if "answers" in json_string["data"]:
                for answer in json_string["data"]["answers"]:
                    list_answers.append(json.dumps(answer) + "\n")

    output_file.writelines(list_answers)
    eval_file.write(str(results_status))

    input_file.close()
    output_file.close()
    eval_file.close()

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])