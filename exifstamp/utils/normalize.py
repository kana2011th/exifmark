def make_model(make: str, model: str) -> str:
    """Normalize Make and Model. Detect and Remove repeating 'EXIF *Make' in 'EXIF *Model' EXIF data."""

    try:
        model = model[model.index(make) + len(make):].strip()
    except:
        model = model

    return "{} {}".format(make, model)
