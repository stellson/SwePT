import sys
import re
from generate_minimal_pairs import process_conllu_to_csv


def create_tense_mp(sentence_data, generate=False):
    """Identifies tensed verbs. If found and generate=False, returns True.
    If found and generate=True, returns a modified sentence where the tensed verb is replaced by its lemma."""
    words = {int(tok[0]): tok for tok in sentence_data if re.match(r'^\d+$', tok[0])}
    modified_words = words.copy()  

    found_tensed_verb = False
    for token in sentence_data:
        index, form, lemma, upos, xpos, feats, head, deprel, *_ = token

        try:
            index = int(index)
        except:
            continue

        # Check if it's a tensed verb
        if upos in {"AUX","VERB"} and ("Tense=Past" in feats or "Tense=Pres" in feats) and "Voice=Pass" not in feats and lemma!=form:
            found_tensed_verb = True
            modified_words[index][1] = lemma  # Replace form with lemma
            break  # Replace only the first tensed verb

    if not found_tensed_verb:
        return None  # Skip sentences without tensed verbs

    if generate == True:
        # Reconstruct sentence with lemmatized verbs
        modified_sentence = " ".join([modified_words[i][1] for i in sorted(modified_words.keys())])

        # Cleanup spacing before punctuation
        modified_sentence = re.sub(r'\s+([?.!":;,)])', r'\1', modified_sentence)

        return modified_sentence
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.conllu output.csv")
    else:
        process_conllu_to_csv(sys.argv[1], sys.argv[2], create_tense_mp, generate=True, n_pairs=50)
        print(f"File saved as {sys.argv[2]}")
