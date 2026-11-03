import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from analysis import (
    load_data,
    clean_data,
    merge_data,
    calculate_movie_stats
)


def main():

    # Load the dataset
    movies, ratings = load_data()

    # Clean the data
    movies, ratings = clean_data(
        movies,
        ratings
    )

    # Merge movies and ratings
    merged = merge_data(
        movies,
        ratings
    )

    # Calculate movie statistics
    movie_stats = calculate_movie_stats(
        merged
    )

    # Keep movies with at least 5 ratings
    data = movie_stats[
        movie_stats["total_ratings"] >= 5
    ].copy()

    if len(data) < 3:
        print(
            "Not enough movies for clustering."
        )
        return

    # Log transformation reduces the influence
    # of extremely large rating counts.
    data["log_rating_count"] = np.log1p(
        data["total_ratings"]
    )

    # Select machine-learning features
    features = data[
        [
            "average_rating",
            "log_rating_count",
            "rating_std"
        ]
    ]

    # Standardize the features
    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        features
    )

    # Apply K-Means
    model = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    data["cluster"] = model.fit_predict(
        scaled_features
    )

    # Save the results
    output_file = (
        "output/movie_clusters.csv"
    )

    data.to_csv(
        output_file,
        index=False
    )

    print("\nMOVIE CLUSTERING RESULTS")
    print("=" * 50)

    print(
        data[
            [
                "title",
                "average_rating",
                "total_ratings",
                "cluster"
            ]
        ].head(20).to_string(index=False)
    )

    print("\nCLUSTER SUMMARY")
    print("=" * 50)

    summary = data.groupby(
        "cluster"
    ).agg(
        movie_count=("movieId", "count"),
        average_rating=("average_rating", "mean"),
        average_rating_count=("total_ratings", "mean"),
        average_rating_variability=("rating_std", "mean")
    )

    print(summary)

    print(
        f"\nCluster results saved to {output_file}"
    )


if __name__ == "__main__":
    main()

