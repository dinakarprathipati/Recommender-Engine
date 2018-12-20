# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def svd(bookname):

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
    
    
    
    #####Recommender systems using SVD##############
    
    from sklearn.decomposition import TruncatedSVD
    SVD=TruncatedSVD(n_components=12,random_state=17)
    
    matrix=SVD.fit_transform(X)
    import warnings
    warnings.filterwarnings("ignore",category =RuntimeWarning)
    corr = np.corrcoef(matrix)
    us_canada_book_title = us_canada_user_rating_pivot2.columns
    us_canada_book_list = list(us_canada_book_title)
    if bookname not in us_canada_book_list:
        return ["Book Not Found in the current Dataset...!"]
    coffey_hands = us_canada_book_list.index(bookname)
    print(coffey_hands)
    corr_coffey_hands  = corr[coffey_hands]
    k=list(us_canada_book_title[(corr_coffey_hands>=0.9)])
    print(k)
    return k

if __name__ == "__main__":
    svd("The Return")


