from PIL import Image
import os

# Get the directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

try:
    # Open the source image
    img = Image.open(os.path.join(current_dir, 'images', 'game_ico.jpg'))
    
    # Convert to ICO format with multiple sizes
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    images = [img.resize(size, Image.Resampling.LANCZOS) for size in sizes]
    
    # Save as ICO with multiple sizes
    icon_path = os.path.join(current_dir, 'icon.ico')
    img.save(icon_path, format='ICO', sizes=sizes)
    print(f"Icon created successfully at {icon_path}")
    
except FileNotFoundError:
    print(f"Error: Could not find game_ico.jpg in the images folder")
    print("Please ensure the image exists in the images folder")
except Exception as e:
    print(f"An error occurred: {str(e)}")
