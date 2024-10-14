import streamlit as st
import os

current_directory = os.getcwd()
path_img_dte = os.path.join(current_directory, 'images', 'DTE.jpg')
path_img_dtp = os.path.join(current_directory, 'images', 'DTP.png')

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("# Welcome to The Dual-Task Calculator!")
st.sidebar.success("Select a model.")
st.markdown(
    """
    **Note:** we only consider here *cognitive-motor* dual-task.
    """
)

# DTE
st.subheader("Dual-Task Effect")
st.markdown(
    """
    The dual-task effect (DTE) is defined as the impact on the performance of realising a task in dual-task condition compared to single-task condition. It is calculated using the formula:
    """
)
st.latex(r'''
    \text{DTE} = \frac{\text{DT} - \text{ST}}{\text{ST}} \times 100
''')
st.markdown(
    """
    With DT = dual-task performance, and ST = single-task performance. The cognitive (DTEcog) and motor (DTEmot) dual-task effect can be calculated.  

    A graphical illustration as been proposed by Plumer et al., (2014) ([DOI: 10.1155/2014/538602](https://onlinelibrary.wiley.com/doi/10.1155/2014/538602)).
    """
)
st.image(path_img_dte, caption="Plummer et al. (2014). Stroke Research and Treatment.", width=50, use_column_width=True)


# DTP
st.subheader("Dual-Task Progress")
st.markdown(
    """
    The dual-task progress (DTP) is defined as the evolution over time of the dual-task effect, for instance between T1 and T2. It is calculated using the formula:
    """
)
st.latex(r'''
    \text{DTP} = \text{DTE}_{2} - \text{DTE}_{1}
''')
st.markdown(
    """
    With DTE2 = dual-task effect at T2, and DTE1 = dual-task effect at T1. The cognitive (DTPcog) and motor (DTPmot) dual-task progress can be calculated.  

    A graphical illustration as been proposed by (...)) ([DOI: (...)]()).
    """
)
st.image(path_img_dtp, caption="Not yet published.", use_column_width=True)

# Footer
st.subheader("Feedback & Use", divider="gray")
feedback_use = ''' This work is distributed freely and openly. To cite:  
    > *(not yet published)*  

    In case of errors or bugs, please use the ["Issues" section](https://github.com/MatthieuGG/DualTaskCalculator/issues) in the dedicated GitHub repository.  
    For any other feedback, please send me an email to: [matthieu.gallou.guyot@gmail.com](mailto:matthieu.gallou.guyot@gmail.com).
        '''
st.markdown(feedback_use)