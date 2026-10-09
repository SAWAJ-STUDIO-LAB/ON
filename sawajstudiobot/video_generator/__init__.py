"""
This module initializes the video generator package.
"""

# Import necessary modules
import os

# Define the path to the current file
current_file_path = os.path.abspath(__file__)

# Get the parent directory of the current file
parent_dir = os.path.dirname(current_file_path)

# Initialize the list of subdirectories to be included
subdirectories = []

# Iterate through the items in the parent directory
for item in os.listdir(parent_dir):
    # Get the full path of the item
    item_path = os.path.join(parent_dir, item)
    
    # If the item is a directory and not starting with a dot, add it to the list
    if os.path.isdir(item_path) and not item.startswith('.'):
        subdirectories.append(item)

# Function to import modules from subdirectories
def import_modules_from_subdirectories(subdirectories):
    """
    Import modules from the specified subdirectories.
    
    Args:
        subdirectories (list): A list of subdirectory names.
    """
    for subdirectory in subdirectories:
        # Attempt to import the module and handle potential errors
        try:
            # Import the module
            __import__(f"video_generator.{subdirectory}", globals(), locals(), ["*"], 0)
            # Print a success message
            print(f"Successfully imported module from {subdirectory}")
        except ImportError as e:
            # Print an error message with the exception
            print(f"Error importing module from {subdirectory}: {e}")
        except Exception as e:
            # Print an error message for any other exception
            print(f"Unexpected error: {e}")

# Call the function to import modules from subdirectories
import_modules_from_subdirectories(subdirectories)

# New feature: Function to list available video generators
def list_video_generators():
    """
    List all available video generator modules.
    
    Returns:
        list: A list of video generator module names.
    """
    return subdirectories

# New feature: Function to get video generator module
def get_video_generator(generator_name):
    """
    Get the specified video generator module.
    
    Args:
        generator_name (str): The name of the video generator module.
    
    Returns:
        module: The requested video generator module or None if not found.
    """
    try:
        return __import__(f"video_generator.{generator_name}", globals(), locals(), ["*"], 0)
    except ImportError:
        print(f"Video generator '{generator_name}' not found.")
        return None

# New feature: Function to generate video using a specific generator
def generate_video(generator_name, **kwargs):
    """
    Generate a video using the specified video generator.
    
    Args:
        generator_name (str): The name of the video generator module.
        **kwargs: Additional keyword arguments to pass to the generator.
    
    Returns:
        object: The generated video or None if generation failed.
    """
    # Get the video generator module
    generator_module = get_video_generator(generator_name)
    
    if generator_module:
        # Attempt to generate the video
        try:
            generator = generator_module.VideoGenerator(**kwargs)
            return generator.generate()
        except Exception as e:
            print(f"Video generation failed: {e}")
            return None
    else:
        print(f"Video generator '{generator_name}' not found.")
        return None

# New feature: Function to generate and upload video
def generate_and_upload_video(generator_name, uploader_name, **kwargs):
    """
    Generate a video using the specified generator and upload it using the specified uploader.
    
    Args:
        generator_name (str): The name of the video generator module.
        uploader_name (str): The name of the video uploader module.
        **kwargs: Additional keyword arguments to pass to the generator and uploader.
    
    Returns:
        bool: True if video generation and upload succeeded, False otherwise.
    """
    # Generate the video
    video = generate_video(generator_name, **kwargs)
    
    if video:
        # Attempt to import the uploader module
        try:
            uploader_module = __import__(f"video_uploader.{uploader_name}", globals(), locals(), ["*"], 0)
            uploader = uploader_module.VideoUploader(**kwargs)
            return uploader.upload(video)
        except ImportError:
            print(f"Video uploader '{uploader_name}' not found.")
        except Exception as e:
            print(f"Video upload failed: {e}")
    return False

# New feature: Function to list available video uploaders
def list_video_uploaders():
    """
    List all available video uploader modules.
    
    Returns:
        list: A list of video uploader module names.
    """
    # Define the path to the video uploader package
    uploader_package_path = os.path.join(os.path.dirname(os.path.dirname(current_file_path)), "video_uploader")
    
    # Get a list of all modules in the video uploader package
    uploader_modules = [f"video_uploader.{module}" for module in os.listdir(uploader_package_path) if os.path.isdir(os.path.join(uploader_package_path, module))]
    
    return uploader_modules

# Logging configuration
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log the list of imported modules
logger.info(f"Imported modules from subdirectories: {subdirectories}")

# Log the list of available video generators
logger.info(f"Available video generators: {list_video_generators()}")

# Log the list of available video uploaders
logger.info(f"Available video uploaders: {list_video_uploaders()}")
