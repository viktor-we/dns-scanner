import sys
import json
import subprocess


def main(input_https_url, input_svcb_url, output_data_url, output_result_url):

    input = open(input_https_url, "r")
    results_https = input.read().split("\n")
    input.close()

    input = open(input_svcb_url, "r")
    results_svcb = input.read().split("\n")
    input.close()

    echconfig_list = list()

    for result in results_https:
        if not result:
            break
        
        if "echconfig" in result:
            echconfig_list.append(result + "\n")

    for result in results_svcb:
        if not result:
            break
    
        if "echconfig" in result:
            echconfig_list.append(result + "\n")

    output_data_file = open(output_data_url, "w")
    output_data_file.writelines(echconfig_list)
    output_data_file.close()

    output_result_file = open(output_result_url, "w")
    output_result_file.write(str(len(echconfig_list)))
    output_result_file.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])