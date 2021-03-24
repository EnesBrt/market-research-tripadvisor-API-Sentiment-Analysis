# API_Tripadvisor

This Api scraps and returns returns useful informations such as : the reviews (in french) and the global score of a restaurant from TripAdvisor

it scraps using the following instructions :
  
  if oyu solely want to extract all restaurants and bare informations from a surrounding area use
  http://127.0.0.1:8000/restaurant/{cityid} 
    
    which you can find from trip advisor
    by default, this scraps only the top 30 restaurants from your surrounding area
  
  following your instruction you can add query such as :
  http://127.0.0.1:8000/restaurant/{cityid}?review=True
  
  or
  
  http://127.0.0.1:8000/restaurant/{cityid}?full=True
    
    which returns whether all reviews from the surrounding area or all restaurants from the area.
    you can combine those query in something like this :
  
  http://127.0.0.1:8000/restaurant/{cityid}?review=True&full=True
  
    this returns all review from all restaurants from the area
    This does take a few hours depending on the numbers of restaurants you intend to extract informations from

you can also scrap useful informations from a unique restaurant using :

  http://127.0.0.1:8000/restaurant/{cityid}/{restaurantid}
  
  this returns the informations from the first webpage displayed on TripAdvisor for the restaurant
  this also takes the queries to extract all reviews
  
this Api can also display a useful dashboard using the instruction :

http://127.0.0.1:8000/restaurant/{cityid}/{restaurantid}/dashboard
  
  this then returns :
    restaurant infos
    list of most used words in the reviews
    a top 10 comments
    a worst 10 comments
    
  (as of yet, it is still a bit laggy, but i will try to focus on it)

This API is a work in progress and intends to ad a Sentiment Analysis part to examine a list of comments you may want to read from a .txt file
or directly from Trip Advisor

the scraping part is based on a github repo made by LaskasP
