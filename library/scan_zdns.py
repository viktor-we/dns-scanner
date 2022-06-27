import os
import sys

call_with_alexa= "~/zdns/zdns/zdns {rr_type} -name-servers 1.1.1.1 -output-file {output_file} -input-file {input_file} -alexa"
call_no_alexa= "~/zdns/zdns/zdns {rr_type} -name-servers 1.1.1.1 -output-file {output_file} -input-file {input_file}"

def main(rr_type, input_file_url, output_file_url, alexa_flag):

    print(f"Now scanning {rr_type}")

    if (alexa_flag=="True"):
        os.system(call_with_alexa.format(rr_type = rr_type, output_file = output_file_url, input_file = input_file_url))
    else:
        os.system(call_no_alexa.format(rr_type = rr_type, output_file = output_file_url, input_file = input_file_url))
    
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])