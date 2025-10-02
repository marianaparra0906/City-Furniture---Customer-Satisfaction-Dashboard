import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io

# Configure page
st.set_page_config(
    page_title="Customer Satisfaction Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for responsive design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }

    .metric-card {
        background: linear-gradient(90deg, #f0f2f6, #ffffff);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }

    .risk-high { border-left-color: #ff4444 !important; }
    .risk-medium { border-left-color: #ffaa00 !important; }
    .risk-low { border-left-color: #00aa00 !important; }

    @media (max-width: 768px) {
        .main-header { font-size: 1.8rem; }
        .metric-card { margin: 0.25rem 0; }
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data for the dashboard
@st.cache_data
def load_data():
    # Daily satisfaction scores from May 30 to Sept 30, 2025
    start_date = datetime(2025, 5, 30)
    end_date = datetime(2025, 9, 30)
    date_range = pd.date_range(start_date, end_date, freq='D')

    # Generate realistic daily satisfaction scores
    np.random.seed(42)
    base_scores = np.random.normal(8.5, 1.2, len(date_range))

    # Add seasonal trends and promotion effects
    daily_data = []
    for i, date in enumerate(date_range):
        score = base_scores[i]

        # Weekend effect (slightly lower satisfaction)
        if date.weekday() >= 5:
            score -= 0.3

        # Promotion periods (higher satisfaction)
        if date.month == 6 and date.day in range(15, 21):  # June promotion
            score += 1.5
        if date.month == 8 and date.day in range(1, 8):    # August promotion
            score += 1.2
        if date.month == 9 and date.day in range(20, 27):  # September promotion
            score += 1.8

        # Special events (mixed effects)
        if date.month == 7 and date.day == 15:  # System maintenance
            score -= 2.5
        if date.month == 8 and date.day == 20:  # Store renovation
            score -= 1.8

        # Ensure realistic bounds
        score = max(0, min(10, score))

        daily_data.append({
            'date': date,
            'satisfaction_score': round(score, 1),
            'month': date.strftime('%B %Y'),
            'month_short': date.strftime('%b'),
            'day_name': date.strftime('%A'),
            'is_weekend': date.weekday() >= 5,
            'week': date.isocalendar()[1]
        })

    daily_df = pd.DataFrame(daily_data)

    # Monthly aggregated data
    monthly_data = daily_df.groupby('month').agg({
        'satisfaction_score': ['mean', 'count', 'std'],
        'is_weekend': 'sum'
    }).round(2)

    monthly_data.columns = ['avg_satisfaction', 'total_responses', 'std_satisfaction', 'weekend_days']
    monthly_data = monthly_data.reset_index()

    # Critical events data
    critical_events = [
        {
            'date': datetime(2025, 6, 18),
            'event': 'Father Day Promotion Launch',
            'severity': 'Low',
            'impact': 'Positive',
            'satisfaction_impact': '+1.5',
            'promotion_type': 'Seasonal',
            'description': 'Special furniture discounts for Father Day'
        },
        {
            'date': datetime(2025, 7, 15),
            'event': 'System Maintenance Downtime',
            'severity': 'High',
            'impact': 'Negative',
            'satisfaction_impact': '-2.5',
            'promotion_type': 'None',
            'description': 'Unexpected system downtime affecting online orders'
        },
        {
            'date': datetime(2025, 8, 5),
            'event': 'Summer Sale Event',
            'severity': 'Medium',
            'impact': 'Positive',
            'satisfaction_impact': '+1.2',
            'promotion_type': 'Sale',
            'description': 'Major summer furniture clearance event'
        },
        {
            'date': datetime(2025, 8, 20),
            'event': 'Store Renovation Disruption',
            'severity': 'Medium',
            'impact': 'Negative',
            'satisfaction_impact': '-1.8',
            'promotion_type': 'None',
            'description': 'Main showroom renovation causing service delays'
        },
        {
            'date': datetime(2025, 9, 23),
            'event': 'Fall Collection Preview',
            'severity': 'Low',
            'impact': 'Positive',
            'satisfaction_impact': '+1.8',
            'promotion_type': 'Product Launch',
            'description': 'Exclusive preview of new fall furniture collection'
        }
    ]

    events_df = pd.DataFrame(critical_events)

    # Risk analysis data
    risk_data = [
        {'category': 'Service Quality', 'probability': 0.7, 'impact': 0.8, 'current_score': 7.2, 'target_score': 9.0},
        {'category': 'Product Availability', 'probability': 0.4, 'impact': 0.9, 'current_score': 8.1, 'target_score': 9.0},
        {'category': 'Delivery Times', 'probability': 0.6, 'impact': 0.7, 'current_score': 6.8, 'target_score': 9.0},
        {'category': 'Customer Support', 'probability': 0.3, 'impact': 0.6, 'current_score': 8.5, 'target_score': 9.0},
        {'category': 'Pricing Satisfaction', 'probability': 0.5, 'impact': 0.8, 'current_score': 7.6, 'target_score': 9.0},
        {'category': 'Website Experience', 'probability': 0.2, 'impact': 0.5, 'current_score': 8.9, 'target_score': 9.0}
    ]

    risk_df = pd.DataFrame(risk_data)
    risk_df['risk_score'] = risk_df['probability'] * risk_df['impact']
    risk_df['performance_gap'] = risk_df['target_score'] - risk_df['current_score']

    return daily_df, monthly_data, events_df, risk_df

# Load data
daily_df, monthly_data, events_df, risk_df = load_data()

# Sidebar
st.sidebar.markdown("### 📊 Dashboard Navigation")
st.sidebar.markdown("---")

# Main header
st.markdown('<h1 class="main-header">City Furniture - Customer Satisfaction Dashboard</h1>', 
           unsafe_allow_html=True)
st.markdown("**Period: May 30 - September 30, 2025**")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Daily Timeline", "📊 Monthly Comparison", "🚨 Critical Events", "⚠️ Risk Analysis"])

# TAB 1: Daily Timeline
with tab1:
    st.header("Daily Satisfaction Timeline")

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        month_filter = st.selectbox(
            "Filter by Month:",
            options=["All Months"] + sorted(daily_df['month'].unique()),
            key="daily_month_filter"
        )

    with col2:
        show_weekends = st.checkbox("Highlight Weekends", value=True)

    with col3:
        show_target = st.checkbox("Show Target Line (9.0)", value=True)

    # Filter data based on selection
    filtered_daily = daily_df.copy()
    if month_filter != "All Months":
        filtered_daily = daily_df[daily_df['month'] == month_filter]

    # Create timeline chart
    fig_timeline = go.Figure()

    # Main satisfaction line
    fig_timeline.add_trace(go.Scatter(
        x=filtered_daily['date'],
        y=filtered_daily['satisfaction_score'],
        mode='lines+markers',
        name='Daily Satisfaction',
        line=dict(color='#1f77b4', width=2),
        marker=dict(
            size=6,
            color=np.where(filtered_daily['satisfaction_score'] < 9.0, 'red', '#1f77b4'),
            line=dict(width=1, color='white')
        ),
        hovertemplate='<b>%{x|%B %d, %Y}</b><br>' +
                      'Satisfaction: %{y}<br>' +
                      '<extra></extra>'
    ))

    # Add target line
    if show_target:
        fig_timeline.add_hline(
            y=9.0,
            line_dash="dash",
            line_color="green",
            annotation_text="Target (9.0)",
            annotation_position="bottom right"
        )

    # Highlight weekends
    if show_weekends:
        weekend_data = filtered_daily[filtered_daily['is_weekend']]
        if not weekend_data.empty:
            fig_timeline.add_trace(go.Scatter(
                x=weekend_data['date'],
                y=weekend_data['satisfaction_score'],
                mode='markers',
                name='Weekends',
                marker=dict(size=8, color='orange', symbol='diamond'),
                hovertemplate='<b>%{x|%B %d, %Y} (Weekend)</b><br>' +
                              'Satisfaction: %{y}<br>' +
                              '<extra></extra>'
            ))

    # Update layout for responsiveness
    fig_timeline.update_layout(
        title="Daily Customer Satisfaction Scores",
        xaxis_title="Date",
        yaxis_title="Satisfaction Score",
        hovermode='closest',
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Make responsive
    fig_timeline.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=50, b=0),
    )

    st.plotly_chart(fig_timeline, use_container_width=True)

    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_score = filtered_daily['satisfaction_score'].mean()
        st.metric("Average Score", f"{avg_score:.1f}")

    with col2:
        below_target = (filtered_daily['satisfaction_score'] < 9.0).sum()
        st.metric("Days Below Target", below_target)

    with col3:
        best_day = filtered_daily.loc[filtered_daily['satisfaction_score'].idxmax()]
        st.metric("Best Score", f"{best_day['satisfaction_score']:.1f}")

    with col4:
        worst_day = filtered_daily.loc[filtered_daily['satisfaction_score'].idxmin()]
        st.metric("Lowest Score", f"{worst_day['satisfaction_score']:.1f}")

# TAB 2: Monthly Comparison
with tab2:
    st.header("Monthly Performance Comparison")

    # Monthly selector
    comparison_months = st.multiselect(
        "Select months to compare:",
        options=monthly_data['month'].tolist(),
        default=monthly_data['month'].tolist(),
        key="monthly_comparison"
    )

    if comparison_months:
        comparison_data = monthly_data[monthly_data['month'].isin(comparison_months)]

        # Monthly cards
        st.subheader("Monthly Performance Cards")

        cols = st.columns(len(comparison_data))
        for i, (_, month_data) in enumerate(comparison_data.iterrows()):
            with cols[i]:
                score = month_data['avg_satisfaction']
                color_class = "risk-high" if score < 7 else "risk-medium" if score < 8.5 else "risk-low"

                st.markdown(f"""
                <div class="metric-card {color_class}">
                    <h3>{month_data["month"]}</h3>
                    <h2>{score:.1f}/10</h2>
                    <p>{month_data["total_responses"]} responses</p>
                    <p>Std Dev: {month_data["std_satisfaction"]:.1f}</p>
                </div>
                """, unsafe_allow_html=True)

        # Bar charts
        col1, col2 = st.columns(2)

        with col1:
            fig_bar = px.bar(
                comparison_data,
                x='month',
                y='avg_satisfaction',
                title="Average Satisfaction by Month",
                color='avg_satisfaction',
                color_continuous_scale='RdYlGn',
                range_color=[6, 10]
            )
            fig_bar.add_hline(y=9.0, line_dash="dash", line_color="red", 
                             annotation_text="Target (9.0)")
            fig_bar.update_layout(height=400)
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            fig_responses = px.bar(
                comparison_data,
                x='month',
                y='total_responses',
                title="Total Responses by Month",
                color='total_responses',
                color_continuous_scale='Blues'
            )
            fig_responses.update_layout(height=400)
            st.plotly_chart(fig_responses, use_container_width=True)

# TAB 3: Critical Events
with tab3:
    st.header("Critical Events Analysis")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        severity_filter = st.multiselect(
            "Filter by Severity:",
            options=['High', 'Medium', 'Low'],
            default=['High', 'Medium', 'Low'],
            key="severity_filter"
        )

    with col2:
        promotion_filter = st.multiselect(
            "Filter by Promotion Type:",
            options=['Seasonal', 'Sale', 'Product Launch', 'None'],
            default=['Seasonal', 'Sale', 'Product Launch', 'None'],
            key="promotion_filter"
        )

    # Filter events
    filtered_events = events_df[
        (events_df['severity'].isin(severity_filter)) &
        (events_df['promotion_type'].isin(promotion_filter))
    ]

    # Display events table
    if not filtered_events.empty:
        # Sort options
        sort_by = st.selectbox(
            "Sort by:",
            options=['date', 'severity', 'satisfaction_impact'],
            key="events_sort"
        )

        sort_order = st.radio("Sort order:", ['Ascending', 'Descending'], horizontal=True, key="events_order")

        sorted_events = filtered_events.sort_values(
            sort_by, 
            ascending=(sort_order == 'Ascending')
        )

        # Display table
        st.subheader("Events Timeline")

        # Create interactive table
        for _, event in sorted_events.iterrows():
            with st.expander(f"{event['date'].strftime('%Y-%m-%d')} - {event['event']} ({event['severity']} Severity)"):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(f"**Impact:** {event['impact']}")
                    st.write(f"**Satisfaction Impact:** {event['satisfaction_impact']}")

                with col2:
                    st.write(f"**Promotion Type:** {event['promotion_type']}")
                    st.write(f"**Severity:** {event['severity']}")

                with col3:
                    if st.button(f"Highlight in Timeline", key=f"highlight_{event['date']}"):
                        # This would highlight the date in the timeline
                        st.success(f"Date {event['date'].strftime('%Y-%m-%d')} highlighted!")

                st.write(f"**Description:** {event['description']}")

        # Events impact visualization
        st.subheader("Events Impact Analysis")

        # Convert satisfaction_impact to numeric for plotting
        sorted_events['impact_numeric'] = sorted_events['satisfaction_impact'].str.replace('+', '').astype(float)

        fig_events = px.scatter(
            sorted_events,
            x='date',
            y='impact_numeric',
            color='severity',
            size=abs(sorted_events['impact_numeric']),
            hover_data=['event', 'promotion_type'],
            title="Event Impact on Customer Satisfaction",
            color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'}
        )
        fig_events.add_hline(y=0, line_dash="dash", line_color="black")
        fig_events.update_layout(height=400)
        st.plotly_chart(fig_events, use_container_width=True)

# TAB 4: Risk Analysis
with tab4:
    st.header("Risk Analysis Dashboard")

    # Risk Matrix
    st.subheader("Risk Matrix")

    fig_risk_matrix = px.scatter(
        risk_df,
        x='probability',
        y='impact',
        size='performance_gap',
        color='risk_score',
        hover_data=['category', 'current_score', 'target_score'],
        title="Risk Assessment Matrix",
        labels={'probability': 'Probability', 'impact': 'Impact'},
        color_continuous_scale='Reds'
    )

    # Add quadrant lines
    fig_risk_matrix.add_vline(x=0.5, line_dash="dash", line_color="gray", opacity=0.5)
    fig_risk_matrix.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.5)

    # Add quadrant labels
    fig_risk_matrix.add_annotation(x=0.25, y=0.75, text="High Impact<br>Low Probability", showarrow=False)
    fig_risk_matrix.add_annotation(x=0.75, y=0.75, text="High Impact<br>High Probability", showarrow=False)
    fig_risk_matrix.add_annotation(x=0.25, y=0.25, text="Low Impact<br>Low Probability", showarrow=False)
    fig_risk_matrix.add_annotation(x=0.75, y=0.25, text="Low Impact<br>High Probability", showarrow=False)

    fig_risk_matrix.update_layout(height=500)
    st.plotly_chart(fig_risk_matrix, use_container_width=True)

    # Risk categories analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Performance Gap Analysis")
        fig_gap = px.bar(
            risk_df.sort_values('performance_gap', ascending=True),
            y='category',
            x='performance_gap',
            orientation='h',
            title="Performance Gap by Category",
            color='performance_gap',
            color_continuous_scale='RdYlBu_r'
        )
        fig_gap.update_layout(height=400)
        st.plotly_chart(fig_gap, use_container_width=True)

    with col2:
        st.subheader("Current vs Target Scores")
        categories = risk_df['category'].tolist()
        current_scores = risk_df['current_score'].tolist()
        target_scores = risk_df['target_score'].tolist()

        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(name='Current Score', x=categories, y=current_scores, marker_color='lightblue'))
        fig_comparison.add_trace(go.Bar(name='Target Score', x=categories, y=target_scores, marker_color='darkblue'))

        fig_comparison.update_layout(
            title="Current vs Target Performance",
            barmode='group',
            height=400,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

    # Risk severity levels
    st.subheader("Risk Severity Assessment")

    # Classify risks
    risk_df['severity_level'] = pd.cut(
        risk_df['risk_score'], 
        bins=[0, 0.3, 0.6, 1.0], 
        labels=['Low', 'Medium', 'High']
    )

    severity_counts = risk_df['severity_level'].value_counts()

    cols = st.columns(len(severity_counts))
    colors = {'Low': 'success', 'Medium': 'warning', 'High': 'error'}

    for i, (level, count) in enumerate(severity_counts.items()):
        with cols[i]:
            st.metric(
                label=f"{level} Risk Categories",
                value=count,
                delta=f"{count/len(risk_df)*100:.0f}% of total"
            )

    # Detailed metric cards
    st.subheader("Detailed Risk Metrics")

    for _, risk in risk_df.iterrows():
        severity = risk['severity_level']
        color_class = f"risk-{severity.lower()}"

        st.markdown(f"""
        <div class="metric-card {color_class}">
            <h4>{risk["category"]}</h4>
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <p><strong>Current Score:</strong> {risk["current_score"]}/10</p>
                    <p><strong>Target Score:</strong> {risk["target_score"]}/10</p>
                </div>
                <div>
                    <p><strong>Risk Score:</strong> {risk["risk_score"]:.2f}</p>
                    <p><strong>Severity:</strong> {severity}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Export functionality
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Export Data")

if st.sidebar.button("Download Daily Data (CSV)"):
    csv_buffer = io.StringIO()
    daily_df.to_csv(csv_buffer, index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv_buffer.getvalue(),
        file_name=f"daily_satisfaction_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

if st.sidebar.button("Download Risk Analysis (CSV)"):
    csv_buffer = io.StringIO()
    risk_df.to_csv(csv_buffer, index=False)
    st.sidebar.download_button(
        label="Download Risk CSV",
        data=csv_buffer.getvalue(),
        file_name=f"risk_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("*Dashboard generated on October 2025 | City Furniture Customer Satisfaction Analysis*")
