import streamlit as st
from example_functions.domain_adaptation_streamlit_example import domain_adaptation_example
from example_functions.video_loading_streamlit_example import demo_1, demo_2, demo_3, demo_4


def go_to(page):
    st.session_state["page"] = page


def home_page():
    # Title
    st.markdown("<h1 style='text-align: center;'>Welcome To The Pykale Example Archive 👋</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Here we explore some examples created in pykale</h5>", unsafe_allow_html=True)

    # nav buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("Video Loading Example", on_click=go_to("video_example"), use_container_width=True)

    with col2:
        st.button("Domain Adaptation Example", on_click=go_to("domain_adaptation"), use_container_width=True)

    with col3:
        st.button("Third Example", on_click=go_to("domain_adaptation"), use_container_width=True)


    
def video_demo_page():
    # Title
    st.button("Back to Home", on_click=go_to("home"))
    st.markdown("<h1 style='text-align: center;'>Video Loading Example</h1>", unsafe_allow_html=True)


    # Demo button
    demo = st.radio(
        "Select Demo To Try Out",
        ["Demo 1",  "Demo 2", "Demo 3", "Demo 4"],
        index=None,
    )


    # state management
    if demo == "Demo 1":
        demo_1()
    elif demo == "Demo 2":
        demo_2()
    elif demo == "Demo 3":
        demo_3()
    elif demo == "Demo 4":
        demo_4()



def domain_adaptation_page():
    st.button("Back to Home", on_click=go_to("home"))
    st.markdown("<h1 style='text-align: center;'>Domain Adaptation Example</h1>", unsafe_allow_html=True)
    domain_adaptation_example()
