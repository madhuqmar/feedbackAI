import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")


# Load the data
@st.cache_data
def load_data(file_path):
    """
    Load the CSV file into a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


# Main function
def main():
    st.title("Customer FeedbackAI")
    st.write("Analyze locations, ratings, and reviews data extracted via Google Places API.")

    # Load data from specified location
    file_path_1 = "data/naturals_chennai_locations_metadata.csv"
    ratings_df = load_data(file_path_1)
    ratings_df["full_location"] = ratings_df["City Area"] + " - " + ratings_df["Name"]

    file_path_2 = "data/naturals_reviews.csv"
    reviews_df = load_data(file_path_2)

    file_path_3 = "data/naturals_sentiments.csv"
    sentiments_df = load_data(file_path_3)

    df = pd.merge(ratings_df, sentiments_df, left_on="Place ID", right_on="place_id", how="right")
    df = df[df["caption"].notna()]

    if not ratings_df.empty and not reviews_df.empty and not sentiments_df.empty:
        st.success("Data loaded successfully!")
    else:
        st.warning("The file is empty or has an unexpected format. Please check the file.")

    #### Filters at the top ####
    st.sidebar.header("Filters")
    # Timeline filter
    timeline = st.sidebar.selectbox("Select Timeline", options=["All"] + list(reviews_df["relative_date"].unique()))

    # Rating filter
    rating = st.sidebar.slider(
        "Select Rating",
        min_value=0,  # Minimum value for the slider
        max_value=5,  # Maximum value for the slider
        value=0,  # Default value
        step=1  # Step size for the slider
    )

    # Location filter with "All" option
    selected_location = st.sidebar.selectbox("Select a Naturals Location",
                                             options=["All"] + list(df['full_location'].unique()))

    # Apply filters
    filtered_df = df.copy()
    if timeline != "All":
        filtered_df = filtered_df[filtered_df['relative_date'] == timeline]
    if rating > 0:
        filtered_df = filtered_df[filtered_df['rating'] == rating]
    if selected_location != "All":
        filtered_df = filtered_df[filtered_df['full_location'] == selected_location]

    #### Top 5 least-rated salons (unaffected by filters) ####
    st.header("Top 5 Locations with Least Rating")
    top_least_rated = ratings_df.sort_values(by="Rating", ascending=True).head(5)
    st.dataframe(top_least_rated[["City Area", "Name", "Rating", "Total Reviews", "Address"]])

    #### Key Metrics ####
    st.header("Key Metrics")
    M1, M2 = st.columns(2)
    m1, m2, m3 = M1.columns(3)

    # Total number of locations
    total_locations = len(filtered_df['place_id'].unique())
    m1.metric(label="Total Locations", value=total_locations)

    # Average Rating
    average_rating = filtered_df["Rating"].mean() if not filtered_df.empty else 0
    m2.metric(label="Overall Average Rating", value=f"{average_rating:.2f}")

    # Total Reviews
    total_reviews = filtered_df['caption'].notna().sum()
    m3.metric(label="Total Number of Reviews", value=total_reviews)

    #### Charts ####
    col1, col2, col3 = st.columns(3)

    # CHART 1: Salon Rating Distribution
    category_counts = filtered_df['Rating'].value_counts().reset_index()
    category_counts.columns = ['rating', 'count']
    fig = px.pie(category_counts, names='rating', values='count', title='Salon Rating Distribution')
    col1.plotly_chart(fig, theme="streamlit")

    # CHART 2: User Rating Distribution
    category_counts = filtered_df['rating'].value_counts().reset_index()
    category_counts.columns = ['rating', 'count']
    fig = px.pie(category_counts, names='rating', values='count', title='User Rating Distribution')
    col2.plotly_chart(fig, theme="streamlit")

    # CHART 3: Sentiment Distribution
    valid_sentiments = ['Positive', 'Negative', 'Neutral', 'Mixed']
    sentiment_counts = filtered_df[filtered_df['sentiment'].isin(valid_sentiments)][
        'sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']
    fig = px.bar(sentiment_counts, x='sentiment', y='count', title='Sentiment Distribution', text='count')
    col3.plotly_chart(fig, theme="streamlit")

    #### Filtered Table ####
    st.header("Filtered Data")
    st.dataframe(filtered_df[["City Area", "Name", "Address", "caption", "rating", "sentiment"]])


# Run the app
if __name__ == "__main__":
    main()
