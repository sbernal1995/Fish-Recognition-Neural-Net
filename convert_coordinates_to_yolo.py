import os
import shutil
from PIL import Image, ImageOps
import yaml

# Función para crear el mapeo de especies a IDs
def create_species_id_mapping(input_file, output_file):
    species_to_id = {}
    current_id = 0

    with open(input_file, 'r') as file:
        for line in file:
            species_name = line.strip()
            if species_name not in species_to_id:
                species_to_id[species_name] = current_id
                current_id += 1

    with open(output_file, 'w') as file:
        yaml.dump({
            'nc': len(species_to_id),
            'names': list(species_to_id.keys())
        }, file)

    return species_to_id

# Función para redimensionar las imágenes y ajustar las coordenadas de los bounding boxes
def resize_image_and_adjust_bbox(image_path, label_path, output_image_dir, output_label_dir, target_size, species_to_id):
    # Cargar la imagen
    with Image.open(image_path) as img:
        img_width, img_height = img.size
        if img_width > target_size[0] or img_height > target_size[1]:
            img.thumbnail(target_size, Image.LANCZOS)
        
        img_padded = ImageOps.pad(img, target_size, color='white')
    
    # Calcular los factores de escala
    scale_x = img_padded.size[0] / img_width
    scale_y = img_padded.size[1] / img_height
    
    # Guardar la imagen redimensionada
    img_padded.save(os.path.join(output_image_dir, os.path.basename(image_path)))
    
    # Ajustar las coordenadas de los bounding boxes
    yolo_lines = []
    with open(label_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            species_name = parts[0]
            x_min, y_min, x_max, y_max = map(int, parts[1:])
            
            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
            width = x_max - x_min
            height = y_max - y_min
            
            # Convertir a coordenadas normalizadas
            x_center = (x_center * scale_x) / target_size[0]
            y_center = (y_center * scale_y) / target_size[1]
            width = (width * scale_x) / target_size[0]
            height = (height * scale_y) / target_size[1]
            
            class_id = species_to_id[species_name]
            yolo_lines.append(f"{class_id} {x_center} {y_center} {width} {height}")
    
    # Guardar las anotaciones ajustadas
    with open(os.path.join(output_label_dir, os.path.basename(label_path)), 'w') as out_file:
        out_file.write("\n".join(yolo_lines))

# Función para crear la estructura de directorios y procesar las imágenes
def create_yolo_structure(base_image_dir, base_bbox_dir, output_image_dir, output_label_dir, target_size, species_to_id):
    if not os.path.exists(output_image_dir):
        os.makedirs(output_image_dir)
    if not os.path.exists(output_label_dir):
        os.makedirs(output_label_dir)
    
    image_count = 0  # Contador de imágenes procesadas
    
    for family_name in os.listdir(base_image_dir):
        family_image_dir = os.path.join(base_image_dir, family_name)
        family_bbox_dir = os.path.join(base_bbox_dir, family_name)
        
        if not os.path.isdir(family_image_dir) or not os.path.isdir(family_bbox_dir):
            continue
        
        for img_file in os.listdir(family_image_dir):
            img_name, img_ext = os.path.splitext(img_file)
            bbox_file = os.path.join(family_bbox_dir, img_name + '.txt')
            
            if os.path.exists(bbox_file):
                resize_image_and_adjust_bbox(
                    os.path.join(family_image_dir, img_file),
                    bbox_file,
                    output_image_dir,
                    output_label_dir,
                    target_size,
                    species_to_id
                )
                image_count += 1
                print(f"Procesando imagen {image_count}: {img_file}")

# Rutas
base_image_dir = "E:/Downloads/fishnet/Image_Library"
base_bbox_dir = "E:/Downloads/FishNet-main/FishNet-main/bbox/all_family"
output_image_dir = "E:/Downloads/output_dataset/images"
output_label_dir = "E:/Downloads/output_dataset/labels"
target_size = (640, 640)  # Tamaño de redimensionamiento para YOLO

# Crear el mapeo de especies a IDs
input_species_file = "E:/Downloads/species_names.txt"
output_yaml_file = "E:/Downloads/dataset.yaml"
species_to_id = create_species_id_mapping(input_species_file, output_yaml_file)

# Procesar las imágenes y anotaciones
create_yolo_structure(base_image_dir, base_bbox_dir, output_image_dir, output_label_dir, target_size, species_to_id)
