# Part 1 
import pandas as pd 
import os 
import plotly.express as px 
import plotly.graph_objects as go 

# Set Working Directory
os.chdir(r'D:\Mission_Blitzkreig\12.Load_clean_calculate_metrics')

# Load your day 12 data 
df = pd.read_csv('ooh_campaigns.csv')

# Recalculate the metrics from Day 12 
df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
df['cpm'] = (df['spend'] / df['impressions'] / 1000).round(2)
df['roi'] = ((df['revenue'] - df['spend']) / df['spend'] * 100).round(2)
df['cvr'] = (df['conversions'] / df['clicks'] * 100).round(2)
df['profit'] = df['revenue'] - df['spend']

print ("Data loaded & Mterics Calculated")


# Part 2 (Bar chart revenue by city)
# Group data by city and revenue 
# Create bar chart 
# Show the bar chart 
# Save the html 

# Part 2: Bar Chart - Revenue by City

# Group data by city
city_revenue = df.groupby('city')['revenue'].sum().reset_index()
city_revenue = city_revenue.sort_values('revenue', ascending=False)

# Create bar chart
fig = px.bar(
    city_revenue,
    x='city',
    y='revenue',
    title='Total Revenue by City',
    labels={'revenue': 'Revenue (€)', 'city': 'City'},
    color='revenue',
    color_continuous_scale='Blues'
)

# Customize layout
fig.update_layout(
    xaxis_title="City",
    yaxis_title="Revenue (€)",
    font=dict(size=14),
    height=500
)

# Show the chart
fig.show()

# Save as HTML
fig.write_html('revenue_by_city.html')
print("✅ Chart saved: revenue_by_city.html")

# Part 3 Visualize spend vs revenue 
# Create scatter plot
df_clean = df.dropna(subset=['impressions'])

fig = px.scatter(
    df,
    x='spend',
    y='revenue',
    size='impressions',  # Bubble size = impressions
    color='roi',  # Color by ROI
    hover_data=['campaign_name', 'city', 'format'],
    title='Campaign Performance: Spend vs Revenue',
    labels={'spend': 'Spend (€)', 'revenue': 'Revenue (€)'},
    color_continuous_scale='RdYlGn'  # Red to Green
)

# Add diagonal line (break-even line)
fig.add_trace(go.Scatter(
    x=[0, df['spend'].max()],
    y=[0, df['spend'].max()],
    mode='lines',
    name='Break-even',
    line=dict(color='red', dash='dash')
))

# Customize
fig.update_layout(
    xaxis_title="Spend (€)",
    yaxis_title="Revenue (€)",
    font=dict(size=14),
    height=600
)

fig.show()
fig.write_html('spend_vs_revenue.html')
print("✅ Chart saved: spend_vs_revenue.html")

# Part 4 : Bar Chart ROI by format 
# Group by format 

format_roi = df.groupby('format').agg({
'roi' : 'mean',
'revenue' : 'sum'
}).reset_index()

format_roi = format_roi.sort_values('roi',ascending=False)

# Create Bar Chart 
fig = px.bar(
    format_roi,
    x='format',
    y='roi',
    title='Average ROI by Format',
    labels={'roi': 'Average ROI(%)', 'format': 'Ad Format'},
    color='roi',
    color_continuous_scale='Viridis',
    text='roi'
)

# Format text on bars 
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')

fig.update_layout(
    xaxis_title="Ad Format",
    yaxis_title="AvergeROI(%)",
    font=dict(size=14),
    height=500
)
fig.show()
fig.write_html('roi_by_format.htmml')
print("Part 4 : roi_by_format.html")

# Part 5 : Multi-Metric Comparision 
# Compare multiple metrics by city 

city_metrics = df.groupby('city').agg({
    'spend': 'sum',
    'revenue': 'sum',
    'profit':'sum',
    'roi': 'mean',
    'ctr':'mean'
}).reset_index()

# Create grouped bar chart 
fig = go.Figure()

fig.add_trace(go.Bar(
    name='Spend',
    x=city_metrics['city'],
    y=city_metrics['spend'],
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    name='Revenue',
    x=city_metrics['city'],
    y=city_metrics['revenue'],
    marker_color='lightsalmon'
))

fig.add_trace(go.Bar(
    name='Profit',
    x=city_metrics['city'],
    y=city_metrics['profit'],
    marker_color='lightgreen'
))

fig.update_layout(
    title='City Performance: Spend, Revenue, and Profit',
    xaxis_title='City',
    yaxis_title='Amount (€)',
    barmode='group',
    font=dict(size=14),
    height=500
)

fig.show()
fig.write_html('city_performance_comparison.html')
print("✅ Chart saved: city_performance_comparison.html")

# Part 6 : Top Performance Chart 
top_campaigns =df.nlargest(5,'roi')[['campaign_name','roi','revenue','spend']]

# Create horizontal bar 
fig =px.bar(
    top_campaigns,
    y='campaign_name',
    x='roi',
    orientation='h',
    title='Top 5 Campaigns by ROI',
    labels={'roi': 'ROI (%)', 'campaign_name': 'Campaign'},
    color='roi',
    color_continuous_scale='Greens',
    text='roi'
)

fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')

fig.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    xaxis_title="ROI (%)",
    yaxis_title="",
    font=dict(size=12),
    height=400
)

fig.show()
fig.write_html('top_campaigns.html')
print("✅ Chart saved: top_campaigns.html")

