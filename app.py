import streamlit as st
import pandas as pd


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
        st.dataframe(top_least_rated[["Name", "Address", "Rating", "Total Reviews"]])
    else:
        st.warning("The file is empty or has an unexpected format. Please check the file.")


# Run the app
if __name__ == "__main__":
    main()
