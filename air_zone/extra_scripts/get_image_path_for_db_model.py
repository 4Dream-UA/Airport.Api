from typing import Callable
import os
import uuid

from django.utils.text import slugify

def get_image_path_for_db_model(
        instance: Callable,
        filename: str,
    ) -> str:
    """
    This function make correct path for ImageFields of models
    """
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)
