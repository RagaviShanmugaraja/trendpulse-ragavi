import pandas as pd
import matplotlib.pyplot as plt
import os


# ---------------------------------------------------------
# STEP 1: Load the analysed CSV
# ---------------------------------------------------------

file_path = "data/trends_analysed.csv"

df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}")


# Create the outputs folder if it does not already exist
os.makedirs("outputs", exist_ok=True)


# ---------------------------------------------------------
# CHART 1: Top 10 Stories by Score
# ---------------------------------------------------------

# Select the 10 stories with the highest scores
top_stories = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..."
    if len(title) > 50
    else title
)

# Reverse the order so the highest score appears at the top
top_stories = top_stories.sort_values("score")

plt.figure(figsize=(10, 6))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

plt.tight_layout()

# Save before showing the chart
plt.savefig("outputs/chart1_top_stories.png")

plt.show()

# Close the figure after displaying it
plt.close()


# ---------------------------------------------------------
# CHART 2: Stories per Category
# ---------------------------------------------------------

category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 6))

# Use a different colour for each category
plt.bar(
    category_counts.index,
    category_counts.values,
    color=[
        "skyblue",
        "lightgreen",
        "orange",
        "violet",
        "salmon"
    ]
)

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.tight_layout()

# Save before showing the chart
plt.savefig("outputs/chart2_categories.png")

plt.show()

plt.close()


# ---------------------------------------------------------
# CHART 3: Score vs Comments
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))


# Separate popular and non-popular stories
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]


# Plot non-popular stories
plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    alpha=0.7
)


# Plot popular stories
plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)


plt.title("Score vs Number of Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

plt.legend()

plt.tight_layout()

# Save before showing the chart
plt.savefig("outputs/chart3_scatter.png")

plt.show()

plt.close()


# ---------------------------------------------------------
# BONUS: Create a combined dashboard
# ---------------------------------------------------------

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Overall dashboard title
fig.suptitle(
    "TrendPulse Dashboard",
    fontsize=18
)


# ---------------------------------------------------------
# Dashboard Chart 1
# ---------------------------------------------------------

axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)

axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")


# ---------------------------------------------------------
# Dashboard Chart 2
# ---------------------------------------------------------

axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=[
        "skyblue",
        "lightgreen",
        "orange",
        "violet",
        "salmon"
    ]
)

axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")


# ---------------------------------------------------------
# Dashboard Chart 3
# ---------------------------------------------------------

axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    alpha=0.7
)

axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)

axes[1, 0].set_title("Score vs Number of Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")
axes[1, 0].legend()


# The fourth dashboard area is unused
axes[1, 1].axis("off")


# Adjust spacing
plt.tight_layout()

# Save the dashboard
plt.savefig("outputs/dashboard.png")

plt.show()

plt.close()


print("\nAll charts saved successfully.")