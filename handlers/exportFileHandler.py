# import os
def export_mtd(file_name: str, mtd_data: tuple):
    T_list, Rot_list, Pht_list, NT = mtd_data
    with open(file_name, 'w') as file:
        file.write('sqrtT  RoT  Pht \n')
        data = [' '.join([str(round(T_list[i], 2)), str(round(Rot_list[i], 2)), str(round(Pht_list[i], 2))]) for i in range(NT)]
        file.write('\n'.join(data))
    return

def export_tdem(file_name: str, tdem_data: tuple):
    ro_t, kernel_abs, w_list, kernel_ifft_abs, T, dHdt_V = tdem_data
    result = ['\t'.join(['Ro(t)', 'Efi(w)', 'w', 'Efi(t)', 't(c)', 'dH/dt(В)'])]
    for i in range(len(w_list)):
        result.append([ro_t[i], kernel_abs[i], w_list[i], kernel_ifft_abs[i], T[i], dHdt_V[i]])

    for i in range(1, len(result)):
        result[i] = [str(x) for x in result[i]]
        result[i] = '\t'.join(result[i])

    result_text = '\n'.join(result)
    with open(file_name, 'w') as file:
        file.write(result_text)
    return
