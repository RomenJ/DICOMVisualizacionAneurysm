import os
import numpy as np
import pydicom
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Función para ordenar archivos numéricamente
def natural_key(filename):
    import re
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', filename)]

# Listar los archivos en la carpeta 'imagedata_Set'
file_list = os.listdir('imagedata_Set')
print(file_list)

# Filtrar solo los archivos .dcm
dcm_files = sorted([f for f in file_list if f.endswith('.dcm')], key=natural_key)
print(dcm_files)

# Leer cada archivo DICOM y agregarlo a una lista
images = []
file_names = []  # Lista para almacenar los nombres de los archivos
for dcm_file in dcm_files:
    dcm_path = os.path.join('imagedata_Set', dcm_file)
    dcm_data = pydicom.dcmread(dcm_path)
    
    # Obtener píxeles y aplicar ajuste de ventana y nivel (windowing)
    img = dcm_data.pixel_array
    window_center = dcm_data.WindowCenter if 'WindowCenter' in dcm_data else img.mean()
    window_width = dcm_data.WindowWidth if 'WindowWidth' in dcm_data else img.max() - img.min()
    img_min = window_center - window_width / 2
    img_max = window_center + window_width / 2
    img = np.clip(img, img_min, img_max)
    img = (img - img_min) / (img_max - img_min) * 255.0
    img = img.astype(np.uint8)
    
    # Redimensionar todas las imágenes al mismo tamaño
    target_size = (512, 512)  # Definir tamaño objetivo
    img_resized = np.array(Image.fromarray(img).resize(target_size, Image.LANCZOS))
    
    images.append(img_resized)
    file_names.append(dcm_file)

# Convertir la lista de imágenes a un array 3D (volumen)
vol = np.stack(images, axis=0)
print('Shape of the volume:', vol.shape)

# Configurar la figura y el eje para la animación
fig, ax = plt.subplots()
ax.set_title('Vista axial (XY) del volumen')
ax.axis('off')

# Añadir texto para mostrar el número de lámina y nombre del archivo
text = ax.text(0.05, 0.95, '', color='blue', fontsize=20, fontname='Arial', transform=ax.transAxes, va='top')

# Función para actualizar la imagen en cada cuadro de la animación
def update(frame):
    vmin = vol[frame, :, :].min()
    vmax = vol[frame, :, :].max()
    ax.imshow(vol[frame, :, :], cmap='gray', vmin=vmin, vmax=vmax)
    text.set_text(f'Lámina {frame + 1} - {file_names[frame]}')

# Crear la animación
# Incrementar el intervalo en un 30%
interval = 250 * 1.3
ani = animation.FuncAnimation(fig, update, frames=range(vol.shape[0]), interval=interval, repeat=False)

# Mostrar la animación
plt.show()
