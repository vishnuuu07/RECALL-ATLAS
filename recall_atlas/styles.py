import streamlit as st

def inject_css():
    st.markdown('''<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');
    .stApp{background:#faf8f3;color:#19333d;font-family:'DM Sans',sans-serif}
    .block-container{max-width:1260px!important;padding:1.1rem 2rem 3rem!important}
    h1,h2,h3{font-family:Fraunces,Georgia,serif!important;letter-spacing:-.018em;color:#19333d!important}
    h1{font-size:2.5rem!important;line-height:1.1!important}h2{font-size:1.55rem!important}h3{font-size:1.25rem!important}
    p,li,[data-testid="stMarkdownContainer"]{font-size:1rem;line-height:1.48}
    [data-testid='stSidebar']{background:#19333d}[data-testid='stSidebar'] *{color:#fbf9f3!important}
    [data-testid='stSidebar'] [role='radiogroup'] label{font-size:.98rem!important;padding:.42rem .1rem}
    .hero{background:linear-gradient(110deg,#19333d,#31695c);padding:1.55rem 1.9rem;border-radius:15px;color:#fff;margin-bottom:1.1rem}
    .hero h1{color:#fff!important;margin:.27rem 0 .55rem!important;font-size:2.3rem!important;max-width:980px}
    .hero p{color:#e9f1ed;max-width:950px;font-size:1rem;margin:0!important}
    .eyebrow{color:#a7e0d0;font-size:.75rem;letter-spacing:.13em;text-transform:uppercase;font-weight:700}
    .metric{background:white;border:1px solid #e1e4de;border-radius:12px;padding:.82rem 1rem;min-height:94px}
    .metric .n{font:700 1.8rem Fraunces,Georgia,serif;color:#226e68}.metric .l{color:#56696a;font-size:.82rem}
    .finding{background:white;border:1px solid #e3e5df;border-radius:11px;padding:1.05rem 1.25rem;margin:.5rem 0}
    .finding h3{margin:.08rem 0 .42rem!important;font-size:1.16rem!important}
    .finding p{margin:.15rem 0!important;font-size:.94rem;color:#30484d}
    .finding .eyebrow{color:#287970;font-size:.68rem}
    .notice{border-left:4px solid #bf873f;background:#fff1dc;border-radius:5px;padding:.8rem 1rem;margin:.6rem 0;font-size:.93rem}
    [data-testid='stExpander']{background:white;border:1px solid #e3e5df;border-radius:8px}
    [data-testid='stMetric']{background:white;border:1px solid #e3e5df;border-radius:10px;padding:12px}
    .stDownloadButton button{border:1px solid #287970;border-radius:8px;color:#205c54}
    footer{color:#617373}small{font-size:.85rem}
    @media(max-width:720px){.block-container{padding:.8rem 1rem 2rem!important}.hero{padding:1.25rem}.hero h1{font-size:1.75rem!important}}
    </style>''',unsafe_allow_html=True)
