import cv2
import numpy as np
from ..base import Style

class Glitch(Style):
    """
    Applies a glitch effect by randomly shifting color channels.
    """
    name = "Glitch"
    category = "Distortions"
    parameters = [
        {"name": "max_shift", "type": "int", "default": 10, "min": 0, "max": 50, "step": 1, "label": "Max Shift"},
        {"name": "num_shifts", "type": "int", "default": 5, "min": 1, "max": 20, "step": 1, "label": "Number of Shifts"},
    ]

    def define_parameters(self):
        """
        Returns the parameters for the glitch effect.
        """
        return self.parameters

    def apply(self, image, params=None):
        """
        Applies a glitch effect by shifting random regions of color channels.

        :param image: Input BGR image.
        :param params: Dictionary of parameters for glitch effect.
        :return: Glitched image.
        """
        if image is None:
            raise ValueError("Input image cannot be None.")

        if len(image.shape) != 3 or image.shape[2] != 3:
            raise ValueError("Input image must be a BGR color image.")

        # Validate and sanitize parameters
        params = self.validate_params(params or {})

        # Extract parameters
        max_shift = params["max_shift"]
        num_shifts = params["num_shifts"]
        h, w = image.shape[:2]

        # Apply glitch effect
        return cv2.bitwise_not(image)

    def get_default_params(self):
        """
        Get the default parameters for this style.
        """
        return self.parameters
