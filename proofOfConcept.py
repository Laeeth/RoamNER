import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()
import pdb
from dateutil.parser import parse

with open("ThePrince.txt", "r") as file:
    rawText = file.read()

doc = nlp(rawText)


tags = []

## Let's filter our data, and make some handy Roam pages
for tag in doc.ents:
    if (tag.label_ in {"PERSON", "DATE", "FAC", "LOC", "EVENT", "WORK_OF_ART", "ORG", "GPE"}):

        ## Check to only get numerical dates:
        if (tag.label_ == "DATE"):
            try:
                parse(tag.text)
                tags.append(tag.text)
                continue

            except:
                print("Not a date: " + tag.text)
                continue

        ## Checking that tagged PERSONs are in camel case - a
        ## quick and dirty way of filtering out most other phrases
        ## that sneak through
        if (tag.label_ == "PERSON"):

            ## Credit: https://stackoverflow.com/questions/10182664/check-for-camel-case-in-python#:~:text=You%20could%20check%20if%20a%20string%20has%20both%20upper%20and%20lowercase.&text=Anchor%20the%20expression%20with%20%5E%20and%20%24%20or%20%5Cz%20if%20required.&text=Use%20a%20library%20like%20inflection,t%20change%2C%20it's%20camel%20case.
            if (tag.text != tag.text.lower() and tag.text != tag.text.upper() and "_" not in tag.text):

                ## Removing nasty illegal characters - I'm sure there are more, but
                ## these popped up most often in The Prince
                for char in ["(", ")", "\\", "+"]:
                    tags.append(tag.text.replace(char, ""))
                continue

            else:
                print("Not a name: " + tag.text)
                continue

        ## Can filter locations, FAC etc in same way. In future versions
        ## I'll just write a function. For now, I want this to run - clock is ticking!
        if (tag.label_ == "FAC"):
            if (tag.text != tag.text.lower() and tag.text != tag.text.upper() and "_" not in tag.text):

                ## Removing nasty illegal characters - I'm sure there are more, but
                ## these popped up most often in The Prince
                for char in ["(", ")", "\\", "+"]:
                    tags.append(tag.text.replace(char, ""))
                continue

            else:
                print("Not a building: " + tag.text)
                continue
        if (tag.label_ == "LOC"):
            if (tag.text != tag.text.lower() and tag.text != tag.text.upper() and "_" not in tag.text):

                ## Removing nasty illegal characters - I'm sure there are more, but
                ## these popped up most often in The Prince
                for char in ["(", ")", "\\", "+"]:
                    tags.append(tag.text.replace(char, ""))
                continue

            else:
                print("Not a location: " + tag.text)
                continue
        if (tag.label_ == "WORK_OF_ART"):
            if (tag.text != tag.text.lower() and tag.text != tag.text.upper() and "_" not in tag.text):

                ## Removing nasty illegal characters - I'm sure there are more, but
                ## these popped up most often in The Prince
                for char in ["(", ")", "\\", "+"]:
                    tags.append(tag.text.replace(char, ""))
                continue

            else:
                print("Not a work of art: " + tag.text)
                continue
        if (tag.label_ == "EVENT"):
            if (tag.text != tag.text.lower() and tag.text != tag.text.upper() and "_" not in tag.text):

                ## Removing nasty illegal characters - I'm sure there are more, but
                ## these popped up most often in The Prince
                for char in ["(", ")", "\\", "+"]:
                    tags.append(tag.text.replace(char, ""))
                continue

            else:
                print("Not an event: " + tag.text)
                continue
        if (tag.label_ == "ORG"):
            if (tag.text != tag.text.lower() and tag.text != tag.text.upper() and "_" not in tag.text):

                ## Removing nasty illegal characters - I'm sure there are more, but
                ## these popped up most often in The Prince
                for char in ["(", ")", "\\", "+"]:
                    tags.append(tag.text.replace(char, ""))
                continue

            else:
                print("Not an organisation: " + tag.text)
                continue
        if (tag.label_ == "GPE"):
            if (tag.text != tag.text.lower() and tag.text != tag.text.upper() and "_" not in tag.text):

                ## Removing nasty illegal characters - I'm sure there are more, but
                ## these popped up most often in The Prince
                for char in ["(", ")", "\\", "+"]:
                    tags.append(tag.text.replace(char, ""))
                continue

            else:
                print("Not a GPE: " + tag.text)
                continue

## Now, we make all of our tags ROAM pages. This is in O(n), which sucks, and
## there's definitely a faster way to do this using spacy. However, that's a
## future issue

roamText = []
for word in rawText.split():
    if word in tags:
        roamText.append("[[" + word + "]]")
    else:
        roamText.append(word)

roamText = " ".join(roamText).split(". ")

labels = [x.label_ for x in doc.ents]
Counter(labels)
pdb.set_trace()

with open ("roamOut.md", "w") as out:
    for line in roamText:
        out.write(line)
        out.write("\n")
