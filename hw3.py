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
    flag = 0
    for sentence in allSentences:
        splitSentence = sentence.split(' ')
        featureVector = [0] * (len(vocab) + 1)

        for word in splitSentence:
            # check if word is in our sentence
            if flag == 0: 
                print(word)
            if word in vocab:
                # get index of word
                index = vocab.index(word)
                if flag == 0:
                    print(index)
                # set the value to 1
                featureVector[index] = 1
        # add the classification
        if allClassifications[allSentences.index(sentence)] == '1':
            featureVector[-1] = 1
        else:
            featureVector[-1] = 0
        featureMatrix.append(featureVector)
        flag = 1
    print (len(featureMatrix[0]))
    return featureMatrix


def main():

    allSentences, allClassifications, vocab = getWordsAndVocab('trainingSet.txt')

    # print the length of allSentences
    # print('Length of allSentences:', len(allSentences))
    # print('Length of allClassifications:', len(allClassifications))
    # print (allSentences)
    # print (allClassifications)
    # print (vocab)

    trainingMatrix = makeFeatures(allSentences, allClassifications, vocab)


    print(trainingMatrix[1])

if __name__ == '__main__':
    main()




