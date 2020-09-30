from queryAnalyzer import getPlayersInQuery, getLeaguesInQuery, getTeamsInQuery, getSeasonsInQuery, getStagesInQuery
import sqlAnswers
import numpy
import random
import json

from flair.data import Sentence

from flair.embeddings import WordEmbeddings
german_embedding = WordEmbeddings('de-crawl')



def preProcessQuery(query):
    query = query.lower()
    
    umlaut_a = 'ä'.encode()
    umlaut_o = 'ö'.encode()
    umlaut_u = 'ü'.encode()
    scharf_s = 'ß'.encode()
    
    query = query.encode()
    
    query = query.replace(umlaut_a, b'ae')
    query = query.replace(umlaut_o, b'oe')
    query = query.replace(umlaut_u, b'ue')
    query = query.replace(scharf_s, b'ss')
    
    query = query.decode('utf-8')
    
    if(query[-1:] == '?' or query[-1:] == '!' or query[-1:] == '.' ):
        return query[:-1]
    return query
 
def getVectorOfAnswer(index, queryV, trainData):
    bestEmbedding = 0
    inIteration1 = True
    trainDataIndex = str(index)
    for trainingSentence in trainData[trainDataIndex]:
        embed = getVectorOfQuery(trainingSentence)
        if(inIteration1 == True):
            bestEmbedding = embed
        elif(angle_between(queryV, bestEmbedding) > angle_between(queryV, embed)): #if a better trining sentence was found
            bestEmbedding = embed
        inIteration1 = False;
            
    return bestEmbedding
    
    
def replaceKeywords(query):
    pQ = getPlayersInQuery(query)
    lQ = getLeaguesInQuery(pQ[1])
    tQ = getTeamsInQuery(lQ[1])
    sQ = getSeasonsInQuery(tQ[1])
    dQ = getStagesInQuery(sQ[1])
    return dQ

def getVectorOfQuery(query):
    sentence = Sentence(query)
    german_embedding.embed(sentence)
    
    embed = 0
    for token in sentence:
        embed += token.embedding.cpu().numpy()
    return embed

def unit_vector(vector):
    return vector / numpy.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return numpy.arccos(numpy.clip(numpy.dot(v1_u, v2_u), -1.0, 1.0))
    
def getAnswer(question, trainData):
    
    answers = sqlAnswers.getAnswers()
    query = preProcessQuery(question)
    
    pQ = getPlayersInQuery(query)
    lQ = getLeaguesInQuery(pQ[1])
    tQ = getTeamsInQuery(lQ[1])
    sQ = getSeasonsInQuery(tQ[1])
    dQ = getStagesInQuery(sQ[1])
    
    queryV = getVectorOfQuery(dQ[1]) # erwarter preprocessed Query, TODO 
    
    queryRefined = [pQ[0],lQ[0],tQ[0],sQ[0],dQ[0]]
    
    queryToCompare = [len(queryRefined[0]),len(queryRefined[1]),len(queryRefined[2]),len(queryRefined[3]),len(queryRefined[4])]
    possibleAnswers = matchByOccurance(queryToCompare)
        
    if(len(possibleAnswers) == 1):
        return [possibleAnswers[0], queryRefined]
    if(len(possibleAnswers) == 0):
        return ["Es konnte leider keine passende Antwort gefunden werden!"]
    angles = []
    for i in possibleAnswers:
        angles.append(angle_between(getVectorOfAnswer(answers[i][6], queryV, trainData),queryV))#answers[answerIndex][6] equals the index of the train data json

    indexOfNeededAnswer = possibleAnswers[angles.index(min(angles))];
    
    return [possibleAnswers,angles, queryRefined]
    
def manualQuestions(inputQuestion):
    with open('trainData.json', encoding='utf-8') as myfile:
        trainData = json.load(myfile)
    answers = sqlAnswers.getAnswers()
    answer = getAnswer(inputQuestion,trainData)
    if(len(answer) == 3):
        possibleAnswers = answer[0]
        angles = answer[1]
        queryRefined = answer[2]
        returnAnswerIndex = possibleAnswers[angles.index(min(angles))]
        return answers[returnAnswerIndex][5](queryRefined)
    if(len(answer) == 2):
        returnAnswerIndex = answer[0]
        queryRefined = answer[1]
        return answers[returnAnswerIndex][5](queryRefined)
    if(len(answer) == 1):
        return answer[0]

def matchByOccurance(queryRefined):
    answers = sqlAnswers.getAnswers()
    possibleAnswers = [] 
    #cpossibleAnswers ontains index with possible answers which could match the query depending
    #on number of name occurances etc

    for x in range(0,len(answers)): #check for every "answer", if [1,0,0,0] matches [1,0,0,0] etc
        occMatches = True;
        for i in range(0, len(queryRefined)): #interate through the whole [0,1,2,3] array and check 
            if(queryRefined[i] != answers[x][i]):  # if something doesnt match, throw it out
                occMatches = False
        if(occMatches):
            possibleAnswers.append(x)
    return possibleAnswers

def useSplitTrainAndTestData():
    with open('trainData.json', encoding='utf-8') as myfile:
        obj = json.load(myfile)
    obj.pop('__comment')
    answers = sqlAnswers.getAnswers()

    
    for i in range(0,23):
        random.shuffle(obj[str(i)])
        objectsToRemove = random.randint(1, int(len(obj[str(i)])/2)) #Zufällige zahl die kleiner ist als die Hälfte der Trainigssätze

        trainData[str(i)] = obj[str(i)][objectsToRemove:]
        testData[str(i)] = obj[str(i)][0:objectsToRemove]
        
def oneMRR(testSize):
# Evaluation over all different Categories of Data

    trainData = dict()
    testData = dict()

    with open('trainData.json', encoding='utf-8') as myfile:
        obj = json.load(myfile)
    obj.pop('__comment')
    answers = sqlAnswers.getAnswers()

        
    for i in range(0,23):
        random.shuffle(obj[str(i)])
        objectsToRemove = int(len(obj[str(i)])*testSize)
        if(objectsToRemove == 0):
            objectsToRemove = 1
        trainData[str(i)] = obj[str(i)][objectsToRemove:]
        testData[str(i)] = obj[str(i)][0:objectsToRemove]

    validtests = 0
    totalscore = 0

    for key,v in testData.items():
        for i in range(0,22):
            if(str(answers[i][6]) == str(key)):
                wantedAnswer = str(i)
        
        for query in testData[key]:
            
            queryV = getVectorOfQuery(query)
            queryToCompare = [query.count("SPIELER"),query.count("COUNTRY"),query.count("TEAM"),query.count("SEASON"),query.count("STAGE")]
            possibleAnswers = matchByOccurance(queryToCompare)
            
            if(len(possibleAnswers)>1):
                angles = {}
                for index in possibleAnswers:
                    vec1 = getVectorOfAnswer(answers[index][6], queryV, trainData)
                    vec2 = queryV
                    if(numpy.any(vec1) != False):
                        cosAngle = angle_between(getVectorOfAnswer(answers[index][6], queryV, trainData),queryV)
                        angles[str(index)] = cosAngle
               
                if wantedAnswer in angles.keys():
                    validtests+=1
                    wantedAngle = angles[wantedAnswer]
                    score = 1
                    for value in angles.values():
                        if(value < wantedAngle):  #lower score if there are better results
                            score = score +1
                    totalscore += 1/score
                    
               
            
    return totalscore/validtests
    
def loopMRR(numLoops, testSize):
    values = []
    for i in range(0, numLoops):
        values.append(oneMRR(testSize))
    return values


def RRbyIndex(position, testSize):
# Evaluation of a specific type of category

    trainData = dict()
    testData = dict()

    with open('trainData.json', encoding='utf-8') as myfile:
        obj = json.load(myfile)
    obj.pop('__comment')
    answers = sqlAnswers.getAnswers()

        
    for i in range(0,23):
        random.shuffle(obj[str(i)])
        objectsToRemove = int(len(obj[str(i)])*testSize)
        trainData[str(i)] = obj[str(i)][objectsToRemove:]
        testData[str(i)] = obj[str(i)][0:objectsToRemove]


    validtests = 0
    totalscore = 0

    for key,v in testData.items():
        for i in range(0,22):
            if(str(answers[i][6]) == str(key)):
                wantedAnswer = str(i)
        
        if(str(key) == str(position)):
            for query in testData[key]:
                
                queryV = getVectorOfQuery(query)
                queryToCompare = [query.count("SPIELER"),query.count("COUNTRY"),query.count("TEAM"),query.count("SEASON"),query.count("STAGE")]
                possibleAnswers = matchByOccurance(queryToCompare)
                if(len(possibleAnswers)>1):
                    angles = {}
                    for index in possibleAnswers:
                        vec1 = getVectorOfAnswer(answers[index][6], queryV, trainData)
                        vec2 = queryV
                        if(numpy.any(vec1) != False):
                            cosAngle = angle_between(getVectorOfAnswer(answers[index][6], queryV, trainData),queryV)
                            angles[str(index)] = cosAngle
                    
                    if wantedAnswer in angles.keys():
                        validtests +=1
                        
                        wantedAngle = angles[wantedAnswer]
                        score = 1
                        for value in angles.values():
                            if(value < wantedAngle):  #lower score if there are better results
                                score = score +1
                        totalscore += 1/score
                        
                        
                   
    if(validtests == 0):
        return 0
    return totalscore/validtests
    
def loopRRbyIndex(numLoops, position, testSize):
    values = []
    for i in range(0, numLoops):
        values.append(RRbyIndex(position, testSize))
    return values