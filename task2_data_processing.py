import pandas as pd
import glob


# Find the JSON file created by Task 1
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in the data folder.")
    exit()

# Get the JSON file name
json_file = json_files[0]

# Load the JSON data into a Pandas DataFrame
df = pd.read_json(json_file)

print(f"Loaded {len(df)} stories from {json_file}")


# Remove duplicate stories based on post_id
df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")


# Remove rows where post_id, title, or score is missing
df = df.dropna(subset=["post_id", "title", "score"])

print(f"After removing nulls: {len(df)}")


# Convert score and num_comments to numeric values
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(
    df["num_comments"],
    errors="coerce"
)

# Remove rows where conversion created missing values
df = df.dropna(subset=["score", "num_comments"])

# Convert both columns to integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# Remove stories with a score below 5
df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")


# Remove extra spaces from the beginning and end of titles
df["title"] = df["title"].str.strip()


# Save the cleaned data as a CSV file
output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")


# Print the number of stories in each category
print("\nStories per category:")

category_counts = df["category"].value_counts()

print(category_counts)