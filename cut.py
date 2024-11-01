from PIL import Image
import os

input_image_path = "./out.png"
output_folder = "./output_images/zoom_level_5"

os.makedirs(output_folder, exist_ok=True)

kube_chunk = 256 # Kube chunk
kube_zone = 32

# Info about image
chunk_start = [-12, -12]
zone_offset = [4, 4]

with Image.open(input_image_path) as img:
    width, height = img.size

    num_tiles_width = (width - zone_offset[0] * kube_zone) // kube_chunk
    num_tiles_height = (height - zone_offset[1] * kube_zone) // kube_chunk

    print(f"Image size: {width}x{height}")
    print(f"Number of chunks: {num_tiles_width}x{num_tiles_height}")

    if width % kube_chunk != 0 or height % kube_chunk != 0:
        raise ValueError(f"Image must be a multiple of {kube_chunk}x{kube_chunk} pixels.")

    for y in range(num_tiles_height):
        for x in range(num_tiles_width):
            tile_x = chunk_start[0] + x
            tile_y = chunk_start[1] + y

            left = x * kube_chunk + zone_offset[0] * kube_zone
            top = y * kube_chunk + zone_offset[1] * kube_zone
            right = (x + 1) * kube_chunk + zone_offset[0] * kube_zone
            bottom = (y + 1) * kube_chunk + zone_offset[1] * kube_zone

            tile = img.crop((left, top, right, bottom))

            tile.save(os.path.join(output_folder, f"chunk_{tile_x}_{tile_y}.png"))
