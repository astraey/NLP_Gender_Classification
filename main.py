import os
import nltk
from scipy.io import arff
from collections import OrderedDict
from operator import itemgetter

datasetPath = 'dataset'

class main():
    def __init__(self, n):
        self.corpus = {}
        self.objN = {}
        self.objFreq = {}

        self.getCorpus()
        self.getN(n)
        self.getFreq()
        self.getArff()

    # Reads the files from the dataset folder
    def getCorpus(self):
        for (subdir, d_, files) in os.walk( datasetPath ):
            for fichero in files:
                archivo = open(os.path.join(subdir, fichero), 'r')
                self.corpus[ fichero ] = archivo.read()

    # Stores in self.objN the N most used words
    def getN(self, n):
        obj = {}
        for val in self.corpus.values():
            for val_ in val.split():
                if len(val_) == 1:
                    if val_ in obj:
                        obj[val_] += 1
                    else:
                        obj[val_] = 1
                else:
                    val_ = val_.lower()
                    val_ = val_.replace(".", " ").replace(",", " ").replace(":", " ").replace(";", " ").replace("!", " ").replace("?", " ")
                    val_ = val_.replace("@", " ").replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ").replace("=", " ")
                    if val_ in obj:
                    	obj[val_] += 1
                    else:
                    	obj[val_] = 1

        obj = OrderedDict(sorted(obj.items(), key=itemgetter(1), reverse=True))
        for i in range(n):
            self.objN[obj.keys()[i]] = obj.values()[i]
        self.objN = OrderedDict(sorted(self.objN.items(), key=itemgetter(1), reverse=True))


    # Gets each atribute's frequency
    def getFreq(self):
        for it, v in self.corpus.items():
            for itt, vv_ in self.objN.items():
                count = 0
                for v_ in v.split():
                    if v_ == itt:
                        count += 1
                psj = str(count/float(vv_))
                if count == 0:
                    if it in self.objFreq.keys():
                        self.objFreq[it].append((itt, "0"))
                    else:
                        self.objFreq[it] = [(itt, "0")]
                else:
                    if it in self.objFreq.keys():
                        self.objFreq[it].append((itt, psj))
                    else:
                        self.objFreq[it] = [(itt, psj)]

    # Stores the values in a .arff file that can be read by weka
    def getArff(self):
        title = str("AttributeRelationFile") + ".arff"
        fichero_ = open(title, "w")
        fichero_.write("% 1. Title: Female or male features\n")
        fichero_.write("% \n")
        fichero_.write("% 2. Source: 1260\n")
        fichero_.write("% \t(a) Creators: J. Garcia del Muro, L. Hysa, J. Curto\n")
        fichero_.write("% \t(b) Date: March, 2017\n")
        fichero_.write("% \n")
        fichero_.write("% 3. Instances: 1260\n")
        fichero_.write("% \n")
        fichero_.write("% 4. Info: The N most common words\n")
        fichero_.write("% \n")
        fichero_.write('@RELATION ' + str("AttributeRelationFile") + '\n\n')
        values_ = self.objFreq.values()[0]
        for value_ in values_:
            fichero_.write('@ATTRIBUTE ' + str(value_[0]) +" NUMERIC" + '\n')
        fichero_.write("@ATTRIBUTE class {male, female} \n\n")
        fichero_.write('@DATA \n')
        i = 0
        for j_, v_ in self.objFreq.items():
            for v__ in v_:
                fichero_.write(str(v__[1])+",")
            if i == len(self.objFreq.keys())-1:
                fichero_.write(str(j_)[j_.find("_")+1:])
            else:
                fichero_.write(str(j_)[j_.find("_")+1:]+'\n')
            i +=1
        fichero_.close()

if __name__ == "__main__":
    main(10)
