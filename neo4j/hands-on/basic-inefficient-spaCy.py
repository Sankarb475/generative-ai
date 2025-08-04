import spacy

# Load English model
nlp = spacy.load("en_core_web_md")

# Input unstructured text
text = "Elon Musk founded SpaceX in 2002 The company is based in California - Musk also co-founded Tesla."

# Process the text
doc = nlp(text)

# Extract triplets
triplets = []

for sent in doc.sents:
    #print(sent)
    subject = ''
    object_ = ''
    verb = ''

    for token in sent:
        # Get subject
        if "subj" in token.dep_:
            subject = token.text

        # Get object
        if "obj" in token.dep_:
            object_ = token.text

        # Get verb
        if token.pos_ == "VERB":
            verb = token.lemma_  # use lemma to normalize (e.g., "founded" -> "found")

    if subject and verb and object_:
        triplets.append((subject, verb, object_))

# Print extracted triplets
for t in triplets:
    print(t)
