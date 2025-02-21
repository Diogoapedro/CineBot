# CineBot 🎬

CineBot is a Discord bot that helps users track the movies they've watched, manage multiple watchlists (including server-wide and personal lists), and rate films. It utilizes **Python**, **Neo4j**, and **Cinemagoer** (formerly IMDbPY) to fetch movie data from IMDb.

<div>
    <img height="48" width="48" src="https://cdn.simpleicons.org/discord/5865f2" style="margin-right: 12px;" />
    <img height="48" width="48" src="https://cdn.simpleicons.org/python/3879af" style="margin-right: 12px;" />
    <img height="48" width="48" src="https://cdn.simpleicons.org/neo4j/038bff" style="margin-right: 12px;" />
    <img height="48" width="48" src="https://cdn.simpleicons.org/imdb/[COLOR]" />
</div>


## 🚀 Features
- **Manage Watchlists:** Add or remove movies from your personal or server-wide watchlist.
- **Track Watched Movies:** Maintain a list of seen movies with ratings.
- **Fetch IMDb Data:** Get IMDb links for movies.
- **Random Movie Picker:** Get a random selection of movies from your watchlist.
- **Multiple Lists:** Support for private, server, and personal lists.

## 📜 Commands

### Watchlist Commands
| Command | Description |
|---------|-------------|
| `!wl` | Returns the list of movies to watch. |
| `!wl add {movie name}` | Adds a movie to the watchlist. |
| `!wl rm {movie name}` | Removes a movie from the watchlist. |

### Seenlist Commands
| Command | Description |
|---------|-------------|
| `!sl` | Returns the list of movies already seen. |
| `!sl add {movie name} {rating}` | Adds a movie to the seen list with a rating. |
| `!sl rm {movie name}` | Removes a movie from the seen list. |

### Movie Info & Randomizer
| Command | Description |
|---------|-------------|
| `!mov {movie name}` | Returns the IMDb link for the specified movie. |
| `!rnd {int}` | Returns a random list of X movies from the watchlist. |

### List Variants
- **Personal Lists:** Add an `s` before the `!` to use your personal list. (`s!wl`, `s!sl` etc.)
- **Private Messages:** Add a `p` before the `!` to manage lists privately. (`p!wl`, `p!sl` etc.)

### Help Command
| Command | Description |
|---------|-------------|
| `!help` | Displays all available commands and usage information. |

## 🛠️ Setup & Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/Diogoapedro/CineBot.git
   cd CineBot
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up Neo4j Database**
   - Install Neo4j and create a database.
   - Configure the connection details in the bot settings with the following step.
3. **Create a `.env` file**
   Inside the project directory, create a `.env` file and add the following variables:
   ```sh
   TOKEN=your_discord_bot_token
   DB_URI=your_neo4j_database_uri
   DB_USERNAME=your_neo4j_username
   DB_KEY=your_neo4j_password
   ```
5. **Run the bot**
   ```sh
   python bot.py
   ```

## ⚡ Technologies Used
- **Python** – Core language
- **Discord.py** – Bot framework
- **Neo4j** – Graph database for storing movie lists
- **Cinemagoer (IMDbPY)** – Fetch movie data from IMDb

## 📜 License
This project is licensed under the MIT License.

---
💡 **Have suggestions or feature requests?** Feel free to open an issue or contribute! 🎥🍿
