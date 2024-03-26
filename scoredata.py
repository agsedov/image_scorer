class ScoreData:
    def  __init__(self,filename, basedir):
        self.filename = filename
        self.basedir = basedir
        self.data = []
        if(os.path.isfile(filename)):
            self.load()
        else:
            self.initData(basedir)
            self.save()

    def save(self):
        with open(self.filename, 'w') as outfile:
            json.dump(self.data, outfile)

    def load(self):
        with codecs.open(self.filename, 'r', 'utf-8') as f:
            self.data = json.load(f)

    def initData(self,basedir):
        for folder, subs, files in os.walk(basedir):
            for file in files:
                self.data.append({
                        'path':os.path.join(folder,file)
                    })

    def unscored(self):
        return list(filter(lambda x: not 'score' in x, self.data))

    def randomunscored(self):
        unscored = self.unscored()
        if len(unscored) > 0 :
            return random.choice(unscored)['path'], len(unscored)
        else:
            return None, 0

    def setScore(self, path, score):
        for entry in self.data:
            if entry['path'] == path:
                entry['score'] = score
        self.save()
