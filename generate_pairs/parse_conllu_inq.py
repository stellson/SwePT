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


def create_inq_mp(sentence_data, generate=False):
    """Identifies indirect questions. If found and generate=False, return True.
    If found and generate=True, swap the position of the verb with the NP in the embedded clause."""
    words = {int(tok[0]): tok for tok in sentence_data if re.match(r'^\d+$', tok[0])}
    matrix_verb = None
    subject_tokens = []
    verb_index = None
    question_word = None
    embedded_verb = None
    auxiliary = None
    subject_index = None
    rel_pron_head = None
    pre_subj_negation_index = None

    for token in sentence_data:
        index, form, lemma, upos, xpos, feats, head, deprel, deps, misc = token
        try:
            index = int(index)
        except:
            continue
        try:
            head = int(head)
        except:
            continue
        
        # Identifying the matrix verb
        if upos == "VERB" and not matrix_verb \
            and lemma in {"undra", "fråga", "veta", "tänka", "fundera", "gissa", "undersöka", "förklara", "diskutera", "beskriva"}:
            matrix_verb = token

        # Identifying the question word/subordinator
        if matrix_verb and not question_word:
            if ("WHInfo-Indirect.WHWord" in misc or "PronType=Int" in feats):
                question_word = token

            if lemma in {"om", "huruvida"} and deprel in {"mark"}:
                question_word = token
        
        # Excludes sentence if neg-subject word order is used 
        if matrix_verb and question_word and not subject_index:
            if lemma == "inte" and index == int(question_word[0])+1:
                pre_subj_negation_index = index
            
            # Identifying the relative pronoun "som", if applicable
            if "PronType=Rel" in feats:
                rel_pron_head = head
            
            # Identifying the subject
            if deprel in {"expl", "nsubj", "nsubj:pass"} and not subject_index and "PronType=Rel" not in feats: 
                subject_index = index
        
        # Identifying the verb in the embedded clause
        if matrix_verb and question_word and subject_index:     
            question_word_head = sentence_data[int(question_word[6])-1]
            if not embedded_verb and int(question_word_head[0]) >= int(question_word[0]):  
                if question_word[2]=="om":
                    if question_word_head[7] in {"ccomp", "cop"}:
                        embedded_verb = question_word_head # Identifying the embedded verb as head of the question_word
                else:
                    if question_word_head[7] in {"ccomp"}: # is ccomp
                        embedded_verb = question_word_head # Identifying the embedded verb as head of the question_word

        # Excludes relative subjects and objects that confounds the minimal pair generation process
        if embedded_verb and rel_pron_head:
            if rel_pron_head == int(embedded_verb[0]): 
                return
        
        # Identifying the auxiliary (if applicable)
        if matrix_verb and question_word and subject_index and embedded_verb:
            if upos == "AUX" and "VerbForm=Fin" in feats and int(head) == int(embedded_verb[0]) and not auxiliary:
                embedded_verb = token
    
    # Identifies all elements of the subject phrase for proper swapping
    if subject_index and embedded_verb and "VerbForm=Fin" in embedded_verb[5]: 
        
        # Builds the ungrammatical sentence
        if generate == True:
            verb_index = embedded_verb[0]
            subject_tokens = get_subject_phrase(sentence_data, subject_index)
            
            new_order = []
            subject_tokens_set = set(subject_tokens)
            verb_index = int(embedded_verb[0])

            for i in sorted(words.keys()):
                if i < min(subject_tokens):
                    new_order.append(i)
            new_order.append(verb_index)
            new_order.extend(subject_tokens)
            for i in sorted(words.keys()):
                if i > max(subject_tokens) and i != verb_index and i not in subject_tokens_set:
                    new_order.append(i)
            
            if pre_subj_negation_index:
                words[verb_index], words[pre_subj_negation_index] = words[pre_subj_negation_index], words[verb_index]  # Move "inte" after verb

            modified_sentence = " ".join([words[i][1] for i in new_order])
            modified_sentence = re.sub(r'\( ', '(', modified_sentence)  # Fix space after '('
            
            assert set(new_order) == set(words.keys()), f"Missing tokens: {set(words.keys()) - set(new_order)}"

            return modified_sentence
        
        return True
    else:
        return


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.conllu output.csv")
    else:
        process_conllu_to_csv(sys.argv[1], sys.argv[2], create_inq_mp, generate=True, n_pairs=50)
        print(f"File saved as {sys.argv[2]}")
