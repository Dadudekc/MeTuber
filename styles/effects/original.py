# styles/effects/original.py

import cv2
from styles.base import Style
import numpy as np
from typing import Optional, Dict, Any

class Original(Style):
    """
    The Original style applies no changes to the frame.
    """
    name = "Original"
    category = "Effects"

    def define_parameters(self):
        """
        The Original style has no parameters.

        Returns:
            list: Empty list since there are no parameters.
        """
        return []

    def apply(self, image: np.ndarray, params: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Apply a slight sharpening effect to the image.
        """
        kernel = np.array([[-1, -1, -1], [-1, 9.5, -1], [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)

    def get_default_params(self):
        """
        Get the default parameters for this style.
        """
        return {}
