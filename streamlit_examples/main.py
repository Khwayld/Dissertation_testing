import streamlit as st
from pages import home_page, video_demo_page, domain_adaptation_page





def main():    
    # init
    st.set_page_config(layout="wide")

    if "page" not in st.session_state:
        st.session_state["page"] = "home"


    # state management
    if st.session_state["page"] == "home":
        home_page()
    elif st.session_state["page"] == "video_example":
        video_demo_page()
    elif st.session_state["page"] == "domain_adaptation":
        domain_adaptation_page()





if __name__ == "__main__":
    main()