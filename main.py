import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI
import uvicorn

app = FastAPI()   

groupdf = pd.read_csv("groupdf.csv")
books2 = pd.read_csv("books2.csv")
ratings = pd.read_csv("ratings.csv")

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

def printDetails(bookID): 
        details = books2[books2['id']==bookID]['title'].values[0]

        return details


def getRecommandations(bookID):
        r = revMap[bookID]
        argsort = np.argsort(cos_similarity[r])
        detail_list = []

        for i in argsort[-10:][:]:
            x = printDetails(Map[i])
            detail_list.append(x)
        return detail_list
        
    
# Displays popular books to new users to start from
def newRecommandations():
    books = []
    for j in popular['title']:
        books.append(j)
    return books

#   @app.get('/book/{user}')
#   async def RECO(NewUSer : str):    
#       output = newRecommandations()
#       return output

@app.get('/book/{bookID}')
async def RECO(bookID : int):    
    output = getRecommandations(bookID)
    return output


if __name__== '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)