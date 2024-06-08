# LinkedIn Profile Scraper

This Streamlit app allows users to scrape LinkedIn profiles using Selenium for web automation and the Proxycurl API. The app searches LinkedIn by first name and last name, retrieves the top 10 search results, and then scrapes detailed profile information if the name matches the search criteria. It stores the data in a CSV file and creates a pickle file. Users can choose between web scraping and API calls to fetch and display the data.

## Features

- Scrape LinkedIn profiles using Selenium
- Fetch profile data using Proxycurl API
- Store data in CSV files and pickle files
- Display profile information in a dataframe
- User-friendly UI for selecting scraping methods

## Demo

[YouTube Demo Link](https://youtu.be/vBipu3pU2iM)

## Screenshots

### UI with Both Options to Scrape with API or Web Scraping
![UI Image](https://github.com/AnupamMittal-21/EcoWiserAssignment/assets/96871662/10c71617-8f26-4dea-b7fa-f816ef62ca3b)

### Results are fetched based on firstname and lastname
![image](https://github.com/AnupamMittal-21/EcoWiserAssignment/assets/96871662/aa2becc6-1393-465f-98de-d56e4b5fdc0d)

### Dataframe Created Using Web Scraping
![Dataframe - Web Scraping](https://github.com/AnupamMittal-21/EcoWiserAssignment/assets/96871662/748bef08-d038-4c57-9d56-1a2fe84aca95)

### Dataframe Created Using API Call
![Dataframe - API Call](https://github.com/AnupamMittal-21/EcoWiserAssignment/assets/96871662/4f91d543-49f3-413f-9b72-8217f089aa65)

### Detailed Information Using API Call
![Detailed Info - API Call](https://github.com/AnupamMittal-21/EcoWiserAssignment/assets/96871662/39007bee-74f9-449e-8530-8c92b75363c7)

### Folder Structure and CSV Files Created with Pickle Files
![Folder Structure](https://github.com/AnupamMittal-21/EcoWiserAssignment/assets/96871662/f964f99b-99e7-490d-94f8-a810fb09e10c)

## Installation

### Prerequisites

1. **Python 3.6+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Google Chrome**: Download and install the latest version of Google Chrome from [google.com/chrome](https://www.google.com/chrome/).

3. **ChromeDriver**: Download the ChromeDriver that matches your Chrome version from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads). 

4. **Proxycurl API Key**: Obtain an API key from [Proxycurl](https://nubela.co/proxycurl/).

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AnupamMittal-21/EcoWiserAssignment.git
   cd EcoWiserAssignment
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**
   - Create a `data.env` file in the root directory of the project.
   - Add your Proxycurl API key and the path to your ChromeDriver in the `data.env` file:
     ```
     DRIVER_PATH = C:\ChromeDriver\chromedriver.exe
     USER_PATH =--user-data-dir=C:\Users\your_user_name\AppData\Local\Google\Chrome\User Data\Default
     USER_NAME = your_email_address
     PASSWORD = your_linkedin_password
     PROXY_CURL_API_KEY = your_proxycurl_api_key
     ```

5. **Run the App**
   ```bash
   streamlit run run.py
   ```

## Usage

1. Open the Streamlit app in your browser.
2. Enter the first name and last name of the LinkedIn profile you want to scrape.
3. Choose between web scraping and API call.
4. View the fetched data in the displayed dataframe.
5. The data is also saved as CSV and pickle files in the specified folder.

## Folder Structure

- `app.py`: Main Streamlit app file.
- `requirements.txt`: Required Python packages.
- `linkedInScraper`: Contains the scraping logic.
- `data/`: Stores CSV and pickle files.
- `data.env`: Contains environment variables (API key, ChromeDriver path).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
