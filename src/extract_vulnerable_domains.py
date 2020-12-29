import sys

def peek_line(fp):
    pos = fp.tell()
    line = fp.readline()
    fp.seek(pos)
    return line

def find_domain_names(fp):
    vulnerable_domains = []
    total_domains = 0
    line = fp.readline()
    while line:
        lines = line.strip().split(" ")
        if len(lines) > 1 and lines[0].isnumeric():
            total_domains += 1
            next_line = peek_line(fp).strip().split(" ")
            if len(next_line) == 1:
                vulnerable_domain = (lines[0], lines[1])
                vulnerable_domains.append(vulnerable_domain)
                print(vulnerable_domain)

        line = fp.readline()

    return vulnerable_domains, total_domains

def main():
    if len(sys.argv) < 2:
        print("Please input the name of the input file as a command line argument")
        return
    file_name = sys.argv[1]
    with open(file_name) as fp:
        domains, total_domains = find_domain_names(fp)
    num_vulnerable = len(domains)
    print("num domains:", num_vulnerable)
    print("percentage of vulnerable domains:", str((num_vulnerable / total_domains) * 100) + "%")

if __name__ == "__main__":
    main()
