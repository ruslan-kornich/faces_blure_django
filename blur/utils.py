def scale_coords(coords, original_size, displayed_size):
    scale_x = original_size[0] / displayed_size[0]
    scale_y = original_size[1] / displayed_size[1]

    scaled_coords = {
        "x": int(coords["x"] * scale_x),
        "y": int(coords["y"] * scale_y),
        "width": int(coords["width"] * scale_x),
        "height": int(coords["height"] * scale_y),
    }
    return scaled_coords
