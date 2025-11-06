# SwePT: a Swedish Processability Theory Minimal Pair Dataset

SwePT is a minimal pair dataset created for the purpose of evaluating the development of grammatical knowledge in LLMs. SwePT consists of 9 subsets, amounting to 8442 minimal pairs in total. Each subset contains minimal pairs with respect to grammatical features representing four stages of the Swedish Processability Theory developmental hierarchy, as follows:
- SVO (canonical word order SVO, 2nd stage), 
- PLUR (plural, 2nd stage), 
- TENSE (tense, 2nd stage)
- ATTR (attributive agreement, 3rd stage)
- PRED_a (predicative agreement, 4th stage)
- PRED_b (predicative agreement with attractors, 4th
stage)
- INV (inversion after topicalization, 4th stage)
- NEGV (preverbal negation, 5th
stage) 
- INQ (Non-inversion in indirect questions, 5th stage). 

The grammatical sentences of each minimal pair were extracted from the Swedish
Talbanken and LinES treebanks from UD (De Marneffe et al., 2021). LinES contains 4,564
annotated trees and 79,812 tokens worth of data translated from English, including
literary works, online help manuals and the Swedish part of the Europarl corpus.
Talbanken consists of roughly 6,000 annotated sentences and 95,000 tokens from a
variety of informative text sources including newspaper articles and textbooks. 

The table shows selected examples of minimal pairs (a grammatical sentence and its ungrammatical equivalent) from SwePT, including their translations.

| Structure | Pairs | Example |
| ----------|-------|----------|
| 5 NEGV| 303| Men det är viktigt, att förlusterna [inte] [blir] onödigt stora. (But it is important that the losses are not unnecessarily large.)|
|   |   | Men det är viktigt, att förlusterna [blir] [inte] onödigt stora.|
| 5 INQ| 94|Jag har lust att fråga honom varför [den] inte [trycktes].(I want to ask him why it wasn't printed.)|
| | |Jag har lust att fråga honom varför [trycktes] [den] inte.|
| 4 INV| 2581| Ovanpå ett skåp i hörnet [satt] [Dobby] hopkrupen. (On top of a cupboard in the corner crouched Dobby. ) |
|   |   | Ovanpå ett skåp i hörnet [Dobby] [satt] hopkrupen.  |
| 4 PRED_a| 226| De flesta u-länder har varit [koloniserade] (Most developing countries have been colonized)|
|   |   | De flesta u-länder har varit [koloniserad] | 
|  4 PRED_b| 27|Resultaten av uppväxten i denna miljö är rätt så [uppenbara]. (The results of growing up in this environment are quite obvious.) |
|  |  |Resultaten av uppväxten i denna miljö är rätt så [uppenbar]. |
| 3 ATTR| 213| Han har inget [civiliserat] ansikte. (He does not have a civilized face. )  |
|   |   | Han har inget [civiliserad] ansikte.  |
|  2 TENSE| 2000|Jag [är] min fars dotter. (I am my father's daughter.) |
|  |  |Jag [vara] min fars dotter.  |
|  2 PLUR| 479|Måste du försöka göra åtta [saker] samtidigt? (Must you try and do eight things at once? ) |
|  |  |Måste du försöka göra åtta [sak] samtidigt?  |
|  2 SVO| 2519|Hon [hade] [en dämpad, tonlös röst] och bröt inte så kraftigt som mannen. (She had a soft, dry voice and her accent was slighter than her husband's. )  |
|  |  |Hon [en dämpad, tonlös röst] [hade] och bröt inte så kraftigt som mannen.  |

