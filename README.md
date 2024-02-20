# About
An interactive dashboard web app built with Plotly Dash that displays real-time stock data aggregated across sectors.
The purpose of the dashboard is not to see information about any specific ticker, but rather to compare the relative performance of different market sectors. 

The data is sourced from Yahoo Finance, using web scraping via Selenium and Chrome Webdriver, as well as the API Dojo Yahoo Finance API. 
The dashboard/web app is created using Dash. This framework builds a web page given some HTML and CSS styling, as well as visualizations generated with other Python libraries. I use Plotly, since it's the most well supported by Dash. 

Data is grouped by sector (technology, real estate, finance, etc.)

The dashboard has two rows. The top row contains the title with an "Update" button, a dropdown menu, and two visualizations. <br>
Clicking the Update button will fetch new, real time stocks data and regenerate the visualizations. <br>
The dropdown menu allows the user to select a Sector to filter the data by. <br>
The first visualization is a list of the 10 largest companies in the given sector. <br>
The second is a treemap which displays the proportional market weights of all the industries within the sector. <br>
The data for this row is scraped.

The bottom row contains three histograms. <br>
These display the distributions for price, price percent change, and volume among the tickers within the sector. <br>
The data for this row comes via API. 


# To Do
 * The web app functions but needs better styling. Edit CSS to properly align elements in the page. Implement flex-box such that elements display properly on a range of window sizes.
 * The final data source for the histograms is not yet determined. The webpage from which this data would be scraped is not accessible by URL, since it's meant to be accessed by a series of redirects. It may be possible to access the page via the webdriver by using CSS selectors. However, this approach would run very slowly regardless. The data can be accessed via the API, but the query has no ability to filter by sector. Rather, stocks from all sectors must be returned and then filtered locally. Despite the brute-force nature of this approach, it actually runs much faster than the scraping approach, and is therefore the preferred (and probably easier) option.
 * The Update button currently has no functionality. I need it to trigger the fetching of new data and subsequent generation of visualization components. However, I'm uncertain about the flow of Dash, and there doesn't seem to be any documentation about control flow specifically. A callback function is probably the key to this.
