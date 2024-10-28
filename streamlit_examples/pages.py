import streamlit as st
from example_functions.domain_adaptation_streamlit_example import domain_adaptation_example
from example_functions.video_loading_streamlit_example import demo_1, demo_2, demo_3, demo_4


def home_page():
    st.markdown("<h1 style='text-align: center;'>Welcome To The Pykale Example Archive 👋</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Here we explore some examples created in pykale</h5>", unsafe_allow_html=True)
    
def video_demo_page():
    st.markdown("<h1 style='text-align: center;'>Video Loading Example</h1>", unsafe_allow_html=True)


    demo = st.radio(
        "Select Demo To Try Out",
        ["Demo 1",  "Demo 2", "Demo 3", "Demo 4"],
        index=None,
    )


    if demo == "Demo 1":
        demo_1()
    elif demo == "Demo 2":
        demo_2()
    elif demo == "Demo 3":
        demo_3()
    elif demo == "Demo 4":
        demo_4()



def domain_adaptation_page():
    st.markdown("<h1 style='text-align: center;'>Domain Adaptation Example</h1>", unsafe_allow_html=True)
    domain_adaptation_example()
