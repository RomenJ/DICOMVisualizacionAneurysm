Este programa en Python está diseñado para procesar y visualizar archivos DICOM (Digital Imaging and Communications in Medicine), un formato estándar para almacenar y transmitir imágenes médicas. Utilizando varias bibliotecas, como os, numpy, pydicom, PIL, y matplotlib, el programa lee los archivos DICOM de una carpeta, procesa las imágenes y las muestra en una animación secuencial. A continuación, se detallan los pasos y las funciones clave del programa.

1. Importación de Bibliotecas
El programa comienza importando las bibliotecas necesarias:

os: Para manejar operaciones del sistema, como listar archivos en un directorio.
numpy: Para operaciones numéricas y de matriz.
pydicom: Para leer archivos DICOM.
PIL (Python Imaging Library): Para manejar y transformar imágenes.
matplotlib: Para visualización y animación de imágenes.
2. Función de Clave Natural
Se define una función natural_key para ordenar los nombres de los archivos numéricamente en lugar de lexicográficamente. Esta función utiliza expresiones regulares para dividir los nombres de los archivos en partes numéricas y alfabéticas, facilitando un ordenamiento más intuitivo.


def natural_key(filename):
    import re
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', filename)]
3. Listar y Filtrar Archivos DICOM
El programa lista todos los archivos en la carpeta imagedata_Set y filtra solo aquellos con la extensión .dcm. Los archivos filtrados se ordenan usando la función natural_key.



file_list = os.listdir('imagedata_Set')
dcm_files = sorted([f for f in file_list if f.endswith('.dcm')], key=natural_key)
4. Procesamiento de Imágenes DICOM
Para cada archivo DICOM, el programa:

Lee el archivo usando pydicom.dcmread.
Extrae los datos de píxeles y aplica el ajuste de ventana y nivel (windowing) para mejorar la visualización.
Redimensiona cada imagen a un tamaño objetivo de 512x512 píxeles utilizando la biblioteca PIL.
Almacena las imágenes procesadas y los nombres de los archivos en listas.
python
Copiar código
images = []
file_names = []
for dcm_file in dcm_files:
    dcm_path = os.path.join('imagedata_Set', dcm_file)
    dcm_data = pydicom.dcmread(dcm_path)
    img = dcm_data.pixel_array
    window_center = dcm_data.WindowCenter if 'WindowCenter' in dcm_data else img.mean()
    window_width = dcm_data.WindowWidth if 'WindowWidth' in dcm_data else img.max() - img.min()
    img_min = window_center - window_width / 2
    img_max = window_center + window_width / 2
    img = np.clip(img, img_min, img_max)
    img = (img - img_min) / (img_max - img_min) * 255.0
    img = img.astype(np.uint8)
    target_size = (512, 512)
    img_resized = np.array(Image.fromarray(img).resize(target_size, Image.LANCZOS))
    images.append(img_resized)
    file_names.append(dcm_file)
5. Creación del Volumen 3D
Las imágenes procesadas se apilan en una matriz tridimensional (volumen), donde cada imagen representa una lámina en el eje Z.


vol = np.stack(images, axis=0)
6. Configuración de la Animación
Se configura una figura y un eje utilizando matplotlib para mostrar la animación de las imágenes. Además, se añade un texto para mostrar el número de lámina y el nombre del archivo.


fig, ax = plt.subplots()
ax.set_title('Vista axial (XY) del volumen')
ax.axis('off')
text = ax.text(0.05, 0.95, '', color='blue', fontsize=20, fontname='Arial', transform=ax.transAxes, va='top')
7. Función de Actualización de Cuadros
La función update se define para actualizar la imagen mostrada en cada cuadro de la animación. La imagen correspondiente se muestra en escala de grises y el texto se actualiza con el número de lámina y el nombre del archivo.



def update(frame):
    vmin = vol[frame, :, :].min()
    vmax = vol[frame, :, :].max()
    ax.imshow(vol[frame, :, :], cmap='gray', vmin=vmin, vmax=vmax)
    text.set_text(f'Lámina {frame + 1} - {file_names[frame]}')
8. Creación y Visualización de la Animación
Finalmente, se crea y muestra la animación utilizando animation.FuncAnimation. El intervalo entre cuadros se incrementa en un 30% para una visualización más pausada.

interval = 250 * 1.3
ani = animation.FuncAnimation(fig, update, frames=range(vol.shape[0]), interval=interval, repeat=False)
plt.show()
Este programa proporciona una herramienta eficaz para visualizar conjuntos de datos DICOM en una secuencia animada, facilitando la exploración de volúmenes de imágenes médicas.
