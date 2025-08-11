import PyInstaller.__main__
import os

# Get the script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create paths using os.path.join
icon_path = os.path.join(current_dir, 'icon.ico')
words_path = os.path.join(current_dir, 'words.csv')
font_path = os.path.join(current_dir, 'fonts', 'press_start_2p', 'PressStart2P-Regular.ttf')
images_path = os.path.join(current_dir, 'images')

PyInstaller.__main__.run([
    '--name=Letter Raider',
    '--onefile',
    '--windowed',
    '--noconsole',
    f'--icon={icon_path}',
    f'--add-data={icon_path};.',
    f'--add-data={words_path};.',
    f'--add-data={font_path};.',
    f'--add-data={images_path};images/',
    f'--add-data={images_path};images/',
    f'--add-data={words_path};.',
    f'--add-data={font_path};.',
    'hangman_gui.py'
])
