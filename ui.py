import streamlit as st
import requests

base_url = 'http://127.0.0.1:8000/'

def recommend(bookID):
    resp = requests.get(base_url + 'book/' + str(bookID))
    return resp.json()


def main():
    st.title('Book Recommender')
    bookID = st.text_input('Enter book id: ')

    if st.button('Recommendations'):
        output = recommend(bookID)
        for o in output:
            st.write(o)



if __name__ == '__main__':
    main()