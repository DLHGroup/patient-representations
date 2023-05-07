#### Paper Reproducibility Project for CS598 DL4H in Spring 2023
### **Learning Patient Representations from Text** by Dmitriy Dligach and Timothy Miller
[Original Repository](https://github.com/dmitriydligach/starsem2018-patient-representations)

#### Dependencies:
We used the below tools and Python packages:
- Google Colab GPU environment using the Pro+ subscription
- openjdk 11.0.18
- Apache cTAKES 4.0.0.1
- Python 3.10.11
- NumPy 1.22.4
- scikit-learn 1.2.2
- Keras 2.12.0
- gensim 4.3.1

#### Data download instruction:
Follow the instructions in this [link](https://eicu-crd.mit.edu/gettingstarted/access/) to get access to **Physionet.org** and then download following files from the [MIMIC III Clinical database](https://physionet.org/content/mimiciii/1.4/)
- NOTEEVENTS.csv
- PROCEDURES ICD.csv
- DIAGNOSES ICD.csv
- CPTEVENTS.csv

For the evaluation data download the i2b2 Obesity Challenge datasets currenty housed [here](https://portal.dbmi.hms.harvard.edu/). You will need the following files.
- obesity_patient_records_training.xml
- obesity_patient_records_training2.xml
- obesity_patient_records_test.xml
- obesity_standoff_annotations_training1.xml
- obesity_standoff_annotations_training2.xml
- obesity_standoff_annotations_test.xml

#### Preprocessing: (Mote stepwise detailed instructions also available in the bonus notebook)
* Create your [UMLS](https://uts.nlm.nih.gov/uts/signup-login?_gl=1*1tk5kri*_ga*ODQ0MDU0MjY1LjE2NDYzNjEyNDE.*_ga_7147EPK006*MTY1MTExNzYwNC4yLjEuMTY1MTExNzYwOC4w*_ga_P1FPTH9PL4*MTY1MTExNzYwNC4yLjEuMTY1MTExNzYwOC4w) account and obtain User Id and key to run cTAKES.
* Follow the instrucions on the [Apache cTAKES](https://cwiki.apache.org/confluence/display/CTAKES/cTAKES+4.0+User+Install+Guide) site to setup the NLP software.

Once the cTAKES software is installed run the pipeline using below command.

Default pipeline
!bash apache-ctakes-4.0.0.1/bin/runClinicalPipeline.sh -i "Input Path" --xmiOut "Output Path" --user username --key userkey

piper file run
!bash apache-ctakes-4.0.0.1/bin/runPiperFile.sh  -p apache-ctakes-4.0.0.1/colab_ctakespipe5.piper --user username --key userkey

#### Training:
Train and build the model using below command

python ft.py cuis.cfg

#### Evaluation:
Evaluate the learned mode against the different baseline models. Each evaluation can be run seprately using below commands.

- python svm.py sparse.cfg
- python svm.py svd.cfg
- python svm.py dense.cfg

#### Models & Corpus built:

- **Codes**: mimic-cuis.data (this is an 80 MB file and has not been uploaded), alphabet.p, model.h5
- **Comorbidity**: alphabet.p

#### Table of Results:

|Disease|Sparse|     |     |SVD  |     |     |Learned|     |    |
| :---: |:---: |:---:|:---:|:---:|:---:|:---:| :---: |:---:|:---|
|	|**P**|**R**|**F1**|**P**|**R**|**F1**|**P**|**R**|**F1**|
Asthma|0.927|0.725|0.784|0.929|0.733|0.791|0.554|0.602|0.533|
CAD|0.586|0.586|0.586|0.590|0.591|0.590|0.569|0.576|0.572|
CHF|0.478|0.358|0.266|0.478|0.358|0.266|0.511|0.515|0.511|
Depression|0.852|0.686|0.724|0.783|0.666|0.694|0.559|0.582|0.548|
Diabetes|0.882|0.840|0.857|0.867|0.824|0.841|0.492|0.497|0.494|
GERD|0.526|0.455|0.474|0.521|0.454|0.473|0.381|0.380|0.380|
Gallstones|0.887|0.616|0.652|0.884|0.610|0.644|0.584|0.650|0.562|
Gout|0.924|0.751|0.808|0.919|0.734|0.793|0.599|0.594|0.596|
Hypercholesterolemia|0.784|0.787|0.785|0.802|0.804|0.803|0.727|0.730|0.725|
Hypertension|0.746|0.647|0.673|0.704|0.637|0.657|0.635|0.696|0.639|
Hypertriglyceridemia|0.976|0.540|0.562|0.977|0.560|0.595|0.526|0.618|0.472|
OA|0.556|0.430|0.452|0.556|0.430|0.452|0.438|0.390|0.399|
OSA|0.645|0.571|0.601|0.649|0.556|0.591|0.412|0.406|0.409|
Obesity|0.807|0.793|0.798|0.797|0.780|0.785|0.630|0.629|0.629|
PVD|0.631|0.502|0.542|0.640|0.497|0.540|0.443|0.418|0.428|
Venous Insufficiency|0.976|0.655|0.725|0.976|0.655|0.725|0.574|0.763|0.547|
**Average**|**0.762**|**0.621**|**0.643**|**0.755**|**0.618**|**0.640**|**0.540**|**0.565**|**0.528**|

#### Descriptive Notebook:
You can also refer to the **Code_Execution_Guide_(Bonus Notenook).ipynb** for detailed stepwise instructions on how to run the code. You may find some other interesting insights too!
