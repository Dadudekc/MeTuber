import cv2
from styles.base import Style
import numpy as np


class OilPainting(Style):
    """
    Applies an oil painting effect to the image.
    """

    name = "Oil Painting"
    category = "Artistic"
    parameters = [
        {
            "name": "size",
            "type": "int",
            "default": 7,
            "min": 1,
            "max": 15,
            "step": 2,
            "label": "Size",
        },
        {
            "name": "dyn_ratio",
            "type": "int",  # Updated to integer to align with OpenCV's requirement
            "default": 1,
            "min": 0,
            "max": 2,
            "step": 1,
            "label": "Dyn Ratio",
        },
    ]

    def define_parameters(self):
        """
        Define the parameters for this style.
        Returns:
            list: List of parameter dictionaries.
        """
        return self.parameters

    def apply(self, image, params: dict) -> np.ndarray:
        """
        Apply oil painting effect to the image.
        """
        # Get parameters
        size = params.get("size", 5)
        dyn_ratio = params.get("dyn_ratio", 1)

        # Apply the oil painting effect
        return cv2.stylization(image, sigma_s=60, sigma_r=0.6)

    def get_default_params(self):
        """
        Get the default parameters for this style.
        Returns:
            dict: Default parameter values.
        """
        return {
            "size": 7,
            "dyn_ratio": 1,
        }
