

# Starts a scan iteration
# input: 
# output: 


from datetime import datetime
import os
import sys
import time
from library import scan_zdns
from library import extract_zdns
from library import eval_zdns
from library import scan_git
from library import hash_addresses
from library import validate_sshfp
from library import validate_ech

resource_records = ["SSHFP", "CERT", "TXT", "HTTPS", "SVCB"]

files_answers_prefix = "post_scan-{}"
files_extractions_prefix = "post_extraction-{}"
files_data_prefix = "post_evaluation-{}"
files_evaluation_all_prefix = "evaluation-all-{}"
files_evaluation_data_prefix = "evaluation-data-{}"
files_addresses_github = "collected_addresses"
files_addresses_hashed = "hashed_addresses"

url_tranco_list = "resources/top-1m.csv"
url_repos = "resources/repos"

def main():

    start = time.time()
	
    #create folder with name containing current time
    current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    url_scan_dir = f"Scans/Scan{current_time}/"
    url_data_dir = f"{url_scan_dir}/data/"

    print(f"Output in: {url_scan_dir}")

    try:
        os.makedirs(url_scan_dir)
        os.makedirs(url_data_dir)
    except FileExistsError:
        print(f"Failed to create directory")

    # Scans of given resource records with ZDNS
    print(f"Phase 1: Scans of Resource Records")

    for rr in resource_records:
        scan_zdns.main(rr, url_tranco_list, url_data_dir + files_answers_prefix.format(rr), "True")

    print(f"Finished scans of Resource Records")

    # Extraction of scans
    print(f"Phase 2: Extraction of data in DNS answers")

    for rr in resource_records:
        extract_zdns.main(rr, url_data_dir + files_answers_prefix.format(rr), url_data_dir + files_extractions_prefix.format(rr), url_scan_dir + files_evaluation_all_prefix.format(rr))

    print(f"Finished extraction of data in DNS answers")

    # Evaluation of data, filtering out CNAME
    print(f"Phase 3: Evaluation of data in DNS answers")

    for rr in resource_records:
        eval_zdns.main(rr, url_data_dir + files_extractions_prefix.format(rr), url_data_dir + files_data_prefix.format(rr), url_scan_dir + files_evaluation_data_prefix.format(rr))

    print(f"Finished evaluation of data in DNS answers")

    # Scans of GitHub repos
    print(f"Phase 4: Scans of GitHub Repos for signed commits")

    scan_git.main(url_repos, url_data_dir + files_addresses_github, url_scan_dir + "eval_github")

    print(f"Finished scans of GitHub Repos for signed commits")

    # Evaluation of collected addresses
    print(f"Phase 5: Hashing and scanning OPENPGPKEY entries")

    hash_addresses.main(url_data_dir + files_addresses_github, url_data_dir + files_addresses_hashed)
    scan_zdns.main("OPENPGPKEY", url_data_dir + files_addresses_hashed, url_data_dir + files_answers_prefix.format("OPENPGPKEY"), "False")

    print(f"Finished hashing and scanning OPENPGPKEY entries")

    # Extraction of scans
    print(f"Phase 6: Extraction of data in OPENPGPKEY entries")
    
    extract_zdns.main("OPENPGPKEY", url_data_dir + files_answers_prefix.format("OPENPGPKEY"), url_data_dir + files_extractions_prefix.format("OPENPGPKEY"), url_scan_dir + files_evaluation_all_prefix.format("OPENPGPKEY"))

    print(f"Finished extraction of data in OPENPGPKEY entries")

    # Evaluation of data, filtering out CNAME
    print(f"Phase 7: Evaluation of data in OPENPGPKEY entries")

    eval_zdns.main("OPENPGPKEY", url_data_dir + files_extractions_prefix.format("OPENPGPKEY"), url_data_dir + files_data_prefix.format("OPENPGPKEY"), url_scan_dir + files_evaluation_data_prefix.format("OPENPGPKEY"))

    print(f"Finished Evaluation of data in OPENPGPKEY entries")

    # Validation of SSHFP RRs
    print(f"Phase 8: Validation of SSHFP RRs")

    validate_sshfp.main(url_data_dir + files_data_prefix.format("SSHFP"), url_data_dir + "SSH-fingerprint_dump", url_data_dir + "validation_data_SSHFP", url_scan_dir + "validation_SSHFP")

    print(f"Finished Validation of SSHFP RRs")

    # Validation of ECH
    print(f"Phase 8: Validation of ECH")

    validate_ech.main(url_data_dir + files_data_prefix.format("HTTPS"), url_data_dir + files_data_prefix.format("SVCB"), url_data_dir + "validation_data_ECH", url_scan_dir + "validation_ECH")

    print(f"Finished Validation of ECH")

    end = time.time()

    print(f"Ended scan in {end - start} seconds")

if __name__ == "__main__":
    main()