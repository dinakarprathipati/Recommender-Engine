# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 22:50:49 2018


import matplotlib.pyplot as plt
import seaborn as sns
import cufflinks as cf
cf.go_offline()
from plotly import __version__
from plotly.offline import init_notebook_mode,iplot,download_plotlyjs,plot
%matplotlib inline
init_notebook_mode(connected=True)



@author: home
"""

import numpy as np
import pandas as pd

def knn(bookname):

    ratings=pd.read_csv('Bx-Book-Ratings.csv',sep=';',error_bad_lines=False,encoding="latin-1")
    names=['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
    books=pd.read_csv('Bx-Books.csv',sep=';',error_bad_lines=False,encoding="latin-1")
    users=pd.read_csv('Bx-Users.csv',sep=';',error_bad_lines=False,encoding="latin-1")
    combine_book_info=pd.merge(ratings,books,on='ISBN')
    to_remove=['Year-Of-Publication', 'Publisher','Book-Author','Image-URL-S', 'Image-URL-M', 'Image-URL-L']
    books_info=combine_book_info.drop(to_remove,axis=1)
    books_info=books_info.dropna(axis=0,subset=['Book-Title'])
    book_ratingcount=(books_info.groupby(by=['Book-Title'])['Book-Rating'].count().reset_index().rename(columns={'Book-Rating':'total_ratings'})[['Book-Title','total_ratings']])
    rating_with_totalratingcount=books_info.merge(book_ratingcount,left_on='Book-Title',right_on='Book-Title',how='left')
    threshold=50
    rating_popular_books=rating_with_totalratingcount.query('total_ratings>=@threshold')
    combined=rating_popular_books.merge(users,left_on='User-ID',right_on='User-ID',how='left')
    us_canada_user_rating=combined[combined['Location'].str.contains('usa|canada')]
    us_canada_user_rating=us_canada_user_rating.drop('Age',axis=1)
    us_canada_user_rating=us_canada_user_rating.drop_duplicates(['User-ID','Book-Title'])
    us_canada_user_rating_pivot=us_canada_user_rating.pivot(index='Book-Title',columns='User-ID',values='Book-Rating').fillna(0)
    from scipy.sparse import csr_matrix
    us_canada_user_rating_matrix=csr_matrix(us_canada_user_rating_pivot.values)
    us_canada_user_rating_pivot2=us_canada_user_rating.pivot(index='User-ID',columns='Book-Title',values='Book-Rating').fillna(0)
    X=us_canada_user_rating_pivot2.values.T
    
    
    ##########Recommender systems using KNN###############
    
    from sklearn.neighbors import NearestNeighbors
    model_knn=NearestNeighbors(metric='cosine',algorithm='brute')
    model_knn.fit(us_canada_user_rating_matrix)
    books_list1=list(us_canada_user_rating_pivot.index)
    if bookname not in books_list1:
        return ["Book Not Found in the current Dataset...!"]
    query_index=books_list1.index(bookname)
    k=[]
    distances,indices=model_knn.kneighbors(np.array(us_canada_user_rating_pivot.iloc[query_index,:]).reshape(1,-1),n_neighbors=6)
    for i in range(0,len(distances.flatten())):
        if i==0:
            k.append(us_canada_user_rating_pivot.index[query_index])
            print('Recommendation for {0}:\n'.format(us_canada_user_rating_pivot.index[query_index]))
        else:
            k.append(us_canada_user_rating_pivot.index[indices.flatten()[i]])
            print('{0}: {1}, with distance of {2}:'.format(i, us_canada_user_rating_pivot.index[indices.flatten()[i]], distances.flatten()[i]))
    #########Recommender systems using
    return k

if __name__ == "__main__":
    knn("The Return")
