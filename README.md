# Estate_AI_project — Property Video Studio

A polished Streamlit application that transforms real estate listing details and uploaded property photos into a promotional MP4 video. Developed as a prototype for the **Viraaj Ventures AI Developer Assignment**.

## Requirements
- Python 3.10 or newer
- An internet connection only for initial package installation (and optional Google Fonts UI styling)

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## How to Use
1. Enter the property name, location, price, type, key features, and call-to-action (CTA).
2. Upload 1–8 JPG/PNG/WEBP property photos (4–8 recommended).
3. Click **Generate Property Video**. Rendering may take a minute.
4. Preview the generated video and download the MP4 file.

## Approach
- Uses deterministic template-based caption and script generation, as permitted by the assignment.
- Does **not** call an LLM or fabricate property facts. Captions are generated from user-provided information.
- Pillow composes branded slides with subtle zoom effects; FFmpeg (via imageio-ffmpeg) encodes the video into H.264 MP4 format.
- Handles missing required fields, missing images, oversized images, and invalid image files.
- All processing is performed locally. Sensitive customer information should not be uploaded.

## Libraries / Services
Streamlit, Pillow, NumPy, imageio-ffmpeg (bundled FFmpeg executable). No external API or paid AI model is required.

## Limitations
- No spoken narration or background audio in the current prototype.
- Images are arranged in upload order and reused when there are more scenes than images.
- Rendering time depends on CPU performance and the number of scenes.
- Uses 960×540 resolution, 12 FPS, and 4 seconds per scene; designed as a working prototype rather than a production video editor.

## Sample Data
`sample_property.json` provides example property details. `sample_images/` contains synthetic illustration images, and `sample_video.mp4` is a generated promotional video example.

## Developer
**Arnav**  
B.Tech — Artificial Intelligence & Machine Learning  
CGC College of Engineering, Landran