"""
Handlers for image files and HTML viewer
"""
import os
import logging
import mimetypes
import tornado.web
from models.image_model import ImageModel

logger = logging.getLogger(__name__)

# Supported image types
IMAGE_TYPES = ['original', 'protanope']


class ImageFileHandler(tornado.web.RequestHandler):
    """Handler for /images/{imagetype}/{filename} - Serve image files"""

    def initialize(self, image_model: ImageModel, images_dir: str):
        """
        Initialize handler with image model and images directory

        Args:
            image_model: ImageModel instance
            images_dir: Base directory for images
        """
        self.image_model = image_model
        self.images_dir = images_dir

    async def get(self, imagetype: str, filename: str):
        """
        GET /images/{imagetype}/{filename}
        Serve the actual image file

        Args:
            imagetype: Type of image (e.g., 'original', 'protanope')
            filename: Image filename
        """
        try:
            # Validate imagetype
            if imagetype not in IMAGE_TYPES:
                logger.warning(f"Invalid imagetype: {imagetype}")
                self.set_status(400)
                self.write(f"Invalid imagetype. Must be one of: {', '.join(IMAGE_TYPES)}")
                return

            # Check if image exists in database
            if not self.image_model.exists(filename):
                logger.warning(f"Image not found in database: {filename}")
                self.set_status(404)
                self.write("Image not found")
                return

            # Build file path
            file_path = os.path.join(self.images_dir, imagetype, filename)

            # Check if file exists on disk
            if not os.path.exists(file_path):
                logger.error(f"Image file not found on disk: {file_path}")
                self.set_status(404)
                self.write("Image file not found on disk")
                return

            # Determine content type
            content_type, _ = mimetypes.guess_type(filename)
            if content_type is None:
                content_type = 'application/octet-stream'

            # Set headers
            self.set_header('Content-Type', content_type)
            self.set_header('Cache-Control', 'public, max-age=3600')

            # Read and serve file
            with open(file_path, 'rb') as f:
                self.write(f.read())

            logger.info(f"Served image: {imagetype}/{filename}")

        except Exception as e:
            logger.error(f"Error serving image {imagetype}/{filename}: {e}", exc_info=True)
            self.set_status(500)
            self.write("Internal server error")


class IndexHandler(tornado.web.RequestHandler):
    """Handler for / - Simple HTML viewer"""

    def initialize(self, image_model: ImageModel):
        """
        Initialize handler with image model

        Args:
            image_model: ImageModel instance
        """
        self.image_model = image_model

    async def get(self):
        """
        GET /
        Serve the HTML viewer from static file
        """
        # Redirect to static index.html
        self.redirect('/static/index.html')