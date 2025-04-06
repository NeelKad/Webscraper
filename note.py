import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# Function to fetch website content and extract useful text
def fetch_website_content(url):
    try:
        # Validate URL
        if not urlparse(url).scheme:
            raise ValueError(
                "Invalid URL. Please make sure the URL includes the scheme (e.g., http://).")

        # Send GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Parse the content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])

        # Split content into sentences and create dot points
        sentences = content.split('. ')
        dot_points = [
            f"- {sentence.strip()}." for sentence in sentences if sentence.strip()]

        return dot_points[:10]  # Limit to 10 bullet points

    except requests.exceptions.RequestException as e:
        return [f"Error fetching the website content: {e}"]
    except ValueError as ve:
        return [str(ve)]
    except Exception as e:
        return [f"An unexpected error occurred: {e}"]


# Function to display website content in a clean and organized manner
def display_content(dot_points):
    if isinstance(dot_points, list) and dot_points:
        st.subheader("Website Summary (Top 10 Sentences)")
        for point in dot_points:
            st.write(point)
    else:
        st.warning("No content to display.")


# Main function to control the flow of the app
def main():
    st.set_page_config(page_title="Website Content Extractor", layout="wide")

    # Title and description
    st.title("Enterprise-Level Website Content Extractor")
    st.markdown("""
        This tool extracts and summarizes the content of a website. Simply enter a URL and get the first 10 key sentences from the page. 
        It helps you quickly scan the most relevant content of any webpage.
    """)

    # User input for URL
    url = st.text_input("Enter the website URL:", "")

    if url:
        with st.spinner("Fetching and processing content..."):
            dot_points = fetch_website_content(url)

        # Display content or error message
        display_content(dot_points)

    # Footer for app branding
    st.markdown("""
        <footer style="font-size: 12px; color: gray; text-align: center;">
            Built with ❤️ by Your Company | <a href="https://www.example.com">Your Website</a>
        </footer>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
