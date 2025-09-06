from PIL import Image, ImageDraw, ImageFont
import os

def create_sunil_logo():
    # Create a new image with white background
    width, height = 400, 200
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Define colors (similar to your original logo)
    dark_blue = (25, 25, 112)  # Dark blue
    light_blue = (0, 191, 255)  # Light cyan-blue
    
    # Draw spiral/wave pattern on the left
    center_x, center_y = 100, 100
    radius = 60
    
    # Draw the spiral
    for i in range(0, 360, 5):
        angle = i * 3.14159 / 180
        r = radius * (1 - i / 360)
        x = center_x + r * 0.8 * (angle / 3.14159)
        y = center_y + r * 0.3 * (angle / 3.14159)
        
        if i < 180:
            color = dark_blue
        else:
            color = light_blue
            
        draw.ellipse([x-3, y-3, x+3, y+3], fill=color)
    
    # Draw ripple effect below
    for i in range(2):
        ripple_y = center_y + 40 + i * 8
        draw.arc([center_x-30, ripple_y-5, center_x+30, ripple_y+5], 0, 180, fill=light_blue, width=2)
    
    # Add text "SUNIL" with alternating colors
    try:
        # Try to use a bold font
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", 48)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    
    text = "SUNIL"
    text_x = 200
    text_y = 80
    
    # Draw each letter with alternating colors and shadow
    for i, letter in enumerate(text):
        x_pos = text_x + i * 35
        
        # Choose color based on position
        if i % 2 == 0:
            color = dark_blue
        else:
            color = light_blue
        
        # Draw shadow (slightly offset)
        draw.text((x_pos + 2, text_y + 2), letter, font=font, fill=(200, 200, 200))
        
        # Draw main text
        draw.text((x_pos, text_y), letter, font=font, fill=color)
    
    # Save the logo
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    img.save(logo_path)
    print(f"Logo created successfully at: {logo_path}")
    
    return logo_path

if __name__ == "__main__":
    create_sunil_logo()
