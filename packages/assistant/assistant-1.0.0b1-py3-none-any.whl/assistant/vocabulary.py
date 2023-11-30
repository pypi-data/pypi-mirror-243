class Vocabulary:

    sentences_sources_dir = None
    word_list_path = None
    
    sentences_list = []
    word_list = []

    def __init__(self):

        self.sentences_list = self.collect_sentences()
        self.word_list = self.as_list()

    def collect_sentences(self):
        pass

    def as_list(self):
        word_list = []
        for sentence in self.sentences_list:
            for word in sentence.split():
                if word not in word_list:
                    word_list.append(word)
        return word_list