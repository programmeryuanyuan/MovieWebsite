import os
import mysql.connector
from flask_mysqldb import MySQL
from flask import Flask, session, request, render_template, jsonify, redirect
from flask_cors import CORS, cross_origin
import base64
import requests
import openai

# Get movie details from TMDB API
url = f'https://api.themoviedb.org/3/movie/'
api_key = '4a11e15a0e60260532c2fbb4c64c3f8a'
openai.api_key = "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"

app = Flask(__name__)
CORS(app)

app.secret_key = 'secret_key'

app.config['MYSQL_HOST'] = 'rm-p0wlv0u95s38js90lyo.mysql.australia.rds.aliyuncs.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aa8821701'
app.config['MYSQL_DB'] = 'database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)



# For chatbot
@app.route('/get_answer', methods=['POST'])
def get_answer():
    user_input = request.json.get('user_input')
    context = request.json.get('context')
    admin=""
    achievements= request.json.get('achievements')
    print(achievements)
    values = [v for k, v in achievements.items() if v]
    if len(values)!=0:
        admin+="this user has got the following achievements:"
        for achievement in values:
            admin+=achievement
            admin+=" "
    admin+="You are a helpful assistant specialized in movies. Don't answer any questions outside of the movie scope. Message provided by assistant is the context"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": admin},
            {"role":"assistant", "content": context},
            {"role": "user", "content": user_input}
        ]
    )
    print(admin)
    response = completion.choices[0].message['content']
    return jsonify({"answer": response})


# register
@app.route('/register', methods=['POST'])
def register():
	# get username and password
    data = request.get_json()
    username = data['username']
    password = data['password']
	# Insert
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
    row = cursor.fetchone()
    if row is not None:
        return jsonify({'error': 'Username already exists'}), 400
    cursor.execute("INSERT INTO User (username, password) VALUES (%s, %s)", (username, password))
    mysql.connection.commit()
    cursor.close()
	# Return
    result = {"message": "Registration successful!"}
    return jsonify(result)


# login
@app.route('/login', methods=['POST'])
def login():
    # Get
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    # Insert
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
    row = cursor.fetchone()
    
    if row is not None:
        if row['password'] == password:
            # Set session data
            #session['user_id'] = row['id']
            #session['username'] = row['username']
            # Redirect to home page
            #return redirect('/home')
            pfp_data = row['pfp']
            pfp_data_base64 = base64.b64encode(pfp_data).decode('utf-8')
            banner_data = row['banner']
            banner_data_base64 = base64.b64encode(banner_data).decode('utf-8')
            user_details = {
                'id': row['id'],
                'username': row['username'],
                'pfp': pfp_data_base64,
                'banner': banner_data_base64,
                'favorite_movie': row['favorite_movie']
    }
            #session['user_id'] = id
            return jsonify(user_details), 200
        
        else:
            return jsonify({'error': 'Incorrect username or password'}), 401
    else:
        return jsonify({'error': 'User not found'}), 404




# pfp
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/user/<int:user_id>/upload_pfp', methods=['POST'])
@cross_origin()
def upload_pfp(user_id):
    # Add this line to set the CORS headers for all origins
    response = jsonify({'success': 'Profile picture updated successfully'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    file = request.files['file']
    username = request.form['username']
    
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(filename)
        with open(filename, 'rb') as f:
            pfp_data = f.read()
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE User SET pfp = %s WHERE username = %s", (pfp_data, username))
        mysql.connection.commit()
        cursor.close()
        # Remove the temporary file from disk
        os.remove(filename)
        return jsonify({'success': 'Profile picture updated successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400
 
 
 # banner
@app.route('/user/<int:user_id>/upload_banner', methods=['POST'])
@cross_origin()
def upload_banner(user_id):
    # Add this line to set the CORS headers for all origins
    response = jsonify({'success': 'Profile picture updated successfully'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    file = request.files['file']
    username = request.form['username']
    
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(filename)
        with open(filename, 'rb') as f:
            banner_data = f.read()
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE User SET banner = %s WHERE username = %s", (banner_data, username))
        mysql.connection.commit()
        cursor.close()
        # Remove the temporary file from disk
        os.remove(filename)
        return jsonify({'success': 'Banner picture updated successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400


# favorite movie
@app.route('/user/<int:user_id>/set_favorite_movie', methods=['POST'])
def set_favorite_movie(user_id):
    #movie_id = request.form['movie_id']
    #print(movie_id)
    movie_id=request.json.get('movie_id')
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE User SET favorite_movie = %s WHERE id = %s", (movie_id, user_id))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'success': 'Favorite movie updated successfully'}), 200




# Achievements Avater

@app.route('/user/<int:user_id>/achievements', methods=['GET'])
@cross_origin()
def show_achievements(user_id):

    cur = mysql.connection.cursor()
    # Get number of reviews written by user

    cur.execute('SELECT COUNT(*) FROM Review WHERE user_id = %s', (user_id,))

    row = cur.fetchone()

    num_reviews = row['COUNT(*)']


    # Set achievement titles based on number of reviews
    review_achievements = ['Novice Reviewer', 'Junior Reviewer', 'Senior Reviewer', 'Expert Reviewer', 'Master Reviewer']
    review_thresholds = [10, 100, 1000, 10000, 100000]
    review_title = review_achievements[0]
    for i in range(1, len(review_achievements)):
        if num_reviews >= review_thresholds[i-1]:
            review_title = review_achievements[i]
    result = {'review_achievement': review_title}

    # Get number of movies in user's wishlist by genre
    genre_achievements = {
        35: ['Comedy Fan', 'Comedy Fanatic', 'Comedy Connoisseur'],
        27: ['Horror Enthusiast', 'Horror Admirer', 'Horror Expert'],
        28: ['Action Enthusiast', 'Action Addict', 'Action Connoisseur', 'Action Expert'],
        16: ['Animation Lover', 'Animation Addict', 'Animation Connoisseur', 'Animation Specialist'],
        10751: ['Family Fan', 'Family Fanatic', 'Family Connoisseur', 'Family Master'],
        10752: ['War Lover', 'War Fanatic', 'War Connoisseur', 'War Master'],
        36: ['History Devotee', 'History Fanatic', 'History Connoisseur', 'History Specialist'],
        80: ['Crime Fan', 'Crime Admirer', 'Crime Connoisseur', 'Crime Connoisseur'],
        878: ['Sci-Fi Buff', 'Sci-Fi Aficionado', 'Sci-Fi Connoisseur', 'Sci-Fi Master'],
        10749: ['Romance Devotee', 'Romance Aficionado', 'Romance Connoisseur', 'Romance Connoisseur']
    }

    for genre_id, achievements in genre_achievements.items():
        cur.execute('SELECT COUNT(*) FROM MovieGenre mg JOIN WishList w ON mg.movie_id = w.movie_id WHERE mg.genre_id = %s AND w.user_id = %s HAVING COUNT(*) >= 5', (genre_id, user_id))
        #num_movies = cur.fetchone()[0]
        num_movies = cur.fetchone()
        num_movies = num_movies[0] if num_movies is not None else 0

        title = ''
        for i in range(1, len(achievements)):
            if num_movies >= 10 * (i+1):
                title = achievements[i]
        result[f'{genre_id}_achievement'] = title
     
    response = jsonify(result),200
    return response



# WishList and BannedList
@app.route('/user/<int:user_id>/wishlist',methods=['GET'])
@cross_origin()
def show_wishlist(user_id):

    cur = mysql.connection.cursor()
    
    # Get movies in user's wishlist
    cur.execute('SELECT * FROM WishList WHERE user_id = %s', (user_id,))
    #wishlist = [movie['movie_id'] for movie in cur.fetchall()]
    wishlist=cur.fetchall()
    #movies = []
    #for movie_id in wishlist:
        #response = requests.get(f'{url}{movie_id}?api_key={api_key}')
        #if response.status_code == 200:
            #movies.append(response.json())
            #movies.append(response)
    
    #return jsonify(movies),200
    return jsonify(wishlist),200

@app.route('/user/<int:user_id>/bannedlist',methods=['GET'])
def show_bannedlist(user_id):
    print("get show bannedlist request")
    cur = mysql.connection.cursor()
    
    # Get users that the specified user has blacklisted
    cur.execute('SELECT * FROM BannedList WHERE user_id = %s', (user_id,))
    print("select sucess")
    #bannedlist=[user['banned_user_id'] for user in cur.fetchall()]
    #bannedlist = [user['banned_user_id'] for user in cur.fetchall()]
    bannedList=cur.fetchall()
    print(bannedList)
    
    return jsonify(bannedList),200



@app.route('/user/<int:user_id>/wishlist', methods=['POST'])
def add_to_wishlist(user_id):
    print("add to wishlist request")
    movie_id = request.json.get('movie_id')
    movie_title=request.json.get('movie_title')
    if movie_id:
        cur = mysql.connection.cursor()
        
        # Check if movie is already in wishlist
        cur.execute('SELECT * FROM WishList WHERE user_id = %s AND movie_id = %s', (user_id, movie_id))
        row = cur.fetchone()
        if row is not None:
            return jsonify({'message': 'Movie is already in your wishlist.'}), 201

        cur.execute("INSERT INTO WishList (user_id, movie_id,movie_title) VALUES (%s, %s,%s)", (user_id, movie_id,movie_title))
        mysql.connection.commit()
        return jsonify({'message': 'Movie added to wishlist.'}), 201
    else:
        return jsonify({'message': 'Movie ID is missing.'}), 400

@app.route('/user/<int:user_id>/bannedlist', methods=['POST'])
def add_to_bannedlist(user_id):
  
    bannedlist_user_id = request.json.get('banned_user_id')
    bannedlist_username=request.json.get('banned_username')

    if bannedlist_user_id:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM BannedList WHERE user_id = %s AND banned_user_id = %s', (user_id, bannedlist_user_id))
        row = cur.fetchone()
        #print(row)
        if row is not None:
            return jsonify({'message': 'User is already in your blacklist.'}), 201

        cur.execute('INSERT INTO BannedList (user_id, banned_user_id,banned_username) VALUES (%s, %s,%s)', (user_id, bannedlist_user_id,bannedlist_username))
        #cur.execute('INSERT INTO BannedList (user_id, banned_user_id) VALUES (%s, %s)', (user_id, bannedlist_user_id))
        mysql.connection.commit()
        return jsonify({'message': 'User added to bannedlist.'}), 201
    else:
        return jsonify({'message': 'User ID is missing.'}), 400





#comment
@app.route('/user/<int:user_id>/add_comment', methods=['POST'])
def add_comment(user_id):
    print("add comment request")
    data = request.get_json()
    movie_id = data['movie_id']
    comment_text = data['comment_text']
    rating = data['rating']
    username=data['username']
    # insert the comment into the database
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO Review (movie_id, user_id, text, rating,username) VALUES (%s, %s, %s, %s,%s)', (movie_id, user_id, comment_text, rating,username))
    cur.execute('UPDATE USER SET comment_count = comment_count + 1 WHERE id = %s', (user_id,))
    mysql.connection.commit()

    # return a success message
    result = {'success': True}
    return jsonify(result),200

@app.route('/movies/<int:movie_id>/show_comment', methods=['GET'])
@cross_origin()
def show_comment(movie_id):
    # Add this line to set the CORS headers for all origins
    #response = jsonify({'success': 'Comments retrieved successfully'})
    #response.headers.add('Access-Control-Allow-Origin', '*') 
    #print("show comment request")
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Review WHERE movie_id = %s', (movie_id,))
    comments = cur.fetchall()
    #print(comments)
    """result = []
    for comment in comments:
        comment_dict = {
            'id': comment['id'],
            'movie_id': comment['movie_id'],
            'user_id': comment['user_id'],
            'text': comment['text'],
            'rating': comment['rating'],
        }
        result.append(comment_dict)"""
    return jsonify(comments),200


'''
# Search Bar
@app.route('/movies', methods=['GET'])
def get_movies_by_director():
  '''  

@app.route('/movies/genre', methods=['POST'])
def get_movies_by_genre():

    genre_name=request.json.get('genre_name')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM Genre WHERE genre_name = %s", (genre_name,))
    
    row = cursor.fetchone()

    cursor.execute("SELECT * FROM MovieGenre WHERE genre_id = %s", (row['id'],))
    movies = [movie['movie_id'] for movie in cursor.fetchall()]
    mysql.connection.commit()
    cursor.close()


    """result=[]
    for movie in movies:
        result.append({
            'movie': movie[0],
            'genre': movie[1]
		})"""
        
    return jsonify(movies),200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)