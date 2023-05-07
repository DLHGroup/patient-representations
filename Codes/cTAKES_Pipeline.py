

# Select a batch of n files. Make sure to set the parameter batch_size

#======================batch_parameters======================================
batch_path="../Codes/MimicIII/batch"
batch_size=1000
#======================batch_parameters======================================

# Look at the total files in Noteevents_txt and the amount produced so far in MIMIC_OUT. It also shows statistics

# NEED TO SET WORKING DIRECTORY

all_code_path = "../Codes/MimicIII/MIMIC_IN/MIMIC_IN"
produced_cui_path = "../Codes/MimicIII/Patients/Cuis"
bsv_cTAKES_path = "../Codes/MimicIII/Patients/piper5_Cuis"

batch_files=os.listdir(batch_path)
all_code_files = os.listdir(all_code_path)
produced_cui_files=os.listdir(produced_cui_path)
bsv_cTAKES_files = os.listdir(bsv_cTAKES_path)
print("batch_files",len(batch_files),batch_files)
print("all_code_files",len(all_code_files),all_code_files)
print("produced_cui_files",len(produced_cui_files),produced_cui_files)
print("bsv_cTAKES_files",len(bsv_cTAKES_files),bsv_cTAKES_files)

print("There are a total of ",len(all_code_files)," files to convert")
#print("and a total of ",len(produced_cui_files), "converted files from the old")

# Store file names in sets

total_code_files=set([x for x in all_code_files])
produced_cui=set([x[:-4] for x in produced_cui_files])
queued_files=set([x for x in batch_files])
bsv_set = set([x[:-13]+".txt" for x in bsv_cTAKES_path])


#unproduced_cui_files = total_code_files - produced_cui - bsv_set 
unproduced_cui_files = total_code_files - bsv_set 

nunproduced = len(unproduced_cui_files)
print("but",len(bsv_set), "newly converted files")
print("So there are ",nunproduced,"files left")
print()

# Convert set into a list, so it is iterable, and copy some files into batch folder

unproduced_cui_files_list = list(unproduced_cui_files)

for x in range(batch_size):
  print(x,"File",unproduced_cui_files_list[x])
  if unproduced_cui_files_list[x] not in bsv_set:
    all_code_path_x = all_code_path + "/" + unproduced_cui_files_list[x]
    batch_path_x = batch_path + "/" + unproduced_cui_files_list[x]
    #print("New source path",all_code_path_x)
    #print("New target path",batch_path_x)
    shutil.copy(all_code_path_x, batch_path_x)

print("end")
#remaining_code_files = total_code_files - bsv_set 
#remaining = len(remaining_code_files)
#print("remaining",remaining)

!bash /content/drive/MyDrive/DLH_Final_Project/apache-ctakes-4.0.0.1/bin/runPiperFile.sh  -p /content/drive/MyDrive/DLH_Final_Project/apache-ctakes-4.0.0.1/colab_ctakespipe5.piper --user studentjemay --key 3425a4d6-cc6a-4237-96d8-fdc7c2f33a0d
