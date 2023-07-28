from mov import movie

#Check bd -> MATCH (k) MATCH(n)-[r]->(m) RETURN k,n,r,m
def get_response(message: str, movie_db: movie, username: str, restrict = None) -> str:
    sp_message = message.split(" ", 1)
    p_message = sp_message[0].lower()
    
    print(sp_message)

    movie_db.connect()
    
    print(1)

    # !wl
    if p_message == "!wl" and len(sp_message) == 1:
        st = "**Watchlist**```\n"
        movies = movie_db.checkMovies(username)
        if(not movies):
            return st + "Empty ```"
        for mov in movies:
            st += f"{mov}\n"
        st += "```"
        return st
    
    print(2)
    
    # !sl
    if p_message == "!sl" and len(sp_message) == 1:
        st = "**Seenlist**```\n"
        movies = movie_db.checkMoviesSeen(username)
        if(not movies):
            return st + "Empty ```"
        for mov in movies.items():
            if(mov[1] == ""):
                st += f"{mov[0]}\n"
            else:
                st += f"{mov[0]} - {mov[1]}\n"
        st += "```"
        return st
    
    print(3)

    # !wl add <name>
    # !wl rm <name>
    if p_message == "!wl" and (len(sp_message) == 2):
        if(restrict):
            return "You Don't have permissions for that"
        
        sp = sp_message[1].split(" ", 1)

        if(len(sp) == 2 and sp[0] == "add"): 
            movie_db.addNew("watch", username, sp[1])
            return "Movie added to the Watchlist"

        if(len(sp) == 2 and sp[0] == "rm"): 
            movie_db.remove("watch", username, sp[1])
            return "Movie removed from the Watchlist"
        
    
    print(4)

    # !sl add <name> <rating>
    # !sl rm <name>
    if p_message == "!sl" and (len(sp_message) == 2):
        if(restrict):
            return "You Don't have permissions for that"

        sp = sp_message[1].split(" ", 1)

        if(len(sp) == 2 and sp[0] == "add"):
            try:
                name, rating = sp[1].rsplit(" ", 1)
                rating = int(rating) 
            except:
                return "Give a rating"
            
            if(not (rating <= 10 and rating >= 0)):
                return "Give a rating between 0 and 10"
            
            movie_db.addNew("seen", username, name, rating)
            return "Movie added to the Seenlist"
        
        if(len(sp) == 2 and sp[0] == "rm"): 
            movie_db.remove("seen", username, sp[1])
            return "Movie removed from the Seenlist"

    print(5)
    
    # !mov <name>
    if p_message == "!mov" and len(sp_message) == 2:
        return movie_db.checkMovie(sp_message[1])

    print(6)

    # !rnd <num>
    if p_message == "!rnd" and len(sp_message) == 2:
        movies = movie_db.randomMovies(username, int(sp_message[1]))
        st = "**Randomlist**```\n"
        for mov in movies:
            if(movies):
                st += f"{mov}\n"
        st += "```"
        return st    
    
    print(7)

    # !help
    if p_message == "!help" or p_message == "!h":
        return """**Commands**```
!wl                              - returns the list of movies to watch
!sl                              - return the list of movies already seen
!wl add {movie name}             - adds a movie to the watchlist
!wl rm  {movie name}             - removes a movie from the watchlist
!sl add {movie name} {rating}    - adds a movie to the seenlist
!sl rm  {movie name}             - removes a movie from the seenlist
!mov    {movie name}             - returns the imdb link of the movie
!rnd    {int}                    - gives a random list of x movies from the Watchlist

To use own lists add 's' before the '!'     -> s!{command}
For private messages add 'p' before the '!' -> p!{command}```"""
    
    print(8)

    return "Use !help"