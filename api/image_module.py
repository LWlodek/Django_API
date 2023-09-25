from PIL import Image, ImageDraw

def create_dummy_image(width=200, height=200, color=(255, 255, 255)):
    image = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), "Test Image", fill="black")
    return image
