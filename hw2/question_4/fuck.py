import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Help: ./fuck.py <filename>")
        exit(0)

    filename = sys.argv[1]
    f = open(filename, "r")
    data = f.read().replace("\r\n", "\n")
    f.close()

    f = open(filename + ".fuck", "w")
    # f = open(filename, "w")
    f.write(data)
    f.close()
