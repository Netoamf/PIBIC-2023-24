from PIL import Image, ImageEnhance
from art import text2art
import os

def ascii_art(image_path, new_width=55, contrast_factor=1.0):
    # Mapeamento de escala de cinza com caracteres de blocos
    chars = ["█", "▓", "▒", "░", " "]
    num_chars = len(chars)
    
    # Abrindo a imagem
    img = Image.open(image_path)
    
    # Convertendo para escala de cinza
    img = img.convert('L')
    
    # Aumentando o contraste
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast_factor)
    
    # Redimensionando a imagem mantendo a proporção
    width, height = img.size
    aspect_ratio = height / float(width)
    new_height = int(aspect_ratio * new_width * 0.45)
    img = img.resize((new_width, new_height))
    
    # Convertendo pixels para caracteres ASCII
    pixels = img.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += chars[pixel * num_chars // 256]
    
    ascii_str_len = len(ascii_str)
    
    # Dividindo a string ASCII em várias linhas de acordo com a largura
    ascii_img = "\n".join([ascii_str[i:i+new_width] for i in range(0, ascii_str_len, new_width)])
    
    return ascii_img

def print_centered_ascii_art(image_path, new_width=55, contrast_factor=1.0):
    ascii_img = ascii_art(image_path, new_width, contrast_factor)
    
    # Obtém a largura do terminal
    terminal_width = os.get_terminal_size().columns
    
    # Centraliza cada linha
    centered_ascii_img = "\n".join(line.center(terminal_width) for line in ascii_img.splitlines())
    
    print(centered_ascii_img)
    
    return ascii_img


def print_centered_text_art(text, font="tarty1"):
    # Gera o texto em arte ASCII
    ascii_art = text2art(text, font=font)
    
    # Obtém a largura do terminal
    terminal_width = os.get_terminal_size().columns
    
    # Centraliza cada linha da arte ASCII
    centered_ascii_art = "\n".join(line.center(terminal_width) for line in ascii_art.splitlines())
    
    print(centered_ascii_art)

if __name__ == "__main__":
    path = "pic_logo.jpg"
    print_centered_ascii_art(path, new_width=55, contrast_factor=1.0)
    print_centered_text_art("Welcome to UParser", font="tarty1")
    print_centered_text_art("Autoria: Antonio Morais e Joao Paulo Cyrino \n Instituição: Universidade Federal da Bahia", font="tiny2")

