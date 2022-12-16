import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.sparse import coo_matrix
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn


testdf = pd.read_csv(r"C:\Users\dell\testdf.csv")
groupdf = pd.read_csv(r"C:\Users\dell\groupdf.csv")
books2 = pd.read_csv(r"C:\Users\dell\books2.csv")
ratings = pd.read_csv(r"C:\Users\dell\ratings.csv")

popular = books2.sort_values('ratings_count', ascending=False)[0:10]

# Initialising variables for the system

List=[] # this will be used to maintain a list of dictionaries

# Each dictionary corresponds to a single book
# Both dictionaries take numeric values
Map = {}
revMap = {}
ptr=0            # pointer

testdf = ratings # we copy the dataset for testing
testdf= testdf[['user_id','rating']].groupby(testdf['book_id'])
# The user_id is the key, while rating given by the user for the book is its value (in the dictionary)

for i in testdf.groups.keys():
    temp={}                                # we create a temporary dictionary for iteratinos
    groupdf = testdf.get_group(i)          # extracting the keys
    for j in range(0,len(groupdf)): 
        temp[groupdf.iloc[j,0]]=groupdf.iloc[j,1]
    Map[ptr]= i
    revMap[i] = ptr
    ptr=ptr+1
    List.append(temp)                      # here we append the dictionary formed in the list

dictVectorizer = DictVectorizer(sparse=True)
vector = dictVectorizer.fit_transform(List)
cos_similarity = cosine_similarity(vector)

class Data(BaseModel):
    NewUser: str

app = FastAPI()     
@app.post('/book/{bk}')
async def RECO(NewUser : str):


# Defining functions for the recommender system 
    def printDetails(bookID): 

        details = {
            'Title' : books2[books2['id']==bookID]['title'].values[0],
            'Author' : books2[books2['id']==bookID]['authors'].values[0],
            'Publication Year' : books2[books2['id']==bookID]['original_publication_year'].values[0],
            'Language' : books2[books2['id']==bookID]['language_code'].values[0],
            'Book ID' : books2[books2['id']==bookID]['id'].values[0]
        }

        return details

# Function argsort(), returns the indices which would sort an array. Used with 2D arrays also.
# Cos_similarity is a 2D matrix which we will use here
    def getRecommandations(bookID):
        r = revMap[bookID]
        a = np.argsort(cos_similarity[r])
        
        detail_list = []
        print('here1')
        for i in a[:10]:
            print(f'he  re{i}')
            x = printDetails(Map[i])
            detail_list.append(x)

        return detail_list
          
       
# Displays popular books to new users to start from
    def newRecommandations():
        books = []

        for j in popular['title']:
            books.append(j)


        return books


    if (yynn=="Yes"):
        output = newRecommandations()

    else:
        bookID=25
        output = getRecommandations(bookID)

    return output

if __name__== '__main__':
    uvicorn.run(app, host='127.0.0.1', port=4000)