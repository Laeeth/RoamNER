import spacy
from collections import Counter
from dateutil.parser import parse

## Can download different models for different languages
import en_core_web_sm
nlp = en_core_web_sm.load()

data = None
# Debugging:
# import pdb
# data = "ThePrince.txt"
# titleName = "The Prince"
# titleAuthor = "Niccolo Machiavelli"

## Taking user input
if data == None:
    data = input("Please input a .txt file to load: ")
    titleName = input("Please input the document's name: ")
    titleAuthor = input("Please input the title's author: ")

## Accessing the data file
with open(data, "r") as file:
    data = file.read().replace("\n", " ")

## Running the raw data through spacy
doc = nlp(data)

## Now let's grab what we need
tags = []
for tag in doc.ents:

    ## First, let's filter out tags we don't want - ordinals, verbs etc
    if (tag.label_ not in {"PERSON", "DATE", "FAC", "LOC", "EVENT", "ORG", "GPE"}):
        continue

    else:
        ## Now, let's clean up the tags we have, starting with dates - they need to be
        ## discrete and not semantic - i.e, 1984 instead of "Someday"
        if (tag.label_ == "DATE"):
            try:
                parse(tag.text)
                tags.append(tag)
                continue
            except:
                continue

        ## This is pretty quick and dirty, but we can check the rest of the tags
        ## and see if they're proper nouns. This should filter out most of the shite
        ## but I'll definitely figure out something better further down the line
        if (tag.text != tag.text.lower() and tag.text != tag.text.upper() and "_" not in tag.text):
            tags.append(tag)
            continue

        else:
            continue

## Creating a header dict - we use this object to note our
## most common tags by category in a Roam Page header
header = Counter([tag.label_ for tag in tags])

## I'm manually reorganising tags because the default spacy ones aren't formatted nicely. This would
## be much easier if the fields in spacy weren't immutable...
header["People"] = {"Count" : header["PERSON"], "lookup" : "PERSON"}
del header["PERSON"]

header["Organisations"] =  {"Count" : header["ORG"], "lookup" : "ORG"}
del header["ORG"]

header["Geopolicial Entities"] = {"Count" : header["GPE"], "lookup" : "GPE"}
del header["GPE"]

header["Locations"] = {"Count" : header["LOC"], "lookup" : "LOC"}
del header["LOC"]

header["Dates"] =  {"Count" : header["DATE"], "lookup" : "DATE"}
del header["DATE"]

header["Structures"] = {"Count" : header["FAC"], "lookup" : "FAC"}
del header["FAC"]

header["Events"] = {"Count" : header["EVENT"], "lookup" : "EVENT"}
del header["EVENT"]



## Finally, let's convert our raw text into markdown with Roam formatting

## Formatting the title
with open (titleName+".md", "w") as out:
    out.write("[["+titleName+"]]" + " by " + "[["+titleAuthor+"]]" + '\n')

## Writing tags to keep organised and for quick reference
    out.write("***Tags:**\n")
    for category in header:
        out.write("    -" + "__"+category+"__" + ": " + str(header[category]["Count"]) + "\n")

        ## Populating our list of referenced pages
        references = []
        for tag in tags:
            if (tag.label_ == header[category]["lookup"]):
                #Lets avoid double entries too while we're at it
                if(tag.text in references):
                    continue

                references.append(tag.text)

        ## Format each item as a ROAM pages. I'm sure there's a cleaner way to do this
        newReferences = []
        for word in references:
            word = "[["+word+"]]"
            newReferences.append(word)

        ## Finally, convert them to a comma-delimited string
        references = ", ".join(newReferences)
        out.write("        -" + references + "\n")

    ## Now we can write the body of the text, with Roam pages. We'll split each
    ## entry onto a seperate line so it will play well with Roam. My method for
    ## doing this is pretty simple, and I haven't handled edge cases like
    ## "Mr. X" or "h.mprt" yet.

    # First, we'll split things into sentences
    formattedText = []
    rawText = data.split(". ")
    rawTags = [x.text for x in tags]

    # Next, let's generate our Roam pages
    for sentence in rawText:
        formattedSentence = []
        for word in sentence.split(" "):
            if word in rawTags:
                formattedSentence.append("[["+word+"]]")
            else:
                formattedSentence.append(word)
        formattedText.append(" ".join(formattedSentence))

    ## And finally, write to file
    out.write("***" + titleName + "** (__raw text__)" + "\n")
    for line in formattedText:
        out.write("    -" + line)
        out.write("    "+"\n")
