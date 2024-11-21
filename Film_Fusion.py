import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from math import sqrt

# Function to create a DataFrame of mutual ratings (movies rated by both users)
def create_movie_user_df(input_data, user1, user2):
    data = []
    for movie in input_data[user1].keys():
        if movie in input_data[user2].keys():
            try:
                data.append((movie, input_data[user1][movie], input_data[user2][movie]))
            except:
                pass
    return pd.DataFrame(data=data, columns=['movie', user1, user2])

# Function to calculate Pearson correlation
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # Find the number of elements
    n = len(si)

    # If they have no ratings in common, return 0
    if n == 0:
        return 0

    # Add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # Sum up the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum up the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate Pearson score
    num = pSum - (sum1 * sum2 / n) #num means numerator
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n)) #den means denominator
    if den == 0:
        return 0

    r = num / den # r means correlation coefficient
    return r 

# Function to add new ratings
def add_new_ratings(movie_user_preferences):
    user = input("Enter the name of the new user: ")
    movie_user_preferences[user] = {}

    while True:
        movie = input("Enter movie name (or type 'done' to finish): ")
        if movie.lower() == 'done':
            break
        rating = float(input(f"Enter rating for '{movie}': "))
        movie_user_preferences[user][movie] = rating
    
    return movie_user_preferences

# Function to load data from a CSV file
def load_data_from_csv(filename):
    return pd.read_csv(filename)

# Function to export DataFrame to CSV
def export_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Data has been saved to {filename}")

# Sample data: movie-user preferences
movie_user_preferences = {
    'Sam': {'Inception': 5, 'Titanic': 4, 'Avatar': 3},
    'William': {'Inception': 4, 'Titanic': 4, 'Avatar': 5},
    'Julia': {'Inception': 5, 'Titanic': 5, 'Avatar': 4}
}

# Option to add new ratings
add_new_ratings(movie_user_preferences)

# Select two users for similarity comparison
user1 = input("Enter the first user for comparison: ")
user2 = input("Enter the second user for comparison: ")

# Create DataFrame for visualization
df = create_movie_user_df(movie_user_preferences, user1, user2)

# Plot the scatter plot for the two selected users
plt.scatter(df[user1], df[user2])
plt.xlabel(user1)
plt.ylabel(user2)
for i, txt in enumerate(df.movie):
    plt.annotate(txt, (df[user1][i], df[user2][i]))
plt.title(f'Scatter plot of {user1} and {user2} ratings')
plt.show()

# Calculate Pearson correlation using the custom function
pearson_score = sim_pearson(movie_user_preferences, user1, user2)
print(f'Pearson correlation between {user1} and {user2}: {pearson_score}')

# Calculate Pearson correlation using scipy's pearsonr function for verification
scipy_score, _ = pearsonr(df[user1], df[user2])
print(f'Pearson correlation (scipy) between {user1} and {user2}: {scipy_score}')

# Visualize correlation with all users (optional)
all_users = list(movie_user_preferences.keys())
for user in all_users:
    if user != user1:
        df_user = create_movie_user_df(movie_user_preferences, user1, user)
        plt.scatter(df_user[user1], df_user[user])
        plt.xlabel(user1)
        plt.ylabel(user)
        for i, txt in enumerate(df_user.movie):
            plt.annotate(txt, (df_user[user1][i], df_user[user][i]))
        plt.title(f'Scatter plot of {user1} and {user} ratings')
        plt.show()

# Save the DataFrame to CSV file
export_to_csv(df, "movie_user_preferences.csv")

# Example usage to load from CSV
# df_from_csv = load_data_from_csv("movie_user_preferences.csv")
