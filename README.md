# RoamNER
_Testing an implementation of Named-Entity Recognition integration for Roam Research_


![Sample output in Roam Research](https://github.com/hmprt/RoamNER/blob/master/img/newFrontPage.png)

**Check out the public RoamNER_V1 knowledge graph [here](https://roamresearch.com/#/app/roamNER_test)**



## Why?

Inpsired by a [tweet](https://twitter.com/balajis/status/1307140423937265664?s=20) by [Balaji Srinivasan](https://balajis.com/), I decided to try and make a working implementation of Named Entity Recognition in Roam.

The upsides of this are enormous; being able to instantly cross-reference ideas from any written content is huge for researchers, students and hackers of all stripes and I'm not even really sure of where the limits on this sort of thing could be, especially with more work - see [this](https://twitter.com/RoamFm/status/1307009419524202496?s=20) thread for a collection of great ideas. Moreover, I also just fancied a challenge and wanted to see what I could hack together in a day.

## Implementation and user guide

Everything is written in Python, and the only dependency is [spacy](https://spacy.io/):  
`pip3 install spacy`

Everything else is plug 'n' play, with the user specifying a .txt file, the name of the text and the author.  
```
$ python3 roamNER_V1.py
> Please input a .txt file to load: ThePrince.txt
> Please input the document's name: The Prince
> Please input the title's author: Niccolo Machiavelli
```
RoamNER_V1 uses **spacy** for Named-Entity Recognition, identifies likely pages, and reformats the .txt input into a Roam-readable markdown file which the user can upload to a graph.

## Bugs and limitations

While V1 works surprisingly well, there are a few issues:
- The user is limited in the size of the markdown file that they can upload to Roam; if the file is too large, Roam won't accept it and will just generate a blank page with the title of the document. This is an issue on Roam's end, and there's not much I can do besides figure out the hard size limit for future versions.
- Spacy's NER is good, but not great - nouns can get miscategorized and the data requires a fair amount of cleaning before it can be written to markdown. I think a lot of this is my being unfamiliar with the library (I only discovered it today!)
- The count feature under tags is currently broken as it takes into account tags that I have discarded when formatting the data - this is an easy fix, but can wait until V2 because I need to eat.

