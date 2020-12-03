import os
import json
import copy

from chessUtil.Features import Features
from chessUtil.AlphaBetaFeatures import AlphaBetaFeatures

features = []

jointFeatures = AlphaBetaFeatures()
firstFile = None

for root, dirs, files in os.walk("trained"):
    for file in files:
        f = open(os.path.join(root, file))
        saveFile = json.load(f)
        firstFile = copy.deepcopy(saveFile)
        f.close()

        fs = AlphaBetaFeatures()
        fs.fromDict(saveFile['weights'])

        features.append((saveFile['episode'], fs))


aEpi = 0

for n, fs in features:
    aEpi += n

for n, fs in features:
    jointFeatures.weights += n/aEpi * fs.weights

firstFile["episode"] = aEpi
firstFile["weights"] = jointFeatures.toDict()

f = open('joint-GrandQ.json', 'w')
f.write(json.dumps(firstFile))
f.close()
