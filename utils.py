import regex as re

def pre_tokenize(text,pattern):
    list_of_strings = re.findall(pattern,text)
    return list_of_strings


def tokenize(list_of_strings):
    tokens=[]
    for i in range(len(list_of_strings)):
        tokens.append(list(list_of_strings[i].encode('utf-8')))
    return tokens
        

def get_pairs_occurence(list_of_token_ids):
    occurence_dict={}
    for token_ids in list_of_token_ids:
        for i in range(len(token_ids)-1):
            occurence_dict[(token_ids[i],token_ids[i+1])]=occurence_dict.get((token_ids[i],token_ids[i+1]),0)+1  
    return occurence_dict



def merge_and_replace(list_of_tokens,pair_to_replace,replacement_id):
    list_of_token_ids_after_replacement = []
    for token_ids in list_of_tokens:
        i=0
        token_ids_after_replacement=[]
        
        while i < (len(token_ids)):
            if token_ids[i]!=pair_to_replace[0]:
                token_ids_after_replacement.append(token_ids[i])
                i+=1
            else:
                if i<len(token_ids)-1 and token_ids[i+1]==pair_to_replace[1]:   #list is not out of range because it checks second condition only if first condition is true
                    token_ids_after_replacement.append(replacement_id)
                    i+=2
                else:
                    token_ids_after_replacement.append(token_ids[i])
                    i+=1
        list_of_token_ids_after_replacement.append(token_ids_after_replacement)  
    return list_of_token_ids_after_replacement



def merge_common_tokens(list_of_tokens,vocab_size):
    num_merges = vocab_size - 256
    merges={}
    
    for i in range(num_merges):
        occurences=get_pairs_occurence(list_of_tokens)
        if len(occurences)==0:
            print('everything has been merged so stopping at vocab:',256+i)
            break
        most_repeating_pair = max(occurences,key=occurences.get)
        list_of_tokens = merge_and_replace(list_of_tokens,most_repeating_pair,256+i)    #255 tokens are occupied for each byte so start with 256
        merges[most_repeating_pair] = 256+i

    vocab = {i :bytes([i]) for i in range (256)}
    for (p0,p1), token  in merges.items():
        vocab[token]=vocab[p0]+vocab[p1]

    return merges,vocab


def encode(text,merges):
    tokens=list(text.encode("utf-8"))
    while True:
        all_pairs=list(get_pairs_occurence([tokens]).keys())
        best_pair = None
        minimum = float('inf')
        for pair in all_pairs:
            merge_priority = merges.get(pair,float('inf'))
            if merge_priority<minimum:
                best_pair=pair
                minimum=merge_priority
        if best_pair:
            tokens = merge_and_replace([tokens],best_pair,merges[best_pair])[0]   #merge and replace gives 2d list 
        else:
            break
    return tokens

def decode(tokens,vocab):
    tokens = b"".join(vocab[token] for token in tokens)
    text = tokens.decode('utf-8',errors='replace')
    return text
