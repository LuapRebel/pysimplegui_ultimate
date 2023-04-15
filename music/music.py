import base64
from io import BytesIO
from pathlib import Path
from PIL import Image
from pygame import mixer, time
import PySimpleGUI as sg


def base64_image_import(path):
    image = Image.open(path)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue())
    return b64


mixer.init()
clock = time.Clock()

path = sg.popup_get_file("Open", no_window=True)
song_name = Path(path).stem
song = mixer.Sound(path)

# timer
song_length = int(song.get_length())
time_since_start = 0
pause_amount = 0
playing = False

sg.theme("reddit")
dir_path = Path(__file__).parent
play_layout = [
    [sg.VPush()],
    [sg.Push(), sg.Text(song_name, font="Arial 20"), sg.Push()],
    [sg.VPush()],
    [
        sg.Push(),
        sg.Button(
            image_data=base64_image_import(f"{dir_path}/play.png"),
            button_color="white",
            border_width=0,
            key="-PLAY-",
        ),
        sg.Push(),
        sg.Button(
            image_data=base64_image_import(f"{dir_path}/pause.png"),
            button_color="white",
            border_width=0,
            key="-PAUSE-",
        ),
        sg.Push(),
    ],
    [sg.VPush()],
    [sg.Progress(song_length, size=(20, 20), key="-PROGRESS-")],
]
volume_layout = [
    [sg.Slider(range=(0, 100), default_value=100, orientation="h", key="-VOLUME-")]
]

layout = [
    [sg.VPush()],
    [
        sg.Push(),
        sg.TabGroup([[sg.Tab("Play", play_layout), sg.Tab("Volume", volume_layout)]]),
        sg.Push(),
    ],
    [sg.VPush()],
]

window = sg.Window("Music Player", layout)

while True:
    event, values = window.read(timeout=1)
    if event == sg.WIN_CLOSED:
        break
    if playing:
        time_since_start = time.get_ticks()
        window["-PROGRESS-"].update((time_since_start - pause_amount) // 1000)
    if event == "-PLAY-":
        playing = True
        pause_amount += time.get_ticks() - time_since_start
        if mixer.get_busy() == False:
            song.play()
        else:
            mixer.unpause()

    if event == "-PAUSE-":
        playing = False
        mixer.pause()
    song.set_volume(values["-VOLUME-"] / 100)


window.close()
