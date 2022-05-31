import string
import math

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
        splitSentence = sentence.split(' ')
        featureVector = [0] * (len(vocab) + 1)

        for word in splitSentence:
            if word in vocab:
                # get index of word
                index = vocab.index(word)
                # set the value to 1
                featureVector[index] = 1
        # add the classification
        if allClassifications[allSentences.index(sentence)] == '1':
            featureVector[-1] = 1
        else:
            featureVector[-1] = 0
        featureMatrix.append(featureVector)

    # print("feature matrix", featureMatrix[0])
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


# This function takes in the vocabulary, the training matrix, and the training classifications. It then
# calculates the probability of a positive review and the probability of a negative review. It then
# calculates the probability of a word being found in a positive review, the probability of a word
# being found in a negative review, the probability of a word not being found in a positive review,
# and the probability of a word not being found in a negative review. It then returns the
# probabilities for each word and the probabilities for a positive review and a negative review.
def createProbabilities(allVocab, trainingMatrix, trainingClassifications):
    positives = 0
    negatives = 0
    results = []
    # print(trainingClassifications)
    for i in range(len(trainingClassifications)):
        if trainingClassifications[i] == '1':
            positives += 1
        else:
            negatives += 1


    probPos = positives/len(trainingClassifications)
    probNeg = negatives/len(trainingClassifications)


    # The below code is calculating the number of times a word is found in a positive review and the
    # number of times a word is found in a negative review. It is also calculating the number of times a
    # word is not found in a positive review and the number of times a word is not found in a negative
    # review.
    for i in range(len(allVocab)):
        found_pos = 0
        found_neg = 0

        notfound_pos = 0
        notfound_neg = 0

        # Iterating through the training matrix and checking if the word is found in a positive review or a
        # negative review. It is also checking if the word is not found in a positive review or a negative
        # review.
        for row in trainingMatrix:
            if row[i] == 1:
                if row[-1] == 1:
                    found_pos += 1
                else:
                    found_neg += 1
            else:
                if row[-1] == 1:
                    notfound_pos += 1
                else:
                    notfound_neg += 1

        # all probabilities for a given vocab word based on all sentences
        # dirichlet not helping accuracy, not gonna do it
        # probFoundPos = (found_pos + 1) / (positives + 2)
        # probFoundNeg = (found_neg + 1) / (negatives + 2)
        # probNotFoundPos = (notfound_pos + 1) / (positives + 2)
        # probNotFoundNeg = (notfound_neg + 1) / (negatives + 2)


        # given that a sentence is positive, what is the probability that this word is present
        probFoundPos = (found_pos ) / (positives)
        # given that a sentence is negative, what is the probability that this word is present
        probFoundNeg = (found_neg ) / (negatives)
        # given that a sentence is positive, what is the probability that this word is not present
        probNotFoundPos = (notfound_pos) / (positives)
        # given that a sentence is negative, what is the probability that this word is not present
        probNotFoundNeg = (notfound_neg) / (negatives)

        # Creating a list of tuples that contain the probabilities of a word being found in a positive review,
        # the probabilities of a word being found in a negative review, the probabilities of a word not being
        # found in a positive review, and the probabilities of a word not being found in a negative review.
        probabilities = (probFoundPos, probFoundNeg, probNotFoundPos, probNotFoundNeg)
        results.append(probabilities)

        # print(allVocab[i], probabilities)



    return results, probPos, probNeg


def testing(sentences, trainedVocab, probPos, probNeg, allVocab):
    result = []

    for i in range(len(sentences)):
        splitSentence = sentences[i].split(' ')

        realProbPos = probPos
        realProbPos = math.log(realProbPos)
        for word in allVocab:
            if word in splitSentence:
                # if i == 0:
                #     print("found TT", word, ", ", trainedVocab[i][0])
                #     print(word)
                # WORD IS IN SENTENCE AND IT AND WE WANT POSITIVE PROBABILITY (TT)


                # get index of current word from allVocab

                index = allVocab.index(word)
                # print(index)
                realProbPos += math.log(trainedVocab[index][0] + 0.0001)
            else:
                # if i == 0:
                #     print("found FT", word, ", ", trainedVocab[i][2])
                #     print(word)
                # WORD IS NOT IN SENTENCE AND WE WANT POSITIVE PROBABILITY (FT)
                index = allVocab.index(word)
                # print(index)
                realProbPos += math.log(trainedVocab[index][2] + 0.0001)



        realProbNeg = probNeg
        realProbNeg = math.log(realProbNeg)
        for word in allVocab:
            if word in splitSentence:
                # if i == 0:
                #     print("found TF", word, ", ", trainedVocab[i][1])
                #     print(word)
                # WORD IS IN SENTENCE AND WE WANT NEGATIVE PROBABILITY (TF)

                index = allVocab.index(word)
                # print(index)
                realProbNeg += math.log(trainedVocab[index][1] + 0.0001)
            else:
                # if i == 0:
                #     print("found FF", word, ", " , trainedVocab[i][3])
                #     print(word)
                # WORD IS NOT IN SENTENCE AND WE WANT NEGATIVE PROBABILITY (FF)

                index = allVocab.index(word)
                # print(index)
                realProbNeg += math.log(trainedVocab[index][3] + 0.0001)

        # print(realProbPos)
        # print(realProbNeg)
        result.append(1) if realProbPos > realProbNeg else result.append(0)
    # print ("result: ", len(result))
    return result

# It takes in two lists of classifications, one for the classifications of the training data and one
# for the classifications of the test data, and returns the accuracy of the classifier
def checkAccuracy(classifications, testClassifications):
    correct = 0
    for i in range(len(classifications)):
        if classifications[i] == int(testClassifications[i]):
            correct += 1
    print(correct)
    print(len(classifications))
    return correct/len(classifications)


def main():

    trainingSentences, trainingClassifications, vocab = getWordsAndVocab('trainingSet.txt')
    testingSentences, testingClassifications, _ = getWordsAndVocab('testSet.txt')

    trainingMatrix = makeFeatures(trainingSentences, trainingClassifications, vocab)

    testingMatrix = makeFeatures(testingSentences, testingClassifications, vocab)

    printPreprocessing(vocab, trainingMatrix, testingMatrix)

    # print(trainingSentences)

    trainedVocab, probPos, probNeg = createProbabilities(vocab, trainingMatrix, trainingClassifications)

    trainedClassifications = testing(trainingSentences, trainedVocab, probPos, probNeg, vocab)
    testClassifications = testing(testingSentences, trainedVocab, probPos, probNeg, vocab)

    # print('Training Classifications: ', trainingClassifications)
    # print('Test Classifications: ', testClassifications)

    print('Training Accuracy:', checkAccuracy(trainedClassifications, trainingClassifications))
    print('Testing Accuracy:', checkAccuracy(testClassifications, testingClassifications))

if __name__ == '__main__':
    main()




