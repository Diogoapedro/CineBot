import random

#movies={wl: {nome: imdb_link}, sl : {nome_filme: rating} }
def get_response(message: str, movies: dict, username: str) -> str:
    admin_users = ["diogopedro", "errad0"]
    banned_users = []
    sp_message = message.split(" ", 1)
    p_message = sp_message[0].lower()

    if(username in banned_users):
        return "You have been banned"

    if p_message == "!wl" and len(sp_message) == 1:
        st = "**Watchlist**```\n"
        for mov in movies["wl"].items():
            st += f"{mov[0]}\n"
        st += "```"
        return st
    

    if p_message == "!sl" and len(sp_message) == 1:
        st = "**Seenlist**```\n"
        for mov in movies["sl"].items():
            if(mov[1] == ""):
                st += f"{mov[0]}\n"
            else:
                st += f"{mov[0]} - {mov[1]}\n"
        st += "```"
        return st
    

    if p_message == "!wladd" and (len(sp_message) == 2):
        x = sp_message[1].rsplit(" ", 1)
        st = sp_message[:1]
        st.extend(x)
        print(st)
        if(len(st) == 3):
            movies["wl"][st[1]] = st[2]
        else:
            print("1")
            if(movies["wl"].get(st[1]) == None):
                print("2")
                movies["wl"][st[1]] = ""
        return "Movie added to the Watchlist"
    

    if p_message == "!wlimdb" and len(sp_message) == 2:
        if(movies["wl"].get(sp_message[1]) == None):
            return "Movie not in the list, check for case sensitive"
        if(movies["wl"].get(sp_message[1]) == ""):
            return "Movie doesn't have imdb in the database"
        return movies["wl"][sp_message[1]]  


    if p_message == "!rndmov" and len(sp_message) == 2:
        if(len(movies["wl"]) <= int(sp_message[1])):
            st = "**Randomlist**```\n"
            for mov in movies["wl"].items():
                st += f"{mov[0]}\n"
            st += "```"
            return st
        
        st = "**Randomlist**```\n"
        got = set()
        for i in range(int(sp_message[1])):
            mv = random.choice(list(movies["wl"].keys()))
            while mv in got:
                mv = random.choice(list(movies["wl"].keys()))
            got.add(mv)
            st += f"{mv}\n"
        st += "```"
        print(st)
        return st
    

    #Case sensitive
    if p_message == "!wlremove" and len(sp_message) == 2:
        if(not (username in admin_users)):
            return "You don't have permission for that"
        
        if(movies["wl"].get(sp_message[1]) == None):
            return "Movie not in list, check for case sensitive"
        del movies["wl"][sp_message[1]]
        return "Movie removed from the Watchlist"
    

    if p_message == "!sladd" and (len(sp_message) == 2):
        if(not (username in admin_users)):
            return "You don't have permission for that"
        
        x = sp_message[1].rsplit(" ", 1)
        st = sp_message[:1]
        st.extend(x)
        print(st)
        if(len(st) == 3):
            if(float(st[2]) <= 10 and float(st[2]) >= 0):
                movies["sl"][st[1]] = st[2]
            else:
                return "Invalid rating"
        else:
            print(1)
            if(movies["sl"].get(st[1]) == None):
                print(2)
                movies["sl"][st[1]] = ""
        return "Movie added to the seenlist"


    #Case sensitive
    if p_message == "!slremove" and len(sp_message) == 2:
        if(not (username in admin_users)):
            return "You don't have permission for that"
        
        if(movies["sl"].get(sp_message[1]) == None):
            return "Movie not in list, check for case sensitive"
        del movies["sl"][sp_message[1]]
        return "Movie removed from the seenlist"
    

    if p_message == "!selfsl" and len(sp_message) == 1:
        st = "**Seenlist**```\n"
        if(not movies.get(username)):
            return "Your list is still empty"
        for mov in movies[username].items():
            if(mov[1] == ""):
                st += f"{mov[0]}\n"
            else:
                st += f"{mov[0]} - {mov[1]}\n"
        st += "```"
        return st



    if p_message == "!selfsladd" and (len(sp_message) == 2):
        
        x = sp_message[1].rsplit(" ", 1)
        st = sp_message[:1]
        st.extend(x)
        print(st)

        if(not movies.get(username)):
            movies[username] = dict()

        if(len(st) == 3):
            if(float(st[2]) <= 10 and float(st[2]) >= 0):
                movies[username][st[1]] = st[2]
            else:
                return "Invalid rating"
        else:
            print(1)
            if(movies[username].get(st[1]) == None):
                print(2)
                movies[username][st[1]] = ""
        return "Movie added to the seenlist"


    #Case sensitive
    if p_message == "!selfslremove" and len(sp_message) == 2:
        
        if(not movies.get(username)):
            movies[username] = dict()

        if(movies[username].get(sp_message[1]) == None):
            return "Movie not in list, check for case sensitive"
        del movies[username][sp_message[1]]
        return "Movie removed from the seenlist"
    
    

    if p_message == "!help":
        return """**Commands**```!wl                              - returns the list of movies to watch
!sl                              - return the list of movies already seen
!selfsl                          - return the list of movies already seen by the user
!wlimdb {movie name}             - returns the imdb link of the movie
!wladd {movie name} {imdb link}  - adds a movie to the watchlist
!wlremove {movie name}           - removes a movie from the watchlist
!sladd {movie name} {rating}     - adds a movie to the seenlist
!slremove {movie name}           - removes a movie from the seenlist
!selfsladd {movie name} {rating} - adds a movie to the user seenlist
!selfslremove {movie name}       - removes a movie from the user seenlist
!rndmov {int}                    - gives a random list of x movies from the Watchlist```"""
    

    return "Use !help"