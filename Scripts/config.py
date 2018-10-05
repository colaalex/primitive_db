"""
Модуль, содержащий значения констант
"""
import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

parent = str(Path(__file__).parents[1])

primary_color = '#03A9F4'  # цвет фона
accent_color = '#607D8B'  # цвет кнопок
button_fore = '#fff'  # цвет текста на кнопках
button_font = 'Calibri 15'  # шрифт на кнопках
text_font = 'Calibri 15'  # цвет остального текста с указанием размера
primary_text = '#212121'  # цвет основого текста
secondary_text = '#757575'  # цвет вспомогательного текста
start_geometry = '600x150'  # размеры первого экрана
bd_path = parent + '\\Data\\dic.shl.dat'  # путь до файла с базой данных
bd_path_2 = parent + '\\Data\\dic.shl'
color_red = '#ff0000'  # код красного цвета
tree_width = 110  # ширина колонки TreeView
button_relief = 'flat'  # рельеф кнопки

# пути к картинкам
img_magnify = parent + '\\Graphics\\magnify.png'
img_pencil = parent + '\\Graphics\\pencil.png'
img_close = parent + '\\Graphics\\close.png'
img_info = parent + '\\Graphics\\info.png'
img_file = parent + '\\Graphics\\file.png'
img_del = parent + '\\Graphics\\delete.png'
favicon = parent + '\\Graphics\\database.ico'

output_dir = parent + '\\Output'

text1 = 'Если какое-либо поле оставить пустым, будут возвращены все элементы, удовлетворяющие остальным критериям поиска'
