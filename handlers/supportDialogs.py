from PyQt5.QtWidgets import QFileDialog

def open_file(file_filter=None):
    response = QFileDialog.getOpenFileName(
        caption='Открыть файл',
        filter=file_filter,
        # initialFilter='Text File (*.txt)'
    )
    if response[0]:
        return response[0]
    else:
        return 0

def save_file(file_filter=None):
    if file_filter is None:
        file_filter = 'Text File (*.txt)'
    response = QFileDialog.getSaveFileName(
        caption='Сохранить файл',
        filter=file_filter,
        initialFilter=file_filter,
        directory='data_file.txt'
    )
    if response[0]:
        return response[0]
    else:
        return 0
