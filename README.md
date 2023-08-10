# Wordle Random Api
 A random word generator API for wordle-like games

# Introduction:
Wordle Random Api is an api that is able to generate a random word or a set of random words according to your criteria. Currently supported language is English.
The api uses a dataset of more than **350,000** English words, of which **3000** words were marked as common words for daily use.

### Usage
The app can be used to generate random words or to verify if a given word is an english word.

Use cases:
- Wordle Game variations
- Word puzzles
- NLP applications

and more.

## Generating random words.
To generate a random word, make a `GET` request to the following endpoint:

`http://127.0.0.1:8000/v1/random`

You'll receive a Json response with a random word to use:

```json
[{"word": "ackton"}]
```

you can also pass some parameters to filter the generated words, for example:

`http://127.0.0.1:8000/v1/random?amount=3&len=5
`
```json
[
    {"word": "tinny"},
    {"word": "tings"},
    {"word": "fools"}
]
```

### Parameters
#### Controlling response count and shape

| Parameter | Function                                                                                                   | Accepted Values |
|-----------|------------------------------------------------------------------------------------------------------------|-----------------|
| amount    | returns a specific amount of words, default is 1, max is 25 per api call.                                  | 1-25            |
| show_info | returns information regarding every returned word such as length, type, and if it's a common words or not. | 0, 1            |

When `show_info` is set to 1 and `amount` is set to 2 you're expecting a response like this:
```json
[{"word": "desert", "length": 6, "type": "NN", "is_common": true}, {"word": "soup", "length": 4, "type": "NN", "is_common": true}]
```

#### Filtering words by length

| Parameter | Function                                                                 | Accepted Values |
|-----------|--------------------------------------------------------------------------|-----------------|
| len       | Returns words only of specified length                                   | Any number      |
| min_len   | Return words that has minimum length of the provided number              | Any number      |
| max_len   | Return words that has minimum length of the provided number              | Any number      |

#### Filtering words by common use

Among all the words in the dataset, a little above 3000 words were marked as common.

| Parameter     | Function                     | Accepted Values |
|---------------|------------------------------|-----------------|
| common_only   | Returns common words only.   | 0 or 1          |
| uncommon_only | Returns uncommon words only. | 0 or 1          |

#### Filtering words by type

Among all the words in the dataset, a little above 3000 words were marked as common.

| Parameter | Function                                    | Accepted Values |
|-----------|---------------------------------------------|-----------------|
| type      | Returns words with the only mentioned type. | word type       |

Available types are:
- CC	coordinating conjunction
- CD	cardinal digit
- DT	determiner
- EX	existential there
- FW	foreign word
- IN	preposition/subordinating conjunction
- JJ	adjective (large)
- JJR	adjective, comparative (larger)
- JJS	adjective, superlative (largest)
- LS	list item marker
- MD	modal (could, will)
- NN	noun, singular
- NNS	noun plural
- NNP	proper noun, singular
- NNPS	proper noun, plural
- PDT	predeterminer
- POS	possessive ending (parent\ 's)
- PRP	personal pronoun (hers, herself, him,himself)
- PRP dollar-sign	possessive pronoun (her, his, mine, my, our )
- RB	adverb (occasionally, swiftly)
- RBR	adverb, comparative (greater)
- RBS	adverb, superlative (biggest)
- RP	particle (about)
- SYM	symbol
- TO	infinite marker (to)
- UH	interjection (goodbye)
- VB	verb (ask)
- VBG	verb gerund (judging)
- VBD	verb past tense (pleaded)
- VBN	verb past participle (reunified)
- VBP	verb, present tense not 3rd person singular(wrap)
- VBZ	verb, present tense with 3rd person singular (bases)
- WDT	wh-determiner (that, what)
- WP	wh- pronoun (who)
- WP dollar-sign	possessive wh-pronoun
- WRB	wh- adverb (how)

#### Filtering words by character manipulation

Among all the words in the dataset, a little above 3000 words were marked as common.

| Parameter     | Function                                                       | Accepted Values |
|---------------|----------------------------------------------------------------|-----------------|
| contains_any  | Returns words with any of the provided letters.                | [a-z]           |
| contains_all  | Returns words that contain all of the provided letters         | [a-z]           |
| contains_only | Returns words that only contain the provided letters           | [a-z]           |
| contains_none | Returns words that doesn't contain any of the provided letters | [a-z]           |

Notes:
- contains_only and contains_none cannot be used together
- provide the letters concatenated to each other (as if they were one word)

Examples:

`http://127.0.0.1:8000/v1/random?amount=3&common_only=1&contains_only=acts`

Response:
```json
[{"word": "cat"}, {"word": "at"}, {"word": "as"}]
```
`http://127.0.0.1:8000/v1/random?amount=3&common_only=1&contains_none=abc`

Response:
```json
[{"word": "refuse"}, {"word": "soul"}, {"word": "student"}]
```

#### Filtering words using a pattern

Among all the words in the dataset, a little above 3000 words were marked as common.

| Parameter | Function                                                                                                                  | Accepted Values |
|-----------|---------------------------------------------------------------------------------------------------------------------------|-----------------|
| pattern   | Returns words that apply to a pattern, specify the shape of the word you want to receive. An astrect (*) means any letter | [a-z] and *     |

Examples:
`http://127.0.0.1:8000/v1/random?amount=5&pattern=sh**t`

Response:
```json
[{"word": "shott"}, {"word": "shoot"}, {"word": "shoat"}, {"word": "sheat"}, {"word": "shaft"}]
```

#### Filtering words using regex

If you need more complex task, then provide your own regex


| Parameter | Function                                     | Accepted Values |
|-----------|----------------------------------------------|-----------------|
| reg       | Returns words that match the provided regex. | a valid regex   |

Examples:
`http://127.0.0.1:8000/v1/random?amount=5&reg=^(?=[a-z]*i)(?![a-z]*[outyase])[a-z]{5}$`

Response:
```json
[{"word": "brick"}, {"word": "blind"}, {"word": "climb"}, {"word": "drink"}, {"word": "civil"}]
```


## Check if a given word is a valid english word.

To check if a given word is valid in english, make a GET request to the following endpoint:

`http://127.0.0.1:8000/v1/is_a_word/<YOUR_WORD>
`

Examples:

`http://127.0.0.1:8000/v1/is_a_word/speed`
Response:
`true`

`http://127.0.0.1:8000/v1/is_a_word/speeeeeeed`
Response:
`false`


| Parameter | Function                                                | Accepted Values |
|-----------|---------------------------------------------------------|-----------------|
| show_info | Show information regarding the given word, default is 0 | 0 or 1          |

Examples:
`http://127.0.0.1:8000/v1/is_a_word/speed?show_info=1`

Response:
```json
{
    "word": "speed",
    "length": 5,
    "type": "NN",
    "is_common": true
}
```

