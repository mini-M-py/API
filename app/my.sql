CREATE TABLE posts (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    published BOOLEAN NOT NULL DEFAULT 'true',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
);

INSERT INTO posts (title, content,) VALUES('first_post', 'first_content');

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fast_api', user='postgres',
                                password='password0000', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Data base connection was sucessfull!")
        break
    except Exception as error:
        print("failed to connect Database!")
        error("Error :", error)
        time.sleep(2)

