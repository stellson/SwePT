import sys
import re
from generate_minimal_pairs import process_conllu_to_csv


def get_subject_phrase(sentence_data, subject_index):
    """Collects all tokens that belong to the subject phrase and returns the phrase."""
    subject_tokens = {subject_index}
    dependents = True
    
    while dependents:
        dependents = False
        for token in sentence_data:
            index, _, _, _, _, _, head, _, *_ = token
            if not re.match(r'^\d+$', index):
                continue
            
            try:
                index = int(index)
            except:
                continue
            try:
                head = int(head)
            except:
                continue

            if head in subject_tokens and index not in subject_tokens:
                subject_tokens.add(index)  # Add dependents recursively
                dependents = True  # Continue checking for more dependents
    
    return sorted(subject_tokens)


def create_inv_mp(sentence_data, generate=False):
    """Identifies sentences with a topicalized constituent. If found and generate=False, return True.
    If found and generate=True, swap the subject with the finite verb after the topicalized constituent."""
    words = {int(tok[0]): tok for tok in sentence_data if re.match(r'^\d+$', tok[0])}  # Map token index to data
    
    verb_index = None
    subject_index = None
    first_position = 1

    # Identifies the fundament position if initial conjunction or punctuation elements
    for token in sentence_data:
        index, _, _, upos, *_ = token
        if not re.match(r'^\d+$', index):
            continue
        index = int(index)

        if upos in {"PUNCT", "CCONJ"}:
            first_position = (index)+1
        else:
            break  

    for token in sentence_data:
        index, form, lemma, upos, xpos, feats, head, deprel, *_ = token
        
        if not re.match(r'^\d+$', index): # Skips non-integer IDs
            continue  
        try:
            index = int(index)
        except:
            continue
        try:
            head = int(head)
        except:
            continue
        
        # Excludes sentences shorter than 3 words
        if len(sentence_data) < 3:
            return
        
        # Excludes questions that start with a question word or imperative
        # Excludes sentences with a subject or expletive (dummy subject) in the fundament
        if index == first_position:
            if "PronType=Int" in feats or "Mood=Imp" in feats or \
                deprel in {"expl", "nsubj", "nsubj:pass"} or lemma == "kanske":
                return

        # Excludes sentences that end with a question mark
        if (sentence_data[-1][2] == "?") or (sentence_data[-1][2] in {'"', "'"} and sentence_data[-2][2] == "?"): 
            return

        # Identifies the finite verb (pivot after topicalized element)
        if (deprel == "root" or sentence_data[head-1][7] == "root") and upos in {"VERB", "AUX"} \
            and "VerbForm=Fin" in feats and "Mood=Ind" in feats and not verb_index:
            if index == first_position:
                return  # Exclude sentence if the sentence starts with a verb
            verb_index = index
            break
    
    # Identifies the subject after the topicalized constituent
    for token in sentence_data:
        index, form, lemma, upos, xpos, feats, head, deprel, *_ = token
        if not re.match(r'^\d+$', index):  
            continue  
        try:
            index = int(index)
        except:
            continue
        try:
            head = int(head)
        except:
            continue
        if verb_index and index <=  verb_index \
            and deprel in {"expl", "nsubj", "nsubj:pass"} and head == verb_index: 
            return  # Excludes the sentence if a subject preceding the root verb is found (no topicalization)
        
        if deprel in {"nsubj", "nsubj:pass", "expl"} and verb_index and subject_index is None:
            subject_index = index  # First subject after the verb
            break  # Stops at first subject found
    
    if verb_index and subject_index:
        if generate:

            subject_tokens = get_subject_phrase(sentence_data, subject_index)
            
            # Moves subject phrase before the verb
            new_order = []
            for i in sorted(words.keys()):
                if i in subject_tokens:
                    continue
                if i == verb_index:
                    new_order.extend(subject_tokens) 
                new_order.append(i)

            modified_sentence = re.sub(r'\( ', '(', " ".join([words[i][1] for i in new_order]))  # Fix space after '('
            
            assert set(new_order) == set(words.keys()), f"Missing tokens: {set(words.keys()) - set(new_order)}"

            return modified_sentence
        return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.conllu output.csv")
    else:
        process_conllu_to_csv(sys.argv[1], sys.argv[2], create_inv_mp, generate=True, n_pairs=50)
        print(f"File saved as {sys.argv[2]}")
