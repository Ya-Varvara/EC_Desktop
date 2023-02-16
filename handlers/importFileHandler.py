import numpy as np

def import_model(file_name):
    with open(file_name, 'r') as f:
        file_type = f.readline().lower()
        if ('dsaa' in file_type):
            Nx, Ny = map(int, f.readline().split(' '))
            x_min, x_max = map(float, f.readline().split(' '))
            y_min, y_max = map(float, f.readline().split(' '))
            z_min, z_max = map(float, f.readline().split(' '))
            z = np.fromfile(f, sep=' ').reshape([Ny, Nx])
            z[z > 1.7e38] = np.nan
            x = np.linspace(x_min, x_max, Nx)
            y = np.linspace(y_min, y_max, Ny)
            return 'dsaa', x, y, z, x_min, x_max, y_min, y_max, z_min, z_max, Nx, Ny
        else:
            N = int(file_type)
            Ro_list = [float(i) for i in f.readline().split()]
            H_list = [float(i) for i in f.readline().split()]
            return 'one row', N, Ro_list, H_list

def import_sec(file_name):
    return np.loadtxt(file_name)

