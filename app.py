# ============================================================
# MOVIE RATINGS ANALYSIS DASHBOARD
# ============================================================
# Project Title:
# Analysis of Movie Ratings and Viewer Preferences for
# Understanding Popularity Patterns and Entertainment Trends
#
# Technologies:
# Python, Pandas, Streamlit, Plotly
#
# Features:
# 1. Complete project title
# 2. Search movies by title
# 3. Individual movie details
# 4. Movie rating distribution
# 5. Popular movies ranking
# 6. Genre analysis
# 7. Release-year analysis
# 8. Overall rating distribution
# 9. Sidebar filters
# 10. CSV downloads
# 11. Dark dashboard styling
# 12. Cached data and efficient aggregation
# ============================================================

from pathlib import Path
import html
import re

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Movie Ratings & Viewer Preferences",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. CUSTOM DARK THEME
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root { --bg:#070B14; --panel:#0F1728; --panel2:#121D31; --line:rgba(148,163,184,.16); --muted:#9BAAC0; --text:#EDF4FF; --cyan:#67E8F9; --blue:#818CF8; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background: radial-gradient(ellipse at 12% 0%, rgba(34,211,238,.09), transparent 30%), radial-gradient(ellipse at 90% 5%, rgba(99,102,241,.12), transparent 28%), var(--bg); color:var(--text); }
    [data-testid="stHeader"] { background:rgba(7,11,20,.75); }
    [data-testid="stToolbar"] { right:1rem; }
    .block-container { max-width:1500px; padding-top:1.6rem; padding-bottom:2.5rem; }
    h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.035em; color:#F4F8FF; }
    h2 { margin-top:.35rem !important; }
    p, label, .stCaption { color:#C4D0E1; }
    section[data-testid="stSidebar"] { background:linear-gradient(180deg,#0D1525 0%,#0A101D 100%); border-right:1px solid var(--line); }
    section[data-testid="stSidebar"] > div { padding-top:1.5rem; }
    .brand-lockup { display:flex; align-items:center; gap:.8rem; padding:.2rem .1rem 1.2rem; }
    .brand-icon { width:48px; height:48px; flex:0 0 48px; display:flex; align-items:center; justify-content:center; }
    .brand-icon svg { display:block; width:100%; height:100%; }
    .brand-copy { min-width:0; }
    .brand-name { font-family:'Space Grotesk',sans-serif; font-size:1.65rem; font-weight:700; letter-spacing:-.07em; line-height:1.05; white-space:nowrap; }
    .brand-name span:first-child { color:#F4F8FF; }
    .brand-name span:last-child { color:#67E8F9; }
    .brand-tagline { margin-top:.35rem; color:#8FA3BE; font-size:.62rem; font-weight:700; letter-spacing:.2em; }
    .sidebar-section-label { color:#91A2BB; font-size:.68rem; font-weight:700; letter-spacing:.14em; padding:.15rem .1rem .4rem; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color:var(--cyan); }
    [data-testid="stMetric"] { background:linear-gradient(145deg,rgba(18,29,49,.96),rgba(12,20,35,.96)); border:1px solid var(--line); border-radius:18px; padding:18px 20px; box-shadow:0 12px 32px rgba(0,0,0,.16); transition:transform .2s ease,border-color .2s ease; }
    [data-testid="stMetric"]:hover { transform:translateY(-3px); border-color:rgba(103,232,249,.42); }
    [data-testid="stMetricLabel"] { color:#A9B8CD !important; font-weight:600; }
    [data-testid="stMetricValue"] { color:var(--cyan) !important; font-family:'Space Grotesk',sans-serif; font-weight:700; }
    [data-testid="stMetricDelta"] { font-size:.8rem; }
    .main-title { font-family:'Space Grotesk',sans-serif; font-size:clamp(2rem,4vw,3.2rem); font-weight:700; letter-spacing:-.055em; line-height:1.12; text-align:left; margin:0; background:linear-gradient(100deg,#F8FAFC 5%,#A5F3FC 48%,#A5B4FC 95%); -webkit-background-clip:text; background-clip:text; color:transparent; }
    .hero-wrap { position:relative; overflow:hidden; padding:2.1rem 2.2rem 1.8rem; border:1px solid rgba(103,232,249,.18); border-radius:24px; background:linear-gradient(120deg,rgba(15,23,42,.97),rgba(15,23,42,.78)), radial-gradient(circle at 95% 10%,rgba(99,102,241,.25),transparent 38%); box-shadow:0 20px 60px rgba(0,0,0,.22); margin-bottom:1.3rem; }
    .hero-wrap:after { content:'🎬'; position:absolute; right:4%; top:12%; font-size:5.5rem; opacity:.12; filter:grayscale(.1); }
    .hero-kicker { display:inline-block; color:#A5F3FC; border:1px solid rgba(103,232,249,.25); background:rgba(34,211,238,.08); padding:.35rem .7rem; border-radius:999px; font-size:.75rem; letter-spacing:.12em; text-transform:uppercase; font-weight:700; margin-bottom:1rem; }
    .subtitle { color:#AAB8CC; font-size:1.02rem; line-height:1.7; max-width:780px; margin-top:.9rem; margin-bottom:0; }
    .section-title { color:#E8F7FF; font-family:'Space Grotesk',sans-serif; font-size:1.45rem; font-weight:700; margin:1.7rem 0 .85rem; padding-left:.8rem; border-left:3px solid var(--cyan); }
    .info-card { background:linear-gradient(145deg,rgba(18,29,49,.95),rgba(12,20,35,.95)); border:1px solid var(--line); border-radius:18px; padding:1.25rem; margin-bottom:1rem; }
    .movie-title { color:var(--cyan); font-family:'Space Grotesk',sans-serif; font-size:1.5rem; font-weight:700; overflow-wrap:anywhere; }
    div[data-testid="stPlotlyChart"], div[data-testid="stDataFrame"], div[data-testid="stTable"] { border:1px solid rgba(148,163,184,.13); border-radius:16px; overflow:hidden; }
    button[data-baseweb="tab"] { color:#AAB8CC; font-weight:650; padding:.8rem 1rem; }
    button[data-baseweb="tab"][aria-selected="true"] { color:var(--cyan) !important; }
    div[data-baseweb="tab-highlight"] { background:var(--cyan) !important; height:3px; }
    div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button { border:1px solid rgba(103,232,249,.28); border-radius:11px; background:linear-gradient(110deg,rgba(34,211,238,.12),rgba(99,102,241,.12)); color:#E8F7FF; font-weight:650; transition:all .18s ease; }
    div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover { border-color:var(--cyan); color:white; transform:translateY(-1px); }
    input, textarea { border-radius:10px !important; }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div { background:#101A2B; border-color:rgba(148,163,184,.22); border-radius:10px; }
    [data-testid="stSlider"] [role="slider"] { background:var(--cyan); }
    hr { border-color:var(--line); margin:1.5rem 0; }
    .footer { text-align:center; color:#8998AE; margin-top:3rem; padding:1.5rem 1rem; border-top:1px solid var(--line); line-height:1.8; }
    .footer b { color:#DCEBFA; }
    @media(max-width:700px) { .block-container { padding-left:1rem; padding-right:1rem; } .hero-wrap { padding:1.4rem; border-radius:18px; } .hero-wrap:after { right:3%; top:8%; font-size:3.5rem; } .subtitle { max-width:90%; font-size:.93rem; } }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. COMPLETE PROJECT TITLE
# ============================================================

st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-kicker">MOVIE DATA INTELLIGENCE · DASHBOARD</div>
        <div class="main-title">Discover the story<br>behind every rating.</div>
        <div class="subtitle">
            Analysis of Movie Ratings and Viewer Preferences for Understanding
            Popularity Patterns and Entertainment Trends. Explore audience scores,
            genre patterns, release timelines, and the movies people love.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. FIND DATASET FILES
# ============================================================

def find_file(filename):
    """
    Search common project folders for a dataset file.

    Supported locations:
    - dataset/
    - data/
    - Project root
    - ml-latest-small/
    - ml-latest/
    """

    project_folder = Path(__file__).resolve().parent

    possible_paths = [
        project_folder / "dataset" / filename,
        project_folder / "data" / filename,
        project_folder / filename,
        project_folder / "ml-latest-small" / filename,
        project_folder / "ml-latest" / filename
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None


# ============================================================
# 5. LOAD AND PROCESS DATA
# ============================================================

@st.cache_data(show_spinner="Loading movie data and calculating statistics...")
def load_data(movies_path, ratings_path):
    """
    Load the CSV files and calculate movie statistics.

    Aggregation is performed before displaying the results.
    This prevents Plotly charts from receiving millions of
    individual rating rows unnecessarily.
    """

    # Load movie information
    movies = pd.read_csv(
        movies_path,
        usecols=["movieId", "title", "genres"]
    )

    # Load rating information
    ratings = pd.read_csv(
        ratings_path,
        usecols=["movieId", "rating"]
    )

    # Ensure the important columns use numeric types
    movies["movieId"] = pd.to_numeric(
        movies["movieId"],
        errors="coerce"
    )

    ratings["movieId"] = pd.to_numeric(
        ratings["movieId"],
        errors="coerce"
    )

    ratings["rating"] = pd.to_numeric(
        ratings["rating"],
        errors="coerce"
    )

    # Remove invalid rows
    movies = movies.dropna(
        subset=["movieId", "title", "genres"]
    )

    ratings = ratings.dropna(
        subset=["movieId", "rating"]
    )

    movies["movieId"] = movies["movieId"].astype("int64")
    ratings["movieId"] = ratings["movieId"].astype("int64")

    # --------------------------------------------------------
    # Calculate statistics for each movie
    # --------------------------------------------------------

    movie_stats = (
        ratings.groupby("movieId")["rating"]
        .agg(
            average_rating="mean",
            rating_count="count",
            rating_std="std"
        )
        .reset_index()
    )

    # --------------------------------------------------------
    # Calculate the global mean rating
    # --------------------------------------------------------

    if ratings.empty:
        global_mean = 0.0
    else:
        global_mean = float(ratings["rating"].mean())

    # Minimum number of ratings used for weighted ranking.
    # This is a configurable ranking parameter, not a
    # statistical confidence guarantee.
    minimum_votes = 20

    # --------------------------------------------------------
    # Calculate a Bayesian-style weighted rating
    # --------------------------------------------------------
    #
    # Weighted Rating =
    # (v / (v + m)) * R + (m / (v + m)) * C
    #
    # R = Movie's average rating
    # v = Number of ratings for the movie
    # m = Minimum rating-count parameter
    # C = Average rating across the entire dataset
    #
    # This prevents a movie with very few ratings from
    # automatically outranking movies with stronger evidence.
    # --------------------------------------------------------

    movie_stats["weighted_rating"] = (
        (
            movie_stats["rating_count"]
            / (movie_stats["rating_count"] + minimum_votes)
        )
        * movie_stats["average_rating"]
        +
        (
            minimum_votes
            / (movie_stats["rating_count"] + minimum_votes)
        )
        * global_mean
    )

    # --------------------------------------------------------
    # Extract release year from movie titles
    # --------------------------------------------------------

    movies["release_year"] = pd.to_numeric(
        movies["title"].str.extract(r"\((\d{4})\)\s*$")[0],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Merge movie information and calculated statistics
    # --------------------------------------------------------

    catalog = movies.merge(
        movie_stats,
        on="movieId",
        how="left"
    )

    # Fill missing values for movies without ratings
    catalog["average_rating"] = catalog["average_rating"].fillna(0)
    catalog["rating_count"] = catalog["rating_count"].fillna(0)
    catalog["rating_std"] = catalog["rating_std"].fillna(0)
    catalog["weighted_rating"] = catalog["weighted_rating"].fillna(0)

    catalog["rating_count"] = catalog["rating_count"].astype("int64")

    # --------------------------------------------------------
    # Prepare genre information
    # --------------------------------------------------------

    catalog["genre_list"] = catalog["genres"].apply(
        lambda value: [
            genre for genre in str(value).split("|")
            if genre and genre != "(no genres listed)"
        ]
    )

    # --------------------------------------------------------
    # Overall rating distribution
    # --------------------------------------------------------

    global_distribution = (
        ratings["rating"]
        .value_counts()
        .sort_index()
        .rename_axis("rating")
        .reset_index(name="count")
    )

    # --------------------------------------------------------
    # Per-movie rating distribution
    # --------------------------------------------------------

    rating_distribution = (
        ratings.groupby(["movieId", "rating"])
        .size()
        .reset_index(name="count")
    )

    # Release year is optional, so retain movies without it.
    # All other returned data is aggregated for efficient
    # dashboard rendering.
    return (
        catalog,
        rating_distribution,
        global_distribution,
        global_mean,
        len(ratings)
    )


# ============================================================
# 6. CHECK DATASET FILES
# ============================================================

movies_file = find_file("movies.csv")
ratings_file = find_file("ratings.csv")

if movies_file is None or ratings_file is None:
    st.error("Dataset files could not be found.")

    st.markdown(
        """
        ### Required folder structure

        Make sure your project contains:

        ```text
        Movie-Ratings-Analysis/
        ├── app.py
        └── dataset/
            ├── movies.csv
            └── ratings.csv
        ```

        Both CSV files must contain the expected MovieLens
        columns: `movieId`, `title`, `genres` in movies.csv,
        and `movieId`, `rating` in ratings.csv.
        """
    )

    st.stop()


# ============================================================
# 7. LOAD DATASET
# ============================================================

try:
    (
        catalog,
        rating_distribution,
        global_distribution,
        global_mean,
        total_rating_rows
    ) = load_data(
        str(movies_file),
        str(ratings_file)
    )

except Exception as error:
    st.error(
        "The dataset could not be loaded. "
        "Please verify the CSV column names and file contents."
    )

    st.exception(error)
    st.stop()


if catalog.empty:
    st.warning("The movies dataset contains no usable movie records.")
    st.stop()


# ============================================================
# 8. SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown(
    """
    <div class="brand-lockup">
        <div class="brand-icon" aria-hidden="true">
            <svg viewBox="0 0 64 64" role="img" xmlns="http://www.w3.org/2000/svg">
                <rect x="5" y="18" width="54" height="40" rx="10" fill="#111C36" stroke="#67E8F9" stroke-width="2.5"/>
                <path d="M8 17 14 5h45l-6 12Z" fill="#818CF8" stroke="#818CF8" stroke-width="2" stroke-linejoin="round"/>
                <path d="m18 7 6 8M31 7l6 8M44 7l6 8" stroke="#0B1220" stroke-width="4" stroke-linecap="round"/>
                <circle cx="32" cy="38" r="13" fill="#0B1220" stroke="#67E8F9" stroke-width="2.5"/>
                <path d="m22 42 7-7 6 4 8-10" fill="none" stroke="#A5B4FC" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="43" cy="29" r="3" fill="#67E8F9"/>
            </svg>
        </div>
        <div class="brand-copy">
            <div class="brand-name"><span>Cine</span><span>Scope</span></div>
            <div class="brand-tagline">MOVIE INSIGHTS</div>
        </div>
    </div>
    <div class="sidebar-section-label">EXPLORE DASHBOARD</div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# Search by movie title
search_text = st.sidebar.text_input(
    "🔎 Search Movie",
    placeholder="Example: Toy Story"
)

# Get all available genres
all_genres = sorted(
    {
        genre
        for genre_list in catalog["genre_list"]
        for genre in genre_list
    }
)

selected_genres = st.sidebar.multiselect(
    "🎭 Filter by Genre",
    options=all_genres,
    default=[]
)

# Get available release years
available_years = catalog["release_year"].dropna()

if not available_years.empty:
    minimum_year = int(available_years.min())
    maximum_year = int(available_years.max())

    if minimum_year < maximum_year:
        selected_years = st.sidebar.slider(
            "📅 Release Year Range",
            min_value=minimum_year,
            max_value=maximum_year,
            value=(minimum_year, maximum_year)
        )
    else:
        selected_years = (minimum_year, maximum_year)

else:
    selected_years = None

# Minimum number of ratings
minimum_ratings = st.sidebar.number_input(
    "⭐ Minimum Number of Ratings",
    min_value=0,
    value=0,
    step=10
)

# Ranking method
sort_option = st.sidebar.selectbox(
    "📊 Rank Movies By",
    options=[
        "Weighted Popularity",
        "Average Rating",
        "Most Rated",
        "Movie Title"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Data is aggregated and cached to improve dashboard performance."
)


# ============================================================
# 9. FILTER THE MOVIE CATALOG
# ============================================================

filtered_catalog = catalog.copy()

# Filter by genre.
# A movie is retained if it has at least one selected genre.
if selected_genres:
    filtered_catalog = filtered_catalog[
        filtered_catalog["genre_list"].apply(
            lambda genres: any(
                genre in genres for genre in selected_genres
            )
        )
    ]

# Filter by release year
if selected_years is not None:
    filtered_catalog = filtered_catalog[
        filtered_catalog["release_year"].between(
            selected_years[0],
            selected_years[1],
            inclusive="both"
        )
        | filtered_catalog["release_year"].isna()
    ]

# Filter by minimum number of ratings
filtered_catalog = filtered_catalog[
    filtered_catalog["rating_count"] >= minimum_ratings
]

# Sort the catalog
if sort_option == "Weighted Popularity":
    filtered_catalog = filtered_catalog.sort_values(
        "weighted_rating",
        ascending=False
    )

elif sort_option == "Average Rating":
    filtered_catalog = filtered_catalog.sort_values(
        ["average_rating", "rating_count"],
        ascending=[False, False]
    )

elif sort_option == "Most Rated":
    filtered_catalog = filtered_catalog.sort_values(
        "rating_count",
        ascending=False
    )

else:
    filtered_catalog = filtered_catalog.sort_values(
        "title",
        ascending=True
    )


# ============================================================
# 10. OVERVIEW METRICS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Dashboard Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Movies",
        f"{len(catalog):,}"
    )

with col2:
    st.metric(
        "Total Ratings",
        f"{total_rating_rows:,}"
    )

with col3:
    st.metric(
        "Average Dataset Rating",
        f"{global_mean:.2f} / 5"
    )

with col4:
    st.metric(
        "Movies After Filters",
        f"{len(filtered_catalog):,}"
    )


# ============================================================
# 11. MOVIE SEARCH AND DETAILS
# ============================================================

st.markdown(
    '<div class="section-title">🎬 Movie Search & Details</div>',
    unsafe_allow_html=True
)

if search_text.strip():

    # Case-insensitive partial title search
    search_results = catalog[
        catalog["title"].str.contains(
            search_text.strip(),
            case=False,
            na=False,
            regex=False
        )
    ].copy()

    if search_results.empty:
        st.warning(
            f"No movies found matching '{search_text}'. "
            "Try a different title or keyword."
        )

    else:
        st.success(
            f"Found {len(search_results):,} matching movie(s)."
        )

        # Display a manageable number of search results
        st.dataframe(
            search_results[
                [
                    "title",
                    "genres",
                    "release_year",
                    "average_rating",
                    "rating_count",
                    "weighted_rating"
                ]
            ].head(100),
            use_container_width=True,
            hide_index=True,
            column_config={
                "title": "Movie Title",
                "genres": "Genres",
                "release_year": st.column_config.NumberColumn(
                    "Release Year",
                    format="%d"
                ),
                "average_rating": st.column_config.NumberColumn(
                    "Average Rating",
                    format="%.2f"
                ),
                "rating_count": st.column_config.NumberColumn(
                    "Total Ratings",
                    format="%d"
                ),
                "weighted_rating": st.column_config.NumberColumn(
                    "Weighted Score",
                    format="%.2f"
                )
            }
        )

        # Choose a specific movie to inspect
        movie_options = search_results["title"].tolist()

        selected_movie_title = st.selectbox(
            "Select a movie to view its details",
            options=movie_options
        )

        movie = search_results[
            search_results["title"] == selected_movie_title
        ].iloc[0]

        movie_id = int(movie["movieId"])

        left, right = st.columns([1, 1])

        # ----------------------------------------------------
        # Movie details displayed as normal Streamlit text
        # ----------------------------------------------------

        with left:
            st.subheader("🎬 Movie Details")

            st.header(str(movie["title"]))

            st.write(
                "**Genres:**",
                str(movie["genres"]).replace("|", " · ")
            )

            if pd.notna(movie["release_year"]):
                st.write(
                    "**Release year:**",
                    int(movie["release_year"])
                )
            else:
                st.write("**Release year:** Unknown")

            if movie["rating_count"] > 0:
                st.write(
                    f"**Average rating:** "
                    f"{movie['average_rating']:.2f} / 5"
                )
            else:
                st.write("**Average rating:** No ratings available")

            st.write(
                f"**Total ratings:** {int(movie['rating_count']):,}"
            )

            st.write(
                f"**Weighted popularity score:** "
                f"{movie['weighted_rating']:.2f} / 5"
            )

            if movie["rating_count"] > 1:
                st.write(
                    f"**Rating standard deviation:** "
                    f"{movie['rating_std']:.2f}"
                )
            else:
                st.write("**Rating standard deviation:** Not enough data")

            st.caption(
                "Weighted popularity considers both the average "
                "rating and the number of ratings."
            )

        # ----------------------------------------------------
        # Selected movie rating distribution
        # ----------------------------------------------------

        with right:
            st.subheader("⭐ Movie Rating Distribution")

            selected_distribution = rating_distribution[
                rating_distribution["movieId"] == movie_id
            ].copy()

            if not selected_distribution.empty:
                selected_distribution = selected_distribution.sort_values(
                    "rating"
                )

                fig_movie = px.bar(
                    selected_distribution,
                    x="rating",
                    y="count",
                    text="count",
                    labels={
                        "rating": "Rating",
                        "count": "Number of Ratings"
                    },
                    title="How Viewers Rated This Movie"
                )

                fig_movie.update_traces(
                    textposition="outside"
                )

                fig_movie.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#080D1A",
                    plot_bgcolor="#111827",
                    font_color="#F1F5F9",
                    xaxis=dict(
                        tickmode="linear",
                        dtick=0.5
                    ),
                    margin=dict(
                        l=20,
                        r=20,
                        t=60,
                        b=20
                    )
                )

                st.plotly_chart(
                    fig_movie,
                    use_container_width=True
                )

            else:
                st.info("No rating distribution is available.")

        st.markdown("---")

else:
    st.info(
        "Enter a movie title in the sidebar to search for a "
        "specific movie and view its complete details."
    )


# ============================================================
# 12. DASHBOARD ANALYTICS TABS
# ============================================================

st.markdown(
    '<div class="section-title">📈 Explore Movie Analytics</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🔥 Popular Movies",
        "⭐ Rating Analysis",
        "🎭 Genre Analysis",
        "📅 Yearly Trends",
        "📋 Movie Catalog"
    ]
)


# ============================================================
# TAB 1: POPULAR MOVIES
# ============================================================

with tab1:
    st.subheader("🔥 Top Movies")

    if filtered_catalog.empty:
        st.warning("No movies match your current filters.")

    else:
        # Only plot the top 20 movies to keep charts readable
        top_movies = filtered_catalog.head(20).copy()

        if sort_option == "Movie Title":
            top_movies = top_movies.sort_values(
                "weighted_rating",
                ascending=True
            )

        else:
            top_movies = top_movies.sort_values(
                "weighted_rating",
                ascending=True
            )

        fig_popular = px.bar(
            top_movies,
            x="weighted_rating",
            y="title",
            orientation="h",
            color="average_rating",
            hover_data={
                "average_rating": ":.2f",
                "rating_count": ":,",
                "weighted_rating": ":.2f"
            },
            labels={
                "weighted_rating": "Weighted Popularity Score",
                "title": "Movie",
                "average_rating": "Average Rating",
                "rating_count": "Total Ratings"
            },
            title="Top 20 Movies by Weighted Popularity"
        )

        fig_popular.update_layout(
            template="plotly_dark",
            paper_bgcolor="#080D1A",
            plot_bgcolor="#111827",
            font_color="#F1F5F9",
            height=650,
            yaxis_title="",
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig_popular,
            use_container_width=True
        )

        st.caption(
            "The weighted score combines the movie's average "
            "rating with the number of ratings it has received."
        )


# ============================================================
# TAB 2: RATING ANALYSIS
# ============================================================

with tab2:
    st.subheader("⭐ Overall Rating Distribution")

    if not global_distribution.empty:

        fig_global = px.bar(
            global_distribution,
            x="rating",
            y="count",
            text="count",
            labels={
                "rating": "Rating",
                "count": "Number of Ratings"
            },
            title="Distribution of All Viewer Ratings"
        )

        fig_global.update_traces(
            textposition="outside"
        )

        fig_global.update_layout(
            template="plotly_dark",
            paper_bgcolor="#080D1A",
            plot_bgcolor="#111827",
            font_color="#F1F5F9",
            xaxis=dict(
                tickmode="linear",
                dtick=0.5
            ),
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig_global,
            use_container_width=True
        )

    else:
        st.info("No rating data is available.")

    st.markdown("---")

    st.subheader("📊 Movie Rating vs. Number of Ratings")

    rated_movies = filtered_catalog[
        filtered_catalog["rating_count"] > 0
    ]

    if not rated_movies.empty:

        # Sample at most 5,000 movies for a responsive scatter plot
        scatter_data = rated_movies

        if len(scatter_data) > 5000:
            scatter_data = scatter_data.sample(
                n=5000,
                random_state=42
            )

        fig_scatter = px.scatter(
            scatter_data,
            x="rating_count",
            y="average_rating",
            color="weighted_rating",
            hover_name="title",
            hover_data=[
                "genres",
                "release_year"
            ],
            labels={
                "rating_count": "Number of Ratings",
                "average_rating": "Average Rating",
                "weighted_rating": "Weighted Popularity"
            },
            title="Relationship Between Rating Count and Average Rating"
        )

        fig_scatter.update_layout(
            template="plotly_dark",
            paper_bgcolor="#080D1A",
            plot_bgcolor="#111827",
            font_color="#F1F5F9",
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

        if len(rated_movies) > len(scatter_data):
            st.caption(
                "The scatter plot uses a random sample of 5,000 "
                "movies for performance. Summary metrics use the "
                "full filtered catalog."
            )

    else:
        st.info("No rated movies match the current filters.")


# ============================================================
# TAB 3: GENRE ANALYSIS
# ============================================================

with tab3:
    st.subheader("🎭 Movie Genre Analysis")

    # Count movies belonging to each genre
    genre_records = []

    for _, row in filtered_catalog.iterrows():
        for genre in row["genre_list"]:
            genre_records.append(
                {
                    "genre": genre,
                    "movieId": row["movieId"],
                    "average_rating": row["average_rating"],
                    "rating_count": row["rating_count"]
                }
            )

    if genre_records:
        genre_data = pd.DataFrame(genre_records)

        # Count unique movies by genre
        genre_summary = (
            genre_data.groupby("genre")
            .agg(
                movie_count=("movieId", "nunique"),
                average_rating=("average_rating", "mean"),
                total_ratings=("rating_count", "sum")
            )
            .reset_index()
            .sort_values(
                "movie_count",
                ascending=False
            )
        )

        left, right = st.columns(2)

        with left:
            fig_genre_count = px.bar(
                genre_summary,
                x="genre",
                y="movie_count",
                labels={
                    "genre": "Genre",
                    "movie_count": "Number of Movies"
                },
                title="Movies by Genre"
            )

            fig_genre_count.update_layout(
                template="plotly_dark",
                paper_bgcolor="#080D1A",
                plot_bgcolor="#111827",
                font_color="#F1F5F9",
                xaxis_tickangle=-45
            )

            st.plotly_chart(
                fig_genre_count,
                use_container_width=True
            )

        with right:
            fig_genre_rating = px.bar(
                genre_summary.sort_values(
                    "average_rating",
                    ascending=False
                ),
                x="genre",
                y="average_rating",
                labels={
                    "genre": "Genre",
                    "average_rating": "Average Movie Rating"
                },
                title="Average Movie Rating by Genre"
            )

            fig_genre_rating.update_layout(
                template="plotly_dark",
                paper_bgcolor="#080D1A",
                plot_bgcolor="#111827",
                font_color="#F1F5F9",
                xaxis_tickangle=-45
            )

            st.plotly_chart(
                fig_genre_rating,
                use_container_width=True
            )

        st.subheader("Genre Statistics")

        st.dataframe(
            genre_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "genre": "Genre",
                "movie_count": st.column_config.NumberColumn(
                    "Number of Movies",
                    format="%d"
                ),
                "average_rating": st.column_config.NumberColumn(
                    "Average Movie Rating",
                    format="%.2f"
                ),
                "total_ratings": st.column_config.NumberColumn(
                    "Sum of Movie Rating Counts",
                    format="%d"
                )
            }
        )

        st.caption(
            "Movies can belong to multiple genres. Therefore, "
            "genre counts overlap, and the sum of genre counts "
            "can exceed the number of unique movies."
        )

    else:
        st.info("No genre information is available for these filters.")


# ============================================================
# TAB 4: YEARLY TRENDS
# ============================================================

with tab4:
    st.subheader("📅 Movie Release Trends")

    yearly_data = filtered_catalog.dropna(
        subset=["release_year"]
    ).copy()

    if not yearly_data.empty:

        yearly_data["release_year"] = (
            yearly_data["release_year"].astype("int64")
        )

        yearly_summary = (
            yearly_data.groupby("release_year")
            .agg(
                movie_count=("movieId", "nunique"),
                average_rating=("average_rating", "mean"),
                total_ratings=("rating_count", "sum")
            )
            .reset_index()
            .sort_values("release_year")
        )

        left, right = st.columns(2)

        with left:
            fig_year_count = px.line(
                yearly_summary,
                x="release_year",
                y="movie_count",
                markers=True,
                labels={
                    "release_year": "Release Year",
                    "movie_count": "Number of Movies"
                },
                title="Number of Movies Released per Year"
            )

            fig_year_count.update_layout(
                template="plotly_dark",
                paper_bgcolor="#080D1A",
                plot_bgcolor="#111827",
                font_color="#F1F5F9"
            )

            st.plotly_chart(
                fig_year_count,
                use_container_width=True
            )

        with right:
            fig_year_rating = px.line(
                yearly_summary,
                x="release_year",
                y="average_rating",
                markers=True,
                labels={
                    "release_year": "Release Year",
                    "average_rating": "Mean Movie Rating"
                },
                title="Mean Movie Rating by Release Year"
            )

            fig_year_rating.update_layout(
                template="plotly_dark",
                paper_bgcolor="#080D1A",
                plot_bgcolor="#111827",
                font_color="#F1F5F9"
            )

            st.plotly_chart(
                fig_year_rating,
                use_container_width=True
            )

        st.subheader("Yearly Summary")

        st.dataframe(
            yearly_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "release_year": st.column_config.NumberColumn(
                    "Release Year",
                    format="%d"
                ),
                "movie_count": st.column_config.NumberColumn(
                    "Number of Movies",
                    format="%d"
                ),
                "average_rating": st.column_config.NumberColumn(
                    "Mean Movie Rating",
                    format="%.2f"
                ),
                "total_ratings": st.column_config.NumberColumn(
                    "Sum of Movie Rating Counts",
                    format="%d"
                )
            }
        )

        st.caption(
            "The yearly mean shown here is the unweighted average "
            "of movie-level averages, not the average of every "
            "individual viewer rating for that year."
        )

    else:
        st.info(
            "No release-year information is available for "
            "the selected movies."
        )


# ============================================================
# TAB 5: COMPLETE MOVIE CATALOG
# ============================================================

with tab5:
    st.subheader("📋 Movie Catalog")

    st.write(
        f"Showing {len(filtered_catalog):,} movie(s) "
        "after applying the selected filters."
    )

    display_columns = [
        "title",
        "genres",
        "release_year",
        "average_rating",
        "rating_count",
        "weighted_rating",
        "rating_std"
    ]

    display_catalog = filtered_catalog[
        display_columns
    ].copy()

    st.dataframe(
        display_catalog,
        use_container_width=True,
        hide_index=True,
        column_config={
            "title": "Movie Title",
            "genres": "Genres",
            "release_year": st.column_config.NumberColumn(
                "Release Year",
                format="%d"
            ),
            "average_rating": st.column_config.NumberColumn(
                "Average Rating",
                format="%.2f"
            ),
            "rating_count": st.column_config.NumberColumn(
                "Total Ratings",
                format="%d"
            ),
            "weighted_rating": st.column_config.NumberColumn(
                "Weighted Popularity",
                format="%.2f"
            ),
            "rating_std": st.column_config.NumberColumn(
                "Rating Standard Deviation",
                format="%.2f"
            )
        }
    )

    # Download only the filtered catalog
    csv_data = display_catalog.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Movie Catalog (CSV)",
        data=csv_data,
        file_name="filtered_movie_catalog.csv",
        mime="text/csv"
    )


# ============================================================
# 13. DOWNLOAD TOP MOVIES
# ============================================================

st.markdown("---")

st.subheader("⬇️ Export Results")

top_download = filtered_catalog.head(100).copy()

top_csv = top_download.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Top 100 Movies",
    data=top_csv,
    file_name="top_100_movies.csv",
    mime="text/csv"
)


# ============================================================
# 14. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <p>
            <b>Movie Ratings and Viewer Preferences Analysis</b>
        </p>
        <p>
            Built using Python, Pandas, Streamlit, and Plotly.
        </p>
        <p>
            An analytical dashboard for exploring movie ratings,
            popularity patterns, genres, and entertainment trends.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

