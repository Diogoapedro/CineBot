from imdb import Cinemagoer
from neo4j import GraphDatabase
from dotenv import load_dotenv
from os import getenv

class movie:

    def __init__(self):
        load_dotenv()
        self.imdb = Cinemagoer()


    def connect(self):
        self.driver = GraphDatabase.driver(getenv("DB_URI"), auth=(getenv("DB_USERNAME"), getenv("DB_KEY")))
        with self.driver as driver:
            driver.verify_connectivity()


    def close(self):
        self.driver.close()


    def addUser(self, username):
        newUser = "CREATE (u:user { name: $userN, permission: False, banned: False })"
        records, summary, keys = self.driver.execute_query(
            newUser,
            userN = username,
            database_="neo4j",
        )
        return("user created")
 

    def checkUser(self, username) -> dict: # {username, banned}
        res = dict()
        userInfo = "MATCH (u:user) WHERE u.name = $userN RETURN (u)"
        records, summary, keys = self.driver.execute_query(
            userInfo,
            userN = username,
            database_="neo4j",
        )
        if(not records):
            print("no record")
            r = self.addUser(username)
            print(r)
            return self.checkUser(username)

        records = records[0]
        res["username"] = records["u"].get("name")
        res["banned"] = records["u"].get("banned")

        return res


    def checkMovie(self, movie) -> str: # imdb url
        movie = self.imdb.search_movie(movie)

        if(len(movie) == 0):
            print("no movie")
            return
        
        url = self.imdb.get_imdbURL(movie[0])

        return url


    def checkMovies(self, username) -> list: #[title]
        movieInfo = "MATCH (u:user) WHERE u.name = $userN MATCH (u)-[:watch]->(m:movie) RETURN m"
        records, summary, keys = self.driver.execute_query(
            movieInfo,
            userN = username,
            database_="neo4j",
        )
        if(not records):
            print("no record")
            return
        
        res = []

        for r in records:
            if(not r["m"].get("title")):
                continue
            res.append(r["m"].get("title"))

        return res
        

    def checkMoviesSeen(self, username) -> list: #{title: (url, rating)}
        moviesSeen = "MATCH (u:user) WHERE u.name = $userN MATCH (u)-[s:seen]->(m:movie) RETURN m, s"
        records, summary, keys = self.driver.execute_query(
            moviesSeen,
            userN = username,
            database_="neo4j",
        )
        if(not records):
            print("no record")
            return

        res = dict()

        for r in records:
            if(not r["m"].get("title")):
                continue
            res[r["m"].get("title")] = r["s"].get("rating")

        return res



    def randomMovies(self, username: str, num: int) -> list: #[titles]
        randomM = "MATCH (u:user) WHERE u.name = $userN MATCH (u)-[w:watch]->(m:movie) RETURN m, rand() as r ORDER BY r LIMIT $num"
        records, summary, keys = self.driver.execute_query(
            randomM,
            userN = username,
            num = num,
            database_="neo4j",
        )
        if(not records):
            print("no record")
            return

        res = []
        for r in records:
            if(not r[0].get("title")):
                continue
            res.append(r[0].get("title"))

        return res



    def remove(self,  rel: str, username: str, movie: str):
        if(rel == "watch"):
            removeRel = "MATCH (u:user)-[r:watch]->(m:movie) WHERE u.name = $userN AND m.title = $mov DELETE r"
        elif(rel == "seen"):
            removeRel = "MATCH (u:user)-[r:seen]->(m:movie) WHERE u.name = $userN AND m.title = $mov DELETE r"
        else:
            return
        
        records, summary, keys = self.driver.execute_query(
            removeRel,
            rela = rel,
            userN = username,
            mov = movie,
            database_="neo4j",
        )

        return "remove complete"
    


    def addNew(self, relation, user, movie_name, rating=None):
        
        if(not (relation in ["seen", "watch"])):
            return # ERROR

        movie = self.imdb.search_movie(movie_name)
        if(len(movie) == 0):
            return "No movie with that name" # or return False
        
        title = movie[0]["title"]
        
        matchMovie = "MATCH (m:movie) WHERE m.title = $mov RETURN m"
        records, summary, keys = self.driver.execute_query(
            matchMovie,
            mov = title,
            database_="neo4j",
        )

        if(not records):
            url = self.imdb.get_imdbURL(movie[0])
            self.newMovie(title, url)
        
        rela = self.checkRelation(user, title, relation)
        print(rela)
        if(not rela[0]):
            self.addRelation(user, title, relation, rating)
            if(rela[1] == "seen"):
                self.removeRelation(user, title)
        else:
            self.updateRelation(user, title, relation, rating)
        

        
    def newMovie(self, movie, url):
        movie_create = "CREATE (:movie { title: $mov, url: $url })"
        records, summary, keys = self.driver.execute_query(
            movie_create,
            mov = movie,
            url = url,
            teste = "teste",
            database_="neo4j",
        )

        return "new movie added"


    def checkRelation(self, username, movie, relation):
        s = ""
        if(relation == "seen"):
            newRel = "MATCH (u)-[:seen]->(m) WHERE u.name = $userN AND m.title = $mov RETURN u"
            s = "seen"
        elif(relation == "watch"):
            newRel = "MATCH (u)-[:watch]->(m) WHERE u.name = $userN AND m.title = $mov RETURN u"
            s = "watch"
        else:
            return
        
        records, summary, keys = self.driver.execute_query(
            newRel,
            userN = username,
            mov = movie,
            database_="neo4j",
        )

        if(records):
            return (True, s)
        else:
            return (False, s)

    
    def updateRelation(self, username, movie, relation, rating):
        if(relation == "seen"):
            updateRel = "MATCH (u)-[r:seen]->(m) WHERE u.name = $userN AND m.title = $mov SET r.rating = $rating"
        else:
            return

        records, summary, keys = self.driver.execute_query(
            updateRel,
            userN = username,
            mov = movie,
            rating = rating,
            database_="neo4j",
        )
        return "new relation added"



    def addRelation(self, username, movie, relation, rating=None):
        if(relation == "seen"):
            if(rating):
                newRel = "MATCH (u:user) WHERE u.name = $userN MATCH (m:movie) WHERE m.title = $mov CREATE (u)-[:seen { rating: $rating }]->(m)"
            else:
                newRel = "MATCH (u:user) WHERE u.name = $userN MATCH (m:movie) WHERE m.title = $mov CREATE (u)-[:seen]->(m)"
        elif(relation == "watch"):
            newRel = "MATCH (u:user) WHERE u.name = $userN MATCH (m:movie) WHERE m.title = $mov CREATE (u)-[:watch]->(m)"
        else:
            return

        records, summary, keys = self.driver.execute_query(
            newRel,
            userN = username,
            mov = movie,
            rating = rating,
            database_="neo4j",
        )
        return "new relation added"


    def removeRelation(self, user, movie):
        newRel = "MATCH (u)-[r:watch]->(m) WHERE u.name = $userN AND m.title = $mov DELETE r"
        
        records, summary, keys = self.driver.execute_query(
            newRel,
            userN = user,
            mov = movie,
            database_="neo4j",
        )
        
