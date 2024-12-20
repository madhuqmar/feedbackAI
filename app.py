import streamlit as st
import pandas as pd
import plotly.express as px

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
    st.title("Google Maps Reviews Dashboard")
    st.write("Analyze locations, ratings, and reviews data extracted via Google Places API.")

    # Load data from specified location
    file_path = "data/naturals_chennai_locations_metadata.csv"
    df = load_data(file_path)

    if not df.empty:
        st.success("Data loaded successfully!")

        # Display metrics
        st.header("Key Metrics")

        m1, m2, m3 = st.columns(3)
        # Total number of locations
        total_locations = df["Place ID"].nunique()
        m1.metric(label="Total Locations", value=total_locations)

        # Average Rating
        average_rating = df["Rating"].mean()
        m2.metric(label="Overall Average Rating", value=f"{average_rating:.2f}")

        # Total Reviews (sum of Total Reviews column)
        total_reviews = df["Total Reviews"].sum()
        m3.metric(label="Total Number of Reviews", value=total_reviews)

        # Display top five locations with least rating
        st.header("Top 5 Locations with Least Rating")
        top_least_rated = df.sort_values(by="Rating", ascending=True).head(5)
        st.dataframe(top_least_rated[["City Area", "Name", "Rating", "Total Reviews", "Address"]])

    else:
        st.warning("The file is empty or has an unexpected format. Please check the file.")

    selected_location = st.selectbox("Select a Naturals Location", options=df['full_location'])

    sentiments_file_path = "data/naturals_reviews_sentiments.csv"
    sentiment_df = load_data(sentiments_file_path)

    df['Place ID'] = df['Place ID'].str.strip('\n')
    sentiment_df['place_id'] = sentiment_df['place_id'].str.strip('\n')

    combined_df = pd.merge(sentiment_df, df, left_on="place_id", right_on="Place ID", how="left")

    if selected_location:
        filtered_df = combined_df[combined_df['full_location'] == selected_location]

        # Calculate value counts for the pie chart
        category_counts = filtered_df['sentiment'].value_counts().reset_index()
        category_counts.columns = ['sentiment', 'count']

        # Create the pie chart
        fig = px.pie(category_counts,
                     names='sentiment',  # Labels for the pie chart
                     values='count',  # Sizes of the pie chart slices
                     title='Sentiment Distribution')

        # Display the chart in Streamlit
        st.plotly_chart(fig)

    else:
        # Calculate value counts for the pie chart
        category_counts = sentiment_df['sentiment'].value_counts().reset_index()
        category_counts.columns = ['sentiment', 'count']

        # Create the pie chart
        fig = px.pie(category_counts,
                     names='sentiment',  # Labels for the pie chart
                     values='count',  # Sizes of the pie chart slices
                     title='Sentiment Distribution')

        # Display the chart in Streamlit
        st.plotly_chart(fig)

# Run the app
if __name__ == "__main__":
    main()
