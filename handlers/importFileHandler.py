import numpy as np

def import_model(file_name):
    def is_name(str):
        try:
            float(str)
            return False
        except ValueError:
            return True
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
        elif is_name(file_type):
            name = f.readline()
            data = f.read().split('\n')
            Ro_list = []
            H_list = []
            for pair in data:
                rh = pair.split()
                Ro_list.append(rh[0])
                H_list.append(rh[1])
            return 'one row', Ro_list, H_list
        else:
            return None

def import_sec(file_name):
    return np.loadtxt(file_name)

