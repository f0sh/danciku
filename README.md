# German Vocabulary Lists

Import pre-made vocabulary sets for learning languages with different learning tools like **Anki**, **TOFU Learn**, and others.

## Languages

### Chinese

For the Chinese language currently the following learning books are supported:

  * New Practical Chinese Reader (NPCR)
  * Discover China (DC)

File structure is:

    # abbr: c_s: simplified character, c_t: traditional character, py: numbered pinyin
    charlist.txt - contains a list of characters with a tag for the unit [Format: char \t unit]
    vocabulary_de.csv - contains the vocabulary set [Format: c_s \t c_t \t py \t meaning \t unit]

The vocabulary list should fulfill the following quality requirements, to not cause import problems to learning software:

  * front (character) and back (meaning) field must be unique
  * for the front only chinese characters can be used, otherwise it can cause render problems
  * all fields need to be filled

Output:

  * **Anki** .apkg and Ankiweb deck, enriched with data from [Chinese Support Redux](https://ankiweb.net/shared/info/1128979221)
  * **TOFU Learn**
  * **Memrise** *(not yet supported)*
