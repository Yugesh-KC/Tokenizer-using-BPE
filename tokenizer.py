from utils import *
import pickle
class Tokenizer:

    def load_pretrained(self,file_location):
        with open(file_location,'rb') as f:
            data=pickle.load(f)
            
        self.merges=data[0]
        self.vocab=data[1]
       
    
    def train(self,input_text,vocab_size,regex_pattern=None):
        
        if regex_pattern:
            list_of_text = pre_tokenize(input_text,regex_pattern)
        else:
            list_of_text=[input_text]   

        tokens = tokenize(list_of_text)
        self.merges,self.vocab = merge_common_tokens(tokens,vocab_size)
       

    def save(self,file_location):
        if file_location.endswith('pkl'):
            with open(file_location, 'wb') as f:
                pickle.dump([self.merges,self.vocab], f)
        else:
            raise ValueError("pls gib pkl file extension")
        
    def encode(self,text):
        if self.vocab:
            tokens = encode(text,self.merges)
            return tokens
        else:
            raise ValueError("pls load or train the model first")
        
    def decode(self,tokens):
        if self.vocab:
            text=decode(tokens,self.vocab)
            return text
        else:
            raise ValueError("pls load or train the model first")

a=Tokenizer()
a.train('aaaaaaaaaaa',300)
print(a.encode('aaaaaa'))