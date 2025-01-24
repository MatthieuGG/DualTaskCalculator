import streamlit as st
import os

current_directory = os.getcwd()

path_img_dte = os.path.join(current_directory, 'images', 'DTE.jpg')
path_results_dte = os.path.join(current_directory, 'samples', 'plot_DTE.png')

path_img_dtp = os.path.join(current_directory, 'images', 'DTP.png')
path_results_dtp = os.path.join(current_directory, 'samples', 'plot_DTP.png')

path_img_dtr = os.path.join(current_directory, 'images', 'DTR.png')

path_logo=os.path.join(current_directory, 'images', 'logo.png')

st.set_page_config(
    page_title="Dual-Task Calculator",
    page_icon="🧠",
)

st.write("# Welcome to The Dual-Task Calculator!")

st.sidebar.success("Select a model.")
st.logo(path_logo, size="medium", link='https://en.wikipedia.org/wiki/Mens_sana_in_corpore_sano', icon_image=None)
st.markdown(
    """
    Please select the model you want to apply for calculation - descriptions are given bellow. 
    Note that we consider here *cognitive-motor* dual-task, but the same can be applied for other dual-task situations.
    """
)

# Say thanks
recipient_email = "matthieu.gallou.guyot@gmail.com"
subject = "Thanks for the DualTaskRepro!"
body = "Dear Matthieu, (...)."
mailto_link = f"mailto:{recipient_email}?subject={subject}&body={body}"

st.sidebar.link_button(
    label="Say Thanks",
    url=mailto_link,
    type="primary",
    icon="💌"
)

# DTE
st.subheader("Dual-Task :blue[Effect]")
with st.expander("Explanations 🧠💪"):
    st.markdown(
        """
        The dual-task effect ($DTE$) is defined as the impact on the performance of realising a task in dual-task condition compared to single-task condition. It is calculated using the formula:
        """
    )
    st.latex(r'''
        \text{DTE} = \frac{\text{DT} - \text{ST}}{\text{ST}} \times 100
    ''')
    st.markdown(
        """
        With $DT$ = dual-task performance, and $ST$ = single-task performance. The cognitive ($DTE_{cog}$) and motor ($DTE_{mot}$) dual-task effect can be calculated.  

        A graphical illustration as been proposed by Plumer et al., (2014) ([DOI: 10.1155/2014/538602](https://onlinelibrary.wiley.com/doi/10.1155/2014/538602)).
        """
    )
    st.image(path_img_dte, caption="Plummer et al. (2014). Stroke Research and Treatment.", width=50, use_container_width=True)
    st.markdown(
        """
        You can access the **Dual Task :blue[Effect]** calculator using the side bar, or clicking [this link](https://dualtaskcalculator.streamlit.app/~/+/Dual_Task_Effect). 
        Providing data manually or by upload, you will obtain downlodable: 1) dataframe with your results, 2) print with explanation for each participants, and 3) a global plot of this kind:  
        """
    )
    st.image(path_results_dte, caption=None, width=50, use_container_width=True)

# DTP
st.subheader("Dual-Task :orange[Progress]")
with st.expander("Explanations 📈"):
    st.markdown(
        """
        The dual-task progress ($DTP$) is defined as the evolution over time of the dual-task effect, for instance between T1 and T2. It is calculated using the formula:
        """
    )
    st.latex(r'''
    \vec{\text{DTP}} = \begin{bmatrix}
    \text{DTE}_{2x} - \text{DTE}_{1x} \\
    \text{DTE}_{2y} - \text{DTE}_{1y}
    \end{bmatrix}
    ''')
    st.markdown(
        """
        With $DTE_{2}$ = dual-task effect at T2, and $DTE_{1}$ = dual-task effect at T1. The cognitive ($DTP_{cog}$) and motor ($DTP_{mot}$) dual-task progress can be calculated.  

        A graphical illustration as been proposed by (...)) ([DOI: (...)]()).
        """
    )
    st.image(path_img_dtp, caption="Not yet published.", use_container_width=True)
    st.markdown(
        """
        You can access the **Dual Task :orange[Progress]** calculator using the side bar, or clicking [this link](https://dualtaskcalculator.streamlit.app/~/+/Dual_Task_Progress). 
        Providing data manually or by upload, you will obtain downloadable: 1) dataframe with your results, 2) print with explanation for each participants, and 3) a global plot of this kind:  
        """
    )
    st.image(path_results_dtp, caption=None, width=50, use_container_width=True)

# DTR
st.subheader("Dual-Task :green[Repro]")
with st.expander("Explanations 📊"):
    st.markdown(
        """
        The dual-task repro ($DTR$) is an automated process that calculates different scores to qualify the reliability of the measures (cognitive and motor, in single and dual task conditions) between two evaluators (*inter*) or two evaluations (*intra*):  
        - Intraclass Correlation Coefficient (ICC)
        - Cronbach's alpha
        - Standard Error of Measurement (SEM)
        - Coefficient of Variation (CV)
        """
    )
    st.markdown(
        """
        You can access the **Dual Task :green[Repro]** calculator using the side bar, or clicking [this link](https://dualtaskcalculator.streamlit.app/~/+/Dual_Task_Repro). 
        Providing data manually or by upload, you will obtain downloadable: 1) dataframe and explanation of your results, 2) confusion matrix and Bland-Altman plots of this kind:  
        """
    )
    st.image(path_img_dtr, use_container_width=True)

# Footer
st.subheader("Feedback & Use", divider="gray")
feedback_use = ''' 
    This work is distributed freely and openly. Enjoy!  

    - Errors or bugs 👉 [GitHub "Issues" section](https://github.com/MatthieuGG/DualTaskCalculator/issues)  
    - Missing functions or new ideas 👉 [GitHub "Discussion" section](https://github.com/MatthieuGG/DualTaskCalculator/discussions)  
    - Any other feedback 📬 [matthieu.gallou.guyot@gmail.com](mailto:matthieu.gallou.guyot@gmail.com)  

    To give credits, please cite:  
    > *(not yet published)*  

    '''
st.markdown(feedback_use)