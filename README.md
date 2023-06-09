# Social media API
This is a RESTful API built using FastAPI for a social media application. 
Currently, it provides endpoint for posts, users, votes, verification of email
 address using otp furthur will be added gradually.

## Installation
* Clone this repository
  > https://github.com/mini-M-py/API.git

## Install required packages
  `pip install -r requirements.txt`
  
  * [postgres](https://www.postgresql.org/download/)

## Usage
 * Create `.env` file of root directory of project folder and name environment variable as following:
      * database_hostname
      * database_port
      * database_name
      * database_username
      * database_password
      * secret_key
      * algorithm
      * access_token_expire_minutes
      * email
      * password `Don't use your email's password insted use App password provided by your email service provider`

* Start the server `uvicorn main:app --reload`
* Navigate to `http://localhost:8000/docs` in your web browser to access the Swagger UI. From here, you can test the API endpoint using the built-in interface.

## Endpoints
The API provides the following endpoints:
* `POST /users/` : create a new user
* `POST /user/verified`: send otp to verify your email
* `GET /user/{id}`: get user information by ID
* `GET /posts/`: get all the posts
* `GET /posts/{id}`: get post's information by ID
* `POSTS /posts/`: create new post.
* `POSTS /{id}`: update post by ID
* `DELETE /posts/{id}`: delete post by ID
* `POST /login`: login user with email
* `POST /vote`: vote the post
* `POST /comments`: create comments for post
* `DELETE /comments{id}`: delete comment by post ID
* `PUT /comments`: update comment
* `GET /comments{id}`: get all comments by post ID
* `GET /`: root

## License
 This project is licensed under the MIT License - see the [LICENSE.md](/LICENSE.md) file for details.

## Contributing
pull requests are welcome.For major changes, please open an issue to discuss what you would like change.
