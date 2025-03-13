# Dual Task Calculator

```
https://dualtaskcalculator.streamlit.app/
```

Automatically calculates the cognitive-motor dual-task effects (DTE) or progress (DTP) from the cognitive and motor performances of subjects at two times (T1 and T2), both realised in single and dual task condition (ST and DT). Can also provide information about the realibility of the measure. 

<details>
<summary><b>Dual-Task Effect</b></summary>
  
Use [this file structure](https://github.com/MatthieuGG/DualTaskCalculator/blob/main/samples/testDTE.csv), and [this part](https://dualtaskcalculator.streamlit.app/~/+/Dual_Task_Effect) of the app. You will obtain this kind of results:  
![Dual Task Effect Graph](https://github.com/MatthieuGG/DualTaskCalculator/blob/main/samples/plot_DTE.png?raw=true)  

`Participant Subject 1: Dual Task Effect (DTE) = Mutual facilitation`  
(etc. for all participants)  

You can download the results as CSV and PNG files.  
</details>

<details>
<summary><b>Dual-Task Progress</b></summary> 

Use [this file structure](https://github.com/MatthieuGG/DualTaskCalculator/blob/main/samples/testDTP.csv), and [this part](https://dualtaskcalculator.streamlit.app/~/+/Dual_Task_Progress) of the app. You will obtain this kind of results:  
![Dual Task Progress Graph](https://github.com/MatthieuGG/DualTaskCalculator/blob/main/samples/plot_DTP.png?raw=true)  

`Participant Subject 1: went from Mutual facilitation at T1, to Cognitive priority tradeoff at T2, with a DTP -/- : mutual increase of CMI`  
(etc. for all participants)  

You can download the results as CSV and PNG files.  
</details>


<details>
<summary><b>Dual-Task Repro</b></summary>  

Use [this file structure](https://github.com/MatthieuGG/DualTaskCalculator/blob/main/samples/testDTR.csv), and [this part](https://dualtaskcalculator.streamlit.app/~/+/Dual_Task_Repro) of the app. You will obtain this kind of results:  
![Dual Task Repro Graph](https://github.com/MatthieuGG/DualTaskCalculator/blob/main/images/DTR.png?raw=true)  

`Agreement between T1 and T2: 23% of DTE similarity.`  
| Mesure                           | Cronbach's alpha | ICC 95% CI           | SEM  | CV (%)  |
|----------------------------------|------------------|----------------------|------|---------|
| Cognitive performance - Single Task | 0.49             | -1.94                | 1.46 | 41.92   |
| Cognitive performance - Dual Task  | -0.09            | -4.1                 | 2.33 | 53.3    |
| Motor performance - Single Task   | 1.00             | 1.00 - 1.00          | 0    | 72.32   |
| Motor performance - Dual Task     | -0.18            | -4.46                | 2.34 | 44.51   |
| Cognitive Dual Task Effect        | 0.66             | -1.3                 | 58.36| 642.47  |
| Motor Dual Task Effect            | 0.92             | 0.68 - 0.98          | 62.1 | 154.55  |


You can download the results as CSV and PNG files.  
</details>

---
This code is provided allong with more detailed informations in this article: [Gallou-Guyot et al., 2025](https://rehab-journal.com/index.php/home/article/view/58). The data has been acquired within the [INCOME research project](https://matthieugg.github.io/income.html).  To cite this work:  
> Gallou-Guyot, M., Bruyneel, A.-V., Mandigout, S., & Perrochon, A. (2025). Using dual-task effect for cognitive-motor change profiling – the Dual-Task Progress model. *European Rehabilitation Journal*, 5(1). [https://doi.org/10.52057/erj.v5i1.58](https://rehab-journal.com/index.php/home/article/view/58)

![Dual Task Progress](https://github.com/MatthieuGG/DualTaskCalculator/blob/main/images/DTP.png?raw=true)
