#!/usr/bin/env python3
"""
Image Viewer RESTful API Server
Tornado-based web server for image viewing with annotations
"""
import os
import logging
import tornado.ioloop
import tornado.web
from models import ImageModel
from handlers import (
    ApiImagesHandler,
    ApiImageDetailHandler,
    ImageFileHandler,
    IndexHandler
)

# Configuration
PORT = 8888
IMAGES_DIR = 'images'
CSV_FILE = 'images.csv'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def make_app(image_model: ImageModel):
    """
    Create and configure the Tornado application

    Args:
        image_model: Initialized ImageModel instance

    Returns:
        Tornado Application instance
    """
    return tornado.web.Application([
        # HTML viewer
        (r"/", IndexHandler, {'image_model': image_model}),

        # API endpoints
        (r"/api/images", ApiImagesHandler, {'image_model': image_model}),
        (r"/api/images/([^/]+)/([^/]+)", ApiImageDetailHandler, {'image_model': image_model}),

        # Image file serving
        (r"/images/([^/]+)/([^/]+)", ImageFileHandler, {
            'image_model': image_model,
            'images_dir': IMAGES_DIR
        }),

        # Static files (HTML, CSS, JS)
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'}),
    ], debug=True)


def main():
    """Main entry point for the server"""
    try:
        # Initialize image model and load data
        logger.info(f"Loading image data from {CSV_FILE}...")
        image_model = ImageModel(csv_path=CSV_FILE)
        image_model.load()
        logger.info(f"Successfully loaded image data")

        # Create application
        app = make_app(image_model)

        # Start server
        app.listen(PORT)
        logger.info(f"Server started on http://localhost:{PORT}")
        logger.info(f"Press Ctrl+C to stop the server")

        # Start event loop
        tornado.ioloop.IOLoop.current().start()

    except FileNotFoundError as e:
        logger.error(f"Required file not found: {e}")
        logger.error(f"Please ensure {CSV_FILE} exists in the current directory")
        return 1

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return 0

    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit(main())
