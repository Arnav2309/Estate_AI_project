import streamlit as st
from PIL import Image, UnidentifiedImageError
from pathlib import Path
from io import BytesIO
import tempfile
from video_generator import generate_video, script_for

st.set_page_config(page_title='EstateMotion | Creative Studio', page_icon='🎞️', layout='wide', initial_sidebar_state='collapsed')
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root{color-scheme:dark}
html,body,.stApp,[data-testid="stAppViewContainer"]{font-family:'DM Sans',sans-serif!important;background:#171613!important;color:#F6F0E7!important}
[data-testid="stHeader"]{background:transparent!important}
[data-testid="stMainBlockContainer"]{max-width:1480px;padding-top:2rem;padding-bottom:5rem}
h1,h2,h3{font-family:'Playfair Display',serif!important;letter-spacing:-.025em!important;color:#FFF6EA!important}
h1{font-size:clamp(2.6rem,5vw,5rem)!important;line-height:1.06!important}
h2{font-size:2rem!important}
h3{font-size:1.4rem!important}
p,span,li,div[data-testid="stMarkdownContainer"]{color:inherit}
[data-testid="stWidgetLabel"] p, label, [data-testid="stCaptionContainer"]{color:#E9DED0!important;opacity:1!important}
input,textarea,[data-baseweb="select"]>div{background:#26231F!important;color:#FFF7EC!important;border:1px solid #786554!important;border-radius:10px!important}
input::placeholder,textarea::placeholder{color:#C5B5A4!important;opacity:1!important}
[data-baseweb="select"] span,[data-baseweb="select"] input{color:#FFF7EC!important}
[data-testid="stFileUploader"]{background:#29241E!important;border:2px dashed #B47C51!important;border-radius:18px;padding:12px}
[data-testid="stFileUploader"] *{color:#F5E9DA!important}
[data-testid="stForm"]{background:#211F1B;border:1px solid #50453A;border-radius:22px;padding:22px}
[data-testid="stButton"] button{background:#2B2722!important;color:#F6EBDD!important;border:1px solid #665244!important;border-radius:12px!important;transition:all .2s ease!important;min-height:48px}
[data-testid="stButton"] button:hover{background:#573D2B!important;border-color:#F3A56E!important;color:#FFF!important;transform:translateY(-2px);box-shadow:0 8px 22px #0005}
[data-testid="stButton"] button[kind="primary"], [data-testid="stFormSubmitButton"] button{background:#EFA36C!important;color:#231811!important;border:0!important;font-weight:800!important}
[data-testid="stButton"] button[kind="primary"]:hover,[data-testid="stFormSubmitButton"] button:hover{background:#FFC194!important;color:#231811!important}
[data-testid="stImage"] img{border-radius:14px;border:1px solid #675140}
[data-testid="stAlert"]{border-radius:14px}
[data-testid="stSidebar"]{background:#24201C!important}
[data-testid="stSidebar"] *{color:#F5E8D9!important}
hr{border-color:#504438!important}
.brand{font-size:1rem;font-weight:800;letter-spacing:.19em;color:#F4AC78;margin-bottom:20px}
.kicker{font-size:.78rem;letter-spacing:.21em;font-weight:800;color:#F4AC78;margin-bottom:12px}
.intro{color:#D5C5B4;font-size:1.12rem;line-height:1.85;max-width:390px}
.editorial{border-left:3px solid #F0A16B;padding:12px 0 12px 18px;margin:26px 0;color:#F3E7D8;line-height:1.75}
.micro{font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:#F1B88E;font-weight:800}
.photo-frame{background:#28231E;border:1px solid #69513E;border-radius:20px;padding:14px;margin:0 0 16px}
.tiny-note{color:#C8B8A7;font-size:.92rem;line-height:1.65}
.section-line{height:1px;background:linear-gradient(90deg,#A76B42,transparent);margin:22px 0}
</style>''', unsafe_allow_html=True)

st.markdown('<div class="brand">◈ ESTATEMOTION <span style="color:#F5EADD;font-weight:400">/ CREATIVE STUDIO</span></div>',unsafe_allow_html=True)
left,center,right=st.columns([0.9,1.25,1.05],gap='large',vertical_alignment='top')
with left:
    st.markdown('<div class="kicker">PROPERTY STORIES, REIMAGINED</div>',unsafe_allow_html=True)
    st.title('Every space has a story.')
    st.markdown('<div class="intro">Turn a collection of property photographs into a captivating, ready-to-share video. No editing timeline. No design experience. Just your listing, brought to life.</div>',unsafe_allow_html=True)
    st.markdown('<div class="editorial"><b style="color:#FFC194">01 / Add your details</b><br>Tell us what makes your property special.<br><br><b style="color:#FFC194">02 / Curate your photos</b><br>Images become the scenes of your story.<br><br><b style="color:#FFC194">03 / Create & share</b><br>Preview your film and export an MP4.</div>',unsafe_allow_html=True)
    st.markdown('<div class="tiny-note">✦ Built for clarity, honest property descriptions and effortless creation. No external AI API key required.</div>',unsafe_allow_html=True)
with center:
    st.markdown('<div class="micro">THE VISUAL CANVAS</div>',unsafe_allow_html=True)
    st.subheader('Your property, in focus.')
    st.markdown('<div class="tiny-note">Add 4–8 photographs for a fuller story. The order of uploaded photos determines the order of video scenes.</div>',unsafe_allow_html=True)
    uploaded=st.file_uploader('Drop your property photographs here',type=['jpg','jpeg','png','webp'],accept_multiple_files=True,help='Up to 8 images, 12 MB each.')
    if uploaded:
        st.markdown(f'<div class="micro">{len(uploaded)} PHOTO(S) SELECTED</div>',unsafe_allow_html=True)
        try:
            st.image(uploaded[0],caption='Cover photograph · Scene 01',use_container_width=True)
            gallery=st.columns(3,gap='small')
            for i,file in enumerate(uploaded[1:8]):
                with gallery[i%3]:st.image(file,caption=f'{i+2:02d}',use_container_width=True)
        except (OSError,UnidentifiedImageError):
            st.warning('One of your photographs could not be previewed. Try a different JPG or PNG.')
    else:
        st.markdown('<div class="photo-frame"><div style="height:260px;display:flex;align-items:center;justify-content:center;flex-direction:column;background:radial-gradient(circle at 40% 35%,#584132,#302820 60%,#241F1B);border-radius:12px;text-align:center"><div style="font-size:3.4rem">▧</div><div style="font-family:Playfair Display,serif;font-size:1.5rem;color:#FFF0E0">Your images take center stage</div><div style="color:#D9BDA6;margin-top:10px">Upload photos to see your visual gallery</div></div></div>',unsafe_allow_html=True)
    st.markdown('<div class="tiny-note">Images stay on your machine while you use this locally hosted app.</div>',unsafe_allow_html=True)
with right:
    st.markdown('<div class="micro">THE PROPERTY BRIEF</div>',unsafe_allow_html=True)
    st.subheader('Tell us about the place.')
    with st.form('property_form'):
        name=st.text_input('Property name *',placeholder='Green Valley Residency')
        location=st.text_input('Location *',placeholder='Sector 150, Noida')
        price=st.text_input('Price *',placeholder='₹85 lakh')
        typ=st.selectbox('Property type',['2 BHK Apartment','3 BHK Apartment','Villa','Studio','Commercial Space','Plot','Other'])
        features=st.text_area('Key features (comma separated)',placeholder='Balcony, modular kitchen, covered parking',height=100)
        cta=st.text_input('Call to action *',value='Contact us to schedule a visit')
        submitted=st.form_submit_button('✦ Create my property video',type='primary',use_container_width=True)
    st.markdown('<div class="tiny-note">All video captions are derived from the facts you enter. Review property details before publishing.</div>',unsafe_allow_html=True)

if name and location and price:
    st.markdown('<div class="section-line"></div><div class="micro">INTERACTIVE STORYBOARD</div>',unsafe_allow_html=True)
    st.subheader('Explore your story, scene by scene.')
    st.caption('Hover over a scene to highlight it. Click to reveal the full text that will appear in your video.')
    data={'name':name,'location':location,'price':price,'type':typ,'features':features,'cta':cta}
    scenes=script_for(data)
    scene_cols=st.columns(min(len(scenes),4),gap='small')
    for i,(tag,headline,detail) in enumerate(scenes):
        with scene_cols[i%len(scene_cols)]:
            if st.button(f'{i+1:02d}  ·  {tag}',key=f'scene_{i}',use_container_width=True):
                st.session_state.selected_scene=i
    selected=st.session_state.get('selected_scene',0)
    if selected>=len(scenes):selected=0
    tag,headline,detail=scenes[selected]
    st.markdown(f'<div style="background:#2B241E;border-left:4px solid #F2A66E;border-radius:12px;padding:20px;margin-top:10px"><div class="micro">SCENE {selected+1:02d} / {tag}</div><div style="font-family:Playfair Display,serif;font-size:1.6rem;color:#FFF3E6;margin:8px 0">{__import__("html").escape(str(headline))}</div><div style="color:#E5D2C0">{__import__("html").escape(str(detail))}</div></div>',unsafe_allow_html=True)

if submitted:
    missing=[label for label,val in [('Property name',name),('Location',location),('Price',price),('Call to action',cta)] if not val.strip()]
    if missing:st.error('Please complete: '+', '.join(missing))
    elif not uploaded:st.error('Please upload at least one image to generate the video.')
    elif len(uploaded)>8:st.error('Please upload a maximum of 8 images.')
    else:
        images=[]
        try:
            for file in uploaded:
                if file.size>12*1024*1024:raise ValueError(f'{file.name} is larger than 12 MB.')
                img=Image.open(BytesIO(file.getvalue()));img.load();images.append(img.copy())
            data={'name':name,'location':location,'price':price,'type':typ,'features':features,'cta':cta}
            st.subheader('Rendering your property story')
            bar=st.progress(0,text='Preparing scenes…')
            with tempfile.TemporaryDirectory() as tmp:
                output=Path(tmp)/'property_video.mp4'
                generate_video(data,images,output,progress_callback=lambda p:bar.progress(int(p*100),text=f'Rendering scenes · {int(p*100)}%'))
                st.session_state.video_bytes=output.read_bytes()
            st.session_state.video_name='estate_motion_'+''.join(c if c.isalnum() else '_' for c in name.lower())+'.mp4'
            st.success('Your property video is ready!')
        except (UnidentifiedImageError,OSError,ValueError,RuntimeError,BrokenPipeError) as exc:
            st.error(f'Unable to create video: {exc}')
if 'video_bytes' in st.session_state:
    st.markdown('<div class="section-line"></div><div class="micro">FINAL CUT</div>',unsafe_allow_html=True)
    st.subheader('Your story is ready to share.')
    st.video(st.session_state.video_bytes)
    st.download_button('↓ Download MP4',data=st.session_state.video_bytes,file_name=st.session_state.video_name,mime='video/mp4',type='primary')
    st.caption('Captions use transparent rule-based templates. No external AI service is required.')
