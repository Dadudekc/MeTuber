#!/usr/bin/env python3
"""
Create a new Dreamscape logo for the application.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_dreamscape_logo():
    """Create a new Dreamscape logo."""
    
    # Create a new image with a dark background
    width, height = 400, 300
    image = Image.new('RGBA', (width, height), (26, 26, 26, 255))  # Dark background
    draw = ImageDraw.Draw(image)
    
    # Try to use a nice font, fallback to default if not available
    try:
        # Try to use a modern font
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw the Dreamscape text
    text = "Dreamscape"
    text_color = (0, 150, 255)  # Blue color
    
    # Get text size and position it
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 20
    
    # Draw the main text
    draw.text((x, y), text, fill=text_color, font=font_large)
    
    # Draw subtitle
    subtitle = "Stream Software"
    subtitle_color = (200, 200, 200)  # Light gray
    
    bbox_subtitle = draw.textbbox((0, 0), subtitle, font=font_small)
    subtitle_width = bbox_subtitle[2] - bbox_subtitle[0]
    
    x_subtitle = (width - subtitle_width) // 2
    y_subtitle = y + text_height + 10
    
    draw.text((x_subtitle, y_subtitle), subtitle, fill=subtitle_color, font=font_small)
    
    # Add a subtle gradient effect
    for i in range(height):
        alpha = int(255 * (1 - i / height) * 0.3)  # Fade from top
        overlay = Image.new('RGBA', (width, 1), (0, 150, 255, alpha))
        image.paste(overlay, (0, i), overlay)
    
    # Save the logo
    logo_path = os.path.join("src", "gui", "assets", "logo.png")
    image.save(logo_path, "PNG")
    
    print(f"✅ Dreamscape logo created and saved to: {logo_path}")
    print("🕊️ Logo features:")
    print("   - Dark professional background")
    print("   - Blue 'Dreamscape' text")
    print("   - 'Stream Software' subtitle")
    print("   - Subtle gradient effect")

if __name__ == "__main__":
    create_dreamscape_logo() 