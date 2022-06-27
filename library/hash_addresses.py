import hashlib
import sys

def main(input_file_location, output_file_location):

    input_file = open(input_file_location,"r+")
    input = input_file.read()

    addresses = input.split('\n')

    hashed_addresses = list()

    for address_string in addresses:

        address = address_string.replace("'","")

        if "@" not in address:
            print(f"Invalid address: {address}")
        else:
            local_part = address.split('@')[0]
            domain = address.split('@')[1]

            local_part = hashlib.sha256(local_part.encode('utf-8')).hexdigest()[:56]

            hashed_addresses.append(f"{local_part}._openpgpkey.{domain}" + "\n")

    output_file = open(output_file_location, 'w')
    output_file.writelines(hashed_addresses)
    output_file.close()

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])