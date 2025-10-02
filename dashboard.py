import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io

# Configure page with modern settings
st.set_page_config(
    page_title="City Furniture - Analytics Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS styling inspired by professional dashboards
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styling */
    .main {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    .main-header h1 {
        color: white;
        font-size: 2.2rem;
        font-weight: 600;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1rem;
    }

    .nav-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2d3748;
        margin: 1rem 0 0.5rem 0;
        padding: 0.5rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }

    .nav-section {
        margin: 1rem 0;
        padding: 0.5rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* Tab Styling */
    .stTabs > div > div > div > div {
        background: white;
        border-radius: 12px;
        padding: 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    .stTabs > div > div > div > div > div {
        border: none;
        border-radius: 12px 12px 0 0;
        background: linear-gradient(90deg, #f7fafc 0%, #edf2f7 100%);
        padding: 0;
    }

    .stTabs > div > div > div > div > div > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        border: none;
        border-radius: 8px;
        margin: 0.5rem;
        padding: 0.7rem 1.5rem;
        background: white;
        color: #4a5568;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .stTabs > div > div > div > div > div > button[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }

    .metric-card h3 {
        color: #2d3748;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-card h1 {
        color: #1a202c;
        font-weight: 700;
        margin: 0;
        font-size: 2.2rem;
    }

    .metric-card p {
        color: #718096;
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }

    /* Status Cards */
    .status-excellent {
        border-left-color: #10b981 !important;
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%) !important;
    }

    .status-good {
        border-left-color: #f59e0b !important;
        background: linear-gradient(135deg, #fffbeb 0%, #fefce8 100%) !important;
    }

    .status-needs-improvement {
        border-left-color: #ef4444 !important;
        background: linear-gradient(135deg, #fef2f2 0%, #fefefe 100%) !important;
    }

    .status-critical {
        border-left-color: #dc2626 !important;
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
    }

    /* Section Headers */
    .section-header {
        color: #1a202c;
        font-weight: 600;
        font-size: 1.5rem;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }

    .subsection-header {
        color: #2d3748;
        font-weight: 500;
        font-size: 1.2rem;
        margin: 1.5rem 0 1rem 0;
    }

    /* Filter and Chart Containers */
    .filter-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    .plot-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    /* Alert Messages */
    .alert-warning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .alert-error {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }

    /* Priority Cards */
    .priority-critical {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #dc2626;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.2);
    }

    .priority-high {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
    }

    .priority-medium {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
    }

    .priority-low {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8rem; }
        .metric-card { margin: 0.25rem 0; padding: 1rem; }
        .metric-card h1 { font-size: 1.8rem; }
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

    # Enhanced events data with more comprehensive information
    enhanced_events_data = [
        # Critical Events
        {'date': datetime(2025, 8, 11), 'day_of_week': 'Tuesday', 'failed_metrics': '7/8', 'failure_percentage': 87.5, 'promotion': 'Without promo', 'severity': 'Critical'},
        {'date': datetime(2025, 8, 13), 'day_of_week': 'Saturday', 'failed_metrics': '6/8', 'failure_percentage': 75.0, 'promotion': 'No promotion', 'severity': 'High'},
        {'date': datetime(2025, 6, 29), 'day_of_week': 'Monday', 'failed_metrics': '6/8', 'failure_percentage': 75.0, 'promotion': '4th of July Event 7% OFF', 'severity': 'High'},
        {'date': datetime(2025, 8, 7), 'day_of_week': 'Sunday', 'failed_metrics': '4/8', 'failure_percentage': 50.0, 'promotion': 'No promotion', 'severity': 'Medium'},
        {'date': datetime(2025, 8, 25), 'day_of_week': 'Thursday', 'failed_metrics': '4/8', 'failure_percentage': 50.0, 'promotion': 'Without promo', 'severity': 'Medium'},
        {'date': datetime(2025, 9, 22), 'day_of_week': 'Tuesday', 'failed_metrics': '4/8', 'failure_percentage': 50.0, 'promotion': 'Without promo', 'severity': 'Medium'},

        # Additional Events (Non-Critical)
        {'date': datetime(2025, 7, 14), 'day_of_week': 'Tuesday', 'failed_metrics': '3/8', 'failure_percentage': 37.5, 'promotion': 'Anniversary Sale Kick Off', 'severity': 'Low'},
        {'date': datetime(2025, 7, 8), 'day_of_week': 'Wednesday', 'failed_metrics': '3/8', 'failure_percentage': 37.5, 'promotion': 'No promotion', 'severity': 'Low'},
        {'date': datetime(2025, 8, 2), 'day_of_week': 'Sunday', 'failed_metrics': '3/8', 'failure_percentage': 37.5, 'promotion': 'No promotion', 'severity': 'Low'},
        {'date': datetime(2025, 8, 13), 'day_of_week': 'Thursday', 'failed_metrics': '3/8', 'failure_percentage': 37.5, 'promotion': 'No promotion', 'severity': 'Low'},
        {'date': datetime(2025, 8, 18), 'day_of_week': 'Monday', 'failed_metrics': '3/8', 'failure_percentage': 37.5, 'promotion': 'No promotion', 'severity': 'Low'},

        # Good Performance Events (for context)
        {'date': datetime(2025, 6, 15), 'day_of_week': 'Monday', 'failed_metrics': '2/8', 'failure_percentage': 25.0, 'promotion': 'Father Day Special 15% OFF', 'severity': 'Low'},
        {'date': datetime(2025, 9, 1), 'day_of_week': 'Tuesday', 'failed_metrics': '2/8', 'failure_percentage': 25.0, 'promotion': 'Labor Day Sale', 'severity': 'Low'},
        {'date': datetime(2025, 7, 20), 'day_of_week': 'Monday', 'failed_metrics': '1/8', 'failure_percentage': 12.5, 'promotion': 'Summer Clearance 20% OFF', 'severity': 'Low'},
        {'date': datetime(2025, 8, 24), 'day_of_week': 'Sunday', 'failed_metrics': '1/8', 'failure_percentage': 12.5, 'promotion': 'Back to School Furniture', 'severity': 'Low'},
        {'date': datetime(2025, 9, 15), 'day_of_week': 'Friday', 'failed_metrics': '0/8', 'failure_percentage': 0.0, 'promotion': 'Fall Collection Launch', 'severity': 'Low'},
    ]

    events_df = pd.DataFrame(enhanced_events_data)

    return daily_df, events_df

# Load data
daily_df, events_df = load_data()

# Modern Sidebar Navigation
with st.sidebar:
    # Company Logo/Header
    st.markdown('<div class="nav-header">🏢 City Furniture<br>Analytics Hub</div>', unsafe_allow_html=True)

    # Navigation Sections
    st.markdown('<div class="nav-section">', unsafe_allow_html=True)
    st.markdown("**📊 Dashboard Overview**")
    if st.button("📈 Performance Summary", key="nav_overview"):
        st.session_state.current_section = "overview"
    if st.button("🎯 Key Metrics", key="nav_metrics"):
        st.session_state.current_section = "metrics"
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-section">', unsafe_allow_html=True)
    st.markdown("**📈 Analytics Sections**")
    if st.button("📅 Daily Timeline", key="nav_daily"):
        st.session_state.current_tab = 0
    if st.button("📊 Monthly Comparison", key="nav_monthly"):
        st.session_state.current_tab = 1
    if st.button("⚠️ Critical Events", key="nav_events"):
        st.session_state.current_tab = 2
    if st.button("🎯 Risk Analysis", key="nav_risk"):
        st.session_state.current_tab = 3
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-section">', unsafe_allow_html=True)
    st.markdown("**🔧 Quick Actions**")
    if st.button("📥 Export Data", key="nav_export"):
        st.session_state.show_export = True
    if st.button("🔄 Refresh Dashboard", key="nav_refresh"):
        st.rerun()
    if st.button("❓ Help & Support", key="nav_help"):
        st.session_state.show_help = True
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick Stats
    st.markdown('<div class="nav-section">', unsafe_allow_html=True)
    st.markdown("**📋 Quick Stats**")
    avg_score = daily_df['satisfaction_score'].mean()
    below_target = (daily_df['satisfaction_score'] < 9.0).sum()
    total_days = len(daily_df)

    st.markdown(f"""
    <div style="background: white; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;">
        <div style="color: #667eea; font-weight: 600;">Average Score</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #1a202c;">{avg_score:.1f}/10</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: white; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;">
        <div style="color: #667eea; font-weight: 600;">Performance Rate</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #1a202c;">{((total_days-below_target)/total_days*100):.1f}%</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🏢 City Furniture - Customer Satisfaction Analytics</h1>
    <p>May 30, 2025 - September 30, 2025 | 124 days analyzed | Real-time Business Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 0

# Create modern tabs with enhanced styling
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Daily Timeline", 
    "📊 Monthly Comparison", 
    "⚠️ Critical Events", 
    "🎯 Risk Analysis"
])

# TAB 1: Daily Timeline with Modern Design
with tab1:
    st.markdown('<h2 class="section-header">📈 Daily Performance Timeline</h2>', unsafe_allow_html=True)

    # Modern Filter Container
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        month_filter = st.selectbox(
            "🗓️ Filter by Month:",
            options=["All Months"] + sorted(daily_df['month'].unique()),
            key="daily_month_filter",
            help="Select a specific month to analyze"
        )

    with col2:
        show_weekends = st.checkbox("🔸 Highlight Weekends", value=True, help="Show weekend performance indicators")

    with col3:
        show_target = st.checkbox("🎯 Show Target Line (9.0)", value=True, help="Display performance target reference")

    st.markdown('</div>', unsafe_allow_html=True)

    # Filter data based on selection
    filtered_daily = daily_df.copy()
    if month_filter != "All Months":
        filtered_daily = daily_df[daily_df['month'] == month_filter]

    # Create modern timeline chart
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    fig_timeline = go.Figure()

    # Main satisfaction line with gradient colors
    fig_timeline.add_trace(go.Scatter(
        x=filtered_daily['date'],
        y=filtered_daily['satisfaction_score'],
        mode='lines+markers',
        name='Daily Satisfaction',
        line=dict(color='#667eea', width=3),
        marker=dict(
            size=7,
            color=['#ef4444' if score < 9.0 else '#10b981' for score in filtered_daily['satisfaction_score']],
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>%{x|%B %d, %Y}</b><br>' +
                      'Satisfaction: %{y}/10<br>' +
                      '<extra></extra>'
    ))

    # Add target line with modern styling
    if show_target:
        fig_timeline.add_hline(
            y=9.0,
            line_dash="dash",
            line_color="#10b981",
            line_width=2,
            annotation_text="🎯 Target (9.0)",
            annotation_position="bottom right"
        )

    # Highlight weekends with modern markers
    if show_weekends:
        weekend_data = filtered_daily[filtered_daily['is_weekend']]
        if not weekend_data.empty:
            fig_timeline.add_trace(go.Scatter(
                x=weekend_data['date'],
                y=weekend_data['satisfaction_score'],
                mode='markers',
                name='🔸 Weekends',
                marker=dict(size=10, color='#f59e0b', symbol='diamond', 
                           line=dict(width=2, color='white')),
                hovertemplate='<b>%{x|%B %d, %Y} (Weekend)</b><br>' +
                              'Satisfaction: %{y}/10<br>' +
                              '<extra></extra>'
            ))

    # Modern chart layout
    fig_timeline.update_layout(
        title="📊 Daily Customer Satisfaction Evolution",
        xaxis_title="📅 Date",
        yaxis_title="⭐ Satisfaction Score",
        font=dict(family="Inter"),
        hovermode='closest',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#e2e8f0",
            borderwidth=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#f1f5f9', gridwidth=1),
        yaxis=dict(gridcolor='#f1f5f9', gridwidth=1)
    )

    st.plotly_chart(fig_timeline, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Modern Summary Statistics Cards
    st.markdown('<h3 class="subsection-header">📊 Performance Summary</h3>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_score = filtered_daily['satisfaction_score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Average Score</h3>
            <h1>{avg_score:.1f}</h1>
            <p>Overall performance rating</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        below_target = (filtered_daily['satisfaction_score'] < 9.0).sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚠️ Days Below Target</h3>
            <h1>{below_target}</h1>
            <p>Out of {len(filtered_daily)} total days</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        best_day = filtered_daily.loc[filtered_daily['satisfaction_score'].idxmax()]
        st.markdown(f"""
        <div class="metric-card status-excellent">
            <h3>🏆 Best Score</h3>
            <h1>{best_day['satisfaction_score']:.1f}</h1>
            <p>{best_day['date'].strftime('%B %d, %Y')}</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        worst_day = filtered_daily.loc[filtered_daily['satisfaction_score'].idxmin()]
        st.markdown(f"""
        <div class="metric-card status-needs-improvement">
            <h3>📉 Lowest Score</h3>
            <h1>{worst_day['satisfaction_score']:.1f}</h1>
            <p>{worst_day['date'].strftime('%B %d, %Y')}</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: Monthly Comparison with Modern Design  
with tab2:
    st.markdown('<h2 class="section-header">📊 Monthly Performance Analysis</h2>', unsafe_allow_html=True)

    # Enhanced metric selector with modern design
    metric_options = {
        'Overall Satisfaction': {'target': 9.0, 'format': '{:.2f}', 'icon': '⭐'},
        'Likelihood to Buy Again': {'target': 9.0, 'format': '{:.2f}', 'icon': '🛒'},
        'Likelihood to Recommend': {'target': 9.0, 'format': '{:.2f}', 'icon': '👍'},
        'Site Design': {'target': 9.0, 'format': '{:.2f}', 'icon': '🎨'},
        'Ease of Finding': {'target': 9.0, 'format': '{:.2f}', 'icon': '🔍'},
        'Product Information Clarity': {'target': 9.0, 'format': '{:.2f}', 'icon': '📋'},
        'Charges Stated Clearly': {'target': 9.0, 'format': '{:.2f}', 'icon': '💰'},
        'Checkout Process': {'target': 9.0, 'format': '{:.2f}', 'icon': '✅'}
    }

    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        selected_metric = st.selectbox(
            "📊 Select Metric for Analysis:",
            options=list(metric_options.keys()),
            index=6,  # Default to "Charges Stated Clearly"
            key="metric_selector",
            help="Choose which customer satisfaction metric to analyze"
        )

    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 8px; text-align: center; margin-top: 1.7rem;">
            <div style="font-size: 2rem;">{metric_options[selected_metric]['icon']}</div>
            <div style="font-weight: 600; font-size: 0.9rem;">ANALYZING</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    target_score = metric_options[selected_metric]['target']
    score_format = metric_options[selected_metric]['format']

    # Generate realistic data for the selected metric
    @st.cache_data
    def generate_metric_data(metric_name):
        # Base scores for different months
        month_data = {
            'May-June 2025': {'period': '2025-05-30 to 2025-06-30', 'total_days': 32, 'base_score': 9.48},
            'July 2025': {'period': '2025-07-01 to 2025-07-31', 'total_days': 31, 'base_score': 9.22},
            'August 2025': {'period': '2025-08-01 to 2025-08-31', 'total_days': 31, 'base_score': 9.16},
            'September 2025': {'period': '2025-09-01 to 2025-09-30', 'total_days': 30, 'base_score': 9.43}
        }

        # Add variations for different metrics
        metric_variations = {
            'Overall Satisfaction': [0, -0.1, -0.2, 0.05],
            'Likelihood to Buy Again': [0.1, -0.05, -0.15, 0.08],
            'Likelihood to Recommend': [-0.05, 0.03, -0.1, 0.12],
            'Site Design': [0.2, 0.15, 0.1, 0.25],
            'Ease of Finding': [0.15, 0.08, 0.05, 0.18],
            'Product Information Clarity': [0.12, 0.06, 0.02, 0.15],
            'Charges Stated Clearly': [0, 0, 0, 0],
            'Checkout Process': [-0.2, -0.15, -0.25, -0.12]
        }

        variations = metric_variations.get(metric_name, [0, 0, 0, 0])

        enhanced_data = []
        for i, (month, data) in enumerate(month_data.items()):
            score = data['base_score'] + variations[i]
            days_below = max(0, int((target_score - score) * data['total_days'] / 2))

            enhanced_data.append({
                'month': month,
                'period': data['period'],
                'total_days': data['total_days'],
                'average_score': score,
                'days_below_target': days_below,
                'days_below_percentage': (days_below / data['total_days']) * 100,
                'performance_vs_target': score - target_score,
                'classification': 'Excellent' if score >= target_score else 'Good' if score >= target_score - 0.5 else 'Needs Improvement'
            })

        return pd.DataFrame(enhanced_data)

    metric_data = generate_metric_data(selected_metric)

    # Month selector with modern design
    comparison_months = st.multiselect(
        "📅 Select months to compare:",
        options=metric_data['month'].tolist(),
        default=metric_data['month'].tolist(),
        key="monthly_comparison_enhanced",
        help="Choose which months to include in the comparison"
    )

    if comparison_months:
        comparison_data = metric_data[metric_data['month'].isin(comparison_months)]

        # Enhanced Monthly Performance Cards
        st.markdown(f'<h3 class="subsection-header">{metric_options[selected_metric]["icon"]} Monthly Performance - {selected_metric}</h3>', unsafe_allow_html=True)

        cols = st.columns(len(comparison_data))
        for i, (_, month_data_row) in enumerate(comparison_data.iterrows()):
            with cols[i]:
                score = month_data_row['average_score']
                classification = month_data_row['classification']

                # Enhanced status colors and styling
                if classification == 'Excellent':
                    status_class = "status-excellent"
                    status_color = "#10b981"
                    status_icon = "🟢"
                elif classification == 'Good':
                    status_class = "status-good"
                    status_color = "#f59e0b"
                    status_icon = "🟡"
                else:
                    status_class = "status-needs-improvement"
                    status_color = "#ef4444"
                    status_icon = "🔴"

                st.markdown(f"""
                <div class="metric-card {status_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <h3 style="margin: 0;">{month_data_row["month"].split()[0]}</h3>
                        <span style="font-size: 1.2rem;">{status_icon}</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #666; margin-bottom: 0.8rem;">
                        {month_data_row["period"]}<br>
                        📊 {month_data_row["total_days"]} days analyzed
                    </div>
                    <div style="text-align: center; margin: 1rem 0;">
                        <div style="font-size: 2.5rem; font-weight: 700; color: {status_color};">
                            {score_format.format(score)}
                        </div>
                        <div style="font-size: 0.9rem; color: #666;">Average Score</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                        <span>🎯 Target: {target_score}</span>
                        <span>📈 Gap: {score - target_score:+.2f}</span>
                    </div>
                    <div style="margin-top: 0.8rem; padding-top: 0.8rem; border-top: 1px solid #e2e8f0;">
                        <div style="font-size: 0.8rem;">
                            <strong>Days below target:</strong><br>
                            {month_data_row["days_below_target"]} ({month_data_row["days_below_percentage"]:.1f}%)
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Enhanced visualizations with modern styling
        st.markdown('<h3 class="subsection-header">📈 Performance Visualizations</h3>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="plot-container">', unsafe_allow_html=True)

            # Modern bar chart with enhanced styling
            fig_bar_enhanced = px.bar(
                comparison_data,
                x='month',
                y='average_score',
                color='classification',
                color_discrete_map={
                    'Excellent': '#10b981',
                    'Good': '#f59e0b', 
                    'Needs Improvement': '#ef4444'
                },
                text='average_score'
            )

            # Add target line
            fig_bar_enhanced.add_hline(
                y=target_score, 
                line_dash="dash", 
                line_color="#10b981", 
                line_width=2,
                annotation_text=f"🎯 Target ({target_score})",
                annotation_position="top right"
            )

            fig_bar_enhanced.update_traces(
                texttemplate='%{text:.2f}', 
                textposition='outside'
            )

            fig_bar_enhanced.update_layout(
                title=f"📊 {selected_metric} - Monthly Performance",
                font=dict(family="Inter"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=450,
                showlegend=True,
                xaxis=dict(title="📅 Period", gridcolor='#f1f5f9'),
                yaxis=dict(title="⭐ Average Score", gridcolor='#f1f5f9')
            )

            st.plotly_chart(fig_bar_enhanced, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="plot-container">', unsafe_allow_html=True)

            # Performance vs Target analysis
            fig_performance = px.bar(
                comparison_data,
                x='month',
                y='performance_vs_target',
                color='performance_vs_target',
                color_continuous_scale='RdYlGn',
                text='performance_vs_target'
            )

            fig_performance.add_hline(y=0, line_dash="solid", line_color="#64748b", line_width=1)

            fig_performance.update_traces(
                texttemplate='%{text:+.2f}', 
                textposition='outside'
            )

            fig_performance.update_layout(
                title=f"🎯 Performance Gap Analysis - {selected_metric}",
                font=dict(family="Inter"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=450,
                xaxis=dict(title="📅 Period", gridcolor='#f1f5f9'),
                yaxis=dict(title="📈 Difference from Target", gridcolor='#f1f5f9')
            )

            st.plotly_chart(fig_performance, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Enhanced Performance Summary
        st.markdown('<h3 class="subsection-header">📋 Performance Summary</h3>', unsafe_allow_html=True)

        summary_cols = st.columns(4)

        with summary_cols[0]:
            overall_avg = comparison_data['average_score'].mean()
            delta = overall_avg - target_score
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Overall Average</h3>
                <h1>{score_format.format(overall_avg)}</h1>
                <p style="color: {'#10b981' if delta >= 0 else '#ef4444'};">
                    {delta:+.2f} vs target
                </p>
            </div>
            """, unsafe_allow_html=True)

        with summary_cols[1]:
            excellent_months = (comparison_data['classification'] == 'Excellent').sum()
            st.markdown(f"""
            <div class="metric-card status-excellent">
                <h3>🌟 Excellent Months</h3>
                <h1>{excellent_months}</h1>
                <p>of {len(comparison_data)} analyzed</p>
            </div>
            """, unsafe_allow_html=True)

        with summary_cols[2]:
            total_days_below = comparison_data['days_below_target'].sum()
            total_days = comparison_data['total_days'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚠️ Days Below Target</h3>
                <h1>{total_days_below}</h1>
                <p>of {total_days} total days</p>
            </div>
            """, unsafe_allow_html=True)

        with summary_cols[3]:
            avg_days_below_pct = comparison_data['days_below_percentage'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>📉 Avg % Below Target</h3>
                <h1>{avg_days_below_pct:.1f}%</h1>
                <p>Average across periods</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="alert-warning">
            <h4>⚠️ No months selected</h4>
            <p>Please select at least one month to display the comparison analysis.</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: Critical Events with Modern Design
with tab3:
    st.markdown('<h2 class="section-header">⚠️ Critical Events Analysis</h2>', unsafe_allow_html=True)

    # Modern filters container
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        failure_threshold = st.slider(
            "📊 Filter by Failure %:",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
            key="failure_filter",
            help="Set minimum failure percentage to display"
        )

    with col2:
        promotion_filter = st.selectbox(
            "🎫 Filter by Promotion:",
            options=['All promotions', 'Without promo', 'No promotion', '4th of July Event 7% OFF', 'Anniversary Sale Kick Off', 'Father Day Special 15% OFF', 'Labor Day Sale', 'Summer Clearance 20% OFF', 'Back to School Furniture', 'Fall Collection Launch'],
            key="promotion_filter_enhanced",
            help="Filter events by promotion type"
        )

    with col3:
        severity_filter = st.multiselect(
            "🚨 Filter by Severity:",
            options=['Critical', 'High', 'Medium', 'Low'],
            default=['Critical', 'High', 'Medium', 'Low'],
            key="severity_filter_enhanced",
            help="Select which severity levels to display"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_events = events_df.copy()
    filtered_events = filtered_events[filtered_events['failure_percentage'] >= failure_threshold]

    if promotion_filter != 'All promotions':
        filtered_events = filtered_events[filtered_events['promotion'] == promotion_filter]

    filtered_events = filtered_events[filtered_events['severity'].isin(severity_filter)]

    # Sort options with modern design
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    sort_col1, sort_col2 = st.columns(2)

    with sort_col1:
        sort_by = st.selectbox(
            "📋 Sort by:",
            options=['date', 'failure_percentage', 'severity'],
            key="events_sort_enhanced"
        )

    with sort_col2:
        sort_order = st.radio(
            "🔄 Sort order:", 
            ['Ascending', 'Descending'], 
            horizontal=True, 
            key="events_order_enhanced"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Sort the data
    if sort_by == 'date':
        sorted_events = filtered_events.sort_values('date', ascending=(sort_order == 'Ascending'))
    elif sort_by == 'failure_percentage':
        sorted_events = filtered_events.sort_values('failure_percentage', ascending=(sort_order == 'Ascending'))
    else:  # severity
        severity_order = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
        sorted_events = filtered_events.copy()
        sorted_events['severity_num'] = sorted_events['severity'].map(severity_order)
        sorted_events = sorted_events.sort_values('severity_num', ascending=(sort_order == 'Ascending'))
        sorted_events = sorted_events.drop('severity_num', axis=1)

    # Results summary with modern cards
    st.markdown(f'<h3 class="subsection-header">📊 Events Analysis Results ({len(sorted_events)} events found)</h3>', unsafe_allow_html=True)

    if not sorted_events.empty:
        # Summary metrics with modern styling
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_failure = sorted_events['failure_percentage'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Avg Failure %</h3>
                <h1>{avg_failure:.1f}%</h1>
                <p>Across all events</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            critical_count = (sorted_events['severity'] == 'Critical').sum()
            st.markdown(f"""
            <div class="metric-card status-critical">
                <h3>🚨 Critical Events</h3>
                <h1>{critical_count}</h1>
                <p>Require immediate attention</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            high_failure = (sorted_events['failure_percentage'] >= 70).sum()
            st.markdown(f"""
            <div class="metric-card status-needs-improvement">
                <h3>⚠️ High Risk Days</h3>
                <h1>{high_failure}</h1>
                <p>Above 70% failure rate</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            promo_events = (sorted_events['promotion'].str.contains('OFF|Sale|Special', case=False, na=False)).sum()
            st.markdown(f"""
            <div class="metric-card status-good">
                <h3>🎫 Promotion Days</h3>
                <h1>{promo_events}</h1>
                <p>Events during promotions</p>
            </div>
            """, unsafe_allow_html=True)

        # Enhanced Events Table
        st.markdown('<h3 class="subsection-header">📋 Detailed Events Timeline</h3>', unsafe_allow_html=True)

        def get_severity_info(severity):
            severity_map = {
                'Critical': {'icon': '🚨', 'color': '#dc2626', 'class': 'priority-critical'},
                'High': {'icon': '⚠️', 'color': '#f59e0b', 'class': 'priority-high'},
                'Medium': {'icon': '🟡', 'color': '#3b82f6', 'class': 'priority-medium'},
                'Low': {'icon': '🟢', 'color': '#10b981', 'class': 'priority-low'}
            }
            return severity_map.get(severity, {'icon': '⚪', 'color': '#64748b', 'class': 'priority-low'})

        # Display events in modern cards
        for idx, (_, event) in enumerate(sorted_events.iterrows()):
            severity_info = get_severity_info(event['severity'])

            st.markdown(f"""
            <div class="{severity_info['class']}">
                <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <h4 style="margin: 0; color: #1a202c;">
                            {severity_info['icon']} {event['date'].strftime('%B %d, %Y')} - {event['day_of_week']}
                        </h4>
                        <p style="margin: 0.2rem 0; color: #64748b; font-size: 0.9rem;">
                            {event['failure_percentage']:.1f}% Failure Rate • {event['severity']} Risk Level
                        </p>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div>
                        <strong>📅 Date:</strong> {event['date'].strftime('%Y-%m-%d')}<br>
                        <strong>📆 Day:</strong> {event['day_of_week']}
                    </div>
                    <div>
                        <strong>📊 Failed Metrics:</strong> {event['failed_metrics']}<br>
                        <strong>📈 Failure Rate:</strong> {event['failure_percentage']:.1f}%
                    </div>
                    <div>
                        <strong>🎫 Promotion:</strong> {event['promotion']}<br>
                        <strong>🚨 Severity:</strong> {event['severity']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="alert-warning">
            <h4>⚠️ No events found</h4>
            <p>No events match the current filter criteria. Try adjusting your filters to see more results.</p>
            <p><strong>💡 Tip:</strong> Lower the failure percentage threshold or select 'All promotions' to see more results.</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 4: Advanced Risk Analysis with Modern Design
with tab4:
    st.markdown('<h2 class="section-header">🎯 Advanced Risk Analysis</h2>', unsafe_allow_html=True)

    # Enhanced risk metrics with modern design
    risk_metric_options = {
        'Overall Satisfaction': {
            'target': 9.0, 'current_scores': [9.48, 9.38, 9.36, 9.48], 'icon': '⭐',
            'risk_factors': ['Service delays', 'Product quality issues', 'Delivery problems'],
            'business_impact': 'Directly affects customer loyalty and retention rates',
            'recommendations': ['Implement proactive monitoring', 'Establish quality checkpoints', 'Create feedback loops']
        },
        'Likelihood to Buy Again': {
            'target': 9.0, 'current_scores': [9.58, 9.33, 9.21, 9.56], 'icon': '🛒',
            'risk_factors': ['Competitive pricing', 'Product availability', 'Customer service experience'],
            'business_impact': 'Critical for revenue retention and customer lifetime value',
            'recommendations': ['Develop loyalty programs', 'Monitor competitor pricing', 'Improve inventory management']
        },
        'Likelihood to Recommend': {
            'target': 9.0, 'current_scores': [9.43, 9.25, 9.06, 9.60], 'icon': '👍',
            'risk_factors': ['Word-of-mouth reputation', 'Social media presence', 'Customer advocacy'],
            'business_impact': 'Affects organic growth and brand reputation',
            'recommendations': ['Create referral programs', 'Monitor online reviews', 'Develop ambassador programs']
        },
        'Site Design': {
            'target': 9.0, 'current_scores': [9.68, 9.37, 9.26, 9.73], 'icon': '🎨',
            'risk_factors': ['User interface complexity', 'Mobile responsiveness', 'Loading speed'],
            'business_impact': 'Influences first impressions and user engagement rates',
            'recommendations': ['Conduct UX/UI testing', 'Implement mobile-first design', 'Optimize site performance']
        },
        'Ease of Finding': {
            'target': 9.0, 'current_scores': [9.63, 9.30, 9.21, 9.66], 'icon': '🔍',
            'risk_factors': ['Search functionality', 'Product categorization', 'Navigation structure'],
            'business_impact': 'Affects conversion rates and user satisfaction',
            'recommendations': ['Enhance search algorithm', 'Improve categorization', 'Add intelligent recommendations']
        },
        'Product Information Clarity': {
            'target': 9.0, 'current_scores': [9.60, 9.28, 9.18, 9.63], 'icon': '📋',
            'risk_factors': ['Product descriptions', 'Image quality', 'Specification completeness'],
            'business_impact': 'Reduces returns and increases purchase confidence',
            'recommendations': ['Standardize information templates', 'Add 360-degree views', 'Include customer Q&A']
        },
        'Charges Stated Clearly': {
            'target': 9.0, 'current_scores': [9.48, 9.22, 9.16, 9.43], 'icon': '💰',
            'risk_factors': ['Hidden fees', 'Shipping transparency', 'Tax calculation accuracy'],
            'business_impact': 'Critical for trust and transaction completion',
            'recommendations': ['Display all fees upfront', 'Implement pricing calculator', 'Provide charge breakdowns']
        },
        'Checkout Process': {
            'target': 9.0, 'current_scores': [9.28, 9.07, 8.91, 9.31], 'icon': '✅',
            'risk_factors': ['Process complexity', 'Payment security', 'Guest checkout availability'],
            'business_impact': 'Directly affects conversion rates and cart abandonment',
            'recommendations': ['Simplify checkout steps', 'Offer multiple payment options', 'Add guest checkout']
        }
    }

    # Metric selector with enhanced design
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])

    with col1:
        selected_risk_metric = st.selectbox(
            "🎯 Select Metric for Risk Analysis:",
            options=list(risk_metric_options.keys()),
            key="risk_metric_selector",
            help="Choose which metric to analyze for risk assessment"
        )

    with col2:
        metric_info = risk_metric_options[selected_risk_metric]
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 8px; text-align: center; margin-top: 1.7rem;">
            <div style="font-size: 2rem;">{metric_info['icon']}</div>
            <div style="font-weight: 600; font-size: 0.9rem;">RISK ANALYSIS</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    target_score = metric_info['target']
    monthly_scores = metric_info['current_scores']
    months = ['May-June 2025', 'July 2025', 'August 2025', 'September 2025']

    # Calculate risk metrics
    performance_gaps = [target_score - score for score in monthly_scores]
    risk_levels = ['High Risk' if gap > 0.5 else 'Medium Risk' if gap > 0.2 else 'Low Risk' for gap in performance_gaps]
    trend_direction = monthly_scores[-1] - monthly_scores[0]

    # Key Metrics Overview with modern cards
    st.markdown(f'<h3 class="subsection-header">{metric_info["icon"]} Risk Analysis: {selected_risk_metric}</h3>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        current_score = monthly_scores[-1]
        delta_value = current_score - target_score
        status_class = "status-excellent" if delta_value >= 0 else "status-needs-improvement"
        st.markdown(f"""
        <div class="metric-card {status_class}">
            <h3>📊 Current Score</h3>
            <h1>{current_score:.2f}</h1>
            <p style="color: {'#10b981' if delta_value >= 0 else '#ef4444'};">
                {delta_value:+.2f} vs target
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        avg_score = sum(monthly_scores) / len(monthly_scores)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Average Score</h3>
            <h1>{avg_score:.2f}</h1>
            <p>4-month average</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        max_gap = max(performance_gaps)
        risk_status = 'High' if max_gap > 0.5 else 'Medium' if max_gap > 0.2 else 'Low'
        risk_class = f"status-{'critical' if risk_status == 'High' else 'good' if risk_status == 'Medium' else 'excellent'}"
        st.markdown(f"""
        <div class="metric-card {risk_class}">
            <h3>🚨 Risk Level</h3>
            <h1>{risk_status}</h1>
            <p>Current risk assessment</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        trend_emoji = "📈" if trend_direction > 0.1 else "📉" if trend_direction < -0.1 else "➡️"
        trend_text = "Improving" if trend_direction > 0.1 else "Declining" if trend_direction < -0.1 else "Stable"
        trend_class = f"status-{'excellent' if trend_direction > 0.1 else 'needs-improvement' if trend_direction < -0.1 else 'good'}"
        st.markdown(f"""
        <div class="metric-card {trend_class}">
            <h3>📊 Trend</h3>
            <h1 style="font-size: 1.5rem;">{trend_emoji}</h1>
            <p>{trend_text}</p>
        </div>
        """, unsafe_allow_html=True)

    # Performance Charts
    st.markdown('<h3 class="subsection-header">📈 Performance Analysis Charts</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        # Performance trend chart (FIXED - removed duplicate title)
        trend_df = pd.DataFrame({
            'Month': months,
            'Score': monthly_scores,
            'Target': [target_score] * len(months)
        })

        fig_trend = go.Figure()

        fig_trend.add_trace(go.Scatter(
            x=trend_df['Month'],
            y=trend_df['Score'],
            mode='lines+markers',
            name='Actual Score',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#667eea')
        ))

        fig_trend.add_trace(go.Scatter(
            x=trend_df['Month'],
            y=trend_df['Target'],
            mode='lines',
            name='Target',
            line=dict(color='#10b981', width=2, dash='dash')
        ))

        # FIXED: Only one title parameter
        fig_trend.update_layout(
            title=f"📊 {selected_risk_metric} - Performance Trend",
            font=dict(family="Inter"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            xaxis=dict(title="📅 Month", gridcolor='#f1f5f9'),
            yaxis=dict(title="⭐ Score", gridcolor='#f1f5f9')
        )

        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        # Risk gap analysis (FIXED - removed duplicate title)
        gap_df = pd.DataFrame({
            'Month': months,
            'Gap': performance_gaps,
            'Risk_Level': risk_levels
        })

        fig_gaps = px.bar(
            gap_df,
            x='Month',
            y='Gap',
            color='Risk_Level',
            color_discrete_map={
                'High Risk': '#ef4444',
                'Medium Risk': '#f59e0b',
                'Low Risk': '#10b981'
            }
        )

        fig_gaps.add_hline(y=0, line_dash="solid", line_color="#64748b", line_width=1)

        # FIXED: Only one title parameter
        fig_gaps.update_layout(
            title=f"🎯 Performance Gap Analysis - {selected_risk_metric}",
            font=dict(family="Inter"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            xaxis=dict(title="📅 Month", gridcolor='#f1f5f9'),
            yaxis=dict(title="📊 Gap from Target", gridcolor='#f1f5f9')
        )

        st.plotly_chart(fig_gaps, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Business Intelligence Insights
    st.markdown('<h3 class="subsection-header">💡 Business Intelligence Insights</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Business Impact</h3>
            <p style="font-size: 1rem; line-height: 1.6; margin: 1rem 0;">
                {metric_info['business_impact']}
            </p>

            <h4 style="color: #ef4444; margin: 1.5rem 0 0.5rem 0;">⚠️ Key Risk Factors:</h4>
            <ul style="margin: 0; padding-left: 1.2rem;">
        """, unsafe_allow_html=True)

        for factor in metric_info['risk_factors']:
            st.markdown(f"<li style='margin: 0.3rem 0;'>{factor}</li>", unsafe_allow_html=True)

        st.markdown("</ul></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card status-excellent">
            <h3>💡 Strategic Recommendations</h3>
            <ol style="margin: 1rem 0; padding-left: 1.2rem;">
        """, unsafe_allow_html=True)

        for rec in metric_info['recommendations']:
            st.markdown(f"<li style='margin: 0.5rem 0;'>{rec}</li>", unsafe_allow_html=True)

        # Performance prediction
        if trend_direction > 0.1:
            prediction = "📈 **Positive Outlook**: Trends suggest continued improvement"
            prediction_color = "#10b981"
        elif trend_direction < -0.1:
            prediction = "📉 **Warning**: Declining trend requires attention"
            prediction_color = "#ef4444"
        else:
            prediction = "➡️ **Stable**: Performance is stable but monitor changes"
            prediction_color = "#667eea"

        st.markdown(f"""
            </ol>
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #e2e8f0;">
                <h4 style="margin: 0 0 0.5rem 0;">🔮 Performance Outlook</h4>
                <p style="color: {prediction_color}; font-weight: 500; margin: 0;">{prediction}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Export functionality with modern design
st.markdown('<div style="margin-top: 3rem;">', unsafe_allow_html=True)
st.markdown('<h3 class="subsection-header">📥 Data Export Center</h3>', unsafe_allow_html=True)

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if st.button("📊 Download Daily Data", key="export_daily", help="Export daily satisfaction data as CSV"):
        csv_buffer = io.StringIO()
        daily_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="💾 Download CSV",
            data=csv_buffer.getvalue(),
            file_name=f"daily_satisfaction_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with export_col2:
    if st.button("⚠️ Download Events Data", key="export_events", help="Export critical events data as CSV"):
        csv_buffer = io.StringIO()
        events_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="💾 Download CSV",
            data=csv_buffer.getvalue(),
            file_name=f"events_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with export_col3:
    if st.button("🎯 Download Risk Analysis", key="export_risk", help="Export risk analysis summary as CSV"):
        risk_summary_data = []
        for metric, info in risk_metric_options.items():
            current = info['current_scores'][-1]
            gap = info['target'] - current
            trend = info['current_scores'][-1] - info['current_scores'][0]
            risk_level = 'High Risk' if gap > 0.5 else 'Medium Risk' if gap > 0.2 else 'Low Risk'

            risk_summary_data.append({
                'Metric': metric,
                'Current_Score': current,
                'Target_Score': info['target'],
                'Performance_Gap': gap,
                'Trend_Direction': trend,
                'Risk_Level': risk_level,
                'Business_Impact': info['business_impact']
            })

        risk_summary_df = pd.DataFrame(risk_summary_data)
        csv_buffer = io.StringIO()
        risk_summary_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="💾 Download CSV",
            data=csv_buffer.getvalue(),
            file_name=f"risk_analysis_summary_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

st.markdown('</div>', unsafe_allow_html=True)

# Modern Footer
st.markdown("""
<div style="margin-top: 4rem; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
            border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <p style="color: #64748b; margin: 0; font-size: 0.9rem;">
        🏢 <strong>City Furniture Analytics Dashboard</strong> | Last Updated: October 2025<br>
        Powered by Advanced Business Intelligence & Real-time Analytics
    </p>
</div>
""", unsafe_allow_html=True)
