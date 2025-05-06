import csv
import re


def read_conllu(file_path):
    """Reads a CoNLL-U file and extracts sentences with their token data."""
    sentences = []
    current_sentence = []
    current_text = ""

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# text ="):
                current_text = line[8:].strip()  # Extract sentence text
            elif line and not line.startswith("#"):
                columns = line.split("\t")
                if len(columns) > 6:
                    current_sentence.append(columns)  # Store token information
            elif not line and current_sentence:
                # If current_text is empty (e.g., no "# text =" line), build it manually
                if not current_text:
                    tokens = [tok[1] for tok in current_sentence if re.match(r'^\d+$', tok[0])]
                    current_text = " ".join(tokens)

                sentences.append((current_text, current_sentence))
                current_sentence = []
                current_text = ""  # Reset for next sentence

    # Handle final sentence if file doesn't end with a blank line
    if current_sentence:
        if not current_text:
            tokens = [tok[1] for tok in current_sentence if re.match(r'^\d+$', tok[0])]
            current_text = " ".join(tokens)

        sentences.append((current_text, current_sentence))

    return sentences



def clean_text(text):
    """Helper function to clean the sentences before and after processing."""
    text = re.sub(r'"', '', text)  # Removes citation marks where whitespace cannot be handled properly  
    text = re.sub(r"'", "", text)
    text = re.sub(r'\s+([?.!",:;)])', r'\1', text)  # Removes space before punctuation
    text = re.sub(r'\(\s+', '(', text)             # Fixes spacing after '(' 
    text = re.sub(r"\s+", " ", text)               # Normalizes whitespace    
    
    return text.strip()


def process_conllu_to_csv(input_file, output_file, create_mp, generate, n_pairs=None):
    """
    Processes the CoNLL-U file and writes grammatical and ungrammatical sentences to a CSV file, removing duplicates.
    
    Args:
        input_file (conllu): A conllu file in which to search for linguistic structures
        output_file (csv): A file to which the minimal pairs are written
        create_mp: The function that identifies the target structure and generates the ungrammatical sentence
        generate (True or False): If True, minimal pairs will be written to file
        n_pairs (None or int): Specifies the number of desired pairs per linguistic structure set. If None, all pairs matched will be returned.

    Returns:
        Writes minimal pairs to a csv file.
    """
    sentences = read_conllu(input_file)
    seen_sentences = set()
    pair_count = 0

    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["grammatical", "ungrammatical"])

        for text, sentence_data in sentences:
            if n_pairs is not None and pair_count >= n_pairs:
                break  # Stop once reached the desired number of pairs
            ungrammatical_text = create_mp(sentence_data, generate)

            if ungrammatical_text:
                text = clean_text(text)
                ungrammatical_text = clean_text(ungrammatical_text)
                sentence_pair = (text, ungrammatical_text)  # Creates a tuple to check uniqueness in case of duplicates in source data

                if sentence_pair not in seen_sentences and text != ungrammatical_text:
                    seen_sentences.add(sentence_pair)
                    writer.writerow([text, ungrammatical_text]) 
                    pair_count += 1 

if __name__ == "__main__":
    
    input_data = "dataset.conllu"  # Input must be in CoNLL-U format

    from parse_conllu_svo import create_svo_mp
    from parse_conllu_plural import create_plural_mp
    from parse_conllu_tense import create_tense_mp
    from parse_conllu_attr import create_attr_mp
    from parse_conllu_pred import create_pred_a_mp, create_pred_b_mp
    from parse_conllu_inv import create_inv_mp
    from parse_conllu_negv import create_negv_mp
    from parse_conllu_inq import create_inq_mp

    SVO = process_conllu_to_csv(input_data, "SVO.csv", create_svo_mp, generate=True, n_pairs=50)
    PLUR = process_conllu_to_csv(input_data, "PLUR.csv", create_plural_mp, generate=True, n_pairs=50)
    TENSE = process_conllu_to_csv(input_data, "TENSE.csv", create_tense_mp, generate=True, n_pairs=50)
    ATTR = process_conllu_to_csv(input_data, "ATTR.csv", create_attr_mp, generate=True, n_pairs=50)
    PRED_a = process_conllu_to_csv(input_data, "PRED_a.csv", create_pred_a_mp, generate=True, n_pairs=50)
    PRED_b = process_conllu_to_csv(input_data, "PRED_b.csv", create_pred_b_mp, generate=True, n_pairs=50)
    INV = process_conllu_to_csv(input_data, "INV.csv", create_inv_mp, generate=True, n_pairs=50)
    NEGV = process_conllu_to_csv(input_data, "NEGV.csv", create_negv_mp, generate=True, n_pairs=50)
    INQ = process_conllu_to_csv(input_data, "INQ.csv", create_inq_mp, generate=True, n_pairs=50)
