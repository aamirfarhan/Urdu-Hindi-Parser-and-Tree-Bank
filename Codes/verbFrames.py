import sys, os, glob, re

inputDir = sys.argv[1]
listOfVBA = []
dictOfVerbs = dict()
count = 1
x = 0

chunkDetails = ""
sentencePattern = re.compile('^<Sentence.*$')
chunkPattern = re.compile('^.*\(\(.*$')
tokenPattern = re.compile('^[0-9]+\.[0-9]+.*$')

inputVerb = input("Enter the verb to search : ")

for filename in os.listdir(inputDir):
    fopen = open(os.path.join(inputDir, filename), 'r')
    lines = fopen.readlines()
    for line in lines:
        if re.search(sentencePattern, line):
            if not dictOfVerbs:
                continue
            else:
                for verb in dictOfVerbs:
                    ans = dictOfVerbs[verb]
                    if ans[0] == inputVerb:
                        listOfVBA.append(ans)
            dictOfVerbs = {}
            continue
        if re.search(chunkPattern, line):
            chunkDetails = []
            chunkFs = line.split('\t')[3].split()
            chunkName = ""
            val = []
            for fs in chunkFs:
                if fs[0:4] == "name":
                    chunkName = fs[6:len(fs)-1]
                if fs[0:4] == "drel":
                    val = fs[6:len(fs)-2].split(':')

            chunkName = chunkName.split('\'')[0]
            if re.search(r'^.*V.*$', chunkName):
                chunkDetails = chunkName
                if chunkName not in dictOfVerbs:
                    dictOfVerbs[chunkName] =  ["temp","temp",[]]

                if not val:
                    continue
                if re.search(r'^.*V.*$', val[1]):
                    if val[1] not in dictOfVerbs:
                        dictOfVerbs.setdefault(val[1], ["temp", "temp_i", [val[0]]])
                    else:
                        dictOfVerbs[val[1]][2].append(val[0])
            else:
                if not val:
                    continue
                if re.search(r'^.*V.*$', val[1]):
                    if val[1] not in dictOfVerbs:
                        dictOfVerbs.setdefault(val[1], ["temp", "temp_i", [val[0]]])
                    else:
                        dictOfVerbs[val[1]][2].append(val[0])
        if re.search(tokenPattern, line):
            if not chunkDetails:
                continue

            else:
                tokenPOS = line.split('\t')[2]
                if tokenPOS == "VM":
                    tokenAF = line.split('\t')[3].split()[1].split(',')
                    tokenINF = tokenAF[len(tokenAF)-2]
                    token_i = tokenINF[0:len(tokenINF)-1]

                    token_name = line.split('\t')[1]
                    dictOfVerbs[chunkDetails][0] = token_name
                    dictOfVerbs[chunkDetails][1] = token_i


count_dict = {}
i=0
for element in listOfVBA:
    print(element, ": ", listOfVBA.count(element))
