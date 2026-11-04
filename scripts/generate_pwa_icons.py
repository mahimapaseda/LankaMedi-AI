import os
from PIL import Image, ImageDraw

icons_dir = os.path.join("static", "icons")
os.makedirs(icons_dir, exist_ok=True)

sizes = [72, 96, 128, 144, 152, 180, 192, 384, 512]

def draw_medical_icon(size, is_maskable=False):
    # Canvas
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Safe padding for maskable icons (15% padding)
    pad = int(size * 0.12) if is_maskable else 0
    bg_box = [(pad, pad), (size - pad, size - pad)]
    
    # Corner radius
    radius = int((size - 2 * pad) * 0.22) if not is_maskable else 0
    
    # Background rounded rect or circle
    # Clinical Emerald / Teal gradient simulation: #0f766e to #0d9488
    draw.rounded_rectangle(bg_box, radius=radius, fill=(15, 118, 110, 255), outline=(13, 148, 136, 255), width=max(1, int(size * 0.02)))
    
    # Inner glow circle
    cx, cy = size // 2, size // 2
    r_inner = int((size - 2 * pad) * 0.36)
    draw.ellipse([(cx - r_inner, cy - r_inner), (cx + r_inner, cy + r_inner)], fill=(13, 148, 136, 120))

    # Medical Cross in crisp white
    arm_w = max(4, int(size * 0.12))
    arm_l = max(12, int(size * 0.44))

    # Vertical bar
    draw.rounded_rectangle(
        [(cx - arm_w // 2, cy - arm_l // 2), (cx + arm_w // 2, cy + arm_l // 2)],
        radius=arm_w // 3,
        fill=(255, 255, 255, 255)
    )
    # Horizontal bar
    draw.rounded_rectangle(
        [(cx - arm_l // 2, cy - arm_w // 2), (cx + arm_l // 2, cy + arm_w // 2)],
        radius=arm_w // 3,
        fill=(255, 255, 255, 255)
    )
    
    # Small pulse heartbeat / dot accent in coral red (#ef4444) on the top right of the cross
    dot_r = max(2, int(size * 0.045))
    dot_cx = cx + int(arm_l * 0.35)
    dot_cy = cy - int(arm_l * 0.35)
    draw.ellipse([(dot_cx - dot_r, dot_cy - dot_r), (dot_cx + dot_r, dot_cy + dot_r)], fill=(239, 68, 68, 255))

    return img

for sz in sizes:
    icon = draw_medical_icon(sz)
    icon.save(os.path.join(icons_dir, f"icon-{sz}x{sz}.png"), "PNG")
    if sz == 180:
        icon.save(os.path.join(icons_dir, "apple-touch-icon.png"), "PNG")

# Maskable 512x512
maskable = draw_medical_icon(512, is_maskable=True)
maskable.save(os.path.join(icons_dir, "icon-maskable-512x512.png"), "PNG")

# Favicon ICO
icon_32 = draw_medical_icon(32)
icon_32.save(os.path.join(icons_dir, "favicon.ico"), format="ICO")

print("All PWA icons generated successfully in static/icons/")
