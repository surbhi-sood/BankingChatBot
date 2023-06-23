import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split as tts
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.svm import SVC
import pyttsx3

nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def cleanup(sentence):
    word_tok = nltk.word_tokenize(sentence)
    stemmed_words = [w for w in word_tok if not w in stop_words]
    return ' '.join(stemmed_words)


le = LE()

tfv = TfidfVectorizer(min_df=1, stop_words='english')

data = pd.read_csv("C:\\Users\\DELL\\Desktop\\SSFB bot\\BankFAQs.csv")

questions = data['Question'].values

X = []

for question in questions:
    X.append(cleanup(question))

tfv.fit(X)
le.fit(data['Class'])

X = tfv.transform(X)

y = le.transform(data['Class'])

trainx, testx, trainy, testy = tts(X, y, test_size=.3, random_state=42)

model = SVC(kernel='linear')
model.fit(trainx, trainy)

class_ = le.inverse_transform(model.predict(X))

# Initialize the TTS engine
engine = pyttsx3.init()

def get_response(usrText):
    # engine.say(usrText)
    # engine.runAndWait()
    while True:
        if usrText.lower() == "bye":
            return "Bye"

        GREETING_INPUTS = ["hello", "hi", "greetings", "sup", "what's up", "hey", "hiii", "hii", "yo"]
        a = [x.lower() for x in GREETING_INPUTS]
        UNSATISFIED_INPUTS = ["no", "wrong", "not", "unacceptable" , "no use" , "not this" , "something else" , "foolish" , "stupid" , "you are stupid" , "this is not what i wanted" , "no this is wrong"]
        q=[x.lower() for x in UNSATISFIED_INPUTS]

        sd = ["Thanks", "Welcome"]
        d = [x.lower() for x in sd]

        am = ["OK"]
        c = [x.lower() for x in am]

        t_usr = tfv.transform([cleanup(usrText.strip().lower())])
        class_ = le.inverse_transform(model.predict(t_usr))
        questionset = data[data['Class'].values == class_]

        cos_sims = []
        for question in questionset['Question']:
            sims = cosine_similarity(tfv.transform([question]), t_usr)
            cos_sims.append(sims)

        ind = cos_sims.index(max(cos_sims))
        max_similarity = max(cos_sims)

        similarity_threshold = 0.4  # Adjust the threshold as per your requirement

        if usrText.lower() in a:
            # Speak the input string
            # engine.say(a)
            # engine.runAndWait()
            return "Hi \U0001F60A"

        if usrText.lower() in q:
            # Speak the input string
            # engine.say(usrText)
            # engine.runAndWait()
            return "Sorry to hear that.\U0001F615 "

        if usrText.lower() in c:
            # Speak the input string
            # engine.say(usrText)
            # engine.runAndWait()
            return "Ok...Alright! \U0001F64C"

        if usrText.lower() in d:
            # Speak the input string
            # engine.say(usrText)
            # engine.runAndWait()
            return "My pleasure! \U0001F607"

        if max_similarity >= similarity_threshold:
            a = data['Answer'][questionset.index[ind]] + "   "
            # Speak the output string
            # engine.say(a)
            # engine.runAndWait()
            return a


        elif max_similarity < similarity_threshold:
            if "how are you" in usrText.lower():
                # Speak the input string
                # engine.say(usrText)
                # engine.runAndWait()
                return "I'm an AI language model, so I don't have feelings,but thanks for asking!"
            elif "what are you doing" in usrText.lower():
                # Speak the input string
                # engine.say(usrText)
                # engine.runAndWait()
                return "I'm here to assist you with any questions you have regarding SSFB."
            else:
                # Speak the input string
                # engine.say(usrText)
                # engine.runAndWait()
                return "Sorry, I couldn't find a matching response. \U0001F615"

def get_response2(usr):
    if usr.lower() == "bye":
        # Speak the input string
        engine.say(usr)
        engine.runAndWait()
        return "Thanks for having a conversation! \U0001F60E"

    GREETING_INPUTS = ["hello", "hi", "greetings", "sup", "what's up", "hey", "hiii", "hii", "yo"]
    a = [x.lower() for x in GREETING_INPUTS]

    UNSATISFIED_INPUTS = ["no", "wrong", "not", "unacceptable", "no use", "not this", "something else", "foolish",
                          "stupid", "you are stupid", "this is not what i wanted", "no this is wrong"]
    q = [x.lower() for x in UNSATISFIED_INPUTS]

    sd = ["Thanks", "Welcome"]
    d = [x.lower() for x in sd]

    am = ["OK"]
    c = [x.lower() for x in am]

    t_usr = tfv.transform([cleanup(usr.strip().lower())])
    class_ = le.inverse_transform(model.predict(t_usr))
    questionset = data[data['Class'].values == class_]

    cos_sims = []
    for question in questionset['Question']:
        sims = cosine_similarity(tfv.transform([question]), t_usr)
        cos_sims.append(sims)

    ind = cos_sims.index(max(cos_sims))
    max_similarity = max(cos_sims)

    similarity_threshold = 0.4  # Adjust the threshold as per your requirement

    if usr.lower() in a:
        # Speak the input string
        # engine.say(usr)
        # engine.runAndWait()
        return ""

    if usr.lower() in q:
        # Speak the input string
        # engine.say(usr)
        # engine.runAndWait()
        return "Please contact SSFB customer care for support 1800 202 5333"

    if usr.lower() in c:
        # Speak the input string
        # engine.say(usr)
        engine.runAndWait()
        return "Cool! \U0001F604"

    if usr.lower() in d:
        # Speak the input string
        # engine.say(usr)
        # engine.runAndWait()
        return "\U0001F44D"

    if max_similarity < similarity_threshold:
        if "how are you" in usr.lower():
            # Speak the input string
            # engine.say(usr)
            # engine.runAndWait()
            return ""
        elif "what are you doing" in usr.lower():
            # Speak the input string
            # engine.say(usr)
            engine.runAndWait()
            return "How may I help you?"
        else:
            # Speak the input string
            # engine.say(usr)
            # engine.runAndWait()
            return "I'm not able to solve this question at the moment. You can call customer support at 1800 202 5333 \U0001F615"

    return ""
