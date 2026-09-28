import pandas as pd
import numpy as np


# ---------------------------------------------------------
# STEP 1: Load and explore the clean CSV
# ---------------------------------------------------------

# Load the CSV created by Task 2
file_path = "data/trends_clean.csv"

df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}")


# Print the first 5 rows
print("\nFirst 5 rows:")
print(df.head())


# Calculate average score and average number of comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")


# ---------------------------------------------------------
# STEP 2: Basic analysis using NumPy
# ---------------------------------------------------------

# Convert the score column into a NumPy array
scores = df["score"].to_numpy()

# Calculate mean, median and standard deviation
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

# Find maximum and minimum scores
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")

print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")


# ---------------------------------------------------------
# Find the category with the most stories
# ---------------------------------------------------------

category_counts = df["category"].value_counts()

most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print(
    f"\nMost stories in: "
    f"{most_common_category} "
    f"({most_common_count} stories)"
)


# ---------------------------------------------------------
# Find the story with the most comments
# ---------------------------------------------------------

most_commented_index = df["num_comments"].idxmax()

most_commented_title = df.loc[
    most_commented_index,
    "title"
]

most_commented_count = df.loc[
    most_commented_index,
    "num_comments"
]

print(
    f'\nMost commented story: '
    f'"{most_commented_title}" '
    f'— {most_commented_count} comments'
)


# ---------------------------------------------------------
# STEP 3: Add new columns
# ---------------------------------------------------------

# Engagement measures comments per upvote
df["engagement"] = (
    df["num_comments"] / (df["score"] + 1)
)


# Mark stories whose score is above the average score
df["is_popular"] = df["score"] > average_score


# ---------------------------------------------------------
# STEP 4: Save the analysed data
# ---------------------------------------------------------

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")