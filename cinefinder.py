import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk

# Function to fetch movie/show data from OMDB API
def fetch_movie_data(title):
    api_key = 'fd03f4a6'
    url = f'http://www.omdbapi.com/?apikey={api_key}&s={title}'
    response = requests.get(url)
    return response.json()

# Function to fetch details of a selected movie/show
def display_movie_details(event=None):
    selected_item = treeview.selection()
    if selected_item:
        item = treeview.item(selected_item)
        movie_id = item['values'][0]
        api_key = 'fd03f4a6'
        url = f'http://www.omdbapi.com/?apikey={api_key}&i={movie_id}&plot=full'
        response = requests.get(url)
        movie_data = response.json()
        
        if movie_data['Response'] == 'True':
            details = f"Title: {movie_data['Title']}\n" \
                      f"Year: {movie_data['Year']}\n" \
                      f"Genre: {movie_data['Genre']}\n" \
                      f"IMDb Rating: {movie_data['imdbRating']}\n" \
                      f"Plot: {movie_data['Plot']}\n" \
                      f"Cast: {movie_data['Actors']}\n" \
                      f"Director: {movie_data['Director']}\n" \
                      f"Writer: {movie_data['Writer']}\n" \
                      f"Language: {movie_data['Language']}\n" \
                      f"Country: {movie_data['Country']}\n"
            
            # Add duration information for movies or web shows
            if movie_data['Type'] == 'movie':
                details += f"Duration: {movie_data['Runtime']}\n"
            elif movie_data['Type'] == 'series':
                details += f"Total Seasons: {movie_data['totalSeasons']}\n"
                total_episodes = 0
                for season in range(1, int(movie_data['totalSeasons']) + 1):
                    season_url = f'http://www.omdbapi.com/?apikey={api_key}&i={movie_id}&Season={season}'
                    season_response = requests.get(season_url)
                    season_data = season_response.json()
                    if season_data['Response'] == 'True':
                        total_episodes += len(season_data['Episodes'])
                details += f"Total Episodes: {total_episodes}\n"
            
            text_details.config(state=tk.NORMAL)
            text_details.delete('1.0', tk.END)
            text_details.insert(tk.END, details)
            text_details.config(state=tk.DISABLED)
            
            # Display movie/show poster on the right side
            poster_url = movie_data.get('Poster')
            if poster_url != 'N/A':
                image = Image.open(requests.get(poster_url, stream=True).raw)
                image = image.resize((int(root.winfo_width() / 3), int(root.winfo_height() / 2)), Image.BILINEAR)
                photo = ImageTk.PhotoImage(image)
                label_poster.config(image=photo)
                label_poster.image = photo
            else:
                label_poster.config(image=None)

            # Show details and poster frames
            frame_details.pack(side=tk.LEFT, padx=20, pady=20, fill='both', expand=True)
            frame_poster.pack(side=tk.LEFT, padx=20, pady=20)
            
        else:
            messagebox.showerror("Error", "Movie/show details not found!")

# Function to handle user input and display search results
def handle_input():
    title = entry_title.get()
    if title:
        treeview.delete(*treeview.get_children())  # Clear previous search results
        movie_data = fetch_movie_data(title)
        if movie_data['Response'] == 'True':
            search_results = movie_data['Search']
            if search_results:
                for result in search_results:
                    treeview.insert('', tk.END, values=(result['imdbID'], result['Title'], result['Year']))
                # Show the search results frame
                frame_results.pack(pady=20)
            else:
                messagebox.showwarning("No Results", "No movies/web shows found!")
        else:
            messagebox.showerror("Error", "API error occurred. Please try again later.")
    else:
        messagebox.showwarning("Input Required", "Please enter a movie/web show title.")
        clear_results()

# Function to clear search results and movie details
def clear_results():
    entry_title.delete(0, tk.END)
    treeview.delete(*treeview.get_children())
    text_details.config(state=tk.NORMAL)
    text_details.delete('1.0', tk.END)
    text_details.config(state=tk.DISABLED)
    label_poster.config(image=None)
    frame_results.pack_forget()
    frame_details.pack_forget()
    frame_poster.pack_forget()

# Create the main window
root = tk.Tk()
root.title("Movie/Show Details")
root.configure(bg='black')

# Make the window full screen
root.attributes('-fullscreen', True)

# Function to exit full-screen mode and close the application
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)
    root.destroy()

# Bind the Escape key to exit full-screen mode and close the application
root.bind("<Escape>", exit_fullscreen)

# Create input section
frame_input = tk.Frame(root, bg='black')
frame_input.pack(pady=20)

label_title = tk.Label(frame_input, text="Enter Movie/Web Show Title:", fg='white', bg='black', font=('Helvetica', 12))
label_title.grid(row=0, column=0)

entry_title = tk.Entry(frame_input, width=50, font=('Helvetica', 12))
entry_title.grid(row=0, column=1)

button_search = tk.Button(frame_input, text="Search", command=handle_input, fg='black', bg='white', font=('Helvetica', 12))
button_search.grid(row=0, column=2, padx=10)

button_clear = tk.Button(frame_input, text="Clear", command=clear_results, fg='black', bg='white', font=('Helvetica', 12))
button_clear.grid(row=0, column=3, padx=10)

# Create search results section
frame_results = tk.Frame(root, bg='black')

columns = ('ID', 'Title', 'Year')
treeview = ttk.Treeview(frame_results, columns=columns, show='headings', selectmode='browse')
treeview.heading('ID', text='ID')
treeview.heading('Title', text='Title')
treeview.heading('Year', text='Year')
treeview.column('ID', width=100, anchor=tk.CENTER)
treeview.column('Title', width=300, anchor=tk.CENTER)
treeview.column('Year', width=100, anchor=tk.CENTER)
treeview.pack(side=tk.LEFT)

scrollbar = ttk.Scrollbar(frame_results, orient='vertical', command=treeview.yview)
scrollbar.pack(side=tk.RIGHT, fill='y')
treeview.configure(yscrollcommand=scrollbar.set)

# Create details section
frame_details = tk.Frame(root, bg='black')

# Create poster section
frame_poster = tk.Frame(root, bg='black')

# Create labels for details and poster
label_details = tk.Label(frame_details, text="Movie/Web Show Details:", fg='white', bg='black', font=('Helvetica', 12))
label_details.pack()

label_poster = tk.Label(frame_poster, bg='black')
label_poster.pack()

# Create text widget for details
text_details = tk.Text(frame_details, width=40, height=20, wrap=tk.WORD, font=('Helvetica', 10))
text_details.pack(side=tk.LEFT, fill='both', expand=True)

# Bind click event to display details
treeview.bind("<ButtonRelease-1>", display_movie_details)

# Run the application
root.mainloop()
