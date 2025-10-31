from typing import Callable


def get_image_path_for_db_model(
        instance: Callable,
        filename: str,
    ) -> str:
    """
    This function make correct path for ImageFields of models
    """
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)
