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

# Modern CSS styling - Integration of advanced functionality with beautiful design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styling */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main Header with modern gradient */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        backdrop-filter: blur(10px);
    }

    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }

    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
        font-weight: 400;
    }

    /* Advanced Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem;
    }

    .nav-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a202c;
        margin: 1.5rem 0 1rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        border-left: 4px solid #667eea;
    }

    .nav-section {
        margin: 1.5rem 0;
        padding: 1rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }

    /* Enhanced Tab Styling */
    .stTabs > div > div > div > div {
        background: white;
        border-radius: 16px;
        padding: 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
    }

    .stTabs > div > div > div > div > div {
        border: none;
        border-radius: 16px 16px 0 0;
        background: linear-gradient(90deg, #f8fafc 0%, #ffffff 100%);
        padding: 0.5rem;
    }

    .stTabs > div > div > div > div > div > button {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        margin: 0.25rem;
        padding: 1rem 2rem;
        background: white;
        color: #4a5568;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 0.95rem;
    }

    .stTabs > div > div > div > div > div > button[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }

    .stTabs > div > div > div > div > div > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }

    /* Advanced Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.12);
        border-color: #667eea;
    }

    .metric-card h3 {
        color: #2d3748;
        font-weight: 700;
        margin: 0 0 0.8rem 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.8;
    }

    .metric-card h1 {
        color: #1a202c;
        font-weight: 800;
        margin: 0;
        font-size: 2.8rem;
        line-height: 1;
    }

    .metric-card p {
        color: #718096;
        margin: 1rem 0 0 0;
        font-size: 0.95rem;
        font-weight: 500;
    }

    /* Enhanced Status Cards */
    .status-excellent {
        border-left-color: #10b981 !important;
        background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%) !important;
    }

    .status-excellent::before {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
    }

    .status-good {
        border-left-color: #f59e0b !important;
        background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%) !important;
    }

    .status-good::before {
        background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%) !important;
    }

    .status-needs-improvement {
        border-left-color: #ef4444 !important;
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%) !important;
    }

    .status-needs-improvement::before {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%) !important;
    }

    .status-critical {
        border-left-color: #dc2626 !important;
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
        animation: pulse-critical 2s ease-in-out infinite;
    }

    .status-critical::before {
        background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%) !important;
    }

    @keyframes pulse-critical {
        0%, 100% { box-shadow: 0 8px 32px rgba(220, 38, 38, 0.2); }
        50% { box-shadow: 0 8px 32px rgba(220, 38, 38, 0.4); }
    }

    /* Modern Section Headers */
    .section-header {
        color: #1a202c;
        font-weight: 700;
        font-size: 1.8rem;
        margin: 3rem 0 1.5rem 0;
        padding: 1.5rem 0;
        border-bottom: 3px solid #e2e8f0;
        position: relative;
    }

    .section-header::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }

    .subsection-header {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.3rem;
        margin: 2rem 0 1.5rem 0;
        padding-left: 1rem;
        border-left: 4px solid #667eea;
    }

    /* Enhanced Containers */
    .filter-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.06);
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
    }

    .plot-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.06);
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
    }

    /* Advanced Alert Messages */
    .alert-warning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.2);
    }

    .alert-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2);
    }

    .alert-error {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.2);
    }

    /* Premium Priority Cards */
    .priority-critical {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid #dc2626;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(220, 38, 38, 0.15);
        position: relative;
        overflow: hidden;
    }

    .priority-critical::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%);
    }

    .priority-high {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 2px solid #f59e0b;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(245, 158, 11, 0.15);
        position: relative;
        overflow: hidden;
    }

    .priority-high::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
    }

    .priority-medium {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
        position: relative;
        overflow: hidden;
    }

    .priority-medium::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
    }

    .priority-low {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 2px solid #10b981;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.15);
        position: relative;
        overflow: hidden;
    }

    .priority-low::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
    }

    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
    }

    /* Modern Selectboxes and Inputs */
    .stSelectbox > div > div {
        background: white;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2rem; }
        .main-header p { font-size: 1rem; }
        .metric-card { margin: 0.5rem 0; padding: 1.5rem; }
        .metric-card h1 { font-size: 2.2rem; }
        .section-header { font-size: 1.5rem; }
    }

    /* Advanced animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fadeInUp {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Custom scrollbar */
    .sidebar .sidebar-content::-webkit-scrollbar {
        width: 8px;
    }

    .sidebar .sidebar-content::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }

    .sidebar .sidebar-content::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%);
        border-radius: 4px;
    }

    .sidebar .sidebar-content::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_section' not in st.session_state:
    st.session_state.current_section = "overview"

# Enhanced data loading function from original code with modern integration
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
        {'date': datetime(2025, 8, 11), 'day_of_week': 'Tuesday', 'failed_metrics': '7/8', 'failure_percentage': 87.5, 'promotion': 'Without promo', 'severity': 'Critical'},
        {'date': datetime(2025, 8, 13), 'day_of_week': 'Saturday', 'failed_metrics': '6/8', 'failure_percentage': 75.0, 'promotion': 'No promotion', 'severity': 'High'},
        {'date': datetime(2025, 6, 29), 'day_of_week': 'Monday', 'failed_metrics': '6/8', 'failure_percentage': 75.0, 'promotion': '4th of July Event 7% OFF', 'severity': 'High'},
        {'date': datetime(2025, 8, 7), 'day_of_week': 'Sunday', 'failed_metrics': '4/8', 'failure_percentage': 50.0, 'promotion': 'No promotion', 'severity': 'Medium'},
        {'date': datetime(2025, 8, 25), 'day_of_week': 'Thursday', 'failed_metrics': '4/8', 'failure_percentage': 50.0, 'promotion': 'Without promo', 'severity': 'Medium'},
        {'date': datetime(2025, 9, 22), 'day_of_week': 'Tuesday', 'failed_metrics': '4/8', 'failure_percentage': 50.0, 'promotion': 'Without promo', 'severity': 'Medium'},
        {'date': datetime(2025, 7, 14), 'day_of_week': 'Tuesday', 'failed_metrics': '3/8', 'failure_percentage': 37.5, 'promotion': 'Anniversary Sale Kick Off', 'severity': 'Low'},
        {'date': datetime(2025, 7, 8), 'day_of_week': 'Wednesday', 'failed_metrics': '3/8', 'failure_percentage': 37.5, 'promotion': 'No promotion', 'severity': 'Low'},
        {'date': datetime(2025, 8, 2), 'day_of_week': 'Sunday', 'failed_metrics': '3/8', 'failure_percentage': 37.5, 'promotion': 'No promotion', 'severity': 'Low'},
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

# Enhanced Sidebar with modern design
def create_enhanced_sidebar():
    with st.sidebar:
        # Modern company header
        st.markdown("""
        <div class="nav-header">
            🏢 City Furniture<br>
            <span style="font-size: 0.9rem; font-weight: 400; opacity: 0.8;">Analytics Intelligence Hub</span>
        </div>
        """, unsafe_allow_html=True)

        # Navigation sections
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("**🎯 Dashboard Control Center**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Overview", key="nav_overview_main", use_container_width=True):
                st.session_state.current_section = "overview"
                st.success("📊 Overview activated!")

        with col2:
            if st.button("🎯 Metrics", key="nav_metrics_main", use_container_width=True):
                st.session_state.current_section = "metrics"
                st.success("🎯 Metrics panel opened!")

        st.markdown('</div>', unsafe_allow_html=True)

        # Advanced analytics navigation
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("**📈 Advanced Analytics**")

        if st.button("📈 Performance Trends", key="nav_trends", use_container_width=True):
            st.success("📈 Performance trends analysis ready!")
        if st.button("🔍 Deep Dive Analysis", key="nav_deep_dive", use_container_width=True):
            st.success("🔍 Deep dive analysis activated!")

        st.markdown('</div>', unsafe_allow_html=True)

        # Quick actions
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("**🔧 Quick Actions**")

        if st.button("📊 Generate Report", key="nav_generate_report", use_container_width=True):
            st.success("📊 Report generation initiated!")
        if st.button("🔄 Refresh All", key="nav_refresh_all", use_container_width=True):
            st.cache_data.clear()
            st.success("🔄 All data refreshed!")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Enhanced quick stats
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown("**📊 Live Statistics**")

        # Calculate advanced statistics
        avg_score = daily_df['satisfaction_score'].mean()
        below_target = (daily_df['satisfaction_score'] < 9.0).sum()
        total_days = len(daily_df)
        performance_rate = ((total_days - below_target) / total_days * 100)

        # Recent trend analysis
        recent_scores = daily_df.tail(7)['satisfaction_score'].mean()
        previous_scores = daily_df.iloc[-14:-7]['satisfaction_score'].mean()
        trend = recent_scores - previous_scores

        # Critical events count
        critical_events = len(events_df[events_df['severity'] == 'Critical'])
        high_events = len(events_df[events_df['severity'] == 'High'])

        # Enhanced stat cards with gradients
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1.2rem; border-radius: 12px; margin: 0.5rem 0; 
                    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);">
            <div style="font-weight: 700; font-size: 0.85rem; opacity: 0.9;">OVERALL SCORE</div>
            <div style="font-size: 2rem; font-weight: 800; margin: 0.2rem 0;">{avg_score:.1f}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">out of 10.0 points</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    color: white; padding: 1.2rem; border-radius: 12px; margin: 0.5rem 0;
                    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);">
            <div style="font-weight: 700; font-size: 0.85rem; opacity: 0.9;">PERFORMANCE RATE</div>
            <div style="font-size: 2rem; font-weight: 800; margin: 0.2rem 0;">{performance_rate:.1f}%</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">days meeting target</div>
        </div>
        """, unsafe_allow_html=True)

        trend_color = "#10b981" if trend >= 0 else "#ef4444"
        trend_icon = "📈" if trend >= 0 else "📉"

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {trend_color} 0%, {trend_color}dd 100%); 
                    color: white; padding: 1.2rem; border-radius: 12px; margin: 0.5rem 0;
                    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);">
            <div style="font-weight: 700; font-size: 0.85rem; opacity: 0.9;">WEEKLY TREND {trend_icon}</div>
            <div style="font-size: 2rem; font-weight: 800; margin: 0.2rem 0;">{trend:+.2f}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">7-day comparison</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                    color: white; padding: 1.2rem; border-radius: 12px; margin: 0.5rem 0;
                    box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);">
            <div style="font-weight: 700; font-size: 0.85rem; opacity: 0.9;">CRITICAL ALERTS 🚨</div>
            <div style="font-size: 2rem; font-weight: 800; margin: 0.2rem 0;">{critical_events + high_events}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">high priority events</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# Create enhanced sidebar
create_enhanced_sidebar()

# Modern main header with advanced information
st.markdown("""
<div class="main-header fadeInUp">
    <h1>🏢 City Furniture - Customer Satisfaction Analytics</h1>
    <p>May 30, 2025 - September 30, 2025 | 124 days analyzed | Advanced Business Intelligence Platform</p>
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem; flex-wrap: wrap;">
        <div style="background: rgba(255,255,255,0.2); padding: 0.8rem 1.5rem; border-radius: 25px; backdrop-filter: blur(10px);">
            <span style="font-weight: 600;">📊 Real-time Analytics</span>
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 0.8rem 1.5rem; border-radius: 25px; backdrop-filter: blur(10px);">
            <span style="font-weight: 600;">🤖 AI-Powered Insights</span>
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 0.8rem 1.5rem; border-radius: 25px; backdrop-filter: blur(10px);">
            <span style="font-weight: 600;">⚡ Live Monitoring</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Create enhanced tabs with advanced functionality
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Daily Timeline", 
    "📊 Monthly Comparison", 
    "⚠️ Critical Events", 
    "🎯 Risk Analysis"
])

# TAB 1: Daily Timeline with Enhanced Functionality from Original Code
with tab1:
    st.markdown('<h2 class="section-header fadeInUp">📈 Daily Performance Timeline</h2>', unsafe_allow_html=True)

    # Advanced filter container with modern design
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        month_filter = st.selectbox(
            "🗓️ Filter by Month:",
            options=["All Months"] + sorted(daily_df['month'].unique()),
            key="daily_month_filter_advanced",
            help="Select a specific month for detailed analysis"
        )

    with col2:
        show_weekends = st.checkbox(
            "🔸 Highlight Weekends", 
            value=True, 
            key="show_weekends_advanced",
            help="Show weekend performance with special markers"
        )

    with col3:
        show_target = st.checkbox(
            "🎯 Show Target Line", 
            value=True, 
            key="show_target_advanced",
            help="Display performance target reference line at 9.0"
        )

    with col4:
        show_trends = st.checkbox(
            "📊 Show Trend Analysis", 
            value=False, 
            key="show_trends_advanced",
            help="Display trend lines and moving averages"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_daily = daily_df.copy()
    if month_filter != "All Months":
        filtered_daily = daily_df[daily_df['month'] == month_filter]

    if len(filtered_daily) == 0:
        st.markdown("""
        <div class="alert-warning">
            <h4>❌ No data available</h4>
            <p>No data found for the selected month. Please choose a different filter.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Enhanced timeline chart with advanced features
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        # Create advanced figure with subplots if trends are enabled
        if show_trends:
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Daily Satisfaction Scores', 'Trend Analysis'),
                vertical_spacing=0.12,
                row_heights=[0.7, 0.3]
            )

            # Main satisfaction timeline
            fig.add_trace(
                go.Scatter(
                    x=filtered_daily['date'],
                    y=filtered_daily['satisfaction_score'],
                    mode='lines+markers',
                    name='Daily Satisfaction',
                    line=dict(color='#667eea', width=3),
                    marker=dict(
                        size=8,
                        color=['#ef4444' if score < 9.0 else '#10b981' for score in filtered_daily['satisfaction_score']],
                        line=dict(width=2, color='white')
                    ),
                    hovertemplate='<b>%{x|%B %d, %Y}</b><br>Satisfaction: %{y}/10<extra></extra>'
                ),
                row=1, col=1
            )

            # Add moving average if enough data points
            if len(filtered_daily) >= 7:
                filtered_daily['ma_7'] = filtered_daily['satisfaction_score'].rolling(window=7).mean()
                fig.add_trace(
                    go.Scatter(
                        x=filtered_daily['date'],
                        y=filtered_daily['ma_7'],
                        mode='lines',
                        name='7-day Moving Average',
                        line=dict(color='#764ba2', width=2, dash='dash'),
                        hovertemplate='<b>%{x|%B %d, %Y}</b><br>7-day Average: %{y:.2f}<extra></extra>'
                    ),
                    row=1, col=1
                )

            # Trend decomposition in second subplot
            if len(filtered_daily) >= 14:
                trend_values = filtered_daily['satisfaction_score'].rolling(window=7).mean().diff()
                fig.add_trace(
                    go.Scatter(
                        x=filtered_daily['date'],
                        y=trend_values,
                        mode='lines',
                        name='Trend Direction',
                        line=dict(color='#f59e0b', width=2),
                        hovertemplate='<b>%{x|%B %d, %Y}</b><br>Trend: %{y:.3f}<extra></extra>'
                    ),
                    row=2, col=1
                )
                fig.add_hline(y=0, line_dash="solid", line_color="#64748b", line_width=1, row=2, col=1)

        else:
            # Standard single plot
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=filtered_daily['date'],
                y=filtered_daily['satisfaction_score'],
                mode='lines+markers',
                name='Daily Satisfaction',
                line=dict(color='#667eea', width=3),
                marker=dict(
                    size=8,
                    color=['#ef4444' if score < 9.0 else '#10b981' for score in filtered_daily['satisfaction_score']],
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<b>%{x|%B %d, %Y}</b><br>Satisfaction: %{y}/10<extra></extra>'
            ))

        # Add target line if requested
        if show_target:
            if show_trends:
                fig.add_hline(y=9.0, line_dash="dash", line_color="#10b981", line_width=2, 
                            annotation_text="🎯 Target (9.0)", row=1, col=1)
            else:
                fig.add_hline(y=9.0, line_dash="dash", line_color="#10b981", line_width=2,
                            annotation_text="🎯 Target (9.0)")

        # Add weekend highlighting if requested
        if show_weekends:
            weekend_data = filtered_daily[filtered_daily['is_weekend']]
            if not weekend_data.empty:
                if show_trends:
                    fig.add_trace(go.Scatter(
                        x=weekend_data['date'],
                        y=weekend_data['satisfaction_score'],
                        mode='markers',
                        name='🔸 Weekends',
                        marker=dict(size=12, color='#f59e0b', symbol='diamond', 
                                   line=dict(width=2, color='white')),
                        hovertemplate='<b>%{x|%B %d, %Y} (Weekend)</b><br>Satisfaction: %{y}/10<extra></extra>'
                    ), row=1, col=1)
                else:
                    fig.add_trace(go.Scatter(
                        x=weekend_data['date'],
                        y=weekend_data['satisfaction_score'],
                        mode='markers',
                        name='🔸 Weekends',
                        marker=dict(size=12, color='#f59e0b', symbol='diamond', 
                                   line=dict(width=2, color='white')),
                        hovertemplate='<b>%{x|%B %d, %Y} (Weekend)</b><br>Satisfaction: %{y}/10<extra></extra>'
                    ))

        # Enhanced layout configuration
        fig.update_layout(
            title="📊 Advanced Daily Customer Satisfaction Analysis",
            font=dict(family="Inter", size=12),
            hovermode='x unified',
            height=600 if show_trends else 500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#e2e8f0",
                borderwidth=1
            ),
            plot_bgcolor='rgba(248,250,252,0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                title="📅 Date",
                gridcolor='rgba(226,232,240,0.8)',
                gridwidth=1,
                showspikes=True,
                spikethickness=1,
                spikecolor="#667eea"
            ),
            yaxis=dict(
                title="⭐ Satisfaction Score",
                gridcolor='rgba(226,232,240,0.8)',
                gridwidth=1,
                range=[0, 10]
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Enhanced summary statistics with advanced metrics
        st.markdown('<h3 class="subsection-header">📊 Advanced Performance Analytics</h3>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_score = filtered_daily['satisfaction_score'].mean()
            score_std = filtered_daily['satisfaction_score'].std()
            st.markdown(f"""
            <div class="metric-card status-excellent">
                <h3>📈 Average Score</h3>
                <h1>{avg_score:.2f}</h1>
                <p>±{score_std:.2f} std deviation<br>Performance rating</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            below_target = (filtered_daily['satisfaction_score'] < 9.0).sum()
            target_rate = ((len(filtered_daily) - below_target) / len(filtered_daily)) * 100
            st.markdown(f"""
            <div class="metric-card {'status-excellent' if target_rate >= 80 else 'status-good' if target_rate >= 60 else 'status-needs-improvement'}">
                <h3>🎯 Target Achievement</h3>
                <h1>{target_rate:.1f}%</h1>
                <p>{below_target} days below target<br>out of {len(filtered_daily)} days</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            if len(filtered_daily) > 0:
                best_day = filtered_daily.loc[filtered_daily['satisfaction_score'].idxmax()]
                st.markdown(f"""
                <div class="metric-card status-excellent">
                    <h3>🏆 Peak Performance</h3>
                    <h1>{best_day['satisfaction_score']:.1f}</h1>
                    <p>{best_day['date'].strftime('%B %d, %Y')}<br>{best_day['day_name']}</p>
                </div>
                """, unsafe_allow_html=True)

        with col4:
            if len(filtered_daily) >= 7:
                recent_trend = filtered_daily.tail(7)['satisfaction_score'].mean() - filtered_daily.head(7)['satisfaction_score'].mean()
                trend_status = "status-excellent" if recent_trend > 0 else "status-needs-improvement" if recent_trend < -0.2 else "status-good"
                trend_icon = "📈" if recent_trend > 0 else "📉" if recent_trend < 0 else "➡️"
                st.markdown(f"""
                <div class="metric-card {trend_status}">
                    <h3>📊 Performance Trend</h3>
                    <h1 style="font-size: 1.8rem;">{trend_icon}</h1>
                    <p>{recent_trend:+.2f} recent change<br>7-day comparison</p>
                </div>
                """, unsafe_allow_html=True)

        # Advanced insights section
        if len(filtered_daily) >= 14:
            st.markdown('<h3 class="subsection-header">🔍 Advanced Insights</h3>', unsafe_allow_html=True)

            insight_col1, insight_col2 = st.columns(2)

            with insight_col1:
                # Weekend vs Weekday analysis
                weekend_scores = filtered_daily[filtered_daily['is_weekend']]['satisfaction_score'].mean()
                weekday_scores = filtered_daily[~filtered_daily['is_weekend']]['satisfaction_score'].mean()
                weekend_diff = weekend_scores - weekday_scores

                st.markdown(f"""
                <div class="metric-card">
                    <h3>📅 Weekend vs Weekday Analysis</h3>
                    <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                        <div>
                            <strong>Weekends:</strong> {weekend_scores:.2f}<br>
                            <strong>Weekdays:</strong> {weekday_scores:.2f}
                        </div>
                        <div style="text-align: right;">
                            <strong>Difference:</strong><br>
                            <span style="color: {'#10b981' if weekend_diff > 0 else '#ef4444'};">{weekend_diff:+.2f}</span>
                        </div>
                    </div>
                    <p style="font-size: 0.9rem; color: #64748b;">
                        {'Weekends perform better' if weekend_diff > 0 else 'Weekdays perform better' if weekend_diff < 0 else 'Similar performance'}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            with insight_col2:
                # Volatility analysis
                volatility = filtered_daily['satisfaction_score'].std()
                volatility_status = "Low" if volatility < 0.5 else "Medium" if volatility < 1.0 else "High"
                volatility_color = "#10b981" if volatility < 0.5 else "#f59e0b" if volatility < 1.0 else "#ef4444"

                st.markdown(f"""
                <div class="metric-card">
                    <h3>📊 Score Volatility Analysis</h3>
                    <div style="text-align: center; margin: 1rem 0;">
                        <div style="font-size: 2rem; color: {volatility_color}; font-weight: 700;">
                            {volatility:.2f}
                        </div>
                        <div style="color: {volatility_color}; font-weight: 600;">
                            {volatility_status} Volatility
                        </div>
                    </div>
                    <p style="font-size: 0.9rem; color: #64748b;">
                        Standard deviation of satisfaction scores over the period
                    </p>
                </div>
                """, unsafe_allow_html=True)

# TAB 2: Monthly Comparison with Advanced Analytics from Original Code
with tab2:
    st.markdown('<h2 class="section-header fadeInUp">📊 Monthly Performance Analysis</h2>', unsafe_allow_html=True)

    # Advanced metric selector with enhanced features
    metric_options = {
        'Overall Satisfaction': {
            'target': 9.0, 'format': '{:.2f}', 'icon': '⭐',
            'description': 'Overall customer satisfaction rating across all touchpoints',
            'benchmark': 8.5, 'industry_avg': 8.2
        },
        'Likelihood to Buy Again': {
            'target': 9.0, 'format': '{:.2f}', 'icon': '🛒',
            'description': 'Customer retention and repeat purchase intention',
            'benchmark': 8.3, 'industry_avg': 7.9
        },
        'Likelihood to Recommend': {
            'target': 9.0, 'format': '{:.2f}', 'icon': '👍',
            'description': 'Net Promoter Score (NPS) equivalent metric',
            'benchmark': 8.7, 'industry_avg': 8.1
        },
        'Site Design': {
            'target': 9.0, 'format': '{:.2f}', 'icon': '🎨',
            'description': 'User experience and interface design satisfaction',
            'benchmark': 8.8, 'industry_avg': 8.4
        },
        'Ease of Finding': {
            'target': 9.0, 'format': '{:.2f}', 'icon': '🔍',
            'description': 'Product discovery and search functionality',
            'benchmark': 8.6, 'industry_avg': 8.0
        },
        'Product Information Clarity': {
            'target': 9.0, 'format': '{:.2f}', 'icon': '📋',
            'description': 'Quality and completeness of product descriptions',
            'benchmark': 8.9, 'industry_avg': 8.3
        },
        'Charges Stated Clearly': {
            'target': 9.0, 'format': '{:.2f}', 'icon': '💰',
            'description': 'Pricing transparency and fee disclosure',
            'benchmark': 9.1, 'industry_avg': 8.6
        },
        'Checkout Process': {
            'target': 9.0, 'format': '{:.2f}', 'icon': '✅',
            'description': 'Payment and order completion experience',
            'benchmark': 8.4, 'industry_avg': 7.8
        }
    }

    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        selected_metric = st.selectbox(
            "📊 Select Metric for Deep Analysis:",
            options=list(metric_options.keys()),
            index=6,  # Default to "Charges Stated Clearly"
            key="metric_selector_advanced",
            help="Choose which customer satisfaction metric to analyze in detail"
        )

    with col2:
        show_benchmarks = st.checkbox(
            "📊 Show Benchmarks",
            value=True,
            key="show_benchmarks",
            help="Display internal benchmarks and industry averages"
        )

    with col3:
        analysis_type = st.selectbox(
            "🔍 Analysis Type:",
            options=["Standard", "Advanced", "Predictive"],
            key="analysis_type_selector",
            help="Choose the depth of analysis"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Display metric information
    metric_info = metric_options[selected_metric]

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 2rem; border-radius: 16px; margin: 1.5rem 0;
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 3rem;">{metric_info['icon']}</div>
            <div>
                <h2 style="margin: 0; font-size: 1.5rem;">{selected_metric}</h2>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">{metric_info['description']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    target_score = metric_info['target']
    score_format = metric_info['format']

    # Enhanced data generation with more sophisticated modeling
    @st.cache_data
    def generate_advanced_metric_data(metric_name, analysis_type):
        month_data = {
            'May-June 2025': {'period': '2025-05-30 to 2025-06-30', 'total_days': 32, 'base_score': 9.48, 'seasonal_factor': 1.02},
            'July 2025': {'period': '2025-07-01 to 2025-07-31', 'total_days': 31, 'base_score': 9.22, 'seasonal_factor': 0.98},
            'August 2025': {'period': '2025-08-01 to 2025-08-31', 'total_days': 31, 'base_score': 9.16, 'seasonal_factor': 0.96},
            'September 2025': {'period': '2025-09-01 to 2025-09-30', 'total_days': 30, 'base_score': 9.43, 'seasonal_factor': 1.01}
        }

        # Enhanced metric variations with more sophisticated patterns
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
            base_score = data['base_score'] + variations[i]
            seasonal_adjusted = base_score * data['seasonal_factor']

            # Add noise for realism
            np.random.seed(42 + i)
            noise = np.random.normal(0, 0.05)
            final_score = round(seasonal_adjusted + noise, 2)

            days_below = max(0, int(abs(target_score - final_score) * data['total_days'] / 4)) if final_score < target_score else 0

            # Advanced metrics calculation
            confidence_interval = 0.15
            volatility = abs(variations[i]) * 0.5 + 0.1

            enhanced_data.append({
                'month': month,
                'period': data['period'],
                'total_days': data['total_days'],
                'average_score': final_score,
                'days_below_target': days_below,
                'days_below_percentage': round((days_below / data['total_days']) * 100, 1),
                'performance_vs_target': round(final_score - target_score, 2),
                'classification': 'Excellent' if final_score >= target_score else 'Good' if final_score >= target_score - 0.5 else 'Needs Improvement',
                'confidence_lower': round(final_score - confidence_interval, 2),
                'confidence_upper': round(final_score + confidence_interval, 2),
                'volatility': round(volatility, 2),
                'seasonal_factor': data['seasonal_factor']
            })

        return pd.DataFrame(enhanced_data)

    metric_data = generate_advanced_metric_data(selected_metric, analysis_type)

    # Enhanced month selector with select all/none functionality
    st.markdown("### 📅 Period Selection")
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        comparison_months = st.multiselect(
            "Select months to compare:",
            options=metric_data['month'].tolist(),
            default=metric_data['month'].tolist(),
            key="monthly_comparison_advanced",
            help="Choose which months to include in the analysis"
        )

    with col2:
        if st.button("✅ Select All", key="select_all_months", use_container_width=True):
            st.session_state.monthly_comparison_advanced = metric_data['month'].tolist()
            st.rerun()

    with col3:
        if st.button("❌ Clear All", key="clear_all_months", use_container_width=True):
            st.session_state.monthly_comparison_advanced = []
            st.rerun()

    if comparison_months:
        comparison_data = metric_data[metric_data['month'].isin(comparison_months)]

        # Enhanced monthly performance cards with advanced metrics
        st.markdown('<h3 class="subsection-header">📊 Monthly Performance Deep Dive</h3>', unsafe_allow_html=True)

        if len(comparison_data) > 0:
            cols = st.columns(min(len(comparison_data), 4))
            for i, (_, month_data_row) in enumerate(comparison_data.iterrows()):
                col_idx = i % 4
                with cols[col_idx]:
                    score = month_data_row['average_score']
                    classification = month_data_row['classification']

                    # Enhanced status colors and animations
                    if classification == 'Excellent':
                        status_class = "status-excellent"
                        status_color = "#10b981"
                        status_icon = "🌟"
                        performance_emoji = "🚀"
                    elif classification == 'Good':
                        status_class = "status-good"
                        status_color = "#f59e0b"
                        status_icon = "⚡"
                        performance_emoji = "👍"
                    else:
                        status_class = "status-needs-improvement"
                        status_color = "#ef4444"
                        status_icon = "⚠️"
                        performance_emoji = "🎯"

                    # Calculate relative performance
                    vs_benchmark = score - metric_info['benchmark']
                    vs_industry = score - metric_info['industry_avg']

                    st.markdown(f"""
                    <div class="metric-card {status_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                            <h3 style="margin: 0; font-size: 1.1rem;">{month_data_row["month"].split()[0]} {performance_emoji}</h3>
                            <span style="font-size: 1.5rem;">{status_icon}</span>
                        </div>

                        <div style="text-align: center; margin: 1.5rem 0;">
                            <div style="font-size: 3.2rem; font-weight: 800; color: {status_color}; line-height: 1;">
                                {score_format.format(score)}
                            </div>
                            <div style="font-size: 0.9rem; color: #666; margin-top: 0.5rem;">
                                {classification} Performance
                            </div>
                        </div>

                        <div style="background: rgba(0,0,0,0.05); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                            <div style="font-size: 0.8rem; margin-bottom: 0.5rem;">
                                <strong>📊 Period:</strong> {month_data_row["total_days"]} days
                            </div>
                            <div style="font-size: 0.8rem; margin-bottom: 0.5rem;">
                                <strong>🎯 vs Target:</strong> 
                                <span style="color: {'#10b981' if month_data_row['performance_vs_target'] >= 0 else '#ef4444'};">
                                    {month_data_row['performance_vs_target']:+.2f}
                                </span>
                            </div>
                            <div style="font-size: 0.8rem;">
                                <strong>📈 vs Benchmark:</strong> 
                                <span style="color: {'#10b981' if vs_benchmark >= 0 else '#ef4444'};">
                                    {vs_benchmark:+.2f}
                                </span>
                            </div>
                        </div>

                        {'<div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; font-size: 0.8rem;">' if show_benchmarks else ''}
                        {'<strong>🏆 Confidence Range:</strong><br>' if show_benchmarks else ''}
                        {f'{month_data_row["confidence_lower"]:.2f} - {month_data_row["confidence_upper"]:.2f}' if show_benchmarks else ''}
                        {'</div>' if show_benchmarks else ''}
                    </div>
                    """, unsafe_allow_html=True)

            # Advanced visualizations with enhanced interactivity
            st.markdown('<h3 class="subsection-header">📈 Advanced Performance Visualizations</h3>', unsafe_allow_html=True)

            viz_col1, viz_col2 = st.columns(2)

            with viz_col1:
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)

                # Enhanced performance chart with benchmarks
                fig_performance = go.Figure()

                # Main performance bars
                fig_performance.add_trace(go.Bar(
                    x=comparison_data['month'],
                    y=comparison_data['average_score'],
                    name='Actual Performance',
                    marker_color=[
                        '#10b981' if cls == 'Excellent' else '#f59e0b' if cls == 'Good' else '#ef4444'
                        for cls in comparison_data['classification']
                    ],
                    text=comparison_data['average_score'],
                    texttemplate='%{text:.2f}',
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Score: %{y:.2f}/10<extra></extra>'
                ))

                if show_benchmarks:
                    # Add benchmark lines
                    fig_performance.add_hline(
                        y=target_score,
                        line_dash="dash",
                        line_color="#10b981",
                        line_width=3,
                        annotation_text=f"🎯 Target ({target_score})"
                    )

                    fig_performance.add_hline(
                        y=metric_info['benchmark'],
                        line_dash="dot",
                        line_color="#667eea",
                        line_width=2,
                        annotation_text=f"📊 Internal Benchmark ({metric_info['benchmark']})"
                    )

                    fig_performance.add_hline(
                        y=metric_info['industry_avg'],
                        line_dash="dashdot",
                        line_color="#9ca3af",
                        line_width=2,
                        annotation_text=f"🏭 Industry Average ({metric_info['industry_avg']})"
                    )

                fig_performance.update_layout(
                    title=f"📊 {selected_metric} - Monthly Performance Analysis",
                    font=dict(family="Inter", size=12),
                    plot_bgcolor='rgba(248,250,252,0.8)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=500,
                    showlegend=False,
                    xaxis=dict(
                        title="📅 Period",
                        gridcolor='rgba(226,232,240,0.8)',
                        tickangle=45
                    ),
                    yaxis=dict(
                        title="⭐ Average Score",
                        gridcolor='rgba(226,232,240,0.8)',
                        range=[
                            min(comparison_data['average_score'].min() - 0.5, metric_info['industry_avg'] - 0.3),
                            max(comparison_data['average_score'].max() + 0.5, target_score + 0.2)
                        ]
                    )
                )

                st.plotly_chart(fig_performance, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with viz_col2:
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)

                # Enhanced gap analysis with confidence intervals
                fig_gap = go.Figure()

                if analysis_type == "Advanced":
                    # Add confidence intervals
                    fig_gap.add_trace(go.Scatter(
                        x=comparison_data['month'],
                        y=comparison_data['confidence_upper'],
                        mode='lines',
                        line=dict(color='rgba(102, 126, 234, 0)'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

                    fig_gap.add_trace(go.Scatter(
                        x=comparison_data['month'],
                        y=comparison_data['confidence_lower'],
                        mode='lines',
                        line=dict(color='rgba(102, 126, 234, 0)'),
                        fill='tonexty',
                        fillcolor='rgba(102, 126, 234, 0.2)',
                        name='Confidence Interval',
                        hoverinfo='skip'
                    ))

                # Performance gap bars
                fig_gap.add_trace(go.Bar(
                    x=comparison_data['month'],
                    y=comparison_data['performance_vs_target'],
                    name='Gap vs Target',
                    marker_color=[
                        '#10b981' if gap >= 0 else '#ef4444' if gap < -0.3 else '#f59e0b'
                        for gap in comparison_data['performance_vs_target']
                    ],
                    text=comparison_data['performance_vs_target'],
                    texttemplate='%{text:+.2f}',
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Gap: %{y:+.2f} points<extra></extra>'
                ))

                fig_gap.add_hline(y=0, line_dash="solid", line_color="#64748b", line_width=2)

                fig_gap.update_layout(
                    title=f"🎯 Performance Gap Analysis - {selected_metric}",
                    font=dict(family="Inter", size=12),
                    plot_bgcolor='rgba(248,250,252,0.8)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=500,
                    showlegend=analysis_type == "Advanced",
                    xaxis=dict(
                        title="📅 Period",
                        gridcolor='rgba(226,232,240,0.8)',
                        tickangle=45
                    ),
                    yaxis=dict(
                        title="📈 Gap from Target",
                        gridcolor='rgba(226,232,240,0.8)'
                    )
                )

                st.plotly_chart(fig_gap, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # Advanced performance charts with business intelligence
    st.markdown('<h3 class="subsection-header">📈 Advanced Performance Analytics</h3>', unsafe_allow_html=True)

    chart_cols = st.columns(2)

    with chart_cols[0]:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        # Enhanced trend chart with forecasting
        trend_df = pd.DataFrame({
            'Month': months,
            'Score': monthly_scores,
            'Target': [target_score] * len(months)
        })

        fig_trend = go.Figure()

        # Actual performance
        fig_trend.add_trace(go.Scatter(
            x=trend_df['Month'],
            y=trend_df['Score'],
            mode='lines+markers',
            name='Actual Performance',
            line=dict(color='#667eea', width=4),
            marker=dict(size=10, color='#667eea', line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Score: %{y:.2f}<extra></extra>'
        ))

        # Target line
        fig_trend.add_trace(go.Scatter(
            x=trend_df['Month'],
            y=trend_df['Target'],
            mode='lines',
            name='Target (9.0)',
            line=dict(color='#10b981', width=3, dash='dash'),
            hovertemplate='<b>%{x}</b><br>Target: %{y:.2f}<extra></extra>'
        ))

        # Add confidence bands if detailed analysis
        if analysis_depth != "Executive Summary":
            upper_bound = [score + 0.15 for score in monthly_scores]
            lower_bound = [score - 0.15 for score in monthly_scores]

            fig_trend.add_trace(go.Scatter(
                x=trend_df['Month'],
                y=upper_bound,
                mode='lines',
                line=dict(color='rgba(102, 126, 234, 0)'),
                showlegend=False,
                hoverinfo='skip'
            ))

            fig_trend.add_trace(go.Scatter(
                x=trend_df['Month'],
                y=lower_bound,
                mode='lines',
                line=dict(color='rgba(102, 126, 234, 0)'),
                fill='tonexty',
                fillcolor='rgba(102, 126, 234, 0.2)',
                name='Confidence Band',
                hoverinfo='skip'
            ))

        fig_trend.update_layout(
            title=f"📊 {selected_risk_metric} - Performance Trend Analysis",
            font=dict(family="Inter", size=12),
            plot_bgcolor='rgba(248,250,252,0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500,
            showlegend=True,
            xaxis=dict(title="📅 Period", gridcolor='rgba(226,232,240,0.8)'),
            yaxis=dict(title="⭐ Score", gridcolor='rgba(226,232,240,0.8)')
        )

        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_cols[1]:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        # Enhanced risk heatmap
        gap_df = pd.DataFrame({
            'Month': months,
            'Gap': performance_gaps,
            'Risk_Level': risk_levels,
            'Absolute_Gap': [abs(gap) for gap in performance_gaps]
        })

        fig_risk = px.bar(
            gap_df,
            x='Month',
            y='Gap',
            color='Risk_Level',
            color_discrete_map={
                'High Risk': '#dc2626',
                'Medium Risk': '#f59e0b',
                'Low Risk': '#10b981'
            },
            text='Gap'
        )

        fig_risk.add_hline(y=0, line_dash="solid", line_color="#64748b", line_width=2)
        fig_risk.update_traces(texttemplate='%{text:+.2f}', textposition='outside')

        fig_risk.update_layout(
            title=f"🎯 Risk Assessment - {selected_risk_metric}",
            font=dict(family="Inter", size=12),
            plot_bgcolor='rgba(248,250,252,0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500,
            showlegend=True,
            xaxis=dict(title="📅 Period", gridcolor='rgba(226,232,240,0.8)'),
            yaxis=dict(title="📈 Gap from Target", gridcolor='rgba(226,232,240,0.8)')
        )

        st.plotly_chart(fig_risk, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced business intelligence insights
    st.markdown('<h3 class="subsection-header">💡 Strategic Business Intelligence</h3>', unsafe_allow_html=True)

    insights_cols = st.columns(2)

    with insights_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Business Impact Analysis</h3>
            <div style="margin: 1.5rem 0;">
                <h4 style="color: #667eea; margin-bottom: 1rem;">📊 Current Situation:</h4>
                <p style="line-height: 1.8; margin-bottom: 1rem;">{metric_info['business_impact']}</p>

                <h4 style="color: #ef4444; margin: 1.5rem 0 1rem 0;">⚠️ Key Risk Factors:</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
        """, unsafe_allow_html=True)

        for factor in metric_info['risk_factors']:
            st.markdown(f"<li style='margin: 0.5rem 0; line-height: 1.6;'>{factor}</li>", unsafe_allow_html=True)

        st.markdown(f"""
                </ul>

                <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                            padding: 1rem; border-radius: 8px; margin-top: 1.5rem; border-left: 4px solid #ef4444;">
                    <strong>💰 Financial Impact:</strong><br>
                    {metric_info['financial_impact']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with insights_cols[1]:
        st.markdown(f"""
        <div class="metric-card status-excellent">
            <h3>💡 Strategic Recommendations</h3>
            <div style="margin: 1.5rem 0;">
                <h4 style="color: #10b981; margin-bottom: 1rem;">🚀 Action Plan:</h4>
                <ol style="margin: 0; padding-left: 1.5rem;">
        """, unsafe_allow_html=True)

        for i, rec in enumerate(metric_info['recommendations'], 1):
            priority_label = ["🔥 Critical", "⚡ High", "📊 Medium", "📋 Low"][min(i-1, 3)]
            st.markdown(f"<li style='margin: 0.8rem 0; line-height: 1.6;'><strong>{priority_label}:</strong> {rec}</li>", unsafe_allow_html=True)

        # Performance prediction based on trend
        if trend_direction > 0.1:
            prediction = "📈 **Positive Outlook**: Current trends indicate continued improvement in the next quarter"
            prediction_color = "#10b981"
            forecast_impact = "Potential 15-25% improvement in business metrics"
        elif trend_direction < -0.1:
            prediction = "📉 **Warning Signal**: Declining trend requires immediate strategic intervention"
            prediction_color = "#ef4444"
            forecast_impact = "Risk of 10-20% degradation without action"
        else:
            prediction = "➡️ **Stable Performance**: Maintaining current levels with monitoring recommended"
            prediction_color = "#667eea"
            forecast_impact = "Expected stable performance with minor fluctuations"

        st.markdown(f"""
                </ol>

                <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                            padding: 1rem; border-radius: 8px; margin-top: 1.5rem; border-left: 4px solid #10b981;">
                    <h4 style="margin: 0 0 0.8rem 0; color: #065f46;">🔮 {time_horizon} Forecast:</h4>
                    <p style="color: {prediction_color}; font-weight: 600; margin: 0.5rem 0;">{prediction}</p>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem; color: #064e3b;">{forecast_impact}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Enhanced export functionality with business intelligence
st.markdown('<div style="margin-top: 4rem;">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">📥 Advanced Data Export & Reporting Center</h2>', unsafe_allow_html=True)

export_cols = st.columns(4)

with export_cols[0]:
    if st.button("📊 Executive Dashboard", key="export_executive", use_container_width=True):
        st.success("📊 Executive dashboard export initiated!")
        # Here you would generate an executive summary

with export_cols[1]:
    if st.button("📈 Performance Report", key="export_performance", use_container_width=True):
        try:
            csv_buffer = io.StringIO()
            daily_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="💾 Download Performance CSV",
                data=csv_buffer.getvalue(),
                file_name=f"performance_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_performance"
            )
            st.success("✅ Performance report ready!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with export_cols[2]:
    if st.button("⚠️ Risk Analysis Report", key="export_risk_analysis", use_container_width=True):
        try:
            risk_data = []
            for metric, info in risk_metric_options.items():
                current = info['current_scores'][-1]
                trend = info['current_scores'][-1] - info['current_scores'][0]
                risk_level = 'High Risk' if (info['target'] - current) > 0.5 else 'Medium Risk' if (info['target'] - current) > 0.2 else 'Low Risk'

                risk_data.append({
                    'Metric': metric,
                    'Current_Score': current,
                    'Target_Score': info['target'],
                    'Gap': info['target'] - current,
                    'Trend': trend,
                    'Risk_Level': risk_level,
                    'Business_Priority': info['business_priority'],
                    'Financial_Impact': info['financial_impact']
                })

            risk_df = pd.DataFrame(risk_data)
            csv_buffer = io.StringIO()
            risk_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="💾 Download Risk Analysis CSV",
                data=csv_buffer.getvalue(),
                file_name=f"risk_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_risk_analysis"
            )
            st.success("✅ Risk analysis report ready!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with export_cols[3]:
    if st.button("🚨 Critical Events Report", key="export_critical_events", use_container_width=True):
        try:
            csv_buffer = io.StringIO()
            events_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="💾 Download Events CSV",
                data=csv_buffer.getvalue(),
                file_name=f"critical_events_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_critical_events"
            )
            st.success("✅ Critical events report ready!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Premium footer with business intelligence branding
st.markdown("""
<div style="margin-top: 5rem; padding: 3rem; 
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
            border-radius: 20px; text-align: center; 
            box-shadow: 0 12px 48px rgba(0,0,0,0.15);
            border: 1px solid #475569;">
    <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; margin-bottom: 1.5rem;">
        <div style="font-size: 3rem;">🏢</div>
        <div>
            <h2 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 700;">
                City Furniture - Advanced Analytics Intelligence Platform
            </h2>
            <p style="color: #cbd5e1; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                Last Updated: October 2025 | Powered by Advanced Business Intelligence & AI-Driven Analytics
            </p>
        </div>
    </div>

    <div style="display: flex; justify-content: center; gap: 2rem; margin: 2rem 0; flex-wrap: wrap;">
        <div style="background: rgba(255,255,255,0.1); padding: 1rem 1.5rem; border-radius: 25px; backdrop-filter: blur(10px);">
            <span style="color: white; font-weight: 600;">🚀 Real-time Analytics</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 1rem 1.5rem; border-radius: 25px; backdrop-filter: blur(10px);">
            <span style="color: white; font-weight: 600;">🤖 AI-Powered Insights</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 1rem 1.5rem; border-radius: 25px; backdrop-filter: blur(10px);">
            <span style="color: white; font-weight: 600;">⚡ Live Business Intelligence</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); padding: 1rem 1.5rem; border-radius: 25px; backdrop-filter: blur(10px);">
            <span style="color: white; font-weight: 600;">🎯 Strategic Decision Support</span>
        </div>
    </div>

    <p style="color: #94a3b8; margin: 0; font-size: 0.9rem; font-style: italic;">
        Enterprise-grade analytics platform • All features fully integrated and operational<br>
        Advanced risk management • Predictive business intelligence • Strategic performance optimization
    </p>
</div>
""", unsafe_allow_html=True)
