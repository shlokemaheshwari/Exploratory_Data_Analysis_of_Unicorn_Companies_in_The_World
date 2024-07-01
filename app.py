import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Unicorn Companies Analysis", page_icon=":unicorn_face:", layout="wide")
st.title(":unicorn_face: Unicorn Companies EDA")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# File uploader
f1 = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(f1, encoding="ISO-8859-1")
else:
    df = pd.read_csv("Unicorn_Companies_Clean.csv", encoding="ISO-8859-1")

# Sidebar options
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Select a section to view",
    ("Home", "Country-wise Analysis", "City-wise Analysis", "Industry-wise Analysis", "Time & Investor-wise Analysis")
)

# Function to show dataset
def show_dataset():
    st.write("### Dataset")
    st.dataframe(df)

# Function for country-wise analysis
def country_wise_analysis():
    st.write("### 1. Country-wise Analysis")
    
    # Top Countries wrt Total Valuation and Number of Unicorns
    st.subheader("1.1 Top Countries by Total Valuation and Number of Unicorns")
    num_countries_valuation = st.sidebar.slider('Select the number of top countries to display by valuation', min_value=1, max_value=len(df['Country'].unique()), value=5)
    temp_valuation = df.groupby(by=['Country']).agg({'Company': ['count'], 'Valuation ($B)': ['sum']})
    temp_valuation = temp_valuation.sort_values([('Company', 'count')], ascending=False)[:num_countries_valuation]
    fig_valuation = px.bar(x=temp_valuation[('Valuation ($B)', 'sum')], y=temp_valuation.index, 
                           text_auto=True, color=temp_valuation[('Company', 'count')], 
                           labels={"y": "Country", "x": "Total Valuation($B)", "color": "Number of Unicorns"})
    st.plotly_chart(fig_valuation)
    
    # Average years taken to become Unicorn wrt Country
    st.subheader("1.2 Average Years Taken to Become Unicorn by Country")
    num_countries_years = st.sidebar.slider('Select the number of countries for average years taken plot', min_value=1, max_value=len(df['Country'].unique()), value=10)
    temp_years = df.groupby(by=['Country']).agg({'Years Taken to become Unicorn': ['mean']})
    temp_years = temp_years.sort_values([('Years Taken to become Unicorn', 'mean')], ascending=False)[:num_countries_years]
    fig_years = px.scatter(y=temp_years[('Years Taken to become Unicorn','mean')], x=temp_years.index, 
                           size=temp_years[('Years Taken to become Unicorn', 'mean')],
                           size_max=30, color=temp_years.index,
                           labels={"y":"Years Taken", "x":"Country", "color":"Country"})
    st.plotly_chart(fig_years)
    
    # Top Countries wrt Total Money raised
    st.subheader("1.3 Top Countries by Total Money Raised")
    num_countries_raised = st.sidebar.slider('Select the number of top countries to display by total money raised', min_value=1, max_value=len(df['Country'].unique()), value=6)
    temp_raised = df.groupby(by=['Country']).agg({'Total Raised': ['sum']})
    temp_raised = temp_raised.sort_values([('Total Raised', 'sum')], ascending=False)[:num_countries_raised]
    fig_raised = px.line(y=temp_raised[('Total Raised', 'sum')], x=temp_raised.index, 
                         labels={"y":"Total Raised($B)", "x":"Country"})
    fig_raised.update_traces(line_color="blue")
    st.plotly_chart(fig_raised)

# Function for city-wise analysis
def city_wise_analysis():
    st.write("### 2. City-wise Analysis")
    
    # Top Cities wrt Total Valuation and Number of Unicorns
    st.subheader("2.1 Top Cities by Total Valuation and Number of Unicorns")
    num_cities_valuation = st.sidebar.slider('Select the number of top cities to display by valuation', min_value=1, max_value=len(df['City'].unique()), value=7)
    temp_valuation = df.groupby(by=['City']).agg({'Company': ['count'], 'Valuation ($B)': ['sum']})
    temp_valuation = temp_valuation.sort_values([('Valuation ($B)', 'sum')], ascending=False)[:num_cities_valuation]
    fig_valuation = px.bar(x=temp_valuation[('Valuation ($B)', 'sum')], y=temp_valuation.index, 
                           text_auto=True, color=temp_valuation[('Company', 'count')], 
                           labels={"y": "City", "x": "Total Valuation($B)", "color": "Number of Unicorns"})
    st.plotly_chart(fig_valuation)
    
    # Scatter plot: Years taken to become Unicorn wrt Country and City
    st.subheader("2.2 Years taken to become Unicorn wrt Country and City")
    fig_years_city = px.scatter(df, x='Years Taken to become Unicorn', y='Country', 
                                hover_data=['City'], color='City')
    st.plotly_chart(fig_years_city)
    
    # Average years taken to become Unicorn wrt City
    st.subheader("2.3 Average Years Taken to Become Unicorn by City")
    num_cities_years = st.sidebar.slider('Select the number of cities for average years taken plot', min_value=1, max_value=len(df['City'].unique()), value=20)
    temp_years_city = df.groupby(by=['City']).agg({'Years Taken to become Unicorn': ['mean']})
    temp_years_city = temp_years_city.sort_values([('Years Taken to become Unicorn', 'mean')], ascending=False)[:num_cities_years]
    fig_years_city_avg = px.scatter(y=temp_years_city[('Years Taken to become Unicorn','mean')], x=temp_years_city.index, 
                                    size=temp_years_city[('Years Taken to become Unicorn', 'mean')],
                                    size_max=30, color=temp_years_city.index,
                                    labels={"y": "Years Taken", "x": "City", "color": "City"})
    st.plotly_chart(fig_years_city_avg)
    
    # Top Cities wrt Total Money raised
    st.subheader("2.4 Top Cities by Total Money Raised")
    num_cities_raised = st.sidebar.slider('Select the number of top cities to display by total money raised', min_value=1, max_value=len(df['City'].unique()), value=9)
    temp_raised = df.groupby(by=['City']).agg({'Total Raised': ['sum']})
    temp_raised = temp_raised.sort_values([('Total Raised', 'sum')], ascending=False)[:num_cities_raised]
    fig_raised = px.line(y=temp_raised[('Total Raised', 'sum')], x=temp_raised.index, 
                         labels={"y":"Total Raised($B)", "x":"City"})
    fig_raised.update_traces(line_color="blue")
    st.plotly_chart(fig_raised)

# Function for industry-wise analysis
def industry_wise_analysis():
    st.write("### 3. Industry-wise Analysis")
    
    # Slider to select number of top Industries to display
    num_industries = st.sidebar.slider('Select the number of top Industries to display', min_value=1, max_value=20, value=10)
    temp = df.groupby(by=['Industry']).agg({'Company': ['count'], 'Valuation ($B)': ['sum', 'mean']})
    temp = temp.sort_values([('Company', 'count')], ascending=False)[:num_industries]
    fig = px.bar(x=temp[('Valuation ($B)', 'sum')], y=temp.index, 
                 text_auto=True, color=temp[('Company', 'count')], 
                 labels={"y": "Industry", "x": "Total Valuation($B)", "color": "Number of Unicorns"})
    st.plotly_chart(fig)

    # Slider to select number of top industries by average valuation
    num_top_industries_valuation = st.sidebar.slider('Select the number of top industries by average valuation', min_value=1, max_value=10, value=6)
    temp_valuation = df.groupby(by=['Industry']).agg({'Company': ['count'], 'Valuation ($B)': ['sum', 'mean']})
    temp_valuation = temp_valuation.sort_values([('Valuation ($B)', 'mean')], ascending=False)[:num_top_industries_valuation]
    fig_valuation = px.bar(x=temp_valuation[('Valuation ($B)', 'mean')], y=temp_valuation.index, 
                       text_auto=True,
                       labels={"y": "Industry", "x": "Average Valuation($B)"})
    st.plotly_chart(fig_valuation)

    # Slider to select number of industries to display in average years taken scatter plot
    num_industries_years = st.sidebar.slider('Select the number of industries for average years taken scatter plot', min_value=2, max_value=15, value=10)
    temp_years = df.groupby(by=['Industry']).agg({'Years Taken to become Unicorn': ['mean']})
    temp_years = temp_years.sort_values([('Years Taken to become Unicorn', 'mean')], ascending=False)[:num_industries_years]
    fig_years = px.scatter(y=temp_years[('Years Taken to become Unicorn','mean')], x=temp_years.index, 
                       size=temp_years[('Years Taken to become Unicorn', 'mean')],
                       size_max=30, color=temp_years.index,
                       labels={"y": "Years Taken", "x": "Industry", "color": "Industry"})
    st.plotly_chart(fig_years)

    # Dropdown to select industry for scatter plot
    selected_industry = st.sidebar.selectbox('Select an industry for scatter plot', df['Industry'].unique())
    # Generate scatter plot based on selected industry
    filtered_df = df[df['Industry'] == selected_industry]
    fig_scatter = px.scatter(filtered_df, x='Years Taken to become Unicorn', y='Country', 
                         hover_data=['Industry'], color='Industry')
    st.plotly_chart(fig_scatter)

# Function for time & investor-wise analysis
def time_investor_wise_analysis():
    st.write("### 4. Time & Investor-wise Analysis")
    
    # Pie chart: Years wrt the highest number of Companies that became Unicorns
    st.subheader("4.1 Years wrt the highest number of Companies that became Unicorns")
    num_years = st.sidebar.slider('Select the number of top years to display', min_value=1, max_value=len(df['Year'].unique()), value=5)
    temp_years = df.groupby(by=['Year']).agg({'Company': ['count']})
    temp_years = temp_years.sort_values([('Company', 'count')], ascending=False)[:num_years]
    fig_years_pie = px.pie(values=temp_years[('Company', 'count')], names=temp_years.index)
    fig_years_pie.update_traces(textinfo='value', textfont_size=20)
    st.plotly_chart(fig_years_pie)
    
    # Bar chart: Founded Years wrt number of Companies that became Unicorn
    st.subheader("4.2 Founded Years wrt number of Companies that became Unicorn")
    num_founded_years = st.sidebar.slider('Select the number of top founded years to display', min_value=1, max_value=len(df['Founded Year'].unique()), value=10)
    temp_founded_years = df.groupby(by=['Founded Year']).agg({'Company': ['count']})
    temp_founded_years = temp_founded_years.sort_values([('Company','count')], ascending=False)[:num_founded_years]
    fig_founded_years = px.bar(y=temp_founded_years[('Company','count')], x=temp_founded_years.index,
                               text=temp_founded_years[('Company','count')].values,
                               labels={"x":"Founded Year", "y":"Number of Unicorns"})
    st.plotly_chart(fig_founded_years)
    
    # Bar chart: Top Investors wrt the Number of Unicorns they invested in
    st.subheader("4.3 Top Investors by Number of Unicorns")
    num_top_investors = st.sidebar.slider('Select the number of top investors to display', min_value=1, max_value=20, value=10)
    investors = df['Select Inverstors'].str.split(', ').explode().value_counts()[:num_top_investors]
    fig_investors = px.bar(x=investors.index, y=investors.values,
                           text=investors.values,
                           labels={"x":"Investors", "y":"Number of Unicorns"})
    fig_investors.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig_investors)
    
    # Scatter plot: Total Raised wrt Valuation of Top Unicorns
    st.subheader("4.4 Total Raised wrt Valuation of Top Unicorns")
    temp = df.sort_values("Valuation ($B)", ascending=False)[:13]
    fig = px.scatter(x=temp['Valuation ($B)'], y=temp['Total Raised'], size=temp['Years Taken to become Unicorn'], 
                     hover_name=temp['Company'], color=temp['Company'], size_max=70,
                     title="Size of the bubble: Years taken to become Unicorn",
                     labels={"x":"Valuation($B)", "y":"Total Raised($B)"})
    st.plotly_chart(fig)

# Combined navigation based on sidebar selection
if option == "Home":
    show_dataset()
elif option == "Country-wise Analysis":
    country_wise_analysis()
elif option == "City-wise Analysis":
    city_wise_analysis()
elif option == "Industry-wise Analysis":
    industry_wise_analysis()
elif option == "Time & Investor-wise Analysis":
    time_investor_wise_analysis()
