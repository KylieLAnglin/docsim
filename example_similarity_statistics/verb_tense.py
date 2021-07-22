import nltk

# nltk.download('averaged_perceptron_tagger')

# %%
def determine_tense_input(sentence):
    text = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(text)

    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len(
        [word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]]
    )
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
    return tense


determine_tense_input(
    "For example, I noticed in your last simulation that you were hesitant to correct Ethan’s behavior. Next time Ethan makes noise or hums I want you to immediately redirect the behavior. For example, you could say: Ethan, voice off, hands together."
)


# Example Transcript 1
example1 = "So, we want to move that specific telling them what you want them to stop to right when you notice it and call their name. So, specifically when – I think it was Ethan got his phone out, and you told him to put it away, and he put it away. And then you were able to establish two rules at that time.  But before, you hadn’t gotten any rules really, right?  So, being specific to the actual student of what you want them to stop is really helpful."

script1 = "To make your next simulation even stronger, I want you to focus on making your redirections more specific so that students know exactly what you want them to stop doing or start doing. This helps us make sure that students aren’t confused. For example, I noticed in your last simulation that you told Ethan to pay attention. The words pay attention can be confusing because it can mean different things for different people and you can’t see if a student is following those directions. Next time Ethan has a side conversation I want you to tell them exactly what you want to see. For example, you could say: Ethan, voice off, hands together."


script2 = "To make your next simulation even stronger, I want you to focus on making your redirections more timely so that you can address the misbehavior right away. This prevents the misbehaviors from distracting other students and taking away from class time. For example, I noticed in your last simulation that you were hesitant to correct Ethan’s behavior. Next time Ethan makes noise or hums I want you to immediately redirect the behavior. For example, you could say: Ethan, voice off, hands together."


determine_tense_input(script1)
determine_tense_input(example1)


# %%
