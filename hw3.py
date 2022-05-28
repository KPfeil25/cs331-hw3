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

def printPreprocessing(vocab, trainingData, testingData):
    outputTraining = open('trainPreprocessed.txt', 'w')
    outputTesting = open('testPreprocessed.txt', 'w')

    for word in vocab:
        outputTraining.write(word + ',')
        outputTesting.write(word + ',')

    outputTraining.write('classlabel\n')
    outputTesting.write('classlabel\n')

    # iterate through all elements of training data
    for i in range(len(trainingData)):
        for j in range(len(trainingData[i])):
            # if its the last element, dont print the comma
            if j == len(trainingData[i]) - 1:
                outputTraining.write(str(trainingData[i][j]))
            else:
                outputTraining.write(str(trainingData[i][j]) + ',')
        outputTraining.write('\n')


    # iterate through all elements of testing data
    for i in range(len(testingData)):
        for j in range(len(testingData[i])):
            # if its the last element, dont print the comma
            if j == len(testingData[i]) - 1:
                outputTesting.write(str(testingData[i][j]))
            else:
                outputTesting.write(str(testingData[i][j]) + ',')
        outputTesting.write('\n')


def main():

    trainingSentences, trainingClassifications, vocab = getWordsAndVocab('trainingSet.txt')
    testingSentences, testingClassifications, doNotUse = getWordsAndVocab('testSet.txt')

    # print the length of allSentences
    # print('Length of allSentences:', len(allSentences))
    # print('Length of allClassifications:', len(allClassifications))
    # print (allSentences)
    # print (allClassifications)
    # print (vocab)

    trainingMatrix = makeFeatures(trainingSentences, trainingClassifications, vocab)

    testingMatrix = makeFeatures(testingSentences, testingClassifications, vocab)

    printPreprocessing(vocab, trainingMatrix, testingMatrix)




    print(trainingMatrix[1])

if __name__ == '__main__':
    main()




