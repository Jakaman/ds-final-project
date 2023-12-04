#!/usr/bin/env python
# coding: utf-8

# In[31]:


import dash
import dash_core_components as dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import ipywidgets as widgets
from dash.dependencies import Input, Output


# In[32]:


data = pd.read_excel("../data/Data_FINAL_PROJECT.xlsx")
data = data.drop(index=0)

data = data.drop(columns=['Mapped_Country'])

for col in data: 
    if col !='Country':
        
        data[col] = pd.to_numeric(data[col], errors = 'coerce')
        


# In[33]:


for year in range(2014, 2023):
    export_column = f'Exports_{year}'
    import_column = f'Imports_{year}'
    gdp_column = f'GDP_{year}'
    openness_column = f'Openness_{year}'
    inflation_column = f'Inflation_{year}'


    data[export_column] = data[export_column].astype(float)
    data[import_column] = data[import_column].astype(float)

    #Trade Openness formula
    data[openness_column] = (data[export_column] + data[import_column]) / 2 / data[gdp_column] * 100


# In[34]:


Asia_countries = data.iloc[0:20]
Asia_countries = Asia_countries[Asia_countries.Country != 'China, P.R.: Mainland']
Europe_countries = data.iloc[20:34]
Middle_east_central_asia_countries = data.iloc[34:57]
Sub_saharan_africa_countries =data.iloc[57:91] 
Western_hemisphere_countries =data.iloc[91:114] 


# In[35]:


regional_data = {
    'Asia': Asia_countries,  # Remplacez par vos DataFrames
    'Sub-Saharan Africa': Sub_saharan_africa_countries,
    'Middle East and Central Asia': Middle_east_central_asia_countries,
    'Western Hemisphere': Western_hemisphere_countries,
    'Europe': Europe_countries
}

# Définition des années et des colonnes correspondantes pour les variables
years = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
export_columns = [f'Exports_{year}' for year in years]
import_columns = [f'Imports_{year}' for year in years]
gdp_columns = [f'GDP_{year}' for year in years]
openness_columns = [f'Openness_{year}' for year in years]
inflation_columns = [f'Inflation_{year}' for year in years]
# Widgets pour la sélection du continent et de la variable
continent_selector = widgets.Dropdown(
    options=['Asia', 'Sub-Saharan Africa', 'Middle East and Central Asia', 'Western Hemisphere', 'Europe'],
    value='Asia',
    description='Continent:',
)

variable_selector = widgets.Dropdown(
    options=['Exports', 'Imports', 'GDP', 'Openness','Inflations'],
    value='Exports',
    description='Variable:',
)


# In[36]:


# Initialize the Dash app
app = dash.Dash(__name__,assets_folder='../assets')

# Define the app layout
app.layout = html.Div([
    html.H1("Dynamics of GDP Growth: The Impact of International Trade Variables"),
    
    dcc.Markdown("""
        ## Introduction
        As a graduate in economics, I wanted to undertake a project related to this field. 
        Therefore, I decided to conduct an analysis related to international trade. Moreover,
        I aim to analyze the impact of this on the economies of emerging countries.

        Objective: To analyze the effect of variables closely related to international trade and examine their impact on the GDP. For my project, I have decided to divide everything into specific regions to facilitate the task and not to do it by country due to the time constraints I have to complete the project
        
        ## Variables definition
        GDP (US$ in millions) : Gross domestic product. The total monetary or market value of all the finished goods and services produced within a country’s borders in a specific time period. 

        Importation (US$ in millions): The bringing of goods or services into a country from abroad for sale

        Exportation (US$ in millions):  The process of selling goods in another country.

        Trade Balance: The difference between the value of a country’s exports and imports for a given period. So basically, trade balance equals to Exports – Imports. If trade balance > 0 = surplus, trade balance < 0 = deficit. 

        Inflation (%): An increase of prices of goods and service over time, causing a reduction in the value of money. 

        Openness (%): Measure of the extent to which a country is engaged in the global trading system. 

                                  Trade Openness = (Exports +Imports/ 2*GDP) x100%

        
        ## Data cleaning and preprocessing
        
        International Monetary Fund : 

          -	  Exportations
          -	  Importations

        The World Bank : 

          -	  GDP
          -	  Inflation 
          
        Steps : 
          
          - Read the files
          - Create trade balance variable 
          - Merge export, import and trade balance
          - Merge with GDP and inflation with mapping
          - Create trade openess variable
          - Convert GDP into millions US $ to match exports & imports

        
        ## Data visualisation
    """),
    
    # Dropdown for Continent Selection
    dcc.Dropdown(
        id='continent-selector',
        options=[{'label': i, 'value': i} for i in regional_data.keys()],
        value='Asia',
    ),

    # Dropdown for Variable Selection
    dcc.Dropdown(
        id='variable-selector',
        options=[
            {'label': 'Exports', 'value': 'Exports'},
            {'label': 'Imports', 'value': 'Imports'},
            {'label': 'GDP', 'value': 'GDP'},
            {'label': 'Openness', 'value': 'Openness'},
            {'label': 'Inflation', 'value': 'Inflation'},
        ],
        value='Exports',
    ),

    # Graph Component
    dcc.Graph(id='interactive-graph'),

    dcc.Markdown("""
        ### Visualisation interpretation 
        All regions experience growth in trade. Notably, Europe's and Asia's trade trajectories appear steeper compared to the other regions.
        Each regions's GDP increased but the Western Hemisphere and Sub-Saharan Afica showed occasional dips. The western Hemisphere seems to be constantly in a deficit situation due to Imports > Exports for all the year. 
        The Inflation rate is more varied among regions. Some regions, like Asia, show a marked increase in inflation in the latter years. Middle and Central Asia, exhibit significant volatility, suggesting instability in consumer prices. 
        
        ## Analysis
        
        Following the display of the graphs, to better understand the impact of my studied variables on the GDP,
        I chose to use a regression model. 
        I implemented the LinearRegression() model from sklearn in a log-log framework. 
        This log-log approach was chosen for several key reasons. 
        It transforms proportional relationships into linear ones, which makes the interpretation of regression coefficients simpler. Additionally, this method is particularly effective for modeling economic relationships, where many variables such as GDP, exports, and imports often follow log-normal distributions.
        By using this approach, I was able to achieve more accurate and robust results compared to a standard linear model, providing more concrete and meaningful insights into the impact of these economic variables on GDP.
"""),

dcc.Dropdown(
        id='continent-selector-reg',
        options=[
            {'label': 'Asia', 'value': 'asiareg.png'},
            {'label': 'Africa', 'value': 'Africa-subreg.png'},
            {'label': 'Europe', 'value': 'Europereg.png'},
            {'label': 'Middle East', 'value': 'middlereg.png'},
            {'label': 'Western Hemisphere', 'value': 'westreg.png'},
        ],
        value='asiareg.png',  # Default value
    ),
    
    # Image placeholder
    html.Img(id='continent-image', style={'width': '70%', 'height': 'auto'}),
    # Below the 'continent-image' component in your layout:
    html.Div(id='interpretation-text', style={'margin-top': '20px'}),

    dcc.Markdown("""
        ## Global summary 
        
        ### Exports
         
         Globally, exports consistently show a positive impact on GDP across all regions.
         The increase in GDP ranges broadly but remains significant, suggesting that higher export levels are generally beneficial for economic growth.
         Regions like Asia and Europe exhibit particularly strong positive relationships between exports and GDP.
        
        ### Imports
        
        Imports also demonstrate a positive correlation with GDP in most regions.
        This positive effect varies across regions, indicating that imports can stimulate economic growth, possibly due to the import of essential goods and capital.
        
        ### Inflation
        
        The impact of inflation on GDP is mixed and generally smaller compared to exports and imports.
        Some regions exhibit a slight negative impact of inflation on GDP, while in others, the effect is slightly positive or inconsistent.
        This variation suggests that the economic context and monetary policies of each region play a significant role in determining how inflation affects GDP.
        
        ### The Openess Problem 
        
        The negative impact of openness on GDP could be viewed as a counterintuitive interpretation. 
        However, to have a more detailed explanation, it is necessary to take into account that a country more open to the international economy does not necessarily mean that it will become richer. 
        In my study, the reason for the negative effect of the degree of openness can be explained in several ways. 
        For example, if the trade balance is negative (more imports than exports), this can possibly affect the GDP negatively.
        Moreover, greater openness means more competition for local businesses, so they can lose market share, which reduces local production and employment. This can also be explained by the economic policies of countries; loss of control of resources to foreigners, etc.
        
        ### R-Squared Values
        
        High R-squared values  and low mean squared errors across most models suggest a good fit, indicating that the models capture a significant portion of the variability in GDP.
    
        ## Conclusion
        This analysis of international trade's impact on GDP in various regions highlights key findings. 
        Exports consistently boost GDP across regions, confirming their vital role in economic growth.
        While imports generally show a positive influence, the negative relationship between trade openness and GDP growth is notable, suggesting complexities in global trade dynamics. 
        These insights underscore the need for region-specific trade policies and strategies, especially in emerging economies. The study offers a broad perspective on trade and economic development, emphasizing the importance of nuanced and informed economic policymaking.
        
        
    """),
])

# Callback for updating the graph
@app.callback(
    Output('interactive-graph', 'figure'),
    [Input('continent-selector', 'value'),
     Input('variable-selector', 'value')]
)
def update_graph(selected_continent, selected_variable):
    region_df = regional_data[selected_continent]
    y_data = None
    if selected_variable == 'Exports':
        y_data = region_df[export_columns].mean() 
    elif selected_variable == 'Imports':
        y_data = region_df[import_columns].mean() 
    elif selected_variable == 'GDP':
        y_data = region_df[gdp_columns].mean() 
    elif selected_variable == 'Openness':
        y_data = region_df[openness_columns].mean()
    elif selected_variable == 'Inflation':
        y_data = region_df[inflation_columns].mean()

    fig = go.Figure(data=go.Scatter(x=years, y=y_data, mode='lines+markers'))
    fig.update_layout(title=f'{selected_variable} for {selected_continent}',
                      xaxis_title='Year',
                      yaxis_title=selected_variable)
    return fig

@app.callback(
    Output('continent-image', 'src'),
    [Input('continent-selector-reg', 'value')]
)
def update_image(selected_image):
    # Update the image source
    return f'/assets/{selected_image}'
# New callback for updating the interpretation text based on the selected continent
@app.callback(
    Output('interpretation-text', 'children'),
    [Input('continent-selector-reg', 'value')]
)
def update_interpretation(selected_continent):
    if selected_continent == 'Africa-subreg.png':  # This should match the value for Africa in the dropdown
        return [
            html.P("Exports: A 1% increase in exports typically raises GDP by 0.833% to 0.978%, showing a strong positive effect."),
            html.P("Imports: A 1% rise in imports is linked to a 0.600% to 0.977% GDP growth, with some yearly variation."),
            html.P("Inflation: The effect of inflation on GDP is minor and inconsistent, varying from a 0.016% decrease to a 0.047% increase."),
            html.P("Openness: Increasing openness by 1% correlates with a 0.568% to 0.649% reduction in GDP, suggesting a consistent negative impact.")
        ]
    elif selected_continent == 'asiareg.png':
        return [
            html.P("Exports: A 1% increase in exports correlates with a 0.55% to 0.64% increase in GDP. This demonstrates a consistently positive and moderately strong effect of exports on GDP."),
            html.P("Imports: : A 1% rise in imports is associated with a 0.33% to 0.42% increase in GDP. This indicates a positive impact of imports on GDP, though it's less pronounced compared to exports."),
            html.P("Inflation: The effect of inflation on GDP is mixed, ranging from a slight decrease to a moderate increase. This suggests a variable influence of inflation on GDP, possibly contingent on other economic conditions"),
            html.P("Openness: Each 1% increase in openness typically results in a decrease in GDP by about 1.03% to 1.10%. This consistently indicates a negative impact of openness on GDP.")
        ]
    elif selected_continent == 'Europereg.png':
        return [
            html.P("A 1% increase in exports correlates with about a 0.70% to 0.80% increase in GDP. This indicates a consistently strong and positive effect of exports on GDP."),
            html.P("A 1% rise in imports is associated with a 0.24% to 0.31% increase in GDP. This suggests a positive but less pronounced impact of imports on GDP compared to exports."),
            html.P("The impact of inflation on GDP is mixed, ranging from a slight decrease to a slight increase. This suggests a generally neutral or marginal effect of inflation on GDP, with variations across the years."),
            html.P("Each 1% increase in openness typically results in a decrease in GDP by about 1.03% to 1.21%. This consistently indicates a negative impact of openness on GDP.")
        ]
    elif selected_continent == 'middlereg.png':
        return [
            html.P("Exports: A 1% rise in exports is associated with an approximate 0.7% to 0.9% increase in GDP, indicating a robust positive effect."),
            html.P("Imports: A 1% increase in imports correlates with approximately a 0.35% to 0.59% GDP growth, displaying variable positive impacts."),
            html.P("Inflation: A 1% uptick in inflation typically results in a slight GDP reduction, suggesting a consistent negative influence."),
            html.P("Openness: Each 1% increase in openness tends to decrease GDP by about 0.66% to 0.81%, consistently showing a negative effect."),
        ]
    elif selected_continent == 'westreg.png':
        return [
            html.P("Exports: A 1% increase in exports correlates with approximately a 0.79% to 1.13% increase in GDP, showing a consistently positive and strong effect."),
            html.P("Imports: A 1% rise in imports is linked with about a 0.53% to 0.87% increase in GDP, indicating a variable but generally positive impact."),
            html.P("Inflation: Inflation's effect ranges from a slight decrease (about -0.04%) to an increase (about 0.09%) in GDP, suggesting a mixed influence."),
            html.P("Openness: Each 1% increase in openness typically results in a decrease in GDP by about 0.41% to 0.63%, consistently indicating a negative impact."),
        ]
    else:
    
        return "" 
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# 
