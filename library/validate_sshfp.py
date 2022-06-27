import sys
import json
import subprocess


def main(input_file_url, output_ssh_url, output_data_url, output_result_url):

    input = open(input_file_url, "r")
    results = input.read().split("\n")
    input.close()

    fingerprints = dict()

    # Classification

    ## fingerprint from SSH connection not in SSHFP RR
    not_in_ssh = list()

    ## no SSH connection
    no_ssh_connection = list()

    ## fingerprint right
    fingerprint_in_ssh = list()

    for result in results:
        if not result:
            break

        result_json = json.loads(result)

        domain = result_json["name"]

        if domain not in fingerprints:
            subprocess_scan = subprocess.Popen(f"ssh-keyscan -D {domain}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
            output, error = subprocess_scan.communicate()
            fingerprints[domain] = output

        if not fingerprints[domain]:
            no_ssh_connection.append(result_json)
        else:
            if result_json["fingerprint"] not in fingerprints[domain]:
                not_in_ssh.append(result_json)
            else:
                fingerprint_in_ssh.append(result_json)

    output_ssh_file = open(output_ssh_url, "w")
    json.dump(fingerprints, output_ssh_file, indent=4)
    output_ssh_file.close()

    data_dict = {"not_in_ssh": not_in_ssh, "no_ssh_connection": no_ssh_connection}
    output_data_file = open(output_data_url, "w")
    json.dump(data_dict, output_data_file, indent= 4)
    output_data_file.close()

    result_dict = {"not_in_ssh": len(not_in_ssh), "no_ssh_connection": len(no_ssh_connection)}
    output_result_file = open(output_result_url, "w")
    json.dump(result_dict, output_result_file, indent= 4)
    output_result_file.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])