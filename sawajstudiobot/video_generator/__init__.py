"""
This module initializes the video generator package and provides utility functions to manage and utilize video generators and uploaders.

Functions:
- import_modules_from_subdirectories: Imports modules from specified subdirectories, handling potential import errors.
- list_video_generators: Lists all available video generator modules.
- get_video_generator: Retrieves the specified video generator module.
- generate_video: Generates a video using the specified video generator.
- generate_and_upload_video: Generates a video and attempts to upload it using the specified uploader.
- list_video_uploaders: Lists all available video uploader modules.

Logging:
- Logs imported modules, available video generators, and available video uploaders.

Error Handling:
- Uses try-except blocks to handle potential import errors and video generation/upload failures.

Example:
```python
# Import the video generator package
from video_generator import get_video_generator, generate_video, generate_and_upload_video

# Get a specific video generator module
fb_ig_story_generator = get_video_generator('fb_ig_story_video_generator')

# Generate a video using the generator
video = generate_video('fb_ig_story_video_generator', duration=10, theme='modern')

# Generate and upload a video
success = generate_and_upload_video('fb_ig_story_video_generator', 'facebook', video_title='My Story', duration=15)
```
"""

import os
import logging
from typing import List, Optional

# Define the path to the current file
current_file_path = os.path.abspath(__file__)

# Get the parent directory of the current file
parent_dir = os.path.dirname(current_file_path)

# Initialize the list of subdirectories to be included
subdirectories: List[str] = []

# Function to import modules from subdirectories with error handling
def import_modules_from_subdirectories(subdirectories: List[str]) -> None:
    """
    Import modules from the specified subdirectories, handling potential import errors.
    
    Args:
        subdirectories (List[str]): A list of subdirectory names.
    """
    for subdirectory in subdirectories:
        try:
            # Import the module
            __import__(f"video_generator.{subdirectory}", globals(), locals(), ["*"])
            logging.info(f"Successfully imported module from {subdirectory}")
        except ImportError as e:
            logging.error(f"Error importing module from {subdirectory}: {e}")
        except Exception as e:
            logging.exception(f"Unexpected error while importing module from {subdirectory}: {e}")

# Function to list available video generators
def list_video_generators() -> List[str]:
    """
    List all available video generator modules.
    
    Returns:
        List[str]: A list of video generator module names.
    """
    return subdirectories

# Function to get video generator module with error handling
def get_video_generator(generator_name: str) -> Optional[object]:
    """
    Get the specified video generator module.
    
    Args:
        generator_name (str): The name of the video generator module.
    
    Returns:
        Optional[object]: The requested video generator module or None if not found/error occurred.
    """
    try:
        return __import__(f"video_generator.{generator_name}", globals(), locals(), ["*"])
    except ImportError:
        logging.error(f"Video generator '{generator_name}' not found.")
        return None
    except Exception as e:
        logging.exception(f"Error getting video generator '{generator_name}': {e}")
        return None

# Function to generate video using a specific generator with error handling
def generate_video(generator_name: str, **kwargs) -> Optional[object]:
    """
    Generate a video using the specified video generator.
    
    Args:
        generator_name (str): The name of the video generator module.
        **kwargs: Additional keyword arguments to pass to the generator.
    
    Returns:
        Optional[object]: The generated video or None if generation failed/error occurred.
    """
    generator_module = get_video_generator(generator_name)
    
    if generator_module:
        try:
            generator = generator_module.VideoGenerator(**kwargs)
            return generator.generate()
        except Exception as e:
            logging.error(f"Video generation failed for generator '{generator_name}': {e}")
            return None
    else:
        logging.error(f"Video generator '{generator_name}' not found.")
        return None

# Function to generate and upload video with error handling
def generate_and_upload_video(generator_name: str, uploader_name: str, **kwargs) -> bool:
    """
    Generate a video using the specified generator and attempt to upload it.
    
    Args:
        generator_name (str): The name of the video generator module.
        uploader_name (str): The name of the video uploader module.
        **kwargs: Additional keyword arguments to pass to the generator and uploader.
    
    Returns:
        bool: True if video generation and upload succeeded, False otherwise/on error.
    """
    video = generate_video(generator_name, **kwargs)
    
    if video:
        try:
            uploader_module = __import__(f"video_uploader.{uploader_name}", globals(), locals(), ["*"])
            uploader = uploader_module.VideoUploader(**kwargs)
            return uploader.upload(video)
        except ImportError:
            logging.error(f"Video uploader '{uploader_name}' not found.")
            return False
        except Exception as e:
            logging.error(f"Video upload failed for uploader '{uploader_name}': {e}")
            return False
    return False

# Function to list available video uploaders
def list_video_uploaders() -> List[str]:
    """
    List all available video uploader modules.
    
    Returns:
        List[str]: A list of video uploader module names.
    """
    uploader_package_path = os.path.join(os.path.dirname(os.path.dirname(current_file_path)), "video_uploader")
    uploader_modules = [f"video_uploader.{module}" for module in os.listdir(uploader_package_path) if os.path.isdir(os.path.join(uploader_package_path, module))]
    return uploader_modules

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log the list of imported modules
logger.info(f"Imported modules from subdirectories: {subdirectories}")

# Log the list of available video generators
logger.info(f"Available video generators: {list_video_generators()}")

# Log the list of available video uploaders
logger.info(f"Available video uploaders: {list_video_uploaders()}")

# Iterate through the items in the parent directory to populate subdirectories list
for item in os.listdir(parent_dir):
    item_path = os.path.join(parent_dir, item)
    if os.path.isdir(item_path) and not item.startswith('.'):
        subdirectories.append(item)

# Import modules from subdirectories
import_modules_from_subdirectories(subdirectories)
