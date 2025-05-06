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


def create_negv_mp(sentence_data, generate=False):
    """Identifies preverbal negation in subclauses. If found and generate=False, returns True.
    If found and generate=True, returns a modified sentence where the negation is placed after the finite verb."""
    words = {int(tok[0]): tok for tok in sentence_data if re.match(r'^\d+$', tok[0])} 
    finite_verb_index = None
    first_position = 1
    main_verb_index = None
    negation_index = None
    subject_tokens = set()

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
        
        if lemma == "inte":
            # Make sure it is the negation in the dependent clause and not the main clause
            head_token = words.get(head, None)  # Retrieves the head of "inte" 
            if index == first_position:  
                return  # Skip token if the negation is topicalized
            if head_token:
                head_index, head_lemma, head_upos, head_feats, head_head, head_deprel = head_token[0], head_token[2], head_token[3], head_token[5], head_token[6], head_token[7]   
                if int(head_index) > index:
                    if head_upos == "VERB" \
                        and head_deprel in {"csubj", "ccomp", "acl", "acl:relcl", "advcl"}:
                        main_verb_index = int(head_index)
                        negation_index = index
                        if "VerbForm=Fin" in head_feats:
                            finite_verb_index = main_verb_index
        
        if main_verb_index and negation_index:

            # Identifies the subject phrase
            if "nsubj" in deprel and head == main_verb_index:
                subject_tokens = get_subject_phrase(sentence_data, index)

            # Identifies the auxiliary in the subclause, if applicable
            if upos == "AUX" \
                and "VerbForm=Fin" in feats \
                    and int(head) == int(main_verb_index) \
                        and index > negation_index \
                            and finite_verb_index != main_verb_index:
                finite_verb_index = int(index)     

    if finite_verb_index and negation_index:

        # Generates the ungrammatical sentence
        if generate == True:
            if subject_tokens and min(subject_tokens) <= finite_verb_index:
                reordered = []
                # Reorders the subclause if the negation precedes the subject
                for i in sorted(words.keys()):
                    if i == negation_index:
                        reordered.extend(subject_tokens) 
                        reordered.append(finite_verb_index)  
                        reordered.append(i)
                    elif i == finite_verb_index or i in subject_tokens:
                        continue 
                    else:
                        reordered.append(i)
            
                modified_words = " ".join([words[i][1] for i in reordered])
            else:
                # Reorders the subclause if the negation succeeds the subject
                words[finite_verb_index], words[negation_index] = words[negation_index], words[finite_verb_index]  # Move "inte" after verb
                modified_words = " ".join([words[i][1] for i in sorted(words.keys())]) 
            return modified_words  
        return True
    return


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.conllu output.csv")
    else:
        process_conllu_to_csv(sys.argv[1], sys.argv[2], create_negv_mp, generate=True, n_pairs=50)
        print(f"File saved as {sys.argv[2]}")
