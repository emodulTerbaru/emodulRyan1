import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import io
import pandas as pd
from pydub import AudioSegment

st.set_page_config(layout="wide")  # Atau "centered"
kata = ['kepala','mata','tangan','senang','sedih','ayah','ibu','kakak','adik','rumah']
kalimat = ['Aku punya tubuh yang hebat',
           'Mataku bisa melihat bunga warna-warni di taman',
           'Telingaku mendengar suara burung di pagi hari',
           'Tanganku bisa menulis dan menggambar',
           'Kakiku bisa berjalan dan berlari',
           'Kadang aku merasa senang',
           'Aku tersenyum saat bermain bersama teman',
           'Kadang aku merasa sedih',
           'Aku menangis jika mainanku hilang',
           'Aku juga punya hobi',
           'Aku suka bermain bola di lapangan',
           'Kadang aku menggambar gunung dan laut',
           'Aku sayang tubuhku',
           'Aku akan menjaga tubuhku tetap sehat dengan makan sayur, buah, dan minum air putih',
           'Aku juga akan berolahraga dan beristirahat cukup']
mengeja = ['A-ku pu-nya tu-buh.',
            'Ma-ta-ku un-tuk me-li-hat.',
            'Te-li-nga-ku un-tuk men-de-ngar.',
            'Ta-ngan-ku un-tuk me-nu-lis.',
            'Ka-ki-ku ber-ja-lan.',
            'A-ku se-nang ber-ma-in.',
            'A-ku pu-nya ho-bi.',
            'A-ku su-ka ber-ma-in bo-la di la-pa-ngan.',
            'A-ku sa-yang tu-buh-ku.',
            'A-ku a-kan men-ja-ga tu-buh-ku te-tap se-hat.'
            ]
if "kelompok" not in st.session_state:
    st.session_state.kelompok={'kondisi1':True, 'kondisi2':False, 'kondisi3':False, 'kondisi4':False, 'kondisi5':False}
if "indeks" not in st.session_state:
    st.session_state.indeks = 0
if "indeks2" not in st.session_state:
    st.session_state.indeks2 = 0
if "tombol" not in st.session_state:
    st.session_state.tombol={'kondisi1':False,'kondisi2':False}
if "hasil1" not in st.session_state:
    st.session_state.hasil1={'benar':0,'salah':0}
if "indeks1" not in st.session_state:
    st.session_state.indeks1 = 0
if "hasil2" not in st.session_state:
    st.session_state.hasil2={'benar':0,'salah':0}
if "kumpulan" not in st.session_state:
    st.session_state.kumpulan = {'Soal':[],'Jawaban':[],'hasil':[]}
if "data_teks" not in st.session_state:
    st.session_state.data_teks={'tulisan':"",'data':[],'cerita':'','kumpulkan':{}}
if "kontrol" not in st.session_state:
    st.session_state.kontrol=False
if "kontrol1" not in st.session_state:
    st.session_state.kontrol1=False
if "tampilkan" not in st.session_state:
    st.session_state.tampilkan=""
if "tampilkan1" not in st.session_state:
    st.session_state.tampilkan1=""
if "kunci2" not in st.session_state:
    st.session_state.kunci2={}
if "kunci3" not in st.session_state:
    st.session_state.kunci3={}
st.markdown("""
<style>
    :root{
        --pink:#ff6fb1;
        --yellow:#ffd166;
        --green:#06d6a0;
        --blue:#4cc9f0;
        --purple:#b5179e;
        --bg:#fff7ef;
        --bg1: #0f172a;
        --bg2: #0b1220;
        --card: rgba(255,255,255,0.06);
        --accent: linear-gradient(90deg,#7c3aed,#06b6d4);
        --glass: rgba(255,255,255,0.06);
        --muted: rgba(255,255,255,0.65);
      }
	.e4man114{
 		background-color:pink;
	}
    .e3g0k5y1{
		background-color:blue;
        color:white;
	}
    #judul{
        font-size: clamp(20px, 4vw, 30px);
        line-height:1.05;
        text-align:center;
        color:white;
        padding:8px 18px;
        border-radius:28px;
        background: linear-gradient(135deg, var(--pink), var(--purple));
        text-shadow: 0 6px 0 rgba(0,0,0,.12);
        display:inline-block;
        transform: translateY(0);
        animation: bubble 3s ease-in-out infinite;
    }
    @keyframes bubble{
        0%,100%{ transform: translateY(0) scale(1); filter: drop-shadow(0 8px 0 rgba(0,0,0,.1)); }
        50%{ transform: translateY(-10px) scale(1.03); filter: drop-shadow(0 16px 0 rgba(0,0,0,.08)); }
    }
    #konten{
        width:100%;
        height:1700px;
        border:2px solid black;
        border-radius:20px;
        margin-top:10px;
        box-shadow:2px 2px 2px 3px red, -2px -2px 2px 3px green;
    }
    #kata{
        font-family:broadway;
        font-size:40px;
        text-align:center;
        color:blue;
        text-shadow:0px 0px 3px yellow;
    }
    #kotak, #kotak1{
        width:40%;
        height:200px;
        border:2px solid black;
        border-radius:30px;
        background-color:white;
        box-shadow:2px 2px 3px 2px yellow, -2px -2px 2px 2px cyan;
        color:black;
        text-align:center;
        padding:20px;
        font-size:60px;
        font-family:"Times New Roman";
        color:green;
        font-weight:bold;
    }
    #kotak1{
        width:100%;
        height:50px;
        font-size:20px;
        padding:5px;
    }
    #kotakan{
        display:flex;
        justify-content: center;
        margin-bottom:20px;
    }
    .st-key-tmbl2 .e1haskxa2{
        background-color:green;
        color:white;
    }
    .st-key-tmbl3 .e1haskxa2{
        background-color:blue;
        color:white;
    }
    .st-key-tmbl4 .e1haskxa2{
        background-color:orange;
        color:black;
    }
    .st-key-tmbl5 .e1haskxa2{
        background-color:yellow;
        color:black;
    }
    .st-key-tmbl10 .e1haskxa2{
        background-color:grey;
        color:blue;
    }
    .hasil{
        font-size:clamp(28px,5vw,44px); font-weight:800;
        animation:colorfade 5s infinite alternate;
    }
    @keyframes colorfade{
        0%{color:#ff6aa2}
        25%{color:#64d2ff}
        50%{color:#5cffb5}
        75%{color:#ffdd57}
        100%{color:#ff6aa2}
    }
    .subjudul{
        text-align:center;
        border:2px solid white;
        border-radius:10px;
        width:100%;
        color:black;
        background-color: cyan;
        font-size:12px;
        padding:5px;
        margin-bottom:10px;
        font-weight:bold;
        box-shadow:0px 0px 2px 5px purple;
    }
    .tulis{
        font-size:60px;
        font-family:broadway;
        color:yellow;
    }
    .skor1{
        font-family:"comic sans ms";
        font-size:20px;
        color:blue;
        text-shadow:0 0 3px 4px yellow;
    }
      /* Card pusat */
    .card{
      width:100%;
      max-width:900px;
      border-radius:18px;
      padding: clamp(22px, 3.5vw, 36px);
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
      box-shadow: 0 8px 30px rgba(2,6,23,0.6), inset 0 1px 0 rgba(255,255,255,0.02);
      backdrop-filter: blur(8px) saturate(120%);
      border: 1px solid rgba(255,255,255,0.04);
      display:grid;
      grid-template-columns: 1fr 260px;
      gap:20px;
      align-items:center;
      margin-bottom:10px;
    }

    /* Area teks */
    .lead{
      padding-right:10px;
    }
    .kicker{
      display:inline-block;
      font-weight:600;
      font-size:13px;
      letter-spacing:0.14em;
      text-transform:uppercase;
      color:var(--muted);
      background: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
      padding:6px 10px;
      border-radius:999px;
      margin-bottom:12px;
    }

    h1{
      font-family: "Playfair Display", serif;
      font-size: clamp(28px, 4.5vw, 48px);
      line-height:1.05;
      margin-bottom:12px;
      letter-spacing:-0.02em;
      background: var(--accent);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      font-weight:700;
      /* subtle entrance */
      opacity:0;
      transform: translateY(6px);
      animation: fadeUp 700ms ease forwards 250ms;
    }

    p.lead-desc{
      color:var(--muted);
      font-size: clamp(14px, 1.6vw, 16px);
      margin-bottom:18px;
      opacity:0;
      transform: translateY(6px);
      animation: fadeUp 700ms ease forwards 420ms;
    }

    /* Typewriter underline for the sentence (pure CSS) */
    .sentence {
      display:inline-block;
      font-weight:600;
      font-size: 25px;
      font-family:"comic sans ms";
      color: yellow;
      position:relative;
      padding-bottom:6px;
      white-space:nowrap;
      overflow:hidden;
      /* simulate typing by clipping width */
      max-width:0ch;
      animation:
        typing 1400ms steps(30,end) forwards 650ms,
        caret 900ms steps(1) infinite 2050ms;
    }

    /* little decorative underline that grows */
    .sentence::after{
      content:"";
      position:absolute;
      left:0;
      bottom:0;
      height:3px;
      width:0%;
      border-radius:4px;
      background:linear-gradient(90deg,#7c3aed,#06b6d4);
      animation: underlineGrow 700ms ease forwards 2100ms;
      opacity:0.95;
    }

    /* side decorative panel */
    .panel{
      display:flex;
      align-items:center;
      justify-content:center;
      border-radius:12px;
      padding:18px;
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border: 1px solid rgba(255,255,255,0.03);
      text-align:center;
      min-height:140px;
    }
    .panel .emoji{
      font-size:48px;
      margin-bottom:8px;
      display:block;
      filter:drop-shadow(0 6px 18px rgba(12,38,63,0.6));
    }
    .panel small{ display:block; color:var(--muted); font-size:13px; margin-top:6px; }

    /* Animations */
    @keyframes typing {
      from { max-width: 0ch; }
      to   { max-width: 60ch; } /* plenty for most sentences */
    }
    @keyframes caret {
      50% { box-shadow: inset -0.6ch 0 0 rgba(255,255,255,0.12); }
    }
    @keyframes underlineGrow {
      from { width: 0%; opacity:0; transform: translateY(4px); }
      to   { width: 66%; opacity:1; transform: translateY(0); }
    }
    @keyframes fadeUp {
      to { opacity:1; transform: translateY(0); }
    }

    /* Responsive tweaks */
    @media (max-width:820px){
      .card{ grid-template-columns: 1fr; }
      .panel{ order:-1; }
    }

    /* accessible focus style (for keyboard users) */
    button:focus, a:focus { outline: 3px solid rgba(99,102,241,0.16); outline-offset:3px; border-radius:8px; }
    .marquee {
      position: relative;
      overflow: hidden;
      white-space: nowrap;
      width: 100%;
      background: linear-gradient(90deg, #ff0055, #ffcc00, #33ccff, #ff0055);
      background-size: 300% 100%;
      animation: bgMove 6s linear infinite;
      margin-bottom:10px;
      border-radius:10px;
    }

    .marquee span {
      display: inline-block;
      padding: 15px 30px;
      font-size: 28px;
      font-weight: bold;
      color: #fff;
      text-transform: uppercase;
      animation: scrollText 20s linear infinite;
    }

    @keyframes scrollText {
      from {
        transform: translateX(100%);
      }
      to {
        transform: translateX(-100%);
      }
    }

    @keyframes bgMove {
      0% { background-position: 0% 50%; }
      100% { background-position: 100% 50%; }
    }

</style>
""",unsafe_allow_html=True)

# Halaman 1
def halaman1():
    st.markdown("""
    <div id='judul'>PEMBAGIAN TEMA PEMBELAJARAN LITERASI BACA TULIS PADA MODEL PROPEPA LEARN E
    </div>""",unsafe_allow_html=True)
    st.markdown("""
    <iframe id='konten' src='https://emodulterbaru.github.io/emodulRyan/tulisan1.html'></iframe>
    """,unsafe_allow_html=True)
    
#teks ke suara
def tulisSuara(teks):
    """Simulasi text-to-speech dengan display yang menarik"""
    # Proses TTS
    tts = gTTS(teks, lang="id")  # bahasa Indonesia
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    # Putar audio di Streamlit
    st.audio(mp3_fp, format="audio/mp3")
    st.success(f"dengarkan kata: **{teks.upper()}**")
    
# Halaman 2

def halaman2():
    st.markdown('''
    <div class="marquee">
    <span> &#128221; Menulis dan Membaca Kata &#128214;</span>
    </div>
    ''',unsafe_allow_html=True)
    st.markdown("<div class='tulis'>&#128221; Menulis Kata</div>",unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div id="kata">Tuliskan Kata:</div>
    """,unsafe_allow_html=True)
    if st.button("berikut",key="tmbl1",type="primary"):
        st.session_state.indeks +=1
    st.write("##### Kata Berikutnya: ")
    st.markdown(f"""
    <div id='kotakan'>
    <div id='kotak'>{kata[st.session_state.indeks]}</div>
    </div>
    """,unsafe_allow_html=True)
    kolom = st.columns(2)
    with kolom[0]:
        tulisan = st.text_input("tulisan kata")
        tekan = st.button("Periksa",key="tmbl4")
        if tulisan and tekan:
            st.session_state.kumpulan['Soal'].append(kata[st.session_state.indeks])
            st.session_state.kumpulan['Jawaban'].append(tulisan)
            if tulisan.lower()==kata[st.session_state.indeks]:
                st.markdown("<div class='hasil'>Benar &#128077;</div>",unsafe_allow_html=True)
                st.session_state.hasil1['benar']+=1
                st.session_state.kumpulan['hasil'].append('benar')
            else:
                st.markdown("<div class='hasil'>Salah &#128531;</div>",unsafe_allow_html=True)
                st.session_state.hasil1['salah']+=1
                st.session_state.kumpulan['hasil'].append('salah')
        if st.session_state.hasil1['benar']>0 or st.session_state.hasil1['salah']>0:
            st.dataframe(st.session_state.hasil1)
            st.dataframe(st.session_state.kumpulan)
            
    with kolom[1]:
        st.write("Kata ke Suara")
        if st.button("Suara",key="tmbl2"):
            tulisSuara(kata[st.session_state.indeks])
    if st.session_state.hasil1['benar']>0 or st.session_state.hasil1['salah']>0:
            st.markdown("<div></div>",unsafe_allow_html=True)
    st.divider()
    st.markdown("<div class='tulis'>&#128214; Membaca Kata</div>",unsafe_allow_html=True)
    durasi = st.slider("Durasi rekaman (detik)", 1, 10, 5)
    if st.button("Mulai Rekam"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info(f"Silakan bicara... (otomatis berhenti setelah {durasi} detik)")
            audio = recognizer.listen(source, phrase_time_limit=durasi)  # otomatis stop
        try:
            text = recognizer.recognize_google(audio, language="id-ID")
            st.success("Hasil Transkripsi:")
            if text.lower()==kata[st.session_state.indeks]:
                st.markdown("<div class='hasil'>Benar &#128077;</div>",unsafe_allow_html=True)
            else:
                st.markdown("<div class='hasil'>Salah &#128531;</div>",unsafe_allow_html=True)
        except sr.UnknownValueError:
            st.error("Suara tidak dikenali")
        except sr.RequestError as e:
            st.error(f"Error: {e}")
        
    
def halaman3():
    st.markdown('''
    <div class="marquee">
    <span> &#128221; Menulis dan Membaca Kalimat &#128214;</span>
    </div>
    ''',unsafe_allow_html=True)
    st.markdown("<div class='tulis'>&#128221; Menulis Kalimat</div>",unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div id="kata">Tuliskan Kalimat:</div>
    """,unsafe_allow_html=True)
    if st.button("berikut",key="tmbl6",type="primary"):
        st.session_state.indeks1 +=1
    st.write("##### Kalimat Berikutnya: ")
    st.markdown(f"""
    <div id='kotakan'>
    <div id='kotak1'>{kalimat[st.session_state.indeks1]}</div>
    </div>
    """,unsafe_allow_html=True)
    kolom = st.columns(2)
    with kolom[0]:
        tulisan = st.text_input("tulisan kata",key='teks1')
        tekan = st.button("Periksa",key="tmbl7")
        if tulisan and tekan:
            if tulisan.lower()==kalimat[st.session_state.indeks1].lower():
                st.markdown("<div class='hasil'>Benar &#128077;</div>",unsafe_allow_html=True)
                st.session_state.hasil2['benar']+=1
            else:
                st.markdown("<div class='hasil'>Salah &#128531;</div>",unsafe_allow_html=True)
                st.session_state.hasil2['salah']+=1
            tulisSuara(tulisan)
    with kolom[1]:
        st.write("Kata ke Suara")
        if st.button("Suara",key="tmbl8"):
            tulisSuara(kalimat[st.session_state.indeks1])
    if st.session_state.hasil2['benar']>0 or st.session_state.hasil2['salah']>0:
            st.markdown("<div></div>",unsafe_allow_html=True)
    st.divider()
    st.markdown("<div class='tulis'>&#128214; Membaca Kalimat</div>",unsafe_allow_html=True)
    st.markdown(f"""
    <div id='kotakan'>
    <div id='kotak1'>{kalimat[st.session_state.indeks1]}</div>
    </div>
    """,unsafe_allow_html=True)
    durasi = st.slider("Durasi rekaman (detik)", 1, 10, 5)
    if st.button("Mulai Rekam",key="tmbl9"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info(f"Silakan bicara... (otomatis berhenti setelah {durasi} detik)")
            audio = recognizer.listen(source, phrase_time_limit=durasi)  # otomatis stop
        try:
            text = recognizer.recognize_google(audio, language="id-ID")
            st.success("Hasil Transkripsi:")
            st.write(text)
            if text.lower()==kalimat[st.session_state.indeks1].lower():
                st.markdown("<div class='hasil'>Benar &#128077;</div>",unsafe_allow_html=True)
            else:
                st.markdown("<div class='hasil'>Salah &#128531;</div>",unsafe_allow_html=True)
        except sr.UnknownValueError:
            st.error("Suara tidak dikenali")
        except sr.RequestError as e:
            st.error(f"Error: {e}")

def halaman4():
    st.markdown('''
    <div class="marquee">
    <span> &#128221; Menulis dan Membaca Cerita &#128214;</span>
    </div>
    ''',unsafe_allow_html=True)
    koding1='''
    <!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cerita Petualangan Si Kucing</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
            position: relative;
        }
        
        .header::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="%23ffffff" fill-opacity="0.1" d="M0,96L48,112C96,128,192,160,288,165.3C384,171,480,149,576,138.7C672,128,768,128,864,144C960,160,1056,192,1152,197.3C1248,203,1344,181,1392,170.7L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
            background-size: cover;
        }
        
        .title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }
        
        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }
        
        .content {
            padding: 40px;
            line-height: 1.8;
        }
        
        .chapter {
            margin-bottom: 40px;
            position: relative;
        }
        
        .chapter-title {
            font-size: 1.8rem;
            color: #5a67d8;
            margin-bottom: 20px;
            padding-left: 20px;
            border-left: 5px solid #667eea;
            font-weight: 600;
        }
        
        .paragraph {
            margin-bottom: 20px;
            font-size: 1.1rem;
            color: #333;
        }
        
        .highlight {
            background: linear-gradient(120deg, #ffd89b 0%, #19547b 100%);
            padding: 2px 8px;
            border-radius: 4px;
            color: #fff;
            font-weight: 600;
        }
      
        .character {
            display: inline-block;
            background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
            padding: 4px 12px;
            border-radius: 20px;
            margin-right: 8px;
            color: #333;
            font-weight: 600;
            box-shadow: 0 2px 10px rgba(255, 154, 158, 0.3);
        }
        
        .illustration {
            width: 100%;
            height: 250px;
            object-fit: contain;
            border-radius: 15px;
            margin: 25px 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
	    background:url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSrLax2wubXh9IYoqh4ZEi0JruyElqEcsDHg&s");
            background-repeat:no-repeat;
            background-size:cover;
        }
         
         .footer {
            text-align: center;
            padding: 30px;
            background: #f8fafc;
            color: #64748b;
            font-size: 0.9rem;
        }
        
        /* Animasi */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .chapter {
            animation: fadeIn 0.8s ease-out forwards;
            opacity: 0;
        }
        
        .chapter:nth-child(1) { animation-delay: 0.2s; }
        .chapter:nth-child(2) { animation-delay: 0.4s; }
        .chapter:nth-child(3) { animation-delay: 0.6s; }
        .chapter:nth-child(4) { animation-delay: 0.8s; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">Tubuhku Hebat</h1>
            <p class="subtitle">(Tema: Diriku – Kata Kunci: Anggota Tubuhku, Perasaanku, dan Hobiku)</p>
        </div>
        
        <div class="content">
	    <img src="https://www.kawananimasiku.id/assets/upload/KARAKTER-MINUM-AIR-LK.gif" alt="Tubuhku Hebat" class="illustration">
            <div class="chapter">
                <p class="paragraph">
                    Aku punya tubuh yang hebat.<br>
		    Mataku bisa melihat bunga warna-warni di taman.<br>
	            Telingaku mendengar suara burung di pagi hari.<br>
	            Tanganku bisa menulis dan menggambar.<br>
		    Kakiku bisa berjalan dan berlari.<br>
                </p>
                <p class="paragraph">
                    Kadang aku merasa senang.<br>
		    Aku tersenyum saat bermain bersama teman.<br>
		    Kadang aku merasa sedih.<br>
		    Aku menangis jika mainanku hilang.<br>
		    Aku juga punya hobi.<br>
		    Aku suka bermain bola di lapangan.<br>
		    Kadang aku menggambar gunung dan laut.<br>
                </p>
  		<p class="paragraph">
                    Aku sayang tubuhku.<br>
		    Aku akan menjaga tubuhku tetap sehat dengan makan sayur, buah, dan minum air putih.<br>
		    Aku juga akan berolahraga dan beristirahat cukup.
                </p>  
            </div>
        
        <div class="footer">
            <p>© 2025 Cerita Anak | Belajar Menulis dan Membaca</p>
        </div>
    </div>
</body>
</html>
    '''
    st.components.v1.html(koding1,height=1250)


def halaman5():
    st.markdown('''
    <div class="marquee">
    <span> 🎉 Mengeja Kalimat 🎉   </span>
    </div>
    ''',unsafe_allow_html=True)
    if st.button("selanjutnya"):
        st.session_state.indeks2 +=1
    st.markdown(f'''
    <div class="card" role="region" aria-label="Kalimat menarik" style="background-color:black">
    <div class="lead">
      <span class="kicker" style="background-color:gray">Eja Kalimat Ini</span>
      <!-- Ganti kalimat di bawah sesuai kebutuhan -->
      <h1><span class="sentence">{mengeja[st.session_state.indeks2]}</span></h1>

    </div>

    <div class="panel" aria-hidden="true" style="background-color:cyan">
      <div>
        <span class="emoji">🎯</span>
        <small style="color:black">Kalimat singkat &amp; menarik</small>
      </div>
    </div>
  </div>
    ''',unsafe_allow_html=True)
    if st.button("Baca Ejaan"):
        st.session_state.kontrol1=True
        st.session_state["ejaan"] = None
        st.rerun()
    if st.session_state.kontrol1:
        audio_value1 = st.audio_input("Silahkan Membaca Kalimat")
        baca_kalimat=''
        kalimat1=[]
        kalimat2={}
        kalimat3={}
        kalimat4=[]
        kalimat5={}
        kalimat6={}
        skor2 = 0
        if audio_value1:
            st.audio(audio_value1)
             # 1. Simpan sementara
            with open("temp_audio.wav", "wb") as f:
                f.write(st.session_state['ejaan'].getbuffer())

            # 2. Konversi audio (kalau bukan wav)
            sound = AudioSegment.from_file("temp_audio.wav")
            sound.export("converted.wav", format="wav")

            # 3. Gunakan SpeechRecognition
            recognizer = sr.Recognizer()
            with sr.AudioFile("converted.wav") as source:
                audio_data = recognizer.record(source)
                try:
                    # Bisa pakai engine lain: sphinx (offline), google (butuh internet)
                    #text = recognizer.recognize_sphinx(audio_data)  # offline
                    text = recognizer.recognize_google(audio_value1, language="id-ID")  # online
                    st.subheader("Hasil Transkripsi:")
                    st.write(text)
                    st.session_state.tampilkan1=text
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
            if st.session_state.tampilkan1:
                baca_kalimat = mengeja[st.session_state.indeks2].replace("-","")
                baca_kalimat = baca_kalimat.replace(".","")
                kalimat1 = baca_kalimat.split(" ")
                kalimat2 = set(kalimat1)
                for i in kalimat2:
                    kalimat3[i.lower()]=kalimat1.count(i)
                kalimat4 = st.session_state.tampilkan1.split(" ")
                kalimat5 = set(kalimat4)
                for i in kalimat5:
                    kalimat6[i.lower()] = kalimat4.count(i)
                for i in kalimat2:
                    try:
                        if kalimat3[i]==kalimat6[i]:
                            skor2 +=1
                    except:
                        pass
                st.write(kalimat3)
                st.write(kalimat6)
            if skor2 == len(list(kalimat3.keys())):
                st.balloons()
        
# Navigasi berdasarkan state
if st.session_state.kelompok['kondisi1']:
    halaman1()
if st.session_state.kelompok['kondisi2']:
    halaman2()
if st.session_state.kelompok['kondisi3']:
    halaman3()
if st.session_state.kelompok['kondisi4']:
    halaman4()
if st.session_state.kelompok['kondisi5']:
    halaman5()
    

# Tombol Sidebar
if st.sidebar.button('Halaman 1',key='tmbl5'):
    st.session_state.kelompok = {'kondisi1':True, 'kondisi2':False, 'kondisi3':False,'kondisi4':False, 'kondisi5':False}
    st.rerun()
st.sidebar.divider()
st.sidebar.markdown("<div class='subjudul'>Diriku dan Keluargaku</div>", unsafe_allow_html=True)
with st.sidebar:
    kolom1 = st.columns(2)
    with kolom1[0]:
        if st.button('Menulis dan Membaca Teks',type="primary"):
            st.session_state.kelompok = {'kondisi1':False, 'kondisi2':True, 'kondisi3':False,'kondisi4':False, 'kondisi5':False}
            st.session_state.kontrol = False
            st.session_state.tampilkan = False
            st.session_state.kontrol1 = False
            st.rerun()
    with kolom1[1]:
        if st.button('Membaca dan Membaca Kalimat', type="secondary", key="tmbl3"):
            st.session_state.kelompok = {'kondisi1':False, 'kondisi2':False, 'kondisi3':True,'kondisi4':False, 'kondisi5':False}
            st.session_state.kontrol = False
            st.session_state.tampilkan = False
            st.session_state.kontrol1 = False
            st.rerun()
    if st.button("Mengeja"):
        st.session_state.kelompok = {'kondisi1':False, 'kondisi2':False, 'kondisi3':False,'kondisi4':False,'kondisi5':True}
        st.session_state.kontrol = False
        st.session_state.tampilkan = False
        st.session_state.kontrol1 = False
        st.rerun()
    if st.button("Menulis dan Membaca Cerita",key="tmbl10"):
        st.session_state.kelompok = {'kondisi1':False, 'kondisi2':False, 'kondisi3':False,'kondisi4':True, 'kondisi5':False}
        st.session_state.kontrol = False
        st.session_state.tampilkan = False
        st.session_state.kontrol1 = False
        st.rerun()
    if st.session_state.kelompok['kondisi4']:
        st.session_state.data_teks['tulisan'] = st.text_area("Tulis Cerita di sini")
        kumpulan=[]
        kumpulan1=[]
        kumpulan2=[]
        if st.button("hasil_teks"):
            kumpulan=st.session_state.data_teks['tulisan'].split('\n')
            for i in kumpulan:
                kumpulan1.extend(i.split(' '))
            for i in kumpulan1:
                if i.endswith("."):
                    kumpulan2.append(i.replace(".",""))
                else:
                    kumpulan2.append(i)
            st.session_state.data_teks['data']=kumpulan2
            st.session_state.data_teks['cerita'] = '\n'.join(kalimat)
            st.session_state.kontrol = True
        st.divider()
        audio_value = st.audio_input("Silahkan Membaca Cerita")
        if audio_value:
            st.audio(audio_value)
             # 1. Simpan sementara
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_value.getbuffer())

            # 2. Konversi audio (kalau bukan wav)
            sound = AudioSegment.from_file("temp_audio.wav")
            sound.export("converted.wav", format="wav")

            # 3. Gunakan SpeechRecognition
            recognizer = sr.Recognizer()
            with sr.AudioFile("converted.wav") as source:
                audio_data = recognizer.record(source)

                try:
                    # Bisa pakai engine lain: sphinx (offline), google (butuh internet)
                    #text = recognizer.recognize_sphinx(audio_data)  # offline
                    text = recognizer.recognize_google(audio_data, language="id-ID")  # online
                    st.subheader("Hasil Transkripsi:")
                    st.write(text)
                    st.session_state.tampilkan=text
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

if st.session_state.kontrol:
    himpunan={'kelompok1':[],'kelompok2':[],'kelompok3':[],'kelompok4':{},'kelompok5':{},
              'kelompok6':[],'kelompok7':{}, 'kelompok8':{},'hasil':0}
    kunci1= st.session_state.data_teks['cerita'].lower()
    for i in kunci1.split("\n"):
        himpunan['kelompok1'].append(i)
    for i in himpunan['kelompok1']:
        himpunan['kelompok2'].extend(i.split(' '))
    for i in himpunan['kelompok2']:
        if i.endswith(','):
            himpunan['kelompok3'].append(i.replace(',',''))
        else:
            himpunan['kelompok3'].append(i)
    himpunan['kelompok4']=set(himpunan['kelompok3'])
    st.session_state.kunci3 = himpunan['kelompok4']
    for i in himpunan['kelompok4']:
        himpunan['kelompok5'][i]=himpunan['kelompok3'].count(i)
    st.session_state.kunci2 = himpunan['kelompok5']
    for i in st.session_state.data_teks['data']:
        if i.endswith(','):
            himpunan['kelompok6'].append(i.replace(',','').lower())
        else:
            himpunan['kelompok6'].append(i.lower())
    himpunan['kelompok7']=set(himpunan['kelompok6'])
    for i in himpunan['kelompok7']:
        himpunan['kelompok8'][i]=himpunan['kelompok6'].count(i)
    st.write("Cek Penguasaan Menulis")
    kolom2 = st.columns([1,1,2])
    with kolom2[0]:
        st.dataframe(himpunan['kelompok5'])
    with kolom2[1]:
        st.dataframe(himpunan['kelompok8'])
    with kolom2[2]:
        for i in himpunan['kelompok4']:
            try:
                    if himpunan['kelompok5'][i]==himpunan['kelompok8'][i]:
                        himpunan['hasil'] +=1
            except:
                pass
        st.markdown(f'<div class="skor1">banyak kata yang tepat: {himpunan["hasil"]} dari {len(himpunan["kelompok5"])}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="skor1">Penguasaan menulis: {himpunan["hasil"]*100/len(himpunan["kelompok5"])} %</div>',unsafe_allow_html=True)
if st.session_state.tampilkan:
    st.write("Cek Membaca")
    tulisan = st.session_state.tampilkan.lower().split(" ")
    himpunan1={'kelompok1':tulisan,'kelompok2':{},'kelompok3':{}}
    himpunan1['kelompok2']=set(himpunan1['kelompok1'])
    for i in himpunan1['kelompok2']:
        himpunan1['kelompok3'][i]=himpunan1['kelompok1'].count(i)
    skor = 0
    kolom3 = st.columns([1,1,2])
    with kolom3[0]:
        st.dataframe(himpunan1['kelompok3'])
    with kolom3[1]:
        st.dataframe(st.session_state.kunci2)
    with kolom3[2]:
        for i in st.session_state.kunci3:
            try:
                if st.session_state.kunci2[i]==himpunan1['kelompok3'][i]:
                    skor +=1
            except:
                pass
        st.markdown(f'<div class="skor1">banyak kata yang tepat: {skor} dari {len(st.session_state.kunci2)}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="skor1">Penguasaan menulis: {skor*100/len(st.session_state.kunci2)} %</div>',unsafe_allow_html=True)      
    
        
    

    










