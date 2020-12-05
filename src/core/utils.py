def read_ncn(file_name):
    with open(file_name, 'r') as f:
        content = f.read()
    data = [d.strip().split()[:-7] for d in content.strip().split('\n')]
    return [[p[0], float(p[1]), float(p[2]), float(p[3])]for p in data]