from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import numpy as np
import imageio_ffmpeg
import subprocess

W, H = 960, 540

# Windows font paths
FONT = "C:/Windows/Fonts/arial.ttf"
BOLD = "C:/Windows/Fonts/arialbd.ttf"


def get_font(size, bold=False):
    """Load the requested font size and weight."""
    font_path = BOLD if bold else FONT

    try:
        return ImageFont.truetype(font_path, size)
    except OSError:
        return ImageFont.load_default()


def script_for(data):
    name = data['name'].strip()
    location = data['location'].strip()
    price = data['price'].strip()
    typ = data['type'].strip()

    features = [
        x.strip()
        for x in data['features'].split(',')
        if x.strip()
    ]

    scenes = [
        ('WELCOME HOME', name, location),
        ('DISCOVER YOUR SPACE', typ, location)
    ]

    for feature in features[:3]:
        scenes.append(('PROPERTY HIGHLIGHT', feature, name))

    scenes.append(('YOUR NEXT MOVE', price, data['cta'].strip()))

    return scenes


def render_frame(photo, scene, index, total, progress):

    im = ImageOps.fit(
        photo.convert('RGB'),
        (W, H),
        method=Image.Resampling.LANCZOS
    )

    # Subtle zoom animation
    z = 1 + 0.055 * progress

    resized = im.resize(
        (int(W * z), int(H * z)),
        Image.Resampling.BICUBIC
    )

    x = (resized.width - W) // 2
    y = (resized.height - H) // 2

    im = resized.crop(
        (x, y, x + W, y + H)
    ).convert('RGBA')

    # Gradient overlay
    gradient = Image.new('RGBA', (W, H))
    gd = ImageDraw.Draw(gradient)

    for yy in range(H):
        opacity = int(220 * (yy / H) ** 1.8)
        gd.line(
            (0, yy, W, yy),
            fill=(7, 14, 25, opacity)
        )

    im = Image.alpha_composite(im, gradient)
    d = ImageDraw.Draw(im)

    # Brand label
    d.rounded_rectangle(
        (46, 35, 225, 70),
        radius=12,
        fill=(255, 255, 255, 38)
    )

    d.text(
        (61, 45),
        'ESTATEMOTION AI',
        font=get_font(14, True),
        fill='white'
    )

    eyebrow, headline, detail = scene

    # Section heading
    d.text(
        (56, 345),
        eyebrow,
        font=get_font(17, True),
        fill=(112, 235, 210)
    )

    # Wrap long headlines
    lines = []
    current = ''

    for word in headline.split():

        candidate = (current + ' ' + word).strip()

        if (
            d.textbbox(
                (0, 0),
                candidate,
                font=get_font(40, True)
            )[2] > W - 112 and current
        ):
            lines.append(current)
            current = word
        else:
            current = candidate

    if current:
        lines.append(current)

    lines = lines[:2]

    y = 377 if len(lines) == 1 else 354

    for line in lines:
        d.text(
            (54, y),
            line,
            font=get_font(40, True),
            fill='white',
            stroke_width=1,
            stroke_fill=(0, 0, 0)
        )
        y += 48

    # Property details
    d.text(
        (57, min(y + 6, 491)),
        detail[:90],
        font=get_font(19),
        fill=(229, 237, 244)
    )

    # Progress bar
    d.rounded_rectangle(
        (55, 515, W - 55, 519),
        radius=2,
        fill=(255, 255, 255, 85)
    )

    d.rounded_rectangle(
        (
            55,
            515,
            55 + int((W - 110) * (index + progress) / total),
            519
        ),
        radius=2,
        fill=(102, 232, 205)
    )

    return im.convert('RGB')


def generate_video(
    data,
    images,
    out_path,
    seconds_per_scene=4,
    fps=12,
    progress_callback=None
):

    if not images:
        raise ValueError(
            'Upload at least one property image.'
        )

    scenes = script_for(data)

    out_path = Path(out_path)
    out_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    frames_per_scene = int(seconds_per_scene * fps)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    cmd = [
        ffmpeg,
        '-y',
        '-loglevel', 'error',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{W}x{H}',
        '-pix_fmt', 'rgb24',
        '-r', str(fps),
        '-i', '-',
        '-an',
        '-vcodec', 'libx264',
        '-preset', 'veryfast',
        '-crf', '24',
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
        str(out_path)
    ]

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:

        for idx, scene in enumerate(scenes):

            photo = images[idx % len(images)]

            for j in range(frames_per_scene):

                frame = render_frame(
                    photo,
                    scene,
                    idx,
                    len(scenes),
                    j / frames_per_scene
                )

                proc.stdin.write(
                    np.asarray(
                        frame,
                        dtype=np.uint8
                    ).tobytes()
                )

            if progress_callback:
                progress_callback(
                    (idx + 1) / len(scenes)
                )

        proc.stdin.close()

        error = proc.stderr.read().decode(
            errors='replace'
        )

        if proc.wait() != 0:
            raise RuntimeError(error)

    except Exception:
        proc.kill()
        proc.wait()
        raise

    finally:
        proc.stderr.close()

    return out_path
