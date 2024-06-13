import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def load_yolo_label(label_path):
    with open(label_path, 'r') as file:
        lines = file.readlines()
        boxes = []
        for line in lines:
            class_id, x_center, y_center, width, height = map(float, line.strip().split())
            boxes.append((class_id, x_center, y_center, width, height))
        return boxes

def visualize_bounding_boxes(image_path, label_path):
    # Load image
    image = Image.open(image_path)
    img_width, img_height = image.size
    
    # Load YOLO labels
    boxes = load_yolo_label(label_path)
    
    # Create figure and axes
    fig, ax = plt.subplots(1)
    ax.imshow(image)
    
    # Draw bounding boxes
    for box in boxes:
        class_id, x_center, y_center, width, height = box
        # Convert normalized coordinates to actual pixel values
        x_center *= img_width
        y_center *= img_height
        width *= img_width
        height *= img_height
        # Calculate the top-left corner of the bounding box
        x_min = x_center - width / 2
        y_min = y_center - height / 2
        # Create a Rectangle patch
        rect = patches.Rectangle((x_min, y_min), width, height, linewidth=2, edgecolor='r', facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)
    
    plt.show()

# Ejemplo de uso
image_path = "E:/Downloads/output_dataset/images/0d629c2b-14fb-4ae8-b58c-4f9ae78abace.jpg"  # Cambia esta ruta a la ruta de una imagen específica
label_path = "E:/Downloads/output_dataset/labels/0d629c2b-14fb-4ae8-b58c-4f9ae78abace.txt"  # Cambia esta ruta a la ruta del label correspondiente

visualize_bounding_boxes(image_path, label_path)
