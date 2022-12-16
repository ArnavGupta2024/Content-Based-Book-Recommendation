# Content-Based Book Recommendation System

## Dataset: [goodbooks-10k](https://www.kaggle.com/datasets/zygmunt/goodbooks-10k)

### About the dataset
This dataset contains ratings for ten thousand popular books.
Ratings go from one to five.
Both book IDs and user IDs are contiguous. For books, they are 1-10000, for users, 1-53424. All users have made at least two ratings.

There are also books marked to read by the users, book metadata (author, year, etc.) and tags.

- to_read.csv provides IDs of the books marked "to read" by each user, as userid, book_id pairs
- book_tags.csv contains tags(genres) assigned by users to books. Tags in this file are represented by their IDs
- tags.csv translates tag IDs to names
- ratings.csv contains ratings

This dataset contains six million ratings for ten thousand most popular (with most ratings) books. There are also:
- books marked to read by the users
- book metadata (author, year, etc.)
- tags (genres)

Book Metadata:
- Book IDs
- ISBN
- Authors
- Publication Year
- Title (with information on the book’s Saga)
- Original Title (book title only)
- Language
- Rating information
- Average Rating
- Number of Total Ratings
- Number of Ratings per Rating Value (1 - 5)
- Number of Text Reviews
- Image URL
