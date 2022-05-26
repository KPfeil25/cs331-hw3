import string

def getWordsAndVocab(filename):
    allSentences = []
    allClassifications = []
    vocab = set()
    getRidOfThese = string.punctuation + '0123456789' + ''
    
    with open(filename, 'r') as f:
        sentences = f.readlines()
        for sentence in sentences:
            sentence = sentence.split('\t')
            classifier = sentence[1].strip(' \n')
            sentence = sentence[0]
            # sorry for this
            strippedSentence = sentence.translate(str.maketrans('', '', getRidOfThese)).lower().strip()
            allSentences.append(strippedSentence)
            allClassifications.append(classifier)

        for sentence in allSentences:
            for word in sentence.split(' '):
                if word != '':
                    vocab.add(word)
        vocab = sorted(vocab)

    return allSentences, allClassifications, vocab

# check this is working correctly
def makeFeatures(allSentences, allClassifications, vocab):
    featureMatrix = []

    for sentence in allSentences:
        featureVector = []
        for word in vocab:
            if word in sentence:
                featureVector.append(1)
            else:
                featureVector.append(0)
        if allClassifications[allSentences.index(sentence)] == 1:
            featureVector.append(1)
        featureMatrix.append(featureVector)
    return featureMatrix

def main():

    allSentences, allClassifications, vocab = getWordsAndVocab('trainingSet.txt')

    # print the length of allSentences
    # print('Length of allSentences:', len(allSentences))
    # print('Length of allClassifications:', len(allClassifications))
    print (allSentences)
    print (allClassifications)
    print (vocab)

    


if __name__ == '__main__':
    main()




