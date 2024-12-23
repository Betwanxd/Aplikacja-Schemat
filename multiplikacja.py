from PIL import Image
import os

# Funkcja do obrócenia obrazu o 90 stopni i zapisania go w nowym pliku
def rotate_and_save(img, output_path_prefix, rotation_number):
    rotated_img = img.rotate(90 * rotation_number, expand=True)  # Obracamy o 90 stopni
    rotated_img.save(f"{output_path_prefix}_rotation_{rotation_number * 90}.png")
    print(f"Obraz zapisano jako: {output_path_prefix}_rotation_{rotation_number * 90}.png")

# Funkcja do przetworzenia obrazu - obrót + odbicia
def process_image(input_path, output_path_prefix):
    with Image.open(input_path) as img:
        # 1. Obrót o 90, 180, 270, 360 stopni
        for i in range(4):
            rotate_and_save(img, output_path_prefix, i + 1)

        # 2. Odbicie horyzontalne + obrót
        flipped_horizontal = img.transpose(Image.FLIP_LEFT_RIGHT)  # Odbicie w poziomie
        for i in range(4):
            rotate_and_save(flipped_horizontal, f"{output_path_prefix}_horizontal", i + 1)


# Funkcja do przetworzenia wszystkich obrazów w folderze
def process_images_in_directory(input_directory, output_directory):
    # Sprawdzenie, czy katalog wyjściowy istnieje, jeśli nie, tworzymy go
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Iteracja przez wszystkie pliki w katalogu
    for filename in os.listdir(input_directory):
        input_path = os.path.join(input_directory, filename)
        if os.path.isfile(input_path):
            # Określenie ścieżki do zapisanego obrazu (prefiks dla wyjściowego pliku)
            output_path_prefix = os.path.join(output_directory, filename.split('.')[0])
            # Przetwarzanie obrazu
            process_image(input_path, output_path_prefix)

# Przykład użycia
input_dir = 'C:/Users/Konrad/Desktop/Schemat_Baza_Danych/Dioda' 
output_dir = 'C:/Users/Konrad/Desktop/Schemat_Baza_Danych/Dioda_rotate' 

# Przetwórz wszystkie obrazy w folderze
process_images_in_directory(input_dir, output_dir)