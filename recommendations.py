import pandas as pd

from analysis import (
    load_data,
    clean_data,
    merge_data,
    calculate_movie_stats,
    calculate_weighted_ratings
)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def main():

    # Load data
    movies, ratings = load_data()

    # Clean data
    movies, ratings = clean_data(
        movies,
        ratings
    )

    # Calculate movie ratings
    merged = merge_data(
        movies,
        ratings
    )

    stats = calculate_movie_stats(
        merged
    )

    stats = calculate_weighted_ratings(
        stats
    )

    # Combine movie information with statistics
    data = movies.merge(
        stats[
            [
                "movieId",
                "average_rating",
                "total_ratings",
                "weighted_rating"
            ]
        ],
        on="movieId",
        how="left"
    )

    # Replace missing genres with empty strings
    data["genres"] = data["genres"].fillna("")

    # Convert genre strings into numerical features
    vectorizer = CountVectorizer(
        tokenizer=str.split,
        token_pattern=None,
        lowercase=False
    )

    genre_matrix = vectorizer.fit_transform(
        data["genres"].str.replace(
            "|",
            " ",
            regex=False
        )
    )

    # Measure genre similarity
    similarity_matrix = cosine_similarity(
        genre_matrix
    )

    # Movie title to search for
    movie_name = input(
        "Enter a movie title: "
    ).strip()

    # Find matching movie titles
    matches = data[
        data["title"].str.contains(
            movie_name,
            case=False,
            na=False,
            regex=False
        )
    ]

    if matches.empty:

        print(
            "No matching movie was found."
        )
        return

    print("\nMatching movies:")

    print(
        matches[
            ["title", "genres"]
        ].head(10).to_string(index=False)
    )

    # Choose the first matching movie
    selected_index = matches.index[0]

    # Find its position in the matrix
    position = data.index.get_loc(
        selected_index
    )

    similarities = similarity_matrix[position]

    # Rank movies by genre similarity
    ranked_indices = similarities.argsort()[::-1]

    # Exclude the selected movie itself
    recommendations = []

    for idx in ranked_indices:

        if data.index[idx] == selected_index:
            continue

        row = data.iloc[idx]

        # Require at least 5 ratings
        if pd.isna(row["total_ratings"]):
            continue

        if row["total_ratings"] < 5:
            continue

        recommendations.append(
            {
                "title": row["title"],
                "genres": row["genres"],
                "average_rating": row["average_rating"],
                "weighted_rating": row["weighted_rating"],
                "similarity": similarities[idx]
            }
        )

        if len(recommendations) == 10:
            break

    if not recommendations:

        print(
            "No recommendations were found."
        )
        return

    result = pd.DataFrame(
        recommendations
    )

    print(
        f"\nRecommended movies similar to "
        f"{data.loc[selected_index, 'title']}:"
    )

    print(
        result.to_string(index=False)
    )


if __name__ == "__main__":
    main()

