import os

def save_folder_names_to_file(directory, output_file):
    folder_names = []
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        if os.path.isdir(folder_path):
            folder_names.append(folder_name)
    
    with open(output_file, 'w') as file:
        for name in folder_names:
            file.write(f"{name}\n")

# Ejemplo de uso
directory = "E:/Downloads/fishnet/Image_Library"  # Cambia esta ruta a la ruta correcta en tu sistema
output_file = "E:/Downloads/folder_names.txt"  # Cambia esta ruta a donde quieres guardar el archivo

save_folder_names_to_file(directory, output_file)
