# ================================================
# HOTEL REVENUE MANAGEMENT DASHBOARD
# Author: Luiz Milaré
# Built with: Streamlit + Python
# ================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ================================================
# PAGE CONFIGURATION
# ================================================

st.set_page_config(
    page_title="Hotel Revenue Dashboard",
    page_icon="🏨",
    layout="wide"
)

# ================================================
# LOAD DATA FROM CSV (for deployment)
# ================================================

@st.cache_data
def load_data():
    """
    Load cleaned reservation data from CSV.
    Uses @st.cache_data to load data only ONCE.
    """
    df = pd.read_csv('hotel_reservations_clean.csv')
    
    # Recreate calculated columns
    df['total_guests'] = df['no_of_adults'] + df['no_of_children']
    
    return df

# ================================================
# HEADER
# ================================================

st.title("🏨 Hotel Revenue Management Dashboard")
st.markdown("**Real-time analytics for data-driven hotel revenue decisions**")
st.markdown("---")

# ================================================
# LOAD DATA
# ================================================

with st.spinner("Loading data..."):
    df = load_data()

st.success(f"✅ Loaded {len(df):,} reservations successfully!")

# ================================================
# SHOW SAMPLE DATA
# ================================================

st.subheader("📊 Sample Data")
st.dataframe(df.head(10), use_container_width=True)

# ================================================
# BASIC STATISTICS
# ================================================

st.subheader("📈 Quick Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Bookings", f"{len(df):,}")

with col2:
    confirmed = len(df[df['booking_status'] == 'Not_Canceled'])
    st.metric("Confirmed Bookings", f"{confirmed:,}")

with col3:
    avg_adr = df[df['booking_status'] == 'Not_Canceled']['avg_price_per_room'].mean()
    st.metric("Average ADR", f"${avg_adr:.2f}")

with col4:
    total_revenue = df[df['booking_status'] == 'Not_Canceled']['total_revenue'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.0f}")

    # ================================================
# SECTION 1: REVENUE BY MARKET SEGMENT
# ================================================

st.markdown("---")
st.header("💰 Revenue by Market Segment")

# Filter only confirmed bookings
df_confirmed = df[df['booking_status'] == 'Not_Canceled'].copy()

# Calculate revenue by segment
segment_revenue = df_confirmed.groupby('market_segment_type').agg({
    'total_revenue': 'sum',
    'Booking_ID': 'count',
    'avg_price_per_room': 'mean'
}).reset_index()

# Rename columns for clarity
segment_revenue.columns = ['Segment', 'Total Revenue', 'Bookings', 'ADR']

# Round values
segment_revenue['Total Revenue'] = segment_revenue['Total Revenue'].round(2)
segment_revenue['ADR'] = segment_revenue['ADR'].round(2)

# Sort by revenue
segment_revenue = segment_revenue.sort_values('Total Revenue', ascending=False)

# Create bar chart
fig1 = px.bar(
    segment_revenue,
    x='Segment',
    y='Total Revenue',
    title='Total Revenue by Market Segment',
    labels={'Total Revenue': 'Revenue ($)', 'Segment': 'Market Segment'},
    color='Total Revenue',
    color_continuous_scale='Blues',
    text='Total Revenue'
)

# Update layout
fig1.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
fig1.update_layout(showlegend=False, height=500)

# Display chart
st.plotly_chart(fig1, use_container_width=True)

# Display data table below chart
with st.expander("📊 View Detailed Data"):
    st.dataframe(segment_revenue, use_container_width=True)

# ================================================
# SECTION 2: MONTHLY REVENUE TREND
# ================================================

st.markdown("---")
st.header("📈 Monthly Revenue Trend")

# Group by year and month
monthly_revenue = df_confirmed.groupby(['arrival_year', 'arrival_month']).agg({
    'total_revenue': 'sum',
    'Booking_ID': 'count',
    'avg_price_per_room': 'mean'
}).reset_index()

# Rename columns
monthly_revenue.columns =['Year', 'Month', 'Revenue', 'Bookings', 'ADR']

# Create year-month label for better visualization
monthly_revenue['Period'] = monthly_revenue['Year'].astype(str) + '-' + monthly_revenue['Month'].astype(str).str.zfill(2)

# Sort by period
monthly_revenue = monthly_revenue.sort_values(['Year', 'Month'])

# Create line chart
fig2 = px.line(
    monthly_revenue,
    x='Period',
    y='Revenue',
    title='Monthly Revenue Trend',
    labels={'Revenue': 'Revenue ($)', 'Period': 'Month'},
    markers=True
)

# Update layout
fig2.update_traces(line_color='#1f77b4', line_width=3, marker=dict(size=8))
fig2.update_layout(height=500, hovermode='x unified')

# Display chart
st.plotly_chart(fig2, use_container_width=True)

# Show key insights
col1, col2, col3 = st.columns(3)

with col1:
    peak_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmax()]
    st.metric(
        "Peak Revenue Month",
        f"{peak_month['Period']}",
        f"{peak_month['Revenue']:.0f}"
    )

with col2:
    lowest_month = monthly_revenue.loc[monthly_revenue['Revenue'].idxmin()]
    st.metric(
        "Lowest Revenue Month",
        f"{lowest_month['Period']}",
        f"{lowest_month['Revenue']:.0f}"
    )

with col3:
    avg_monthly = monthly_revenue['Revenue'].mean()
    st.metric(
        "Average Monthly Revenue",
        f"${avg_monthly:.0f}"
    )

# Show data table
with st.expander("📊 View Monthly Data"):
    st.dataframe(monthly_revenue[['Period','Revenue', 'Bookings', 'ADR']], use_container_width=True)

# ================================================
# SECTION 3: CANCELLATION ANALYSIS BY LEAD TIME
# ================================================

st.markdown("---")
st.header("⚠️ Cancellation Analysis by Lead Time")

# Create lead time buckets
def categorize_lead_time(days):
    if days < 7:
        return '1. Last Minute (0-6 days)'
    elif days < 30:
        return '2. Short Notice (7-29 days)'
    elif days < 90:
        return '3. Standard (30-89 days)'
    elif days < 180:
        return '4. Early Booking (90-179 days)'
    else:
        return '5. Very Early (180+ days)'

# Apply categorization
df['booking_window'] = df['lead_time'].apply(categorize_lead_time)

# Calculate cancellation rate by booking window
cancel_analysis = df.groupby('booking_window').agg({
    'Booking_ID': 'count',
    'booking_status': lambda x: (x == 'Canceled').sum(),
    'avg_price_per_room': 'mean',
    'lead_time': 'mean'
}).reset_index()

# Rename columns
cancel_analysis.columns = ['Booking Window', 'Total Bookings', 'Canceled', 'ADR', 'Avg Lead Time']

# Calculate cancellation rate percentage
cancel_analysis['Cancellation Rate (%)'] = (cancel_analysis['Canceled'] / cancel_analysis['Total Bookings'] * 100).round(1)

# Sort by booking window
cancel_analysis = cancel_analysis.sort_values('Booking Window')

# Create combined bar chart
fig3 = px.bar(
    cancel_analysis,
    x='Booking Window',
    y='Cancellation Rate (%)',
    title='Cancellation Rate by Booking Window',
    labels={'Cancellation Rate (%)': 'Cancellation Rate (%)', 'Booking Window': 'Booking Window'},
    color='Cancellation Rate (%)',
    color_continuous_scale='Reds',
    text='Cancellation Rate (%)'
)

# Update traces
fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig3.update_layout(showlegend=False, height=500)

# Display chart
st.plotly_chart(fig3, use_container_width=True)

# Show insights based on YOUR analysis!
st.subheader("💡 Key Insights & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🔴 High Risk Categories:**
    - **Very Early (180+ days):** 73.8% cancellation rate
    - **Problem:** High volume but very unreliable
    
    **Recommendation:**
    - Implement non-refundable advance purchase rate with 20-25% discount
    - Require deposit for bookings 180+ days in advance
    """)

with col2:
    st.markdown("""
    **✅ Low Risk Categories:**
    - **Last Minute (0-6 days):** ~10% cancellation rate
    - **Opportunity:** Most reliable segment
    
    **Recommendation:**
    - Implement dynamic pricing: +20-30% premium for urgency
    - Offer incentives to increase volume in this segment
    """)

# Show data table
with st.expander("📊 View Detailed Cancellation Data"):
    st.dataframe(cancel_analysis, use_container_width=True)

# ================================================
# SECTION 4: ROOM TYPE PERFORMANCE
# ================================================

st.markdown("---")
st.header("🏨 Room Type Performance Analysis")

# Calculate metrics by room type
room_analysis = df.groupby('room_type_reserved').agg({
    'Booking_ID': 'count',
    'booking_status': lambda x:(x == 'Canceled').sum(),
    'total_revenue': lambda x: x[df.loc[x.index, 'booking_status'] == 'Not_Canceled'].sum(),
    'avg_price_per_room': lambda x: x[df.loc[x.index, 'booking_status'] == 'Not_Canceled'].mean()
}).reset_index()

# Rename columns
room_analysis.columns = ['Room Type', 'Total Bookings', 'Canceled', 'Total Revenue', 'ADR']

# Calculate additional metrics
room_analysis['Confirmed'] = room_analysis['Total Bookings'] - room_analysis['Canceled']
room_analysis['Cancellation Rate (%)'] = (room_analysis['Canceled'] / room_analysis['Total Bookings'] *100).round(1)
room_analysis['Revenue per Booking'] = (room_analysis['Total Revenue'] / room_analysis['Total Bookings']).round(2)


# Round values
room_analysis['Total Revenue'] = room_analysis['Total Revenue'].round(2)
room_analysis['ADR'] = room_analysis['ADR'].round(2)

# Sort by total revenue
room_analysis = room_analysis.sort_values('Total Revenue', ascending=False)

# Create two columns for side-by-side charts
col1, col2 = st.columns(2)

# ================================================
# CHART 1: Total Revenue by Room Type
# ================================================

with col1:
    fig4a = px.bar(
        room_analysis,
        x='Room Type',
        y='Total Revenue',
        title='Total Revenue by Room Type',
        labels={'Total Revenue': 'Revenue ($)', 'Room Type': 'Room Type'},
        color='Total Revenue',
        color_continuous_scale='Blues',
        text='Total Revenue'
    )
    
    fig4a.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig4a.update_layout(showlegend=False, height=450)
    
    st.plotly_chart(fig4a, use_container_width=True)

# ================================================
# CHART 2: ADR vs Cancellation Rate
# ================================================

with col2:
    # Create figure
    fig4b = go.Figure()
    
    # Add ADR bars (green)
    fig4b.add_trace(go.Bar(
        name='ADR ($)',
        x=room_analysis['Room Type'],
        y=room_analysis['ADR'],
        yaxis='y',
        marker_color='#2ca02c',
        text=room_analysis['ADR'],
        texttemplate='$%{text:.0f}',
        textposition='outside',
        offsetgroup=1  
    ))
    
    # Add Cancellation Rate bars (red)
    fig4b.add_trace(go.Bar(
        name='Cancellation Rate (%)',
        x=room_analysis['Room Type'],
        y=room_analysis['Cancellation Rate (%)'],
        yaxis='y2',
        marker_color='#d62728',
        text=room_analysis['Cancellation Rate (%)'],
        texttemplate='%{text:.1f}%',
        textposition='outside',
        offsetgroup=2  
    ))
    
    # Update layout
    fig4b.update_layout(
        title='ADR vs Cancellation Rate by Room Type',
        xaxis=dict(title='Room Type'),
        yaxis=dict(
            title='ADR ($)',
            side='left',
            showgrid=False,
            range=[0, room_analysis['ADR'].max() * 1.2]  
        ),
        yaxis2=dict(
            title='Cancellation Rate (%)',
            side='right',
            overlaying='y',
            showgrid=False,
            range=[0, room_analysis['Cancellation Rate (%)'].max() * 1.2]  
        ),
        barmode='group',
        height=450,
        legend=dict(x=0.01, y=0.99),
        bargap=0.2  
    )
    
    st.plotly_chart(fig4b, use_container_width=True)

# Show strategic recommendations
st.subheader("💎 Strategic Recommendations by Room Type")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🔴 Critical Issues:**
    
    **Room Type 2:**
    - Low volume (557)
    - Low ADR ($83.38)
    - High cancellation (33.2%)
    
    **Action:** Phase out or convert to better room type
    """)

with col2:
    st.markdown("""
    **💎 Hidden Gem:**
    
    **Room Type 5:**
    - Low volume but lowest cancellation (27.2%)
    - Good ADR ($118.31)
    
    **Action:** Increase marketing, improve visibility, test pricing optimization
    """)

with col3:
    st.markdown("""
    **🏆 Premium Opportunity:**
    
    **Room Type 6:**
    - Highest ADR ($178.53)
    - Highest revenue per booking ($507.85)
    - BUT: 42.2% cancellation
    
    **Action:** Non-refundable rate with perks, minimum 2-night stay
    """)

# Detailed metrics table
st.subheader("📊 Detailed Room Type Metrics")
display_cols = ['Room Type', 'Total Bookings', 'Confirmed', 'Canceled', 'Cancellation Rate (%)', 
                'ADR', 'Total Revenue', 'Revenue per Booking']
st.dataframe(room_analysis[display_cols], use_container_width=True)