# Django API Project


## Endpoints

- POST /favorite/ Favorite
-------------------------
Users should then be able to favorite the posts they like from the results along with a tag they want to categorize the link with. You should save this information in your service. You will not be "favoriting" anything in Reddit itself.

- GET /favorites/ Favorites
-------------------------
Users should then be able to get back their favorite posts that they have saved and the tags they used.

- POST /login/ Login
-------------------------
If a user has registered but they no longer have an access token they should be able to login to get one. The user will not be logging into Reddit. Just your service.

- GET /reddit/ Reddit
-------------------------
If a user has an access_token they should be able to get back a list of items from Reddit.

- POST /register/ Register
-------------------------
Have the ability for a user to register with a username and password. If registered successfully you should return an access token. The user will NOT be registering with Reddit. Just your service.

- GET /tag/ Tags
-------------------------
Returns posts for a given tag name.



