# CineFinder

**Project Description**<br>
Developed a Python-based application using the Tkinter library that allows users to search for movies and web shows, view a list of matching results, and display detailed information for a selected title.

<u>**Key Features**</u>:
1. User Input Handling: Users can input a movie or web show title in a search bar.
2. Search Functionality:
  Utilizes the OMDB API to search for titles matching the user input.
  Displays search results in a list using a Tkinter Treeview widget.
3. Detailed Information Display: Upon selecting a title from the search results, fetches detailed information about the movie or web show, including title, year, genre, IMDb rating, plot, cast, director, writer, language, country, duration (for movies), and total seasons and episodes (for web shows).
4. Poster Display: Fetches and displays the poster image of the selected title using the PIL library.
5. Error Handling: Provides user feedback for various error conditions (e.g., no results found, API errors).
6. Full-Screen Mode: The application runs in full-screen mode, with an option to exit using the Escape key.

<u>**Technologies Used**</u>:<br>
1. Programming Language: Python
2. GUI Library: Tkinter for the graphical user interface
3. API Integration: OMDB API for fetching movie and web show data
4. Image Processing: PIL (Pillow) for handling and displaying poster images
