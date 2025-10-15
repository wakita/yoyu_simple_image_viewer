"""
API handlers for RESTful endpoints
"""
import logging
import tornado.web
from models.image_model import ImageModel
from handlers.image_handler import IMAGE_TYPES

logger = logging.getLogger(__name__)


class ApiImagesHandler(tornado.web.RequestHandler):
    """Handler for /api/images - List all images with pagination"""

    def initialize(self, image_model: ImageModel):
        """
        Initialize handler with image model

        Args:
            image_model: ImageModel instance
        """
        self.image_model = image_model

    def set_default_headers(self):
        """Set CORS headers"""
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")

    async def options(self):
        """Handle preflight requests"""
        self.set_status(204)
        self.finish()

    async def get(self):
        """
        GET /api/images?page=1&page_size=20
        Returns paginated list of all images
        """
        try:
            # Get pagination parameters
            page = int(self.get_argument('page', '1'))
            page_size = int(self.get_argument('page_size', '20'))

            # Validate parameters
            if page < 1:
                raise ValueError("Page must be >= 1")
            if page_size < 1 or page_size > 100:
                raise ValueError("Page size must be between 1 and 100")

            # Get paginated data
            result = self.image_model.get_all(page=page, page_size=page_size)

            self.write(result)
            logger.info(f"Returned page {page} with {len(result['data'])} images")

        except ValueError as e:
            logger.warning(f"Invalid parameter: {e}")
            self.set_status(400)
            self.write({"error": str(e)})

        except Exception as e:
            logger.error(f"Error in ApiImagesHandler: {e}", exc_info=True)
            self.set_status(500)
            self.write({"error": "Internal server error"})


class ApiImageDetailHandler(tornado.web.RequestHandler):
    """Handler for /api/images/{imagetype}/{filename} - Get image details"""

    def initialize(self, image_model: ImageModel):
        """
        Initialize handler with image model

        Args:
            image_model: ImageModel instance
        """
        self.image_model = image_model

    def set_default_headers(self):
        """Set CORS headers"""
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")

    async def options(self, imagetype: str, filename: str):
        """Handle preflight requests"""
        self.set_status(204)
        self.finish()

    async def get(self, imagetype: str, filename: str):
        """
        GET /api/images/{imagetype}/{filename}
        Returns details for a specific image

        Args:
            imagetype: Type of image ('original' or 'protanope')
            filename: Image filename
        """
        try:
            # Validate imagetype
            if imagetype not in IMAGE_TYPES:
                self.set_status(400)
                self.write({"error": f"Invalid imagetype: {imagetype}. Must be one of: {', '.join(IMAGE_TYPES)}"})
                return

            # Get image data
            image_data = self.image_model.get_by_filename(filename)

            if image_data is None:
                logger.warning(f"Image not found: {filename}")
                self.set_status(404)
                self.write({"error": f"Image not found: {filename}"})
                return

            # Return the complete row data
            self.write(image_data)
            logger.info(f"Returned details for {imagetype}/{filename}")

        except Exception as e:
            logger.error(f"Error in ApiImageDetailHandler: {e}", exc_info=True)
            self.set_status(500)
            self.write({"error": "Internal server error"})