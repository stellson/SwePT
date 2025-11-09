# SwePT: a Swedish Processability Theory Minimal Pair Dataset

SwePT is a minimal pair dataset created for the purpose of evaluating the development of grammatical knowledge in LLMs, specifically with respect to the stages of grammar acquisition as theorized in Processability Theory [^1]. SwePT consists of nine separate datasets containing 8442 minimal pairs in total, targeting Swedish syntactic and morphological structures that represent four stages of the Swedish Processability Theory developmental hierarchy. This repository contains the minimal pair dataset [SwePT](https://github.com/stellson/SwePT/tree/main/SwePT) as well as the [scripts](https://github.com/stellson/SwePT/tree/main/generate_pairs) used to identify the grammatical structures and create the minimal pairs. 

## Repository Content

- [SwePT](https://github.com/stellson/SwePT/tree/main/SwePT)
    - [ATTR.csv](https://github.com/stellson/SwePT/blob/main/SwePT/ATTR.csv)
    - [INQ.csv](https://github.com/stellson/SwePT/blob/main/SwePT/INQ.csv)
    - [INV.csv](https://github.com/stellson/SwePT/blob/main/SwePT/INV.csv)
    - [NEGV.csv](https://github.com/stellson/SwePT/blob/main/SwePT/NEGV.csv)
    - [PLUR.csv](https://github.com/stellson/SwePT/blob/main/SwePT/PLUR.csv)
    - [PRED_a.csv](https://github.com/stellson/SwePT/blob/main/SwePT/PRED_a.csv)
    - [PRED_b.csv](https://github.com/stellson/SwePT/blob/main/SwePT/PRED_b.csv)
    - [SVO.csv](https://github.com/stellson/SwePT/blob/main/SwePT/SVO.csv)
    - [TENSE.csv](https://github.com/stellson/SwePT/blob/main/SwePT/TENSE.csv)
 - [generate_pairs](https://github.com/stellson/SwePT/tree/main/generate_pairs)
    - [generate_minimal_pairs.py](https://github.com/stellson/SwePT/blob/main/generate_pairs/generate_minimal_pairs.py)
    - [parse_conllu_attr.py](https://github.com/stellson/SwePT/blob/main/generate_pairs/parse_conllu_attr.py)
    - [parse_conllu_inq.py](https://github.com/stellson/SwePT/blob/main/generate_pairs/parse_conllu_inq.py)
    - [parse_conllu_inv.py](https://github.com/stellson/SwePT/blob/main/generate_pairs/parse_conllu_inv.py)
    - [parse_conllu_negv.py](https://github.com/stellson/SwePT/blob/main/generate_pairs/parse_conllu_negv.py)
    - [parse_conllu_plur.py](https://github.com/stellson/SwePT/blob/main/generate_pairs/parse_conllu_plur.py)
    - [parse_conllu_pred_a.py](https://github.com/stellson/SwePT/blob/main/generate_pairs/parse_conllu_pred_a.py)
    - [parse_conllu_pred_b.py](https://github.com/stellson/SwePT/blob/main/generate_pairs/parse_conllu_pred_b.py)
    - [parse_conllu_svo.py](https://github.com/stellson/SwePT/blob/main/generate_pairs/parse_conllu_svo.py)
    - [parse_conllu_tense.py](https://github.com/stellson/SwePT/blob/main/generate_pairs/parse_conllu_tense.py)

## Minimal Pair Data

The minimal pairs of each subset are stored in a csv file with two columns, containing a grammatical sentence in the first column and its ungrammatical counterpart in the second column. 

### Morphology:
- Plural marking on nouns (PLUR, 2nd stage), 
- Tense inflection of verbs (TENSE, 2nd stage)
- Attributive agreement (ATTR, 3rd stage)
- Predicative agreement (PRED_a, 4th stage)
- Predicative agreement with attractors (PRED_b, 4th stage)

### Syntax:
- Canonical word order (SVO, 2nd stage)
- Inversion after topicalization (INV, 4th stage)
- Preverbal negation in subclauses (NEGV, 5th stage) 
- Non-inversion in indirect questions (INQ, 5th stage) 

The table below displays selected examples of minimal pairs (a grammatical sentence and its ungrammatical equivalent) from SwePT, including their translations which are not present in the csv files.

|Stage| Structure | n of pairs|Grammatical | Ungrammatical | 
|---|----------|-------|----------|---|
|  5 |NEGV| 303 | ✅ Men det är viktigt, att förlusterna [inte] [blir] onödigt stora. (*But it is important that the losses are not unnecessarily large.*)|❌ Men det är viktigt, att förlusterna [blir] [inte] onödigt stora.|
|  5 |INQ|94| ✅ Jag har lust att fråga honom varför [den] inte [trycktes]. (*I want to ask him why it wasn't printed.*)|❌ Jag har lust att fråga honom varför [trycktes] [den] inte. |
|  4 |INV| 2581 |✅ Ovanpå ett skåp i hörnet [satt] [Dobby] hopkrupen. (*On top of a cupboard in the corner crouched Dobby.*)  |❌ Ovanpå ett skåp i hörnet [Dobby] [satt] hopkrupen.  |
|  4 |PRED_a|226 | ✅ De flesta u-länder har varit [koloniserade] (*Most developing countries have been colonized*)| ❌ De flesta u-länder har varit [koloniserad]  |
|  4 |PRED_b| 27 |✅ Resultaten av uppväxten i denna miljö är rätt så [uppenbara]. (*The results of growing up in this environment are quite obvious.*)|❌  Resultaten av uppväxten i denna miljö är rätt så [uppenbar].  |
|  3 |ATTR| 213 | ✅ Han har inget [civiliserat] ansikte. (*He does not have a civilized face.*)|❌ Han har inget [civiliserad] ansikte.   |
|  2 |TENSE|2000| ✅Jag [är] min fars dotter. (*I am my father's daughter.*)|❌  Jag [vara] min fars dotter.   |
|  2 |PLUR|479| ✅ Måste du försöka göra åtta [saker] samtidigt? (*Must you try and do eight things at once?* ) | ❌ Måste du försöka göra åtta [sak] samtidigt?   |
|  2 |SVO|  2519 |✅ Hon [hade] [en dämpad, tonlös röst] och bröt inte så kraftigt som mannen. (*She had a soft, dry voice and her accent was slighter than her husband's.*) |❌ Hon [en dämpad, tonlös röst] [hade] och bröt inte så kraftigt som mannen |

## Dataset Creation

The grammatical sentences of each minimal pair were extracted from the Swedish Talbanken and LinES treebanks from Universal Dependencies corpora. The target linguistic structures were identified through a processing pipeline consisting of [nine rule-based Python scripts](https://github.com/stellson/SwePT/tree/main/generate_pairs) targeting each PT structure, respectively. The scripts were written by performing several manual iterations of systematically relaxing the heuristics and reviewing the output.

The pipeline performs three main consecutive steps: 
1. identifying and extracting sentences containing the PT structures from the source CoNLL-U files through a dependency tree search (also used for labeling the training data),
2. duplicating the sentences to form the minimal pairs,
3. altering the duplicates into ungrammatical sentences with respect to their target structures.

To form the minimal pairs of the syntactic structures (SVO, INV, INQ and NEGV), relevant grammatical constituents and arguments were identified and had their positions switched with respect to the target structure. The alteration of the morphological structures (PLUR, TENSE, ATTR and PRED_a) was performed by converting the conjugated target structures into their neutral form (lemma). The alteration process for the PRED_b minimal pairs was performed manually in order to minimize errors, due to the small amount of extracted sentences and the complexity of the alteration task.

The whole process is described in more detail in [my dissertation](https://www.diva-portal.org/smash/get/diva2:1975439/FULLTEXT01.pdf).


[^1]: Pienemann, M. (1998). Language processing and second language development: Processability theory (Vol. 15). John Benjamins Publishing.
[^2]: Taktasheva, E., Bazhukov, M., Koncha, K., Fenogenova, A., Artemova, E., & Mikhailov, V. (2024). Rublimp: Russian benchmark of linguistic minimal pairs. arXiv preprint arXiv:2406.19232.
