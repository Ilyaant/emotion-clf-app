from emotion_model import predict
import PySimpleGUI as sg
from PIL import Image
import io


def prepare_image(path):
    res = Image.open(path)
    res.thumbnail((400, 400))
    bio = io.BytesIO()
    res.save(bio, format="PNG")
    return bio.getvalue()


def create_help_window():
    layout_help = [
        [sg.Text('Нажмите на кнопку "Выбрать файл...", чтобы перейти к поиску необходимой фотографии.')],
        [sg.Text('Нажмите на кнопку "Распознать эмоцию" и ожидайте окончания выполнения процесса.')],
        [sg.Button('Закрыть')]
    ]
    return sg.Window('Помощь', layout_help)


layout = [
    [sg.Text('Пожалуйста, выберите изображение:')],
    [sg.InputText(key='-FILEPATH-'), sg.FileBrowse(button_text='Выбрать файл...',
                                                   file_types=[('JPG Files', '*.jpg'), ('PNG Files', '*.png'), ('JPEG Files', '*.jpeg')])],
    [sg.Text('Ваше изображение:')],
    [sg.Image(key='-IMAGE-')],
    [sg.Text('Распознанная эмоция:', key='-EMOTION-')],
    [sg.Button('Распознать эмоцию'), sg.Button('Выход'), sg.Push(), sg.Button('Помощь')]
]

window = sg.Window('Распознавание эмоции на фото', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Выход':
        break

    if event == 'Распознать эмоцию':
        img = prepare_image(values['-FILEPATH-'])
        window['-IMAGE-'].update(data=img)
        emotion = predict.make_prediction(values['-FILEPATH-'])['preds_name']
        window['-EMOTION-'].update(f'Распознанная эмоция: {emotion}')

    if event == 'Помощь':
        window_help = create_help_window()
        while True:
            event2, values2 = window_help.read()
            if event2 == 'Закрыть' or event2 == sg.WINDOW_CLOSED:
                break
        window_help.close()

window.close()
