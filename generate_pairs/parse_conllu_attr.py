import sys
import re
from generate_minimal_pairs import process_conllu_to_csv


def create_attr_mp(sentence_data, generate=False):
    """Finds adjectives with attributive agreement. If found and generate=False, it returns True.
    If found and generate=False, it returns the sentence with the adjective replaced by its lemma."""
    words = {int(tok[0]): tok for tok in sentence_data if re.match(r'^\d+$', tok[0])}
    modified_words = words.copy()  # Create a copy to modify

    found_valid_adjective = False
    for token in sentence_data:
        index, form, lemma, upos, xpos, feats, head, deprel, *_ = token
        try:
            index = int(index)
        except:
            continue

        # Check if it's an attributive adjective
        if upos == "ADJ" and deprel == "amod" and "Degree=Pos" in feats and "Definite=Ind" in feats:
            
            # Ensure it's NOT in singular and common form or that there is no distinction between the lemma and the form
            if found_valid_adjective == False and not (("Number=Sing" in feats \
                and ("Gender=Com" in feats or "UTR" in xpos)) or lemma == form.lower()):
                found_valid_adjective = True
                
                # Generate minimal pairs (replace form with lemma)
                if generate == True:
                    if form[0].isupper():
                        lemma = lemma.capitalize() # Capitalize the modified word in the ungrammatical sentence if the original word is capitalized
                    modified_words[index][1] = lemma 

                    # Reconstruct sentence with lemmatized adjectives
                    modified_sentence = " ".join([modified_words[i][1] for i in sorted(modified_words.keys())])

                    # Cleanup spacing before punctuation
                    modified_sentence = re.sub(r'\s+([?.!":;,)])', r'\1', modified_sentence)

                    return modified_sentence
                return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.conllu output.csv")
    else:
        process_conllu_to_csv(sys.argv[1], sys.argv[2], create_attr_mp, generate=True, n_pairs = 50)
        print(f"File saved as {sys.argv[2]}")
