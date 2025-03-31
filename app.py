from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

top50_df = pickle.load(open('model/top50.pkl', 'rb'))
pt = pickle.load(open('model/pt.pkl', 'rb'))
books = pickle.load(open('model/books.pkl', 'rb'))
similarity_score = pickle.load(open('model/similarity_score.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/top50')
def top50():
    return render_template('popular.html',
                            book_name = list(top50_df.head(50)['Book-Title'].values),
                            book_author = list(top50_df.head(50)['Book-Author'].values),
                            num_ratings = list(top50_df.head(50)['num_ratings'].values),
                            avg_ratings = [round(i,2) for i in list(top50_df.head(50)['avg_rating'].values)],
                            image_url = list(top50_df.head(50)['Image-URL-L'].values)
                          )


@app.route('/recommend')
def recommend():
    return render_template('recommend.html')


@app.route('/suggestions')
def suggestions():
    query = request.args.get("query", "").strip().lower()
    if(not query):
        return jsonify([])

    matching_books = [title for title in pt.index if query in title.lower()]

    if(not matching_books) :
        return jsonify([])
    
    print(matching_books)
    return jsonify(matching_books[:10])


@app.route('/recommend_books', methods=['post'])
def recommend_books():
    user_book_input = request.form.get('user_book_input')

    try:
        book_name = user_book_input
        index = np.where(pt.index==book_name)[0][0]
        similar_books = sorted(list(enumerate(similarity_score[index])), key = lambda x : x[1], reverse=True)[1:7]

        data = []
        for i in similar_books:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L']))

            data.append(item)
        return render_template('recommend.html', data = data)
    
    except Exception as e:
        return render_template('errorPage.html', message = "Book not found") 



@app.route('/contact')
def contact():
    return render_template('contact.html')



if __name__ == "__main__":
    app.run()