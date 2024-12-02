import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import os

path_logo = os.path.join(os.path.dirname(__file__), "../images/logo.png")

st.set_page_config(
    page_title="Dual-Task Effect",
    page_icon="💪",
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

# DTE
def calculate_dual_task_effect(df, task_type, better_higher):
    single_task_col = f"{task_type} performance - Single Task"
    dual_task_col = f"{task_type} performance - Dual Task"
    effect_col = f"{task_type} Dual Task Effect"

    if better_higher:
        df[effect_col] = (df[dual_task_col] - df[single_task_col]) / df[single_task_col] * 100
    else:
        df[effect_col] = (df[single_task_col] - df[dual_task_col]) / df[single_task_col] * 100

    return df

# DTE category
def determine_effect_category(row):
    cog_effect = row["Cognitive Dual Task Effect"]
    motor_effect = row["Motor Dual Task Effect"]

    if cog_effect > 0 and motor_effect == 0:
        return 'Cognitive facilitation'
    elif cog_effect > 0 and motor_effect > 0:
        return 'Mutual facilitation'
    elif motor_effect > 0 and cog_effect == 0:
        return 'Motor facilitation'
    elif motor_effect > 0 and cog_effect < 0:
        return 'Motor priority trade off'
    elif motor_effect == 0 and cog_effect < 0:
        return 'Cognitive interference'
    elif motor_effect < 0 and cog_effect < 0:
        return 'Mutual interference'
    elif motor_effect < 0 and cog_effect == 0:
        return 'Motor interference'
    elif cog_effect > 0 and motor_effect < 0:
        return 'Cognitive priority tradeoff'
    elif cog_effect == 0 and motor_effect == 0:
        return 'No interference'
    return 'Unknown'


st.title("Dual-Task :blue[Effect]")

# Test orientation
st.subheader("What are your tests orientation?")
orientation_score = '''**Positive**: higher score means higher performance (ex: distance run in 10 s).  
**Negative**: lower score means higher performance (ex: time to run over 100 m).
'''
st.markdown(orientation_score)

col1, col2 = st.columns(2)
with col1:
    cognitive_orientation = st.radio("Cognitive test orientation", ["Positive", "Negative"])

with col2:
    motor_orientation = st.radio("Motor test orientation", ["Positive", "Negative"])

cog_better_higher = cognitive_orientation == "Positive"
mot_better_higher = motor_orientation == "Positive"

# Data
st.subheader("What is your data source?")
st.markdown('''**Warning:** none of your data should be missing, or equal to 0.''')
data_method = st.radio("Choose data source:", ["Manual Entry", "Upload CSV"])

# Manual
if data_method == "Manual Entry":
    subjects_number = st.number_input("Number of subjects", min_value=1, step=1)
    
    data = {
        "ID": [f"Subject {i + 1}" for i in range(subjects_number)],
        "Cognitive performance - Single Task": [0.0] * subjects_number,
        "Cognitive performance - Dual Task": [0.0] * subjects_number,
        "Motor performance - Single Task": [0.0] * subjects_number,
        "Motor performance - Dual Task": [0.0] * subjects_number
    }
    df = pd.DataFrame(data)
    df = st.data_editor(df)

#import
else:
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(df)
    
    data_formating = '''
    Please respect the data structure bellow. You can find data structure example [here](https://github.com/MatthieuGG/DualTaskCalculator/blob/main/samples/testDTE.csv).  

    | ID           | Cognitive performance - Single Task | Cognitive performance - Dual Task | Motor performance - Single Task | Motor performance - Dual Task |
    |--------------|-------------------------------------|-----------------------------------|---------------------------------|-------------------------------|
    | Participant 1|                                     |                                   |                                 |                               |
    | ...          |                                     |                                   |                                 |                               |
    '''
    st.markdown(data_formating)

# Calculation
if st.button("Calculate Dual-Task Effect"):
    if df is not None:
        # DTE
        df = calculate_dual_task_effect(df, "Cognitive", cog_better_higher)
        df = calculate_dual_task_effect(df, "Motor", mot_better_higher)

        df["Dual Task Effect"] = df.apply(determine_effect_category, axis=1)

        st.subheader("Results:")
        st.dataframe(df)

        # Plot
        fig, ax = plt.subplots()
        colors = plt.cm.rainbow(np.linspace(0, 1, len(df)))

        for i, row in df.iterrows():
            ax.scatter(row['Cognitive Dual Task Effect'], row['Motor Dual Task Effect'], color=colors[i], label=row['ID'])

        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.set_title('Dual Task Effect (DTE)')
        ax.set_xlabel('Cognitive Dual Task Effect (%)')
        ax.set_ylabel('Motor Dual Task Effect (%)')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        st.pyplot(fig)

        # Print
        for i, row in df.iterrows():
            st.write(f"Participant {row['ID']}: Dual Task Effect = {row['Dual Task Effect']}")

        # Explanations
        st.caption("The results are displayed as follow: 'Participant [ID]: Dual Task Effect = [category]'")

        # Download CSV
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(df)

        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name="results_DTE.csv",
            mime="text/csv"
        )

        # Download PNG
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        
        st.download_button(
            label="Download Plot as PNG",
            data=buffer,
            file_name="plot_DTE.png",
            mime="image/png"
        )
