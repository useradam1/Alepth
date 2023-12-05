from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
from fontTools.ttLib import TTFont
from math import sqrt

# Получение списка всех поддерживаемых символов в шрифте
font = TTFont("NotoSans-Light.ttf")
supported_characters = []
for table in font['cmap'].tables:
    for codepoint, glyphname in table.cmap.items():
        supported_characters.append(chr(codepoint))
font.close()

count_of_characters : int = int(sqrt(len(supported_characters)))




# Количество квадратиков
width = 256
height = 256

# Размер и цвет квадратиков
square_size = 33
square_color = (255, 255, 255, 255)

square_vec2 = ((square_size*width)+1, (square_size*height)+1)


# Создание нового изображения
image = Image.new("RGBA", square_vec2, (0,0,0,0))
draw = ImageDraw.Draw(image)

'''
# Рисование квадратиков в сетке
for y in range(0, square_vec2[1], square_size):
    for x in range(0, square_vec2[0], square_size):
        draw.rectangle(
            [
                x, 
                y, 
                
                x + square_size, 
                y + square_size
            ], 
            outline = square_color
        )
#'''

# Открываем файл шрифта
font = ImageFont.truetype("NotoSans-Light.ttf", square_size*0.5)
offset = ((square_size*0.295),(square_size*0.1))
x,y=0,0


for char in supported_characters:
    x = ord(char) & (width-1)
    y = ord(char) // width
    draw.text(
        xy = ((x*(square_size))+offset[0], (y*(square_size))+offset[1]),
        text = char, 
        fill = square_color, 
        font = font
    )
    '''
    draw.text(
        xy = ((x*(square_size+1))+offset[0], (y*(square_size+1))+offset[1]),
        text = f'{y}', 
        fill = square_color, 
        #font = font
    )#'''

#'''
image.save("font.png")
image.show()
image.close()
#'''


'''
# Преобразуем изображение в оттенки серого
image_gray = image.convert("L")

# Проходим по каждому пикселю и преобразуем его в черный или белый
threshold = 75  # Пороговое значение для бинаризации
image_bw = image_gray.point(lambda p: 0 if p < threshold else 255, "1")

# Сохраняем альфа-канал
alpha_channel = image.split()[3]

# Преобразуем альфа-канал в 1 бит
alpha_bw = alpha_channel.point(lambda p: 0 if p < threshold else 255, "1")

# Создаем новое изображение с альфа-каналом и черно-белыми каналами
final_image = Image.new("RGBA", image.size)
final_image.paste(image_bw, (0, 0), alpha_bw)

# Сохраняем изображение с альфа-каналом и глубиной цвета 1 бит
final_image.save("font.png")

final_image.show()

# Закрываем изображения
image.close()
image_gray.close()
image_bw.close()
alpha_bw.close()
final_image.close()
#'''