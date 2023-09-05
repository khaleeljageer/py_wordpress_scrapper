import requests
from bs4 import BeautifulSoup
import sqlite3

base_url = 'https://www.kaniyam.com/wp-json/wp/v2/posts'


def scrap_page():
    # Initialize variables for pagination
    page = 1
    posts_per_request = 100

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('tamil_words.db')
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS kaniyam
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       content TEXT NOT NULL)''')
    print('Database created...')

    while True:
        # Set parameters for the API request
        params = {
            'per_page': posts_per_request,
            'page': page
        }
        # Send HTTP request to get JSON response of all posts
        print('Params : ', params)
        response = requests.get(base_url, params=params)
        data = response.json()
        # Check if there are more posts
        if not response.ok or not data:
            # No more posts to retrieve
            break

        # Loop through all posts and insert title and content into database
        for post in data:
            post_title = BeautifulSoup(post['title']['rendered'], 'html.parser').get_text(strip=True)
            post_content = BeautifulSoup(post['content']['rendered'], 'html.parser').get_text(strip=True)
            # Insert data into the database
            cursor.execute('INSERT INTO kaniyam (content) VALUES (?)', (post_content,))
            print(f'Inserted post with ID {post_title}')

        # Increment the page counter for the next request
        page += 1

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print('Data inserted into the database successfully.')


if __name__ == '__main__':
    scrap_page()
