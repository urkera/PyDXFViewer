def read_ncn(file_name):
    with open(file_name, 'r') as f:
        content = f.read()
    data = [d.strip().split()[:-7] for d in content.strip().split('\n')]
    return [[p[0], float(p[1]), float(p[2]), float(p[3])] for p in data]


def euclidean_dist(p1, p2):
    delta = p1 - p2.point
    return delta.x() ** 2 + delta.y() ** 2
