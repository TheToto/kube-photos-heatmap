from PIL import Image
import os
import re

def get_chunk_coordinates(chunk_dir):
    chunk_files = os.listdir(chunk_dir)
    coordinates = []

    for file in chunk_files:
        match = re.match(r'chunk_(-?\d+)_(-?\d+)\.png', file)
        if match:
            x, y = int(match.group(1)), int(match.group(2))
            coordinates.append((x, y))

    return coordinates

def combine_chunks(chunk_dir, chunk_size, zoom_level):
    coordinates = get_chunk_coordinates(chunk_dir)
    if not coordinates:
        raise ValueError("No chunk files found in the directory")

    min_x = min(x for x, y in coordinates)
    min_y = min(y for x, y in coordinates)
    max_x = max(x for x, y in coordinates)
    max_y = max(y for x, y in coordinates)

    combined_image = Image.new('RGB', ((max_x - min_x + 1) * chunk_size, (max_y - min_y + 1) * chunk_size))

    for x, y in coordinates:
        chunk_path = os.path.join(chunk_dir, f"chunk_{x}_{y}.png")
        chunk_image = Image.open(chunk_path)
        combined_image.paste(chunk_image, ((x - min_x) * chunk_size, (y - min_y) * chunk_size))

    return combined_image, min_x, min_y

def generate_zoom_levels(base_dir, output_dir, chunk_size, max_zoom_level):
    for zoom_level in range(max_zoom_level, 0, -1):
        input_dir = os.path.join(base_dir, f"zoom_level_{zoom_level}")
        output_zoom_dir = os.path.join(output_dir, f"zoom_level_{zoom_level - 1}")
        os.makedirs(output_zoom_dir, exist_ok=True)

        coordinates = get_chunk_coordinates(input_dir)
        if not coordinates:
            raise ValueError(f"No chunk files found in the directory {input_dir}")

        min_x = min(x for x, y in coordinates)
        min_y = min(y for x, y in coordinates)
        max_x = max(x for x, y in coordinates)
        max_y = max(y for x, y in coordinates)

        # fix min/max values to be multiples of 2
        min_x = min_x - (min_x % 2)
        min_y = min_y - (min_y % 2)
        max_x = max_x + (2 - max_x % 2) - 1
        max_y = max_y + (2 - max_y % 2) - 1

        for x in range(min_x, max_x + 1, 2):
            for y in range(min_y, max_y + 1, 2):
                combined_chunk = Image.new('RGB', (chunk_size, chunk_size))

                for dx in range(2):
                    for dy in range(2):
                        chunk_path = os.path.join(input_dir, f"chunk_{x + dx}_{y + dy}.png")
                        if os.path.exists(chunk_path):
                            chunk_image = Image.open(chunk_path)
                            combined_chunk.paste(chunk_image.resize((chunk_size // 2, chunk_size // 2), Image.LANCZOS), (dx * (chunk_size // 2), dy * (chunk_size // 2)))

                combined_chunk.save(os.path.join(output_zoom_dir, f"chunk_{(x // 2)}_{(y // 2)}.png"))
                print(f"Saved chunk_{(x // 2)}_{(y // 2)}.png in {output_zoom_dir}")

if __name__ == "__main__":
    base_dir = "output_images"
    output_dir = "output_images"
    chunk_size = 256
    max_zoom_level = 5

    generate_zoom_levels(base_dir, output_dir, chunk_size, max_zoom_level)