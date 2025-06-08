import streamlit as st
import pickle
import numpy as np

st.title('Book Recommender System')

st.sidebar.title('Navigation')
selected_page=st.sidebar.radio("Go to",["Home", "Recommendation"])

file_path1=r"C:\Users\geniu\OneDrive\Desktop\personal\Project\Book_Recommender_System\popular_df.pkl"
with open(file_path1,'rb') as f:
    popular_df=pickle.load(f)
file_path2=r"C:\Users\geniu\OneDrive\Desktop\personal\Project\Book_Recommender_System\pt.pkl"
file_path3=r"C:\Users\geniu\OneDrive\Desktop\personal\Project\Book_Recommender_System\books.pkl"
file_path4=r"C:\Users\geniu\OneDrive\Desktop\personal\Project\Book_Recommender_System\similarity_scores.pkl"
with open(file_path2,'rb') as f:
    pt=pickle.load(f)

with open(file_path3,'rb') as f:
    books=pickle.load(f)

with open(file_path4,'rb') as f:
    similarity_scores=pickle.load(f)


def recommend(book_name):
    # index fetch
    if book_name not in pt.index:
        return []
    
    index = pt.index.get_loc(book_name)
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        # item = []
        # temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        # item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        # item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        # item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        # data.append(item)
        temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title').iloc[0]
        data.append({
            'title': temp_df['Book-Title'],
            'author': temp_df['Book-Author'],
            'image': temp_df['Image-URL-M']
        })

    
    return data


def home():
    st.subheader("Top 25 Books")
    for i in range(0, len(popular_df), 5):
        cols = st.columns(5)
        for j, (idx, row) in enumerate(popular_df.iloc[i:i+5].iterrows()):
            with cols[j]:
                st.markdown(
                    f'<img src="{row["Image-URL-M"]}" style="width:120px; height:180px; object-fit:cover; border-radius:5px;"/>',
                    unsafe_allow_html=True
                )
                st.markdown(f"**{row['Book-Title']}**")
                st.markdown(f"*by {row['Book-Author']}*")
                st.markdown(f" {row['avg_rating']:.2f} |  {row['num_ratings']} ratings")

def recomm():
    st.subheader("Recommendations for You")
    st.write("Type in a book name and get 5 similar recommendations.")

    book_name = st.selectbox("Choose a book to get recommendations:", pt.index)

    if st.button("Submit"):
        with st.spinner("Finding recommendations..."):
            recommendations = recommend(book_name)

        if recommendations:
            st.success("Here are 5 books you might like:")

            cols = st.columns(3)  # 3 columns for side-by-side layout

            for i, book in enumerate(recommendations):
                with cols[i % 3]:
                    st.image(book['image'], width=120)
                    st.markdown(f"**{book['title']}**")
                    st.markdown(f"*by {book['author']}*")

        else:
            st.error("Book not found. Try a different name.")


if selected_page=="Home":
    home()
elif selected_page=="Recommendation":
    recomm()