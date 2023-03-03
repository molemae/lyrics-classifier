import os
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# list of artists

# artist1 = 'tallest_man_on_earth'
# artist2 = 'bob_dylan'

def train_fit_pred(artist1,artist2='bob_dylan'):
# create a lyrcis df for each artist
    def lyrics_to_df(artist):
        # read data
        path = f'./data/{artist}'
        file_list = os.listdir(path=path)

        # create lyrics and titles list
        lyrics_list = list()
        title_list = list()
        for song in file_list:
            title = song.split('.')[0]
            title_list.append(title)
            with open(file=f'{path}/{song}', mode ='r') as file_in:
                lyric = file_in.read()
            lyrics_list.append(lyric)
        df = pd.DataFrame()
        df.insert(0,'title',title_list)  
        df.insert(1,'lyrics',lyrics_list)  
        df.insert(0,'artist',artist)  
        return df

    # run the artist lyric function
    df_1 = lyrics_to_df(artist1)
    df_2 = lyrics_to_df(artist2)


    #concat both artits
    df_lyrics = pd.concat((df_2,df_1),axis=0)
    # df_lyrics.head()

    # Split data
    X = df_lyrics['lyrics']
    y = df_lyrics ['artist']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=420,stratify=y)

    # Apply CountVectorizer to vectorize words
    cv = CountVectorizer(stop_words='english',ngram_range=(1,1))
    X_tran = cv.fit_transform(X_train)
    # cv.get_feature_names_out()
    # pd.DataFrame(X_tran.todense(),columns=cv.get_feature_names_out(),index=y_train)

    # Apply Tf-Idf Transformer (Normalization)
    tf = TfidfTransformer()
    tf_X_tran = tf.fit_transform(X_tran)
    # pd.DataFrame(tf_X_tran.todense(), columns=cv.get_feature_names_out(),index=y_train)

    # CountVectorizer and Tf-Idf:
    cv_tfdif_pipe = make_pipeline(CountVectorizer(stop_words='english',ngram_range=(1,1)),TfidfTransformer())
    
    X_train_tran = cv_tfdif_pipe.fit_transform(X_train)
    X_test_tran = cv_tfdif_pipe.transform(X_test)

    # LogReg
    model = LogisticRegression()
    model.fit(X_train_tran,y_train)
    train_score = model.score(X_train_tran,y_train)
    test_score =  model.score(X_test_tran,y_test)
    print(f'Train Accuracy: {train_score}\nTest Accuray: {test_score}')



# test With songs from X_test
# y_test.unique()

# def pred_art(art_name):
#     lyrics_to_predict = X_test[y_test == art_name] 
#     lyrics_to_predict_tran =  cv.transform(lyrics_to_predict)
#     X_pred_trans = tf.transform(lyrics_to_predict_tran)
#     return lreg.predict(X_pred_trans)


# for art in y_test.unique():
#     print(f'Artist: {art}')
#     pred_art(art)


# # df_lyrics[['artist']].iloc(1)
# bd_f = pred_art('bob_dylan')=='tallest_man_on_earth'
# test = X_test[y_test == 'bob_dylan'].index

# df_lyrics.iloc[test[bd_f]]