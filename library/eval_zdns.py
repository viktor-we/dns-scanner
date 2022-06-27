import json
import sys

def main(rr_type, input_file_url, output_file_url, eval_file_url):

    print(f"Now evaluating data from {rr_type}")

    data_answers = dict()
    data_filtered = list()

    input_file = open(input_file_url, "r")
    output_file = open(output_file_url, "w")
    eval_file = open(eval_file_url, "w")

    while True:
        line = input_file.readline()
        if not line:
            break
        json_string = json.loads(line)
        if json_string["type"] in data_answers:
            data_answers[json_string["type"]] +=1
        else:
            data_answers[json_string["type"]] = 1
        if json_string["type"] != "CNAME":
            data_filtered.append(json.dumps(json_string) + "\n")

    output_file.writelines(data_filtered)
    eval_file.write(str(data_answers))

    input_file.close()
    output_file.close()
    eval_file.close()

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
