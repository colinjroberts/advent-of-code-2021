import string

def get_input_as_list(input_filename, type):
    output = []
    with open(input_filename) as f:
        output.extend(list(f))

    if type == "raw":
        return [x for x in output]
    elif type == "string":
        return [x.strip() for x in output]
    elif type == "int":
        int_output = []
        for item in output:
            while not item.isnumeric():
                item = item.strip(string.ascii_letters)
                item = item.strip()
            int_output.append(int(item.strip()))
        return int_output