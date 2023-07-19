import random


#movies={wl: {nome: imdb_link}, sl : {nome_filme: rating} }
def get_response(message: str, movies: dict, username: str) -> str:
    sp_message = message.split(" ")
    p_message = sp_message[0].lower()

    if p_message == "!wl" and len(sp_message) == 1:
        st = "**Watchlist**\n```"
        for mov in movies["wl"].items():
            st += f"{mov[0]}\n"
        st += "```"
        return st
    

    if p_message == "!sl":
        st = "**Seenlist**\n```"
        for mov in movies["sl"].items():
            if(mov[1] == ""):
                st += f"{mov[0]}\n"
            else:
                st += f"{mov[0]} - {mov[1]}\n"
        st += "```"
        return st
    

    if p_message == "!wladd" and (len(sp_message) == 2 or len(sp_message) == 3):
        if(len(sp_message) == 3):
            movies["wl"][sp_message[1]] = sp_message[2]
        else:
            if(movies["wl"].get([sp_message[1]]) == None):
                movies["wl"][sp_message[1]] = ""
        return "Movie added to the Watchlist"
    

    if(username != "diogopedro" or username != "errad0"):
        return "You don't have permission for that"
    

    #Case sensitive
    if p_message == "!wlremove" and len(sp_message) == 2:
        if(movies["wl"].get(sp_message[1]) == None):
            return "Movie not in list, check for case sensitive"
        del movies["wl"][sp_message[1]]
        return "Movie removed from the Watchlist"
    

    if p_message == "!sladd" and (len(sp_message) == 2 or len(sp_message) == 3):
        if(len(sp_message) == 3):
            if(int(sp_message[2]) <= 10 and int(sp_message[2]) >= 0):
                movies["sl"][sp_message[1]] = sp_message[2]
            else:
                return "Invalid rating"
        else:
            if(movies["sl"].get([sp_message[1]]) == None):
                movies["sl"][sp_message[1]] = ""
        return "Movie added to the seenlist"


    #Case sensitive
    if p_message == "!slremove" and len(sp_message) == 2:
        if(movies["sl"].get(sp_message[1]) == None):
            return "Movie not in list, check for case sensitive"
        del movies["sl"][sp_message[1]]
        return "Movie removed from the seenlist"
    

    if p_message == "!rndmov" and len(sp_message) == 2:
        if(len(movies["wl"]) <= int(sp_message[1])):
            st = "**Randomlist**\n```"
            for mov in movies["wl"].items():
                st += f"{mov[0]}\n"
            st += "```"
            return st
        
        random_items = random.sample(list(movies["wl"].items()), int(sp_message[1]))
        print(random_items)
        index = 1
        st = "**Randomlist**\n```"
        for mov in random_items:
            st += f"{mov[0]}\n"
        st += "```"
        return st


    if p_message == "!help":
        return """**Commands**```!wl                             - returns the list of movies to watch
!sl                             - return the list of movies already seen
!wladd {movie name} {imdb link} - adds a movie to the watchlist
!wlremove {movie name}          - removes a movie from the watchlist
!sladd {movie name} {rating}    - adds a movie to the seenlist
!slremove {movie name}          - removes a movie from the seenlist
!rndmov {int}                    - gives a random list of x movies from the Watchlist```"""

    return "Use !help"