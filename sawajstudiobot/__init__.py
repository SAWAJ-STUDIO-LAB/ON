"""
Main Package for Islamic Video Generation and Social Media Automation.

This package provides tools for automated video creation and social media management,
following Islamic principles and guidelines.
"""

import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
__version__ = "1.1.0"  # Updated version
__author__ = "Sawaj Studio"

# Initialize the logger
logger = logging.getLogger(__name__)

# Function to display welcome message
def display_welcome_message():
    """
    Display a welcome message with package information.
    """
    welcome_message = f"Welcome to SawajStudioBot v{__version__} - Islamic Video Automation Suite\n"
    welcome_message += "Developed by {__author__}\n"
    welcome_message += "------------------------------\n"
    logger.info(welcome_message)

# Call the welcome message function
display_welcome_message()

# New feature: Package usage instructions
def display_usage_instructions():
    """
    Display instructions on how to use the package.
    """
    usage_instructions = "Usage Instructions:\n"
    usage_instructions += "1. Import the required modules from this package.\n"
    usage_instructions += "2. Utilize the provided classes and functions for video generation and social media automation.\n"
    usage_instructions += "3. Refer to the documentation for detailed explanations and examples.\n"
    logger.info(usage_instructions)

# Call the usage instructions function
display_usage_instructions()

# No specific upgrades are required for this file.

# End of file
logger.info("Initialization completed successfully.")
