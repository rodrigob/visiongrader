name = "TestParser"

def describe():
    return "Just a test parser."

def recognize(file):
    fstline = file.readline()
    fstline = fstline.strip().rstrip()
    if fstline == "test_file_format":
        return True
    else:
        return False

def parse(file):
    ret = ResultData()
    return ret
