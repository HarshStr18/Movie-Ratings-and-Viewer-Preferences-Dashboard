import pandas as pd
import numpy as np
from pathlib import Path

# -------------------------------------------------
# 1. DEFINE DATASET PATHS
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dataset"

MOVIES_FILE = DATA_DIR / "movies.csv"
RATINGS_FILE = DATA_DIR / "ratings.csv"


# -------------------------------------------------
# 2. LOAD DATA
# -------------------------------------------------

def load_data():

    if not MOVIES_FILE.exists():
        raise FileNotFoundError(
            f"Movie dataset not found: {MOVIES_FILE}"
        )

    if not RATINGS_FILE.exists():
        raise FileNotFoundError(
            f"Ratings dataset not found: {RATINGS_FILE}"
        )

    movies = pd.read_csv(MOVIES_FILE)
    ratings = pd.read_csv(RATINGS_FILE)

    return movies, ratings


# -------------------------------------------------
# 3. CLEAN DATA
# -------------------------------------------------

def clean_data(movies, ratings):

    movies = movies.copy()
    ratings = ratings.copy()

    # Remove duplicate movie IDs
    movies = movies.drop_duplicates(
        subset=["movieId"]
    )

    # Remove duplicate user-movie ratings
    ratings = ratings.drop_duplicates(
        subset=["userId", "movieId"]
    )

    # Convert rating columns to numeric values
    ratings["rating"] = pd.to_numeric(
        ratings["rating"],
        errors="coerce"
    )

    # Remove missing essential values
    movies = movies.dropna(
        subset=["movieId", "title", "genres"]
    )

    ratings = ratings.dropna(
        subset=["userId", "movieId", "rating"]
    )

    # Keep ratings within the expected MovieLens range
    ratings = ratings[
        ratings["rating"].between(0.5, 5.0)
    ]

    # Keep ratings associated with known movies
    ratings = ratings[
        ratings["movieId"].isin(movies["movieId"])
    ]

    # Convert movie IDs to integers
    movies["movieId"] = movies["movieId"].astype(int)
    ratings["movieId"] = ratings["movieId"].astype(int)

    return movies, ratings


# -------------------------------------------------
# 4. MERGE MOVIES AND RATINGS
# -------------------------------------------------

def merge_data(movies, ratings):

    merged = ratings.merge(
        movies,
        on="movieId",
        how="inner"
    )

    return merged


# -------------------------------------------------
# 5. CALCULATE MOVIE STATISTICS
# -------------------------------------------------

def calculate_movie_stats(merged):

    movie_stats = merged.groupby(
        ["movieId", "title"],
        as_index=False
    ).agg(
        average_rating=("rating", "mean"),
        total_ratings=("rating", "count"),
        rating_std=("rating", "std")
    )

    movie_stats["rating_std"] = (
        movie_stats["rating_std"].fillna(0)
    )

    return movie_stats


# -------------------------------------------------
# 6. CALCULATE WEIGHTED MOVIE RATINGS
# -------------------------------------------------

def calculate_weighted_ratings(movie_stats):

    result = movie_stats.copy()

    # Overall average rating
    global_mean = result["average_rating"].mean()

    # Minimum number of ratings needed for a
    # movie to qualify as sufficiently rated
    minimum_votes = 20

    # Weighted rating formula
    result["weighted_rating"] = (
        (
            result["total_ratings"]
            / (result["total_ratings"] + minimum_votes)
        )
        * result["average_rating"]
        +
        (
            minimum_votes
            / (result["total_ratings"] + minimum_votes)
        )
        * global_mean
    )

    return result


# -------------------------------------------------
# 7. ANALYZE GENRES
# -------------------------------------------------

def calculate_genre_stats(merged):

    genre_data = merged.copy()

    # Split multiple genres into separate rows
    genre_data["genres"] = (
        genre_data["genres"].str.split("|")
    )

    genre_data = genre_data.explode("genres")

    # Ignore the unknown-genre category
    genre_data = genre_data[
        genre_data["genres"] != "(no genres listed)"
    ]

    genre_stats = genre_data.groupby(
        "genres",
        as_index=False
    ).agg(
        average_rating=("rating", "mean"),
        total_ratings=("rating", "count"),
        unique_movies=("movieId", "nunique"),
        unique_users=("userId", "nunique")
    )

    return genre_stats.sort_values(
        "average_rating",
        ascending=False
    )


# -------------------------------------------------
# 8. ANALYZE RELEASE YEAR TRENDS
# -------------------------------------------------

def calculate_year_stats(movies, ratings):

    movie_data = movies.copy()

    # Extract year from titles such as Toy Story (1995)
    movie_data["year"] = pd.to_numeric(
        movie_data["title"].str.extract(
            r"\((\d{4})\)\s*$"
        )[0],
        errors="coerce"
    )

    merged = ratings.merge(
        movie_data[["movieId", "year"]],
        on="movieId",
        how="inner"
    )

    merged = merged.dropna(
        subset=["year"]
    )

    year_stats = merged.groupby(
        "year",
        as_index=False
    ).agg(
        average_rating=("rating", "mean"),
        total_ratings=("rating", "count"),
        unique_movies=("movieId", "nunique")
    )

    return year_stats.sort_values("year")


# -------------------------------------------------
# 9. PRINT SUMMARY
# -------------------------------------------------

def print_summary(movies, ratings, movie_stats, genre_stats):

    print("\n" + "=" * 55)
    print("MOVIE RATINGS AND VIEWER PREFERENCES ANALYSIS")
    print("=" * 55)

    print(f"\nTotal movies in dataset: {len(movies)}")
    print(f"Total ratings analyzed: {len(ratings)}")
    print(f"Unique users: {ratings['userId'].nunique()}")
    print(
        "Overall average rating: "
        f"{ratings['rating'].mean():.2f}/5"
    )

    print("\nTOP 10 MOVIES BY WEIGHTED RATING")
    print("-" * 55)

    eligible = movie_stats[
        movie_stats["total_ratings"] >= 20
    ]

    print(
        eligible.sort_values(
            "weighted_rating",
            ascending=False
        )[
            [
                "title",
                "average_rating",
                "total_ratings",
                "weighted_rating"
            ]
        ].head(10).to_string(index=False)
    )

    print("\nTOP 10 GENRES BY AVERAGE RATING")
    print("-" * 55)

    print(
        genre_stats[
            genre_stats["total_ratings"] >= 20
        ].head(10).to_string(index=False)
    )


# -------------------------------------------------
# 10. MAIN EXECUTION
# -------------------------------------------------

def main():

    movies, ratings = load_data()

    movies, ratings = clean_data(
        movies,
        ratings
    )

    merged = merge_data(
        movies,
        ratings
    )

    movie_stats = calculate_movie_stats(
        merged
    )

    movie_stats = calculate_weighted_ratings(
        movie_stats
    )

    genre_stats = calculate_genre_stats(
        merged
    )

    year_stats = calculate_year_stats(
        movies,
        ratings
    )

    # Create output directory
    output_dir = BASE_DIR / "output"
    output_dir.mkdir(exist_ok=True)

    # Save analysis results
    movie_stats.to_csv(
        output_dir / "movie_statistics.csv",
        index=False
    )

    genre_stats.to_csv(
        output_dir / "genre_statistics.csv",
        index=False
    )

    year_stats.to_csv(
        output_dir / "year_statistics.csv",
        index=False
    )

    print_summary(
        movies,
        ratings,
        movie_stats,
        genre_stats
    )

    print("\nAnalysis completed successfully!")
    print(f"Results saved in: {output_dir}")


if __name__ == "__main__":
    main()

