import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras import layers, models

# Ścieżka do folderu z danymi
dataset_path = "path_to_your_dataset"  # Zmień to na ścieżkę do folderu z danymi

# Wczytanie zbioru danych
train_dataset = image_dataset_from_directory(
    dataset_path,
    image_size=(500, 500),  # Zmieniamy rozmiar obrazów na 500x500, dostosuj to do swoich potrzeb
    batch_size=32,  # Rozmiar partii
    label_mode="int",  # Używamy etykiet numerycznych (0 dla diody, 1 dla rezystora, 2 dla źródła zasilania)
    validation_split=0.2,  # 20% danych na walidację
    subset="training",  # 80% danych na trening
    seed=123  # Ziarno dla powtarzalności
)

# Zbiór walidacyjny
val_dataset = image_dataset_from_directory(
    dataset_path,
    image_size=(500, 500),  # Zmieniamy rozmiar obrazów na 500x500
    batch_size=32,
    label_mode="int",  # Etykiety numeryczne
    validation_split=0.2,
    subset="validation",  # 20% na walidację
    seed=123
)

# Budowa modelu CNN
model = models.Sequential([
    # Warstwa konwolucyjna 1
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(500, 500, 3)),  # Dopasowanie rozmiaru wejścia
    layers.MaxPooling2D(2, 2),
    
    # Warstwa konwolucyjna 2
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    
    # Warstwa konwolucyjna 3
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(2, 2),
    
    # Spłaszczanie obrazu do jednego wektora
    layers.Flatten(),
    
    # Warstwa w pełni połączona
    layers.Dense(128, activation='relu'),
    
    # Warstwa wyjściowa (klasyfikacja wieloklasowa)
    layers.Dense(3, activation='softmax')  # 3 klasy: dioda, rezystor, źródło zasilania
])

# Kompilacja modelu
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',  # Używamy funkcji strat dla wieloklasowej klasyfikacji
              metrics=['accuracy'])

# Trenowanie modelu
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=10  # Liczba epok
)

# Zapisanie modelu
model.save("model_dioda_rezystor_zrodlo_zasilania.h5")

# Testowanie modelu na nowym obrazie
test_image_path = 'path_to_test_image.jpg'
img = tf.keras.preprocessing.image.load_img(test_image_path, target_size=(500, 500))  # Dopasowanie rozmiaru obrazu
img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Dodajemy batch dimension

predictions = model.predict(img_array)

# Wyświetlanie wyników
class_names = ['dioda', 'rezystor', 'zrodlo_zasilania']
predicted_class = class_names[tf.argmax(predictions[0]).numpy()]
print(f"Model przewiduje: {predicted_class}")