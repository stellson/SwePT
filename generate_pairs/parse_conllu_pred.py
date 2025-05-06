import sys
import re
from generate_minimal_pairs import process_conllu_to_csv


def create_pred_a_mp(sentence_data, generate=False):
    """Identifies predicative agreement. If generate=False, return True if found.
    If generate=True, return a modified sentence where the adjective is replaced by its lemma, if found."""
    words = {int(tok[0]): tok for tok in sentence_data if re.match(r'^\d+$', tok[0])}
    modified_words = words.copy()  
    subject = None
    copula = None
    adjective = None
    adj_index = None
    for token in sentence_data:
        index, form, lemma, upos, xpos, feats, head, deprel, *_ = token

        try:
            index = int(index)
        except:
            continue

        if upos in {"NOUN"} and deprel in {"nsubj"} and subject == None:  # Identifying the subject
            subject = token
        if deprel == "cop":  # Identifying the copula and adjective
            adj_index = head
            copula = token
        if adj_index and index == int(adj_index) and upos=="ADJ" and "Degree=Pos" in feats and subject and index == int(subject[6]):  # Identifying the adjective
            if form.lower() != lemma:
                adjective = token 
                modified_words[index][1] = lemma

    
    if not (subject and copula and adjective):
        return
    if (int(subject[0]) > int(copula[0])): 
        return

    if generate == True:
        # Build the modified sentence
        modified_sentence = " ".join([modified_words[i][1] for i in sorted(modified_words.keys())]) 

        # Cleanup spacing before punctuation
        modified_sentence = re.sub(r'\s+([?.!":,)])', r'\1', modified_sentence)  # Fix space before special characters

        return modified_sentence
    return True


def create_pred_b_mp(sentence_data, generate=False):
    """Identifies predicative agreement with an attractor. If generate=False, returns True if found.
    If generate=True, returns sentence. Observe that if run through the generate_minimal_pairs script, 
    no sentences will be returned since the returned sentence contains no modification and thus is identical 
    to the original sentence. If used, a special character must be added to the modified sentence at the end of this function, and manually altered."""
    words = {int(tok[0]): tok for tok in sentence_data if re.match(r'^\d+$', tok[0])}
    modified_words = words.copy()  # Create a copy to modify
    
    subject = None
    second_noun = None
    copula = None
    adjective = None
    adj_index = None

    for token in sentence_data:
        index, form, lemma, upos, xpos, feats, head, deprel, *_ = token
        if upos in {"NOUN"} and deprel in {"nsubj"} and subject == None:  # Identifying the subject
            subject = token
        if upos == "NOUN" and subject and head == subject[0] and deprel == "nmod" and int(index) > int(subject[0]) :#not in {"conj", "appos"}:  # Identifying the second_noun
            second_noun = token
        if deprel == "cop":  # Identifying the copula and adjective
            adj_index = head
            copula = token
        if second_noun and index == adj_index and upos=="ADJ" and "Degree=Pos" in feats and deprel == "root":  # Identifying the adjective
            adjective = token  
    
    if not (subject and copula and adjective) or (int(subject[0]) > int(copula[0])):  # Exclude sentence if the subject is not in the fundament
        return

    # Exclude the sentence if the adjective has no distinction between gender or numerus
    if "UTR/NEU|SIN/PLU" in adjective[4]: 
        return
    # Exclude the sentence if the adjective has no distinction between gender and if the attractor is in singular
    if "UTR/NEU|SIN" in adjective[4] and "Number=Plur" not in second_noun[5]:
        return
    # Exclude the sentence if the attractor is in singular and the adjective makes no distinction between gender
    if "Number=Sing" in second_noun[5] and adjective[1].lower() == adjective[2]:
        return
    # Exclude the sentence if the attractor and the subject have the same gender and both are singular
    if ("Number=Sing" in subject[5] and "Number=Sing" in second_noun[5]) or ("SIN" in subject[4] and "SIN" in second_noun[4]):
        if ("UTR" in subject[4] and "UTR" in second_noun[4]) or ("Gender=Com" in subject[5] and "Gender=Com" in second_noun[5]):
            return 
        if ("NEU" in subject[4] and "NEU" in second_noun[4]) or ("Gender=Neut" in subject[5] and "Gender=Neut" in second_noun[5]):
            return
    # Exclude the sentence if the subject and the attractor are both plural
    if "PLU" in subject[4] and "PLU" in second_noun[4]:
        return
    # Exclude the sentence if the subject and attractor differ in gender but the adjective does not have a singular lemma
    if "PLU" in second_noun[4] and adjective[1].lower() == adjective[2]:
        return

    # Generating the duplicated sentence (must add character at the end of modified_sentence to ensure the grammatical and ungrammatical sentence are not identical)
    if generate == True:
        # Reconstruct sentence with lemmatized nouns
        modified_sentence = " ".join([modified_words[i][1] for i in sorted(modified_words.keys())])

        # Cleanup spacing before punctuation
        modified_sentence = re.sub(r'\s+([?.!":,)])', r'\1', modified_sentence)

        return modified_sentence + "+"
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.conllu output.csv") # For "function", define create_pred_a_mp or create_pred_b_mp
    else:
        process_conllu_to_csv(sys.argv[1], sys.argv[2], create_pred_a_mp, generate=True, n_pairs=50)
        print(f"File saved as {sys.argv[2]}")
