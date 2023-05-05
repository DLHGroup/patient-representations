import csv
import sys
import os
import pickle

if __name__ == '__main__':
    counter = 0
    corpus = []
    finalfile = os.path.dirname(sys.path[0]) + '/Data/Word2VecModels/mimic-cuis.data'
    with open(finalfile, 'wb') as ffile:
        for cuisfile in os.listdir(os.path.dirname(sys.path[0]) + '/Data/Patients/Cuis'):
            if cuisfile[-3:]=="txt":
                cuis_file = os.path.dirname(sys.path[0]) + '/Data/Patients/Cuis/' + cuisfile
                print(cuis_file)
                with open(cuis_file) as f:
                    content = f.read()
                    mini_corp = []
                    for item in content.split():
                        mini_corp.append (item)
                    corpus.append(mini_corp)
                    counter = counter +1
        pickle.dump (corpus, ffile)
        print(counter)
                #cuis_file = os.path.dirname(sys.path[0]) + '/Data/Patients/Cuis/' + cuisfile
                # textfile = open(cuis_file, 'r')
                # filetext = textfile.read()
                # textfile.close()
                # d.write (textfile)
                # d.write("\n")
    #             for row in file:
    #                 arr = row[0].split()
    #                 allcuis.update (arr)
    # allcuis = list(allcuis)
    # with open(finalfile, 'w') as f:
    #     for i in range(len(allcuis)-1):
    #         out = allcuis[i] + " "
    #         f.writelines(out)
    #     f.writelines(allcuis[-1])