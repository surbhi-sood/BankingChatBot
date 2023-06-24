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

data = pd.read_csv("C:\\Users\\DELL\\Desktop\\SSFB bot\\BankFAQs_new - BankFAQs_new.csv.csv")

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

def get_max5(arr):
    ixarr = []
    for ix, el in enumerate(arr):
        ixarr.append((el, ix))


    ixarr.sort()

    ixs = []
    for i in ixarr[-5:]:

        ixs.append(i[1])

    return ixs[::-1]


def get_response(usrText):

    # while True:


        GREETING_INPUTS = ["hello", "hi", "greetings", "sup", "what's up", "hey", "hiii", "hii", "yo" , "hi!" , "hii!"]
        a = [x.lower() for x in GREETING_INPUTS]
        UNSATISFIED_INPUTS = ["no", "wrong", "not", "unacceptable" , "no use" , "not this" , "something else" , "foolish" , "stupid" , "you are stupid" , "this is not what i wanted" , "no this is wrong"]
        q=[x.lower() for x in UNSATISFIED_INPUTS]
        TERMINATING_INPUTS = ["bye" , "goodbye" , "tata" , "see ya" , "see you"]
        ti= [x.lower() for x in TERMINATING_INPUTS]
        ABOUT_YOU = ["how are you?" , "how's you?", "how are you" , "How's you" , "how are u?" , "How's u" ]
        au=[x.lower() for x in ABOUT_YOU]
        WHAT_YOU = ["What are you doing?" , "What are u doing?" , "What are you doing" , "What are u doing" ]
        wu=[x.lower() for x in WHAT_YOU]
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

            return "Hi \U0001F60A"

        if usrText.lower() in q:

            return "Sorry to hear that \U0001F615.\n Please try asking something else "

        if usrText.lower() in c:

            return "Ok...Alright! \U0001F64C"

        if usrText.lower() in d:

            return "My pleasure! \U0001F607"


        if usrText.lower() in ti:
            return "Bye"


        if usrText.lower() in au:
            return "I'm an AI language model, so I don't have feelings,but thanks for asking!"


        if usrText.lower() in wu:
            return "I'm here to assist you with any questions you have regarding banking & SSFB.\n How may I help you?"

        if max_similarity >= similarity_threshold:
            x = data['Answer'][questionset.index[ind]] + "   "
            return x


        elif max_similarity < similarity_threshold:

            return "Sorry, I couldn't find a matching response \U0001F615 .\nPlease contact SSFB customer care for support 1800 202 5333 "

def get_response2(usr):


    t_usr = tfv.transform([cleanup(usr.strip().lower())])
    class_ = le.inverse_transform(model.predict(t_usr))
    questionset = data[data['Class'].values == class_]

    cos_sims = []
    for question in questionset['Question']:
        sims = cosine_similarity(tfv.transform([question]), t_usr)
        cos_sims.append(sims)

    ind = cos_sims.index(max(cos_sims))
    max_similarity = max(cos_sims)

    similarity_threshold = 0.4

    if max_similarity >= similarity_threshold:
        inds = get_max5(cos_sims)

        questions = [
            data['Question'][questionset.index[ind]] for ind in inds
        ]

        suggested_questions = "\n".join(questions)

        return  "Suggested Questions\n{}".format(suggested_questions)


    return ""


