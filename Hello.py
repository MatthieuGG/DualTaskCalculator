import streamlit as st
import os

current_directory = os.getcwd()

path_img_dte = os.path.join(current_directory, 'images', 'DTE.jpg')
path_results_dte = os.path.join(current_directory, 'samples', 'plot_DTE.png')

path_img_dtp = os.path.join(current_directory, 'images', 'DTP.png')
path_results_dtp = os.path.join(current_directory, 'samples', 'plot_DTP.png')

st.set_page_config(
    page_title="Dual-Task Calculator",
    page_icon="🧠",
)

st.write("# Welcome to The Dual-Task Calculator!")
st.sidebar.success("Select a model.")
st.markdown(
    """
    Please select the model you want to apply for calculation - descriptions are given bellow. 
    Note that we consider here *cognitive-motor* dual-task, but the same can be applied for other dual-task situations.
    """
)

# DTE
st.divider()
st.subheader("Dual-Task :blue[Effect]")
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
    With DT = dual-task performance, and ST = single-task performance. The cognitive (DTE cog) and motor (DTE mot) dual-task effect can be calculated.  

    A graphical illustration as been proposed by Plumer et al., (2014) ([DOI: 10.1155/2014/538602](https://onlinelibrary.wiley.com/doi/10.1155/2014/538602)).
    """
)
st.image(path_img_dte, caption="Plummer et al. (2014). Stroke Research and Treatment.", width=50, use_column_width=True)
st.markdown(
    """
    You can access the **Dual Task :blue[Effect]** calculator using the side bar, or clicking [this link](https://dualtaskcalculator.streamlit.app/~/+/Dual_Task_Effect). 
    Providing data manually or by upload, you will obtain downloadable: 1) dataframe with your results, 2) print with explanation for each participants, and 3) a global plot of this kind:  
    """
)
st.image(path_results_dte, caption=None, width=50, use_column_width=True)



# DTP
st.divider()
st.subheader("Dual-Task :orange[Progress]")
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
    With DTE2 = dual-task effect at T2, and DTE1 = dual-task effect at T1. The cognitive (DTP cog) and motor (DTP mot) dual-task progress can be calculated.  

    A graphical illustration as been proposed by (...)) ([DOI: (...)]()).
    """
)
st.image(path_img_dtp, caption="Not yet published.", use_column_width=True)
st.markdown(
    """
    You can access the **Dual Task :orange[Progress]** calculator using the side bar, or clicking [this link](https://dualtaskcalculator.streamlit.app/~/+/Dual_Task_Progress). 
    Providing data manually or by upload, you will obtain downloadable: 1) dataframe with your results, 2) print with explanation for each participants, and 3) a global plot of this kind:  
    """
)
st.image(path_results_dtp, caption=None, width=50, use_column_width=True)

# Footer
st.subheader("Feedback & Use", divider="gray")
feedback_use = ''' 
    This work is distributed freely and openly. 
    In case of errors or bugs, please use the GitHub ["Issues" section](https://github.com/MatthieuGG/DualTaskCalculator/issues).
    In case of missing functions or ideas to add, please use the GitHub ["Discussion" section](https://github.com/MatthieuGG/DualTaskCalculator/discussions). 
    For any other feedback, please send me an email to: [matthieu.gallou.guyot@gmail.com](mailto:matthieu.gallou.guyot@gmail.com).  

    Please give credits citing:  
    > *(not yet published)*  

    '''
st.markdown(feedback_use)