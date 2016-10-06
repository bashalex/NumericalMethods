
def integrate_p_func():
    try:
        with open('./data/p_func.csv') as f:
            x = [float(e) for e in f.readline().split()]
            y = [float(e) for e in f.readline().split()]
            integral = [0 for i in range(len(x))]
    except FileNotFoundError:
        print("File './data/p_func.csv' Not Found!")
        return -1
    return integral
