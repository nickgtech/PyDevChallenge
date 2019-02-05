# PyDevChallenge

To run the application locally all that's required is Python 3.6. Clone the repo and start the application by running app.py with the command 'python app.py'. The application will run on localhost:5000 using a sqlite database. The application was originally configured with a mysql database but for ease of running it on multiple devices I implemented sqlite. 

Known Issues: 
- A user cannot access another users profile but just gets a simple error page. 
- the giphy api is not allowing me to set an offset larger than 100, didn't get the chance to investigate further. 

Possible enhancements: 
- Creating blueprints to separate the website from the api.
- Password reset functionality.
- Paginating the user profile page.
- Admin Panel for super users.
- Implementing Oauth/JWT tokens. 
- Using varying sized gifs. 

