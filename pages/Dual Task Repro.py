import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import pingouin as pg
from sklearn.metrics import confusion_matrix
import seaborn as sns
import numpy as np
import os

path_img_dtr = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'DTR.png')
path_logo = os.path.join(os.path.dirname(__file__), "../images/logo.png")

st.set_page_config(
    page_title="Dual-Task Repro",
    page_icon="📊",
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

# REPRO
def calculate_agreement_rate(df):
    df['Agreement'] = df['T1 - Dual Task Effect'] == df['T2 - Dual Task Effect']
    agreement_rate = df['Agreement'].mean() * 100
    print(f"Agreement rate between T1 and T2 - Dual Task Effect: {agreement_rate:.2f}%")
    return agreement_rate


def plot_confusion_matrix(df):
    labels = df['T1 - Dual Task Effect'].unique()
    cm = confusion_matrix(df['T1 - Dual Task Effect'], df['T2 - Dual Task Effect'], labels=labels)

    # percentages
    cm_percentage = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100

    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    cm_percentage_df = pd.DataFrame(cm_percentage, index=labels, columns=labels)

    annotations = [
        f"{v} ({p:.1f}%)" for v, p in zip(cm_df.values.flatten(), cm_percentage_df.values.flatten())
    ]
    annotations = np.array(annotations).reshape(cm_df.shape)

    # matrix
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm_percentage_df, annot=annotations, fmt='', cmap='Blues', cbar=False, annot_kws={"size": 12}, ax=ax)
    
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=45, ha='right', fontsize=10)
    
    ax.set_xlabel("T2 - Dual Task Effect")
    ax.set_ylabel("T1 - Dual Task Effect")
    ax.set_title("Confusion matrix between T1 and T2 - Dual Task Effect")
    ax.tick_params(axis='both', which='both', labelsize=10)

    return fig

def transform_to_long_icc(df):
    value_vars = [
        "T1 - Cognitive performance - Single Task", 
        "T1 - Cognitive performance - Dual Task",
        "T1 - Motor performance - Single Task", 
        "T1 - Motor performance - Dual Task",
        "T2 - Cognitive performance - Single Task", 
        "T2 - Cognitive performance - Dual Task",
        "T2 - Motor performance - Single Task", 
        "T2 - Motor performance - Dual Task",
        "T1 - Cognitive Dual Task Effect", 
        "T2 - Cognitive Dual Task Effect",
        "T1 - Motor Dual Task Effect", 
        "T2 - Motor Dual Task Effect"
    ]

    df_long = pd.melt(
        df,
        id_vars=["ID"],
        value_vars=value_vars,
        var_name="Mesure",
        value_name="Score"
    )
    
    df_long['Eval 1 or 2'] = df_long['Mesure'].str.extract(r'(T1|T2)')
    df_long['Mesure'] = df_long['Mesure'].str.replace(r'(T1|T2) - ', '', regex=True)

    return df_long

def calculate_cronbach_alpha_icc_with_metrics(df, time1='T1', time2='T2'):
    results = []
    
    for mesure in df['Mesure'].unique():
        df_mesure = df[df['Mesure'] == mesure]
        df_pivot = df_mesure.pivot(index='ID', columns='Eval 1 or 2', values='Score')
        
        if not df_pivot.empty and df_pivot.shape[1] > 1:
            # Cronbach alpha & ICC
            alpha, ci = pg.cronbach_alpha(data=df_pivot, nan_policy='pairwise')
            icc = pg.intraclass_corr(data=df_mesure, targets='ID', raters='Eval 1 or 2', ratings='Score').iloc[0]['ICC']
            
            # SEM & CV
            score_std = df_mesure['Score'].std() 
            score_mean = df_mesure['Score'].mean() 
            sem = score_std * (1 - alpha) ** 0.5 
            cv = (score_std / score_mean) * 100 if score_mean != 0 else None 
            
            results.append({
                'Mesure': mesure,
                "Cronbach's alpha": round(alpha, 2),
                'ICC 95% CI': f"{ci[0]:.2f} - {ci[1]:.2f}",
                'SEM': round(sem, 2),
                'CV (%)': round(cv, 2) if cv is not None else 'N/A'
            })
    
    results_df = pd.DataFrame(results)

    return results_df

def create_bland_altman_plots(df):
    mesures = df['Mesure'].unique()
    n_mesures = len(mesures)

    fig, axes = plt.subplots(nrows=n_mesures, ncols=1, figsize=(8, n_mesures * 4))

    for i, mesure in enumerate(mesures):
        df_mesure = df[df['Mesure'] == mesure].pivot(index='ID', columns='Eval 1 or 2', values='Score')

        if 'T1' in df_mesure.columns and 'T2' in df_mesure.columns:
            df_mesure = df_mesure.dropna(subset=['T1', 'T2']) 
            if len(df_mesure) > 0:
                ax = axes[i] if n_mesures > 1 else axes  
                pg.plot_blandaltman(df_mesure['T1'], df_mesure['T2'], ax=ax)
                ax.set_title(f"{mesure}")
            else:
                print(f"No data for {mesure}: not included in plot.")

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    return fig

######################### Page
st.title("Dual-Task :green[Repro]")

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
        Providing data manually or by upload, you will obtain downloadable: 1) dataframe and explanation of your results, 2) confusion matrix and Bland-Altman plots of this kind:  
        """
    )
    st.image(path_img_dtr, use_column_width=True)

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
    st.caption('''T1 and T2 are the test values at time 1 and time 2 for the same evaluator (**intra-eval**), or for the evaluators 1 and evaluator 2 at the same time (**inter-eval**).''')

# Import
else:
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(df)
    
    data_formating = '''
    Please resect the data structure bellow. You can find data structure example [here](https://github.com/MatthieuGG/DualTaskCalculator/blob/main/samples/testDTR.csv).

    | ID           | T1 - Cognitive performance - Single Task | T1 - Cognitive performance - Dual Task | T1 - Motor performance - Single Task | T1 - Motor performance - Dual Task | T2 - Cognitive performance - Single Task | T2 - Cognitive performance - Dual Task | T2 - Motor performance - Single Task | T2 - Motor performance - Dual Task |
    |--------------|------------------------------------------|----------------------------------------|--------------------------------------|------------------------------------|------------------------------------------|----------------------------------------|--------------------------------------|------------------------------------|
    | Participant 1|                                          |                                        |                                      |                                    |                                          |                                        |                                      |                                    |
    | ...          |                                          |                                        |                                      |                                    |                                          |                                        |                                      |                                    |
    '''
    st.markdown(data_formating)

# Calculation
if st.button("Calculate Dual-Task Repro"):
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

        df_icc = transform_to_long_icc(df)

        # Results
        st.subheader("Results:")

        st.dataframe(df)

        ### agreement
        agreement_rate = calculate_agreement_rate(df)
        st.write("**Agreement between T1 and T2:**")
        st.write(f"{agreement_rate}% of DTE similarity")
        fig1 = plot_confusion_matrix(df)
        st.pyplot(fig1)
        
        # Download PNG
        buffer = io.BytesIO()
        fig1.savefig(buffer, format="png")
        buffer.seek(0)

        st.download_button(
            label="Download Confusion Matrix",
            data=buffer,
            file_name="confusion_matrix.png",
            mime="image/png"
        )

        ### reliability
        st.write("**Reliability between T1 and T2:**")

        # csv
        icc_results = calculate_cronbach_alpha_icc_with_metrics(df_icc)
        st.dataframe(icc_results)
        st.caption("How to interprete these scores: Cronbach's alpha [[1]](https://pubmed.ncbi.nlm.nih.gov/28029643/),[[2]](https://pingouin-stats.org/build/html/generated/pingouin.cronbach_alpha.html), Intraclass Correlation Coefficient [[3]](https://pubmed.ncbi.nlm.nih.gov/27330520/),[[4]](https://pingouin-stats.org/build/html/generated/pingouin.intraclass_corr.html), Standard Error of Measurment [[5]](https://www.fldoe.org/core/fileparse.php/7567/urlt/y1996-7.pdf), Coefficient of Variation [[4]](https://stats.oarc.ucla.edu/other/mult-pkg/faq/general/faq-what-is-the-coefficient-of-variation/#:~:text=The%20higher%20the%20CV%2C%20the,of%20a%20good%20model%20fit.).")

        # Download CSV
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(icc_results)

        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name="results_DTR.csv",
            mime="text/csv"
        )

        # plot
        fig2 = create_bland_altman_plots(df_icc)
        st.pyplot(fig2)

        # Download PNG
        buffer = io.BytesIO()
        fig2.savefig(buffer, format="png")
        buffer.seek(0)

        st.download_button(
            label="Download Bland-Altman",
            data=buffer,
            file_name="bland_altman.png",
            mime="image/png"
        )
