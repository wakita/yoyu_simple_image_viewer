"""
Image data model for managing CSV-based image metadata
"""
import logging
from typing import Dict, Optional
import pandas as pd

logger = logging.getLogger(__name__)


class ImageModel:
    """Manages image metadata from CSV file using Pandas DataFrame"""

    def __init__(self, csv_path: str = 'images.csv'):
        """
        Initialize the image model

        Args:
            csv_path: Path to the CSV file containing image metadata
        """
        self.csv_path = csv_path
        self.df: Optional[pd.DataFrame] = None

    def load(self) -> None:
        """Load image data from CSV file into memory as DataFrame"""
        try:
            self.df = pd.read_csv(self.csv_path)
            logger.info(f"Loaded {len(self.df)} images from {self.csv_path}")
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            raise

    def get_all(self, page: int = 1, page_size: int = 20) -> Dict:
        """
        Get all images with pagination

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            Dictionary containing paginated results and metadata
        """
        if self.df is None:
            raise RuntimeError("Data not loaded. Call load() first.")

        total = len(self.df)
        total_pages = (total + page_size - 1) // page_size

        # Validate page number
        if page < 1:
            page = 1
        if page > total_pages and total_pages > 0:
            page = total_pages

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        # Get paginated data and convert to list of dicts
        paginated_df = self.df.iloc[start_idx:end_idx]
        data = paginated_df.to_dict('records')

        return {
            'data': data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': total_pages
            }
        }

    def get_by_filename(self, filename: str) -> Optional[Dict[str, str]]:
        """
        Get image data by filename

        Args:
            filename: The image filename

        Returns:
            Image data dictionary or None if not found
        """
        if self.df is None:
            raise RuntimeError("Data not loaded. Call load() first.")

        result = self.df[self.df['filename'] == filename]
        if len(result) > 0:
            return result.iloc[0].to_dict()
        return None

    def get_annotation(self, filename: str, imagetype: str) -> Optional[str]:
        """
        Get annotation for a specific image type

        Args:
            filename: The image filename
            imagetype: Type of image ('original' or 'protanope')

        Returns:
            Annotation text or None if not found
        """
        image_data = self.get_by_filename(filename)
        if image_data and imagetype in image_data:
            return image_data[imagetype]
        return None

    def exists(self, filename: str) -> bool:
        """
        Check if an image exists in the database

        Args:
            filename: The image filename

        Returns:
            True if image exists, False otherwise
        """
        if self.df is None:
            raise RuntimeError("Data not loaded. Call load() first.")

        return len(self.df[self.df['filename'] == filename]) > 0