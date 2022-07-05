from PIL import Image

SIZE = 1000


def png_convert(inPath, outPath):
    with Image.open(inPath) as im:
        print()
        print(im.getbbox())

        (_, _, width, height) = im.getbbox()
        print(f"width: {width}")
        print(f"height: {height}")

        half = SIZE / 2

        # New corners for cropped image
        # See: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#coordinate-system
        # (0, 0) is the upper left corner
        left = max(0, int((width / 2) - half))
        upper = max(0, int((height / 2) - half))
        right = min(width, int((width / 2) + half))
        lower = min(height, int((height / 2) + half))

        print(f"left: {left}, upper: {upper}, right: {right}, lower: {lower}")

        im = im.crop((left, upper, right, lower))

        # Resize in case image is too small
        im = im.resize((SIZE, SIZE))

        # Convert to black and white
        im = im.convert("L")

        im.save(outPath)


def test_helper(name):
    png_convert(f"test/img/{name}.png", f"test/out/{name}.png")


def main():
    test_helper("small_x_small_y")
    test_helper("small_x_large_y")
    test_helper("large_x_small_y")
    test_helper("large_x_large_y")


if __name__ == "__main__":
    main()
