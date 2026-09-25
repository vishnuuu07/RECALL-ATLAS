import streamlit as st


def inject_css() -> None:
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono&family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600;700&display=swap');
    .stApp { background:#f7f3ea; color:#11212b; font-family:Inter,sans-serif; }
    h1,h2,h3 { font-family:Fraunces,Georgia,serif !important; color:#102b37; letter-spacing:-.025em; }
    .block-container { max-width:1300px; padding-top:2.1rem; padding-bottom:4rem; }
    [data-testid='stSidebar'] { background:#102b37; }
    [data-testid='stSidebar'] * { color:#f6f2e9 !important; }
    .hero { background:linear-gradient(115deg,#102b37 0%,#135a5d 74%,#d9a542 150%); padding:3rem; border-radius:22px; color:#f7f3ea; margin-bottom:1.6rem; }
    .hero h1 { color:#fff8e8!important; font-size:3.3rem!important; margin:0!important; }
    .eyebrow { font-family:'DM Mono',monospace; letter-spacing:.1em; text-transform:uppercase; font-size:.76rem; color:#55d0be; }
    .metric { background:#fffdf8; border:1px solid #dfddd4; border-radius:14px; padding:1rem 1.15rem; min-height:108px; }
    .metric .n { font:700 2rem Fraunces,serif; color:#0b6967; } .metric .l { font-size:.8rem; color:#52626b; }
    .card { background:#fffdf8; border:1px solid #dfddd4; border-radius:14px; padding:1.2rem; margin:.55rem 0; }
    .tag { display:inline-block; background:#dff2ed; border-radius:999px; color:#086861; padding:.18rem .55rem; font: .73rem 'DM Mono',monospace; margin:.12rem; }
    .warning { border-left:4px solid #d88d2a; padding:.65rem 1rem; background:#fff0d7; border-radius:4px; }
    .stDownloadButton button { border-radius:8px; border:1px solid #0b716d; color:#075f5b; }
    </style>""", unsafe_allow_html=True)

