#importing all the libraries needed
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm 

#building the main function to recommend books based on a choosen book_id and owner_id
def f_recommend(book_id, owner_id):
    
    df = pd.read_csv(r'd:\naomy\LIA-FastAPI-MySQL\data\data.csv') #reading the csv file containing the books
    df_copy = df.copy()
    df.rename(columns={'id':'book_id'},inplace=True)
    #normalizing pages and book rating columns
    df['pages_norm'] = normalize(df['pages'].values) 
    df['book_rating_norm'] = normalize(df['classification'].values)
    #one hot encodes the categorial columns 
    df = ohe(df = df, enc_col = 'genre')
    df = ohe(df = df, enc_col = 'author')
    cols = ['pages', 'genre', 'description', 'title', 'author','classification']
    df.drop(columns = cols, inplace = True)
    df.set_index('book_id', inplace = True)

    df_recommendations = recommend(df.index[book_id], owner_id, df)
    df_seila= df_copy.loc[df_copy['id'].isin(df_recommendations.index.values), ['title']]#returns dataframe with the titles associated to the book ids
    df_seila.drop_duplicates(inplace=True)
    list_books = df_seila.to_dict(orient='list')
    return list_books
    
def normalize(data):
    '''
    Gets dataframe and normalizes input data to be between 0 and 1
    '''
    min_val = min(data)
    if min_val < 0:
        data = [x + abs(min_val) for x in data]
    max_val = max(data)
    return [x/max_val for x in data]

def ohe(df, enc_col):
    '''
    One hot encodes specified columns and adds them back
    onto the input dataframe
    '''
    
    ohe_df = pd.get_dummies(df[enc_col])
    ohe_df.reset_index(drop = True, inplace = True)
    return pd.concat([df, ohe_df], axis = 1)

def cosine_sim(v1,v2):
    '''
    Calculates the cosine similarity between two vectors
    '''
    return dot(v1,v2)/(norm(v1)*norm(v2))

def recommend(book_id, owner_id, df):
    """
    Content based recommendations.
    Calls the cosine similarity function to calculate similarities and returns the
    most similar books, excluding the ones listed by the user
    """
    book_id = book_id - 1 #because it starts from zero in the csv, while the ids in the database start from 1
    
    # calculate similarity of input book_id vector and all other vectors in the table
    inputVec = df.loc[book_id].values #gets values of the book_id inputed
    df['sim']= df.apply(lambda x: cosine_sim(inputVec,x.values), axis=1)  #goes through all the book vectors in the table
                                                         #and creates a column containing the values of the cosine similarity
    
    df_rec = df.nlargest(10, columns='sim')#gets only the 10 most similars (10 bigger values of the cosine similarity)
    df_final = df_rec.loc[df['owner_id'] != owner_id]#excludes books already listed by the user
    # returns up to 10 similar books that the user didnt list already
    return df_final