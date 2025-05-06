import sys
import re
from generate_minimal_pairs import process_conllu_to_csv


def get_dependents(sentence_data, head_index):
    """Collects all dependent tokens of a phrase (e.g., an object phrase)."""
    dependents = {head_index}
    found_new = True

    while found_new:
        found_new = False
        for token in sentence_data:
            token_index, _, _, _, _, _, head, _, *_ = token
            if not re.match(r'^\d+$', token_index):
                continue
            token_index, head = int(token_index), int(head)
            if head in dependents and token_index not in dependents:
                dependents.add(token_index)
                found_new = True

    return sorted(dependents)


def create_svo_mp(sentence_data, generate=False):
    """Identifies SVO word order. If found and generate=False, generates True.
    If found and generate=True, returns a modified sentence where the
    position of the object phrase is swapped with the position of the finite verb."""
    words = {int(tok[0]): tok for tok in sentence_data if re.match(r'^\d+$', tok[0])}
    
    object_tokens = []
    root_verb_index = None
    finite_verb_index = None
    subject_index = None
    first_position = 1

    # Excludes sentences shorter than 3 words
    if len(sentence_data) < 3:
        return    

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
        index, _, _, upos, _, feats, head, deprel, *_ = token
        if not re.match(r'^\d+$', index):
            continue
        
        # Exclude sentences that end with a question mark, i.e. questions
        if (sentence_data[-1][2] == "?") or (sentence_data[-1][2] in {'"', "'"} and sentence_data[-2][2] == "?"): 
            return   
        
        # Excluding sentences that start with a question word, subordinator or verb (ellipsis or imperative clause)
        if index == first_position:
            if (feats in {"PronType=Int", "PronType=Rel"} or upos in {"SCONJ", "VERB"}):  
                return
        
        # Finding the root verb
        if deprel == "root" and upos == "VERB": 
            root_verb_index = int(index)
            if "VerbForm=Fin" in feats:
                finite_verb_index = root_verb_index
            break  # Break the loop when the root verb is found

    if root_verb_index is None:
        return  # Skip the sentence if there is no root verb

    for token in sentence_data:
        index, _, _, upos, xpos, feats, head, deprel, *_ = token
        if deprel == "nsubj" and upos in {"NOUN", "PNOUN", "PRON", "DET"} \
            and (int(index) < int(root_verb_index)) and int(head) == root_verb_index: # Ensure that the subject precedes the root verb and that it is a dependent of the root
            subject_index = int(index)

        # Identifies the auxiliary in the subclause, if applicable
        if upos == "AUX" \
            and root_verb_index \
                and "VerbForm=Fin" in feats \
                    and int(head) == int(root_verb_index) \
                        and finite_verb_index != root_verb_index:
            finite_verb_index = int(index)  

        # Find direct objects (obj) and clausal complements (ccomp) of the root verb
        if head.isdigit() and int(head) == int(root_verb_index) and deprel in {"obj", "ccomp"}: 
            deps = get_dependents(sentence_data, int(index))
            object_tokens.extend(deps)

    
    if not finite_verb_index or not subject_index or not object_tokens:
        return 

    # Create new word order by swapping the position of the object phrase and finite verb
    if generate == True:

        new_order = []
        for i in sorted(words.keys()):
            if i == finite_verb_index:
                new_order.extend(object_tokens)  # Move object before verb
                new_order.append(i)              # Then the verb
            elif i not in object_tokens:
                new_order.append(i)              # Add everything else

        modified_sentence = re.sub(r'\( ', '(', " ".join([words[i][1] for i in new_order]))  # Fix space after '('
        modified_sentence = re.sub(r'\s+([?.!":,)])', r'\1', modified_sentence)  # Fix space before special characters

        assert set(new_order) == set(words.keys()), f"Missing tokens: {set(words.keys()) - set(new_order)}"
    
        return modified_sentence

    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.conllu output.csv")
    else:
        process_conllu_to_csv(sys.argv[1], sys.argv[2], create_svo_mp, generate=True, n_pairs=50)
        print(f"File saved as {sys.argv[2]}")
