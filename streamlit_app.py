import streamlit as st
import pandas as pd
import plotly.express as px

# Brining in the data from the CSV File
df = pd.read_csv('bls_data.csv')

# Formatting each datetime
def format_date(date_series):
    return date_series.dt.strftime('%b-%Y')  # Mon-YYYY

# Function to properly sort date from earliers to most recent
def sort_data_by_date(data):
    return data.sort_values('Date', ascending=True)  # Sorting date in ascending order

# Adding a side bar menu for an Overview and individual views
menu_options = ["Overview", "Nonfarm Payroll", "Unemployment Rate", "CPI", "PPI"]
selection = st.sidebar.radio("Select an Option", menu_options)

# Fromating the layout of the overview page 
if selection == "Overview":
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>BLS Data Dashboard - Overview</h1>", unsafe_allow_html=True)
    
    # Adding brief explanation of how these pieces of economic data can be used
    st.markdown("""
    By analyzing these four series together, we can gain valuable insights into the economic landscape:

    1. **Nonfarm Payrolls** combined with a decreasing **Unemployment Rate** suggests a robust and growing economy. If both are declining, it may indicate economic contraction or stagnation.
    
    2. **CPI** and **PPI** give us clues about inflationary pressures. A rising **CPI** indicates that consumer prices are increasing, reducing purchasing power, while a rising **PPI** suggests that producers are facing higher input costs, which may eventually lead to higher consumer prices.

    3. **Economic Lag and Lead Indicators**: The **Nonfarm Payrolls** and **Unemployment Rate** often lead or lag inflation data. For example, strong job growth can eventually reduce unemployment, while inflationary pressures (seen in **CPI** and **PPI**) can impact job growth and wages.

    By examining these indicators together, we can better understand **economic growth**, **inflation**, and **employment trends** in the U.S. economy.
    """)

    # Adjusting overview visuals to be in a 2x2 column/row
    col1, col2 = st.columns([3, 3])

    # Visual for NonFarm Payroll
    with col1:
        nonfarm_data = df[df['seriesID'] == 'CES0000000001'] # Extracts NonFarm Payroll data from Data Frame
        nonfarm_data['Date'] = pd.to_datetime(nonfarm_data['year'].astype(str) + '-' + nonfarm_data['period'].apply(lambda x: x[1:]), format='%Y-%m') # Combining year and period to create a date
        nonfarm_data['Formatted Date'] = format_date(nonfarm_data['Date'])  # Fromatting the date using the format_date function
        nonfarm_data = sort_data_by_date(nonfarm_data)  # Sorting date using the sort_data_by_date function

        fig_nonfarm = px.line(nonfarm_data, x='Formatted Date', y='value', title="Nonfarm Payrolls", labels={'value': 'Number of Jobs (in millions)', 'Formatted Date': 'Month'}) # Creation of a line chart for the data
        fig_nonfarm.update_traces(line=dict(width=4, color='blue')) # Including some additonal formation 
        fig_nonfarm.update_layout(
            title_font_size=20, 
            title_x=0.40,  # Move title further to the left to help center it
            title_y=1.0,  # Title vertically centered
            xaxis_title="Rolling 12 months", # Axis title
            yaxis_title="Jobs (in millions)", # Axis title
            xaxis_tickangle=-45, 
            margin=dict(t=60, b=60, l=60, r=60),  # Adjusting margins
            dragmode=False  # Removing zoom function to help keep visual clean and as it should be
        )
        st.plotly_chart(fig_nonfarm, use_container_width=True)

    # Visual for Unemployment Rate (practically copying the formation from the Nonfarm payroll for the rest of the visuals)
    with col2:
        unemployment_data = df[df['seriesID'] == 'LNS14000000']
        unemployment_data['Date'] = pd.to_datetime(unemployment_data['year'].astype(str) + '-' + unemployment_data['period'].apply(lambda x: x[1:]), format='%Y-%m')
        unemployment_data['Formatted Date'] = format_date(unemployment_data['Date'])
        unemployment_data = sort_data_by_date(unemployment_data)

        fig_unemployment = px.line(unemployment_data, x='Formatted Date', y='value', title="Unemployment Rate", labels={'value': 'Unemployment Rate (%)', 'Formatted Date': 'Month'})
        fig_unemployment.update_traces(line=dict(width=4, color='red'))
        fig_unemployment.update_layout(
            title_font_size=20, 
            title_x=0.40,
            title_y=1.0,
            xaxis_title="Rolling 12 months", 
            yaxis_title="Unemployment Rate (%)", 
            xaxis_tickangle=-45,
            margin=dict(t=60, b=60, l=60, r=60),
            dragmode=False
        )
        st.plotly_chart(fig_unemployment, use_container_width=True)

    # Visual for CPI (similar format from visuals above)
    col1, col2 = st.columns([3, 3])

    with col1:
        cpi_data = df[df['seriesID'] == 'CUUR0000SA0']
        cpi_data['Date'] = pd.to_datetime(cpi_data['year'].astype(str) + '-' + cpi_data['period'].apply(lambda x: x[1:]), format='%Y-%m')
        cpi_data['Formatted Date'] = format_date(cpi_data['Date'])
        cpi_data = sort_data_by_date(cpi_data)

        fig_cpi = px.line(cpi_data, x='Formatted Date', y='value', title="CPI", labels={'value': 'CPI Value', 'Formatted Date': 'Month'})
        fig_cpi.update_traces(line=dict(width=4, color='orange'))
        fig_cpi.update_layout(
            title_font_size=20, 
            title_x=0.40,
            title_y=1.0,
            xaxis_title="Rolling 12 months", 
            yaxis_title="CPI Value", 
            xaxis_tickangle=-45,
            margin=dict(t=60, b=60, l=60, r=60),
            dragmode=False
        )
        st.plotly_chart(fig_cpi, use_container_width=True)

    # Visual for PPI (similar format from visuals above)
    with col2:
        ppi_data = df[df['seriesID'] == 'WPUFD4']
        ppi_data['Date'] = pd.to_datetime(ppi_data['year'].astype(str) + '-' + ppi_data['period'].apply(lambda x: x[1:]), format='%Y-%m')
        ppi_data['Formatted Date'] = format_date(ppi_data['Date'])
        ppi_data = sort_data_by_date(ppi_data)

        fig_ppi = px.line(ppi_data, x='Formatted Date', y='value', title="PPI", labels={'value': 'PPI Value', 'Formatted Date': 'Month'})
        fig_ppi.update_traces(line=dict(width=4, color='green'))
        fig_ppi.update_layout(
            title_font_size=20, 
            title_x=0.40,
            title_y=1.0,
            xaxis_title="Rolling 12 months", 
            yaxis_title="PPI Value", 
            xaxis_tickangle=-45,
            margin=dict(t=60, b=60, l=60, r=60),
            dragmode=False
        )
        st.plotly_chart(fig_ppi, use_container_width=True)

### This is the beginning of each individual tab for each Series ID ###

# Starting with NonFarm Payroll
elif selection == "Nonfarm Payroll":
    st.markdown("<h1 style='text-align: center; color: #2196F3;'>Nonfarm Payrolls</h1>", unsafe_allow_html=True) # Title adjustment to center and add color
    st.markdown("""
    **Nonfarm Payrolls** represents the total number of jobs outside of the agricultural sector in the U.S.
    
    This data helps us gauge the overall strength of the labor market and can be an early indicator of economic expansion or contraction. A **rising** number of jobs typically signals a healthy economy, while **declining** payrolls may indicate economic slowdown or recession.
    """) # Included a brief description of the what this peice of economic data means
    nonfarm_data = df[df['seriesID'] == 'CES0000000001'] # Grabbing data from Series ID
    nonfarm_data['Date'] = pd.to_datetime(nonfarm_data['year'].astype(str) + '-' + nonfarm_data['period'].apply(lambda x: x[1:]), format='%Y-%m') # Formatting the year and period to create a date
    nonfarm_data['Formatted Date'] = format_date(nonfarm_data['Date'])  # Formating the date
    nonfarm_data = sort_data_by_date(nonfarm_data)  # Sorting the date

    fig_nonfarm = px.line(nonfarm_data, x='Formatted Date', y='value', title="Nonfarm Payrolls", labels={'value': 'Number of Jobs (in millions)', 'Formatted Date': 'Month'})
    fig_nonfarm.update_traces(line=dict(width=4, color='blue'))
    fig_nonfarm.update_layout(
        title_font_size=20, 
        title_x=0.40,  # Move title further to the left to help center under visual
        title_y=1.0,  # Axis title vertically centered
        xaxis_title="Rolling 12 months", 
        yaxis_title="Jobs (in millions)", 
        xaxis_tickangle=-45,
        margin=dict(t=60, b=60, l=60, r=60),  # Adjusting margins
        dragmode=False  # Removing zoom feature to keep visual clean
    )
    st.plotly_chart(fig_nonfarm, use_container_width=True)

# Individual tab for Unemplopyment (Same formating as individual tab above)
elif selection == "Unemployment Rate":
    st.markdown("<h1 style='text-align: center; color: #F44336;'>Unemployment Rate</h1>", unsafe_allow_html=True)
    st.markdown("""
    The **Unemployment Rate** represents the percentage of the labor force that is actively seeking work but is unable to find employment.
    
    A **high** unemployment rate typically signals a weaker economy, while a **low** unemployment rate is indicative of a healthy economy with ample job opportunities.
    """)
    unemployment_data = df[df['seriesID'] == 'LNS14000000']
    unemployment_data['Date'] = pd.to_datetime(unemployment_data['year'].astype(str) + '-' + unemployment_data['period'].apply(lambda x: x[1:]), format='%Y-%m')
    unemployment_data['Formatted Date'] = format_date(unemployment_data['Date'])
    unemployment_data = sort_data_by_date(unemployment_data)

    fig_unemployment = px.line(unemployment_data, x='Formatted Date', y='value', title="Unemployment Rate", labels={'value': 'Unemployment Rate (%)', 'Formatted Date': 'Month'})
    fig_unemployment.update_traces(line=dict(width=4, color='red'))
    fig_unemployment.update_layout(
        title_font_size=20, 
        title_x=0.40,
        title_y=1.0,
        xaxis_title="Rolling 12 months", 
        yaxis_title="Unemployment Rate (%)", 
        xaxis_tickangle=-45,
        margin=dict(t=60, b=60, l=60, r=60),
        dragmode=False
    )
    st.plotly_chart(fig_unemployment, use_container_width=True)

# Individual tab for CPI (same formatting as other individual tabs)
elif selection == "CPI":
    st.markdown("<h1 style='text-align: center; color: #FF9800;'>CPI (Consumer Price Index)</h1>", unsafe_allow_html=True)
    st.markdown("""
    The **Consumer Price Index (CPI)** tracks the changes in prices for goods and services commonly purchased by urban consumers.
    
    A rising CPI indicates inflationary pressure, as consumers are paying more for goods and services. A **stable or falling CPI** suggests lower inflation or even deflation.
    """)
    cpi_data = df[df['seriesID'] == 'CUUR0000SA0']
    cpi_data['Date'] = pd.to_datetime(cpi_data['year'].astype(str) + '-' + cpi_data['period'].apply(lambda x: x[1:]), format='%Y-%m')
    cpi_data['Formatted Date'] = format_date(cpi_data['Date'])
    cpi_data = sort_data_by_date(cpi_data)

    fig_cpi = px.line(cpi_data, x='Formatted Date', y='value', title="CPI (Consumer Price Index)", labels={'value': 'CPI Value', 'Formatted Date': 'Month'})
    fig_cpi.update_traces(line=dict(width=4, color='orange'))
    fig_cpi.update_layout(
        title_font_size=20, 
        title_x=0.40,
        title_y=1.0,
        xaxis_title="Month", 
        yaxis_title="CPI Value", 
        xaxis_tickangle=-45,
        margin=dict(t=60, b=60, l=60, r=60),
        dragmode=False
    )
    st.plotly_chart(fig_cpi, use_container_width=True)

# Individual tab for PPI (same formatting as other individual tabs)
elif selection == "PPI":
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>PPI (Producer Price Index)</h1>", unsafe_allow_html=True)
    st.markdown("""
    The **Producer Price Index (PPI)** measures the changes in prices producers receive for their output.
    
    An increasing PPI suggests that producers are facing higher input costs, which may eventually lead to higher consumer prices (CPI). A **stable or declining PPI** signals a more stable price environment.
    """)
    ppi_data = df[df['seriesID'] == 'WPUFD4']
    ppi_data['Date'] = pd.to_datetime(ppi_data['year'].astype(str) + '-' + ppi_data['period'].apply(lambda x: x[1:]), format='%Y-%m')
    ppi_data['Formatted Date'] = format_date(ppi_data['Date'])
    ppi_data = sort_data_by_date(ppi_data)

    fig_ppi = px.line(ppi_data, x='Formatted Date', y='value', title="PPI (Producer Price Index)", labels={'value': 'PPI Value', 'Formatted Date': 'Month'})
    fig_ppi.update_traces(line=dict(width=4, color='green'))
    fig_ppi.update_layout(
        title_font_size=20, 
        title_x=0.40,
        title_y=1.0,
        xaxis_title="Month", 
        yaxis_title="PPI Value", 
        xaxis_tickangle=-45,
        margin=dict(t=60, b=60, l=60, r=60),
        dragmode=False
    )
    st.plotly_chart(fig_ppi, use_container_width=True)
