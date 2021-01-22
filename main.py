import pandas as pd
import streamlit as st
import gensim.downloader as api
import itertools
import time



def generateClues(model, words_cleaned):
    combinations = []
    stuff = words_cleaned
    for i in range(1, len(words_cleaned) + 1):
        for subset in itertools.combinations(stuff, i):
            if (len(subset) == 1):
                s = []
                s.append(subset[0])
                combinations.append(s)
            else:
                combinations.append(subset)
    list_of_masters = []

    for i in combinations:
        master = []
        master.append(i)
        test = model.most_similar(
            positive=i,
            restrict_vocab=75000,
            topn=10
        )
        results = []
        for x in test:
            if ('_' not in x[0]):
                if (x[0].lower() not in i):
                    status = True
                    for word in i:
                        if word.lower() in x[0]:
                            status = False
                        if x[0] in word.lower():
                            status = False
                        if x[0] in stuff:
                            status = False
                    if (status == True):
                        results.append(x)

        master.append(results[0][0])
        master.append(results[0][1])
        list_of_masters.append(master)

    list_of_masters.sort(key=lambda tup: tup[2], reverse=True)
    return list_of_masters


def printClues(lst, num_cards):
    counter = 0
    text = ""
    st.write("Your best " + str(num_cards) + " card clues (a score above 0.6 is very good) :\n")
    st.markdown("---")
    for i in lst:
        if counter < 10:
            if len(i[0]) == num_cards:
                if i[2] > 0.2:  # change if computer getting wonky
                    st.markdown("**Similarity score:** " + str(round(i[2], 3)))
                    st.markdown("**Clue: **" + str(i[1]))
                    list_as_string = ""
                    for card in i[0]:
                        list_as_string = list_as_string + card + ", "
                    list_as_string = list_as_string[:len(list_as_string) - 2]
                    st.markdown("**Cards Targeted: **" + list_as_string)
                    st.markdown("---")
                    counter = counter + 1

@st.cache(allow_output_mutation=True)
def load_model():
    with st.spinner('Downloading model... please hold... (sry this can take like 2-5 minutes)'):
        model = api.load('word2vec-google-news-300')
    return model


def main():
    st.markdown('<style>h1{font-family: "Rockwell";text-align: center;}</style>', unsafe_allow_html=True)
    st.title('CODENAMES BOT')
    st.markdown("Welcome to Codenames Bot! Once the model has finished downloading, simply input your remaining cards into the machine, select the number of cards you'd like to target, and push the button to generate potential clues!")
    #st.video('https://www.youtube.com/watch?v=z6-gBN2xp74', format='video/mp4', start_time=0)
    model = load_model()
    st.success('Done!')
    
    word_1 = st.text_input("Word 1")
    word_2 = st.text_input("Word 2")
    word_3 = st.text_input("Word 3")
    word_4 = st.text_input("Word 4")
    word_5 = st.text_input("Word 5")
    word_6 = st.text_input("Word 6")
    word_7 = st.text_input("Word 7")
    word_8 = st.text_input("Word 8")
    word_9 = st.text_input("Word 9")
    num_cards = st.slider(label="Select the number of cards to target",min_value=1, max_value=5, value=3)
    word_array = [word_1, word_2, word_3, word_4, word_5, word_6, word_7, word_8, word_9]
    words_cleaned = []
    for i in word_array:
        if i == "":
            continue
        else:
            words_cleaned.append(i.lower())
    if st.button("Generate Clues"):
        lst = generateClues(model, words_cleaned)
        printClues(lst, num_cards)


if __name__=='__main__':
    main()
