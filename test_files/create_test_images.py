"""
Create test images for preview rendering.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def create_test_image(filename: str, text: str, size=(1200, 630), color="#0a66c2"):
    """Create a simple test image with text"""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)

    # Try to use a nice font, fall back to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        font = ImageDraw.ImageFont.load_default()

    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2)

    # Draw text
    draw.text(position, text, fill="white", font=font)

    # Save
    output_path = Path(__file__).parent / filename
    img.save(output_path)
    print(f"✓ Created: {output_path}")
    return output_path


if __name__ == "__main__":
    print("Creating test images...\n")

    # Create various test images
    create_test_image("test_image_1.png", "LinkedIn Post Image", color="#0a66c2")
    create_test_image("test_image_2.png", "Second Image", color="#057642")
    create_test_image("test_image_3.png", "Third Image", color="#f5b800")
    create_test_image("test_image_4.png", "Fourth Image", color="#cc1016")
    create_test_image("video_thumbnail.png", "▶ Video Preview", color="#1a1a1a")

    print("\n✓ All test images created!")
