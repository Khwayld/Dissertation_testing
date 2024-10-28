import streamlit as st
from pages import home_page, video_demo_page, domain_adaptation_page





def main():
    st.navigation([
        st.Page(home_page, title="Home", icon="🏠"),
        st.Page(video_demo_page, title="Video Loading Example", icon="🚀"),
        st.Page(domain_adaptation_page, title="Domain Adaptation Example", icon="🚀")
    ]).run()



if __name__ == "__main__":
    main()