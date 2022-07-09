import random
from PIL import Image, ImageOps

# Load images
images_path = "img"
top_img, top_right, top_bottom, top_bottom_right, all_sides = [
    Image.open(f"{images_path}/{file}.png")
    for file in ["one_side", "two_sides", "two_opposite_sides", "three_sides", "all_sides"]
]
empty_img = Image.open(f"{images_path}/empty.png")
image_size = empty_img.width

# We use binary representation with the bit at 1's place denoting top edge is filled.
# The bit at 2's place denoting the right edge is filled and so-on in clockwise direction.
# We use this to find images for all the possible orientations and store them in a list.
top = 1
right = 2
bottom = 4
left = 8
all_images = []
# 0 = Blank
all_images.append(empty_img)
# 1 = Top edge filled
all_images.append(top_img)
# 2 = Right edge filled
all_images.append(top_img.transpose(Image.Transpose.ROTATE_270))
# 3 = Top & right edges filled
all_images.append(top_right)
# 4 = Bottom edge filled
all_images.append(top_img.transpose(Image.Transpose.FLIP_TOP_BOTTOM))
# 5 = Bottom & top edges filled
all_images.append(top_bottom)
# 6 = Bottom & right edges filled
all_images.append(top_right.transpose(Image.Transpose.FLIP_TOP_BOTTOM))
# 7 = Bottom, right & top edges filled
all_images.append(top_bottom_right)
# 8 = Left edge filled
all_images.append(top_img.transpose(Image.Transpose.ROTATE_90))
# 9 = Left & top edges filled
all_images.append(top_right.transpose(Image.Transpose.FLIP_LEFT_RIGHT))
# 10 = Left & right edges filled
all_images.append(top_bottom.transpose(Image.Transpose.ROTATE_90))
# 11 = Left, right & top edges filled
all_images.append(top_bottom_right.transpose(Image.Transpose.ROTATE_90))
# 12 = Left & bottom edges filled
all_images.append(top_right.transpose(Image.Transpose.ROTATE_180))
# 13 = Bottom, left & top edges filled
all_images.append(top_bottom_right.transpose(Image.Transpose.FLIP_LEFT_RIGHT))
# 14 = Bottom, left & right edges filled
all_images.append(top_bottom_right.transpose(Image.Transpose.ROTATE_270))
# 15 = All the edges filled
all_images.append(all_sides)


class TileFiller:
    def __init__(self, num_tiles, tiles=None, options=None):
        """
        Instnatiate TileFiller instance.

        For a brand new Tile pattern, just pass in number of tiles.
        Optionally, you can specify custom list of tiles and options.
        """
        self.num_tiles = num_tiles
        self.tiles = (
            tiles
            if tiles is not None
            else [[-1 for i in range(num_tiles)] for j in range(num_tiles)]
        )
        self.options = (
            options
            if options is not None
            else [
                [{i for i in range(16)} for i in range(num_tiles)]
                for j in range(num_tiles)
            ]
        )

    def next_tile(self):
        """
        Get the next tile which can potentially be filled.
        """
        smallest_option = min(
            [
                min(
                    [
                        len(tile_options)
                        for tile_options in options_row
                        if len(tile_options) > 0
                    ],
                    default=16,
                )
                for options_row in self.options
            ]
        )
        viable_options = [
            (i, j)
            for j in range(self.num_tiles)
            for i in range(self.num_tiles)
            if len(self.options[i][j]) == smallest_option
        ]
        viable_option = random.sample(viable_options, 1)[0]
        return viable_option

    def fill_one_tile(self):
        """
        Fill one tile at a time.
        """
        i, j = self.next_tile()
        tile_options = list(self.options[i][j])
        tile_fill = random.sample(tile_options, 1)[0]
        self.tiles[i][j] = tile_fill
        self.options[i][j] = set()
        self.recompute_neighbor_options(i, j)

    def recompute_neighbor_options(self, i, j):
        """
        Fetch the different neighbor options for all other tiles after the tile at (i,j) get filled.
        """
        added_tile = self.tiles[i][j]
        if (i > 0) and self.tiles[i - 1][j] == -1:
            if added_tile & top > 0:
                self.options[i - 1][j] = self.options[i - 1][j].difference(
                    [opt for opt in self.options[i - 1][j] if (opt & bottom) == 0]
                )
            else:
                self.options[i - 1][j] = self.options[i - 1][j].difference(
                    [opt for opt in self.options[i - 1][j] if (opt & bottom) > 0]
                )

        if i + 1 < self.num_tiles and self.tiles[i + 1][j] != 0:
            if added_tile & bottom > 0:
                self.options[i + 1][j] = self.options[i + 1][j].difference(
                    [opt for opt in self.options[i + 1][j] if (opt & top == 0)]
                )
            else:
                self.options[i + 1][j] = self.options[i + 1][j].difference(
                    [opt for opt in self.options[i + 1][j] if (opt & top > 0)]
                )

        if j + 1 < self.num_tiles and self.tiles[i][j + 1] != 0:
            if added_tile & right > 0:
                self.options[i][j + 1] = self.options[i][j + 1].difference(
                    [opt for opt in self.options[i][j + 1] if (opt & left) == 0]
                )
            else:
                self.options[i][j + 1] = self.options[i][j + 1].difference(
                    [opt for opt in self.options[i][j + 1] if (opt & left) > 0]
                )
        if j > 0 and self.tiles[i][j - 1] != 0:
            if added_tile & left > 0:
                self.options[i][j - 1] = self.options[i][j - 1].difference(
                    [opt for opt in self.options[i][j - 1] if (opt & right) == 0]
                )
            else:
                self.options[i][j - 1] = self.options[i][j - 1].difference(
                    [opt for opt in self.options[i][j - 1] if (opt & right) > 0]
                )

    def fill_all_tiles(self):
        """
        Single function to fill all the tiles for an empty TileMap instance.
        """
        [self.fill_one_tile() for _ in range(self.num_tiles * self.num_tiles)]

    def get_image(self):
        """
        Get the image representation of the TileMap instance.
        """
        im = Image.new(
            "RGBA", (image_size * self.num_tiles, image_size * self.num_tiles)
        )
        im.paste(
            (0, 0, 0, 255),
            [0, 0, image_size * self.num_tiles, image_size * self.num_tiles],
        )
        for i in range(self.num_tiles):
            for j in range(self.num_tiles):
                img_code = self.tiles[i][j]
                tile_img = empty_img if img_code == -1 else all_images[img_code]
                im.paste(tile_img, (image_size * j, image_size * i))
        return im


# Get an image containing 20x20 tiles.
tf = TileFiller(20)
tf.fill_all_tiles()
image = tf.get_image()

# Save the generated tile image in generated.png
image.save("img/generated.png")
