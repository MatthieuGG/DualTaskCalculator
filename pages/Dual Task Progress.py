import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import os

path_img_dtp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',  'images', 'DTP.png')
path_results_dtp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',  'samples', 'plot_DTP.png')

path_logo = os.path.join(os.path.dirname(__file__), "../images/logo.png")

st.set_page_config(
    page_title="Dual-Task Progress",
    page_icon="📈",
)
#logo
st.logo(path_logo, size="medium", link='https://en.wikipedia.org/wiki/Mens_sana_in_corpore_sano', icon_image=None)
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

######################### Computation

# Dual Task effect
def calculate_dual_task_effect(df, task_type, better_higher, time_point):
    single_task_col = f"{time_point} - {task_type} performance - Single Task"
    dual_task_col = f"{time_point} - {task_type} performance - Dual Task"
    effect_col = f"{time_point} - {task_type} Dual Task Effect"

    if better_higher:
        df[effect_col] = (df[dual_task_col] - df[single_task_col]) / df[single_task_col] * 100
    else:
        df[effect_col] = (df[single_task_col] - df[dual_task_col]) / df[single_task_col] * 100

    return df

# Dual Task Progress
def calculate_dual_task_progress(df, task_type):
    t1_effect_col = f"T1 - {task_type} Dual Task Effect"
    t2_effect_col = f"T2 - {task_type} Dual Task Effect"
    progress_col = f"{task_type} Dual Task Progress"
    
    if t1_effect_col in df.columns and t2_effect_col in df.columns:
        df[progress_col] = df[t2_effect_col] - df[t1_effect_col]
    else:
        print(f"Effect columns for {task_type} not found in the DataFrame")
    
    return df

# DTE category T1
def determine_effect_category_t1(row):
    cog_effect_t1 = row["T1 - Cognitive Dual Task Effect"]
    motor_effect_t1 = row["T1 - Motor Dual Task Effect"]

    if cog_effect_t1 > 0 and motor_effect_t1 == 0:
        return 'Cognitive facilitation'
    elif cog_effect_t1 > 0 and motor_effect_t1 > 0:
        return 'Mutual facilitation'
    elif motor_effect_t1 > 0 and cog_effect_t1 == 0:
        return 'Motor facilitation'
    elif motor_effect_t1 > 0 and cog_effect_t1 < 0:
        return 'Motor priority trade off'
    elif motor_effect_t1 == 0 and cog_effect_t1 < 0:
        return 'Cognitive interference'
    elif motor_effect_t1 < 0 and cog_effect_t1 < 0:
        return 'Mutual interference'
    elif motor_effect_t1 < 0 and cog_effect_t1 == 0:
        return 'Motor interference'
    elif cog_effect_t1 > 0 and motor_effect_t1 < 0:
        return 'Cognitive priority tradeoff'
    elif cog_effect_t1 == 0 and motor_effect_t1 == 0:
        return 'No interference'
    return 'Unknown'

# DTE category T2
def determine_effect_category_t2(row):
    cog_effect_t2 = row["T2 - Cognitive Dual Task Effect"]
    motor_effect_t2 = row["T2 - Motor Dual Task Effect"]

    if cog_effect_t2 > 0 and motor_effect_t2 == 0:
        return 'Cognitive facilitation'
    elif cog_effect_t2 > 0 and motor_effect_t2 > 0:
        return 'Mutual facilitation'
    elif motor_effect_t2 > 0 and cog_effect_t2 == 0:
        return 'Motor facilitation'
    elif motor_effect_t2 > 0 and cog_effect_t2 < 0:
        return 'Motor priority trade off'
    elif motor_effect_t2 == 0 and cog_effect_t2 < 0:
        return 'Cognitive interference'
    elif motor_effect_t2 < 0 and cog_effect_t2 < 0:
        return 'Mutual interference'
    elif motor_effect_t2 < 0 and cog_effect_t2 == 0:
        return 'Motor interference'
    elif cog_effect_t2 > 0 and motor_effect_t2 < 0:
        return 'Cognitive priority tradeoff'
    elif cog_effect_t2 == 0 and motor_effect_t2 == 0:
        return 'No interference'
    return 'Unknown'

# DTP category
def determine_progress_category(row):
    cognitive_progress = row["Cognitive Dual Task Progress"]
    motor_progress = row["Motor Dual Task Progress"]

    if cognitive_progress < 0 and motor_progress == 0:
        return 'DTP -/0 : cognitive increase of CMI'
    elif cognitive_progress < 0 and motor_progress < 0:
        return 'DTP -/- : mutual increase of CMI'
    elif cognitive_progress == 0 and motor_progress < 0:
        return 'DTP 0/- : Motor increase of CMI'
    elif cognitive_progress > 0 and motor_progress < 0:
        return 'DTP +/- : motor trade-off of CMI'
    elif cognitive_progress > 0 and motor_progress == 0:
        return 'DTP +/0 : cognitive decrease of CMI'
    elif cognitive_progress > 0 and motor_progress > 0:
        return 'DTP +/+ : mutual decrease of CMI'
    elif cognitive_progress == 0 and motor_progress > 0:
        return 'DTP 0/+ : motor decrease of CMI'
    elif cognitive_progress < 0 and motor_progress > 0:
        return 'DTP -/+ : cognitive trade-off of CMI'
    elif cognitive_progress == 0 and motor_progress == 0:
        return 'DTP 0/0 : no progress'
    return 'Unknown'

######################### Page
st.title("Dual-Task :orange[Progress]")

#explanations
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
        Providing data manually or by upload, you will obtain downloadable: 1) dataframe with your results, 2) print with explanation for each participants, and 3) a global plot of this kind:  
        """
    )
    st.image(path_results_dtp, caption=None, width=50, use_container_width=True)

# Test orientation
st.subheader("What are your tests orientation?")
st.markdown('''
            **Positive**: a higher score indicates better performance (e.g., distance covered in 10 seconds).  
            **Negative**: a lower score indicates better performance (e.g., time taken to run 100 meters).
            '''
)

col1, col2 = st.columns(2)
with col1:
    cognitive_orientation = st.radio("Cognitive test orientation", ["Positive", "Negative"])

with col2:
    motor_orientation = st.radio("Motor test orientation", ["Positive", "Negative"])

cog_better_higher = cognitive_orientation == "Positive"
mot_better_higher = motor_orientation == "Positive"


# Data
st.subheader("What is your data source?")
st.markdown('''**Warning:** none of your data should be missing or 0.''')
data_method = st.radio("Choose data source:", ["Manual Entry", "Upload CSV"])

# Manual
if data_method == "Manual Entry":
    subjects_number = st.number_input("Number of subjects", min_value=1, step=1)
    data = {
        "ID": [f"Subject {i + 1}" for i in range(subjects_number)],
        "T1 - Cognitive performance - Single Task": [0.0] * subjects_number,
        "T1 - Cognitive performance - Dual Task": [0.0] * subjects_number,
        "T1 - Motor performance - Single Task": [0.0] * subjects_number,
        "T1 - Motor performance - Dual Task": [0.0] * subjects_number,

        "T2 - Cognitive performance - Single Task": [0.0] * subjects_number,
        "T2 - Cognitive performance - Dual Task": [0.0] * subjects_number,
        "T2 - Motor performance - Single Task": [0.0] * subjects_number,
        "T2 - Motor performance - Dual Task": [0.0] * subjects_number,

    }
    df = pd.DataFrame(data)
    df = st.data_editor(df)

# Import
else:
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(df)

    with st.expander("Data formating"):    
        st.markdown('''
        Please respect the data structure bellow. You can find data structure example [here](https://github.com/MatthieuGG/DualTaskCalculator/blob/main/samples/testDTP.csv).

        | ID           | T1 - Cognitive performance - Single Task | T1 - Cognitive performance - Dual Task | T1 - Motor performance - Single Task | T1 - Motor performance - Dual Task | T2 - Cognitive performance - Single Task | T2 - Cognitive performance - Dual Task | T2 - Motor performance - Single Task | T2 - Motor performance - Dual Task |
        |--------------|------------------------------------------|----------------------------------------|--------------------------------------|------------------------------------|------------------------------------------|----------------------------------------|--------------------------------------|------------------------------------|
        | Participant 1|                                          |                                        |                                      |                                    |                                          |                                        |                                      |                                    |
        | ...          |                                          |                                        |                                      |                                    |                                          |                                        |                                      |                                    |
        '''
        )

# Calculation
if st.button("Calculate Dual-Task Progress"):
    if df is not None:
        # DTE
        df = calculate_dual_task_effect(df, "Cognitive", cog_better_higher, "T1")
        df = calculate_dual_task_effect(df, "Cognitive", cog_better_higher, "T2")
        df = calculate_dual_task_effect(df, "Motor", mot_better_higher, "T1")
        df = calculate_dual_task_effect(df, "Motor", mot_better_higher, "T2")

        df["T1 - Dual Task Effect"] = df.apply(determine_effect_category_t1, axis=1)
        df["T2 - Dual Task Effect"] = df.apply(determine_effect_category_t2, axis=1)

        # DTP
        df = calculate_dual_task_progress(df, "Cognitive")
        df = calculate_dual_task_progress(df, "Motor")

        df["Dual Task Progress"] = df.apply(determine_progress_category, axis=1)

        # Results
        st.subheader("Results:")
        st.dataframe(df)

        # Plot
        fig, ax = plt.subplots()
        colors = plt.cm.rainbow(np.linspace(0, 1, len(df['ID'].unique())))

        for i, id_value in enumerate(df['ID'].unique()):
            subset = df[df['ID'] == id_value]
            x_start = subset['T1 - Cognitive Dual Task Effect'].values[0]
            x_end = subset['T2 - Cognitive Dual Task Effect'].values[0]
            y_start = subset['T1 - Motor Dual Task Effect'].values[0]
            y_end = subset['T2 - Motor Dual Task Effect'].values[0]

            ax.scatter(x_start, y_start, color=colors[i], label=id_value, alpha=0.6)
            ax.scatter(x_end, y_end, color=colors[i], marker='X', alpha=0.6)

            ax.quiver(x_start, y_start, x_end - x_start, y_end - y_start, angles='xy', scale_units='xy', scale=1, color=colors[i])

        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        ax.set_title('Dual Task Progress (DTP)')
        ax.set_xlabel('Cognitive Dual Task Effect (%)')
        ax.set_ylabel('Motor Dual Task Effect (%)')

        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))

        st.pyplot(fig)
        
        # Print
        for i, row in df.iterrows():
            st.write(f"Participant {row['ID']}: went from {row['T1 - Dual Task Effect']} at T1, to {row['T2 - Dual Task Effect']} at T2, with a {row['Dual Task Progress']}")

        # Explanations
        st.caption("The results are displayed as follow: 'Participant [ID]: went from [DTE category] at T1, to [DTE category] at T2, with a [DTP cog/mot category]'")

        # Download CSV
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(df)

        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name="results_DTP.csv",
            mime="text/csv"
        )

        # Download PNG
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        
        st.download_button(
            label="Download plot as PNG",
            data=buffer,
            file_name="plot_DTP.png",
            mime="image/png"
        )
