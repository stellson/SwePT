import sys
import re
from generate_minimal_pairs import process_conllu_to_csv


def create_plural_mp(sentence_data, generate=False):
    """Identifies numerals modifying nouns. If found and generate=False, returns True.
    If found and generate=True, returns a modified sentence where the noun is replaced with its lemma."""
    words = {int(tok[0]): tok for tok in sentence_data if re.match(r'^\d+$', tok[0])}
    modified_words = words.copy()  # Create a copy to modify
    found_valid_numeral = False
    modified = False

    for token in sentence_data:
        index, form, lemma, upos, xpos, feats, head, deprel, *_ = token
        try:
            index = int(index)  
        except:
            continue
        try:
            head = int(head)
        except:
            continue

        # Check if the word is a plural numeral modifier
        if upos == "NUM" and lemma not in {"en", "ett", "1"} and head > index and "nummod" in deprel:  
            for noun_token in sentence_data:
                noun_index, noun_form, noun_lemma, noun_upos, noun_xpos, noun_feats, noun_head, *_ = noun_token
                try:
                    noun_index = int(noun_index) # Skips floats (ellipsis)
                except:
                    continue
                if modified == False:

                    if noun_upos == "NOUN" and noun_index == head and ("Abbr=Yes" not in noun_feats)\
                        and noun_form.lower() != noun_lemma and "Case=Gen" not in noun_feats and "Number=Plur" in noun_feats: #and noun_lemma not in seen_lemmas:
                        found_valid_numeral = True
                        modified_words[noun_index][1] = noun_lemma  # Replace noun with lemma
                        modified = True
    
    if found_valid_numeral:
        if generate == True:
            # Reconstruct sentence with lemmatized nouns
            modified_sentence = " ".join([modified_words[i][1] for i in sorted(modified_words.keys())])

            # Cleanup spacing before punctuation
            modified_sentence = re.sub(r'\s+([?.!":,)])', r'\1', modified_sentence)

            return modified_sentence
        return True

    return


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.conllu output.csv")
    else:
        process_conllu_to_csv(sys.argv[1], sys.argv[2], create_plural_mp, generate=True, n_pairs=50)
        print(f"File saved as {sys.argv[2]}")
