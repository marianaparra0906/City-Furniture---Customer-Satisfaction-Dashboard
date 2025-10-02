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

# ============================================================================
# NEW FILE UPLOAD FEATURE - INTEGRATED AT THE TOP
# ============================================================================

# Initialize session state for data persistence
if "data" not in st.session_state:
    st.session_state["data"] = None

# File Upload Section
st.markdown("### 📁 Data Upload Center")
st.markdown("Upload your own CSV or Excel files to override the default dataset, or leave empty to use the demo data.")

uploaded_files = st.file_uploader(
    "Choose CSV or Excel files",
    accept_multiple_files=True,
    type=['csv', 'xlsx', 'xls'],
    help="Upload multiple files and they will be concatenated into a single dataset"
)

# Process uploaded files
if uploaded_files:
    try:
        dataframes = []
        file_info = []

        for uploaded_file in uploaded_files:
            # Read file based on extension
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:  # Excel files
                df = pd.read_excel(uploaded_file)

            dataframes.append(df)
            file_info.append({
                'filename': uploaded_file.name,
                'rows': len(df),
                'columns': len(df.columns)
            })

        # Concatenate all dataframes
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)
            st.session_state["data"] = combined_df

            # Show upload success and file info
            st.success(f"✅ Successfully uploaded and processed {len(uploaded_files)} file(s)!")

            # Display file information
            st.markdown("#### 📋 Uploaded Files Summary")
            info_df = pd.DataFrame(file_info)
            st.dataframe(info_df, use_container_width=True)

            # Show quick preview of combined data
            st.markdown("#### 👀 Data Preview")
            st.dataframe(combined_df.head(10), use_container_width=True)

            # Show quick statistics
            st.markdown("#### 📊 Quick Statistics")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Dataset Overview:**")
                st.write(f"• Total rows: {len(combined_df):,}")
                st.write(f"• Total columns: {len(combined_df.columns)}")
                st.write(f"• Memory usage: {combined_df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")

            with col2:
                st.markdown("**Numeric Columns Summary:**")
                numeric_cols = combined_df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    st.dataframe(combined_df[numeric_cols].describe())
                else:
                    st.write("No numeric columns found")

    except Exception as e:
        st.error(f"❌ Error processing uploaded files: {str(e)}")
        st.session_state["data"] = None

elif st.session_state["data"] is not None:
    # Files were previously uploaded but now removed - show current data info
    st.info(f"📊 Currently using uploaded data with {len(st.session_state['data'])} rows and {len(st.session_state['data'].columns)} columns")

    if st.button("🗑️ Clear uploaded data and use default dataset"):
        st.session_state["data"] = None
        st.rerun()

else:
    st.info("📂 No files uploaded. Using default demo dataset.")

st.markdown("---")  # Separator line

# ============================================================================
# END FILE UPLOAD FEATURE
# ============================================================================

# Custom CSS for responsive design
st.markdown("""

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

# Load data - MODIFIED to use uploaded data if available
if st.session_state["data"] is not None:
    # Use uploaded data
    daily_df = st.session_state["data"]
    # For events, we'll still use the default since it's specific to your demo
    # but if uploaded data has events, you could modify this logic
    _, events_df = load_data()
else:
    # Use default data
    daily_df, events_df = load_data()

# Sidebar
st.sidebar.markdown("### 📊 Dashboard Navigation")
st.sidebar.markdown("---")

# Main header
st.markdown("""
# 🏢 City Furniture - Customer Satisfaction Dashboard
### Comprehensive Analytics for Business Intelligence

Welcome to the **Customer Satisfaction Analytics Dashboard**. This powerful tool provides deep insights into customer experience metrics, performance trends, and critical business events.

---
""")

# Display current data source info
if st.session_state["data"] is not None:
    st.info(f"📊 **Currently analyzing uploaded data**: {len(daily_df)} rows × {len(daily_df.columns)} columns")
else:
    st.info("📊 **Currently analyzing demo data**: May 30 - September 30, 2025 (124 days)")

st.markdown("---")

# Key Performance Indicators
st.markdown("## 🎯 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

# Check if we have the expected columns for the demo calculations
if st.session_state["data"] is None:
    # Use original logic for demo data
    avg_satisfaction = daily_df['satisfaction_score'].mean()
    total_days = len(daily_df)
    days_below_target = (daily_df['satisfaction_score'] < 9.0).sum()
    target_achievement = ((total_days - days_below_target) / total_days) * 100

    with col1:
        st.metric(
            label="📈 Average Satisfaction",
            value=f"{avg_satisfaction:.2f}/10",
            delta=f"{avg_satisfaction - 9:.2f} vs target"
        )

    with col2:
        st.metric(
            label="🎯 Target Achievement",
            value=f"{target_achievement:.1f}%",
            delta=f"{days_below_target} days below target"
        )

    with col3:
        best_day = daily_df.loc[daily_df['satisfaction_score'].idxmax()]
        st.metric(
            label="🏆 Best Performance",
            value=f"{best_day['satisfaction_score']:.1f}/10",
            delta=best_day['date'].strftime('%b %d')
        )

    with col4:
        worst_day = daily_df.loc[daily_df['satisfaction_score'].idxmin()]
        st.metric(
            label="⚠️ Lowest Score",
            value=f"{worst_day['satisfaction_score']:.1f}/10",
            delta=worst_day['date'].strftime('%b %d')
        )
else:
    # For uploaded data, show basic statistics
    numeric_cols = daily_df.select_dtypes(include=[np.number]).columns

    with col1:
        st.metric(
            label="📊 Total Records",
            value=f"{len(daily_df):,}",
            delta=f"{len(daily_df.columns)} columns"
        )

    with col2:
        if len(numeric_cols) > 0:
            avg_val = daily_df[numeric_cols].mean().mean()
            st.metric(
                label="📈 Avg Numeric Value",
                value=f"{avg_val:.2f}",
                delta=f"{len(numeric_cols)} numeric cols"
            )
        else:
            st.metric(
                label="📈 Numeric Columns",
                value="0",
                delta="No numeric data"
            )

    with col3:
        missing_values = daily_df.isnull().sum().sum()
        completeness = ((len(daily_df) * len(daily_df.columns) - missing_values) / (len(daily_df) * len(daily_df.columns))) * 100
        st.metric(
            label="✅ Data Completeness",
            value=f"{completeness:.1f}%",
            delta=f"{missing_values} missing values"
        )

    with col4:
        unique_values = daily_df.nunique().sum()
        st.metric(
            label="🔍 Unique Values",
            value=f"{unique_values:,}",
            delta="across all columns"
        )

# Continue with the rest of your original dashboard code...
# The rest remains exactly as it was in your original file

# Create tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["📈 Daily Timeline", "📊 Monthly Comparison", "⚠️ Critical Events", "🎯 Risk Analysis"])

# TAB 1: Daily Timeline Analysis
with tab1:
    st.markdown("### 📈 Daily Performance Timeline")

    if st.session_state["data"] is None:
        # Original logic for demo data

        # Filters
        col1, col2, col3 = st.columns(3)

        with col1:
            month_filter = st.selectbox(
                "🗓️ Filter by Month:",
                options=["All Months"] + sorted(daily_df['month'].unique()),
                key="daily_month_filter"
            )

        with col2:
            show_weekends = st.checkbox("🔸 Highlight Weekends", value=True)

        with col3:
            show_target = st.checkbox("🎯 Show Target Line (9.0)", value=True)

        # Apply filters
        filtered_data = daily_df.copy()
        if month_filter != "All Months":
            filtered_data = daily_df[daily_df['month'] == month_filter]

        # Create timeline chart
        fig_timeline = px.line(
            filtered_data,
            x='date',
            y='satisfaction_score',
            title='Daily Customer Satisfaction Scores',
            labels={'satisfaction_score': 'Satisfaction Score', 'date': 'Date'}
        )

        # Add target line
        if show_target:
            fig_timeline.add_hline(
                y=9.0,
                line_dash="dash",
                line_color="green",
                annotation_text="Target (9.0)"
            )

        # Highlight weekends
        if show_weekends:
            weekend_data = filtered_data[filtered_data['is_weekend']]
            fig_timeline.add_scatter(
                x=weekend_data['date'],
                y=weekend_data['satisfaction_score'],
                mode='markers',
                marker=dict(size=8, color='orange'),
                name='Weekends'
            )

        fig_timeline.update_layout(height=500)
        st.plotly_chart(fig_timeline, use_container_width=True)

        # Summary statistics
        st.markdown("#### 📊 Summary Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Average Score",
                f"{filtered_data['satisfaction_score'].mean():.2f}"
            )

        with col2:
            st.metric(
                "Days Below Target",
                f"{(filtered_data['satisfaction_score'] < 9.0).sum()}"
            )

        with col3:
            st.metric(
                "Best Performance",
                f"{filtered_data['satisfaction_score'].max():.1f}"
            )

        with col4:
            st.metric(
                "Standard Deviation",
                f"{filtered_data['satisfaction_score'].std():.2f}"
            )

    else:
        # For uploaded data, show a generic timeline if date column exists
        st.info("📊 Uploaded data detected. Showing basic data visualization.")

        # Try to identify date and numeric columns
        date_cols = daily_df.select_dtypes(include=['datetime64', 'object']).columns
        numeric_cols = daily_df.select_dtypes(include=[np.number]).columns

        if len(date_cols) > 0 and len(numeric_cols) > 0:
            col1, col2 = st.columns(2)

            with col1:
                selected_date_col = st.selectbox("Select Date Column:", options=date_cols.tolist())

            with col2:
                selected_numeric_col = st.selectbox("Select Value Column:", options=numeric_cols.tolist())

            if selected_date_col and selected_numeric_col:
                # Try to convert to datetime if needed
                try:
                    plot_data = daily_df.copy()
                    if not pd.api.types.is_datetime64_any_dtype(plot_data[selected_date_col]):
                        plot_data[selected_date_col] = pd.to_datetime(plot_data[selected_date_col])

                    fig = px.line(
                        plot_data,
                        x=selected_date_col,
                        y=selected_numeric_col,
                        title=f'Timeline: {selected_numeric_col} over {selected_date_col}'
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    st.error(f"Could not create timeline plot: {str(e)}")
                    st.dataframe(daily_df.head())
        else:
            st.warning("No suitable date and numeric columns found for timeline visualization.")
            st.dataframe(daily_df.head())

# TAB 2: Monthly Comparison
with tab2:
    st.markdown("### 📊 Monthly Performance Comparison")

    if st.session_state["data"] is None:
        # Your original monthly comparison logic here

        # Enhanced metric selector
        metric_options = {
            'Overall Satisfaction': {'target': 9.0, 'format': '{:.2f}'},
            'Likelihood to Buy Again': {'target': 9.0, 'format': '{:.2f}'},
            'Likelihood to Recommend': {'target': 9.0, 'format': '{:.2f}'},
            'Site Design': {'target': 9.0, 'format': '{:.2f}'},
            'Ease of Finding': {'target': 9.0, 'format': '{:.2f}'},
            'Product Information Clarity': {'target': 9.0, 'format': '{:.2f}'},
            'Charges Stated Clearly': {'target': 9.0, 'format': '{:.2f}'},
            'Checkout Process': {'target': 9.0, 'format': '{:.2f}'}
        }

        selected_metric = st.selectbox(
            "📊 Select Metric:",
            options=list(metric_options.keys()),
            index=6  # Default to "Charges Stated Clearly"
        )

        # Generate sample data for comparison
        months = ['May-Jun 2025', 'July 2025', 'August 2025', 'September 2025']
        scores = [9.48, 9.22, 9.16, 9.43]  # Sample scores

        # Create comparison chart
        fig_comparison = px.bar(
            x=months,
            y=scores,
            title=f'{selected_metric} - Monthly Performance',
            labels={'x': 'Month', 'y': 'Average Score'}
        )

        # Add target line
        target = metric_options[selected_metric]['target']
        fig_comparison.add_hline(
            y=target,
            line_dash="dash",
            line_color="green",
            annotation_text=f"Target ({target})"
        )

        fig_comparison.update_layout(height=400)
        st.plotly_chart(fig_comparison, use_container_width=True)

        # Performance cards
        st.markdown("#### 📋 Monthly Performance Cards")

        cols = st.columns(len(months))
        for i, (month, score) in enumerate(zip(months, scores)):
            with cols[i]:
                delta = score - target
                st.metric(
                    label=month,
                    value=f"{score:.2f}",
                    delta=f"{delta:+.2f} vs target"
                )

    else:
        # For uploaded data
        st.info("📊 Uploaded data detected. Showing data summary by groups if possible.")

        # Try to group by different columns
        categorical_cols = daily_df.select_dtypes(include=['object', 'category']).columns
        numeric_cols = daily_df.select_dtypes(include=[np.number]).columns

        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            col1, col2 = st.columns(2)

            with col1:
                group_by_col = st.selectbox("Group By Column:", options=categorical_cols.tolist())

            with col2:
                analyze_col = st.selectbox("Analyze Column:", options=numeric_cols.tolist())

            if group_by_col and analyze_col:
                try:
                    grouped_data = daily_df.groupby(group_by_col)[analyze_col].agg(['mean', 'count', 'std']).reset_index()

                    fig = px.bar(
                        grouped_data,
                        x=group_by_col,
                        y='mean',
                        title=f'Average {analyze_col} by {group_by_col}'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)

                    st.dataframe(grouped_data)

                except Exception as e:
                    st.error(f"Could not create grouped analysis: {str(e)}")
        else:
            st.warning("No suitable categorical and numeric columns found for grouping analysis.")
            st.dataframe(daily_df.head())

# TAB 3: Critical Events
with tab3:
    st.markdown("### ⚠️ Critical Events Analysis")

    if st.session_state["data"] is None:
        # Your original events analysis

        # Filters
        col1, col2, col3 = st.columns(3)

        with col1:
            failure_threshold = st.slider(
                "📊 Minimum Failure %:",
                min_value=0,
                max_value=100,
                value=0,
                step=5
            )

        with col2:
            severity_filter = st.multiselect(
                "🚨 Severity Levels:",
                options=['Critical', 'High', 'Medium', 'Low'],
                default=['Critical', 'High', 'Medium', 'Low']
            )

        with col3:
            sort_by = st.selectbox(
                "📋 Sort by:",
                options=['date', 'failure_percentage', 'severity']
            )

        # Apply filters
        filtered_events = events_df[
            (events_df['failure_percentage'] >= failure_threshold) &
            (events_df['severity'].isin(severity_filter))
        ]

        # Sort data
        if sort_by == 'date':
            filtered_events = filtered_events.sort_values('date', ascending=False)
        elif sort_by == 'failure_percentage':
            filtered_events = filtered_events.sort_values('failure_percentage', ascending=False)
        else:
            severity_order = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
            filtered_events['severity_num'] = filtered_events['severity'].map(severity_order)
            filtered_events = filtered_events.sort_values('severity_num', ascending=False)

        # Display results
        st.markdown(f"#### 📊 Found {len(filtered_events)} events")

        if not filtered_events.empty:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Average Failure %", f"{filtered_events['failure_percentage'].mean():.1f}%")

            with col2:
                critical_count = (filtered_events['severity'] == 'Critical').sum()
                st.metric("Critical Events", critical_count)

            with col3:
                high_failure = (filtered_events['failure_percentage'] >= 70).sum()
                st.metric("High Risk Days", high_failure)

            with col4:
                avg_impact = filtered_events['failure_percentage'].mean()
                st.metric("Risk Level", "High" if avg_impact > 60 else "Medium" if avg_impact > 30 else "Low")

            # Events timeline
            fig_events = px.scatter(
                filtered_events,
                x='date',
                y='failure_percentage',
                color='severity',
                size='failure_percentage',
                hover_data=['day_of_week', 'failed_metrics', 'promotion'],
                title='Critical Events Timeline'
            )

            fig_events.update_layout(height=500)
            st.plotly_chart(fig_events, use_container_width=True)

            # Detailed events table
            st.markdown("#### 📋 Detailed Events")
            display_cols = ['date', 'day_of_week', 'failure_percentage', 'failed_metrics', 'severity', 'promotion']
            st.dataframe(
                filtered_events[display_cols],
                use_container_width=True,
                height=400
            )
        else:
            st.info("No events found matching the current filters.")

    else:
        # For uploaded data
        st.info("📊 Uploaded data detected. Showing data distribution analysis.")

        numeric_cols = daily_df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Select column to analyze for outliers/events:", options=numeric_cols.tolist())

            if selected_col:
                col_data = daily_df[selected_col].dropna()

                # Calculate outliers using IQR method
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = daily_df[(daily_df[selected_col] < lower_bound) | (daily_df[selected_col] > upper_bound)]

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Total Records", len(daily_df))
                    st.metric("Outliers Found", len(outliers))

                with col2:
                    st.metric("Lower Bound", f"{lower_bound:.2f}")
                    st.metric("Upper Bound", f"{upper_bound:.2f}")

                # Box plot
                fig = px.box(daily_df, y=selected_col, title=f'Box Plot: {selected_col}')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

                if not outliers.empty:
                    st.markdown("#### 📋 Detected Outliers")
                    st.dataframe(outliers, use_container_width=True)
        else:
            st.warning("No numeric columns found for outlier analysis.")

# TAB 4: Risk Analysis
with tab4:
    st.markdown("### 🎯 Advanced Risk Analysis")

    if st.session_state["data"] is None:
        # Your original risk analysis

        # Risk metrics
        risk_metrics = {
            'Overall Satisfaction': [9.48, 9.38, 9.36, 9.48],
            'Likelihood to Buy Again': [9.58, 9.33, 9.21, 9.56],
            'Likelihood to Recommend': [9.43, 9.25, 9.06, 9.60],
            'Site Design': [9.68, 9.37, 9.26, 9.73],
            'Ease of Finding': [9.63, 9.30, 9.21, 9.66],
            'Product Information Clarity': [9.60, 9.28, 9.18, 9.63],
            'Charges Stated Clearly': [9.48, 9.22, 9.16, 9.43],
            'Checkout Process': [9.28, 9.07, 8.91, 9.31]
        }

        selected_risk_metric = st.selectbox(
            "🎯 Select Risk Metric:",
            options=list(risk_metrics.keys())
        )

        # Calculate risk indicators
        scores = risk_metrics[selected_risk_metric]
        months = ['May-Jun 2025', 'July 2025', 'August 2025', 'September 2025']
        target = 9.0

        current_score = scores[-1]
        avg_score = sum(scores) / len(scores)
        trend = scores[-1] - scores[0]

        # Risk dashboard
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Current Score",
                f"{current_score:.2f}",
                delta=f"{current_score - target:+.2f} vs target"
            )

        with col2:
            st.metric(
                "Average Score",
                f"{avg_score:.2f}",
                delta="4-month average"
            )

        with col3:
            risk_level = "High" if (target - current_score) > 0.5 else "Medium" if (target - current_score) > 0.2 else "Low"
            st.metric("Risk Level", risk_level)

        with col4:
            trend_direction = "Improving" if trend > 0.1 else "Declining" if trend < -0.1 else "Stable"
            st.metric("Trend", trend_direction, delta=f"{trend:+.2f}")

        # Risk trend chart
        fig_risk = go.Figure()

        fig_risk.add_trace(go.Scatter(
            x=months,
            y=scores,
            mode='lines+markers',
            name='Actual Score',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ))

        fig_risk.add_trace(go.Scatter(
            x=months,
            y=[target] * len(months),
            mode='lines',
            name='Target',
            line=dict(color='green', width=2, dash='dash')
        ))

        fig_risk.update_layout(
            title=f'{selected_risk_metric} - Risk Trend Analysis',
            height=400,
            yaxis_title='Score',
            xaxis_title='Period'
        )

        st.plotly_chart(fig_risk, use_container_width=True)

        # Risk assessment
        st.markdown("#### 💡 Risk Assessment")

        if risk_level == "High":
            st.error(f"🚨 **High Risk**: {selected_risk_metric} is significantly below target. Immediate action required.")
        elif risk_level == "Medium":
            st.warning(f"⚠️ **Medium Risk**: {selected_risk_metric} needs attention to prevent further decline.")
        else:
            st.success(f"✅ **Low Risk**: {selected_risk_metric} is performing well and meeting targets.")

        # Recommendations
        recommendations = {
            'Overall Satisfaction': ['Implement customer feedback loops', 'Enhance service quality training', 'Regular satisfaction surveys'],
            'Likelihood to Buy Again': ['Develop loyalty programs', 'Improve customer service', 'Competitive pricing analysis'],
            'Likelihood to Recommend': ['Create referral incentives', 'Monitor online reviews', 'Social media engagement'],
            'Site Design': ['UX/UI improvements', 'Mobile optimization', 'User testing sessions'],
            'Ease of Finding': ['Search functionality enhancement', 'Navigation improvements', 'Category optimization'],
            'Product Information Clarity': ['Content quality review', 'Product description standards', 'Visual content enhancement'],
            'Charges Stated Clearly': ['Pricing transparency', 'Fee disclosure improvements', 'Checkout clarity'],
            'Checkout Process': ['Process simplification', 'Multiple payment options', 'Mobile checkout optimization']
        }

        st.markdown("#### 📋 Recommended Actions")
        for rec in recommendations.get(selected_risk_metric, []):
            st.markdown(f"• {rec}")

    else:
        # For uploaded data
        st.info("📊 Uploaded data detected. Showing correlation and risk analysis.")

        numeric_cols = daily_df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) >= 2:
            # Correlation heatmap
            corr_matrix = daily_df[numeric_cols].corr()

            fig_corr = px.imshow(
                corr_matrix,
                title='Correlation Matrix',
                color_continuous_scale='RdBu_r',
                aspect='auto'
            )
            fig_corr.update_layout(height=500)
            st.plotly_chart(fig_corr, use_container_width=True)

            # Risk indicators based on data variability
            st.markdown("#### 📊 Variability Risk Analysis")

            risk_analysis = []
            for col in numeric_cols:
                col_data = daily_df[col].dropna()
                if len(col_data) > 1:
                    cv = (col_data.std() / col_data.mean()) * 100  # Coefficient of variation
                    risk_level = "High" if cv > 50 else "Medium" if cv > 20 else "Low"

                    risk_analysis.append({
                        'Column': col,
                        'Mean': col_data.mean(),
                        'Std Dev': col_data.std(),
                        'CV (%)': cv,
                        'Risk Level': risk_level
                    })

            if risk_analysis:
                risk_df = pd.DataFrame(risk_analysis)
                st.dataframe(risk_df, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns for correlation analysis.")
            st.dataframe(daily_df.describe())

# Export functionality
st.markdown("---")
st.markdown("### 📥 Export Data")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Export Daily Data"):
        csv = daily_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"daily_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col2:
    if st.session_state["data"] is None and st.button("⚠️ Export Events Data"):
        csv = events_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"events_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col3:
    if st.button("📋 Export Summary Report"):
        # Create a summary report
        if st.session_state["data"] is None:
            summary_data = {
                'Metric': ['Average Satisfaction', 'Target Achievement', 'Total Days', 'Days Below Target'],
                'Value': [
                    f"{daily_df['satisfaction_score'].mean():.2f}",
                    f"{((len(daily_df) - (daily_df['satisfaction_score'] < 9.0).sum()) / len(daily_df) * 100):.1f}%",
                    str(len(daily_df)),
                    str((daily_df['satisfaction_score'] < 9.0).sum())
                ]
            }
        else:
            summary_data = {
                'Metric': ['Total Records', 'Total Columns', 'Numeric Columns', 'Missing Values'],
                'Value': [
                    str(len(daily_df)),
                    str(len(daily_df.columns)),
                    str(len(daily_df.select_dtypes(include=[np.number]).columns)),
                    str(daily_df.isnull().sum().sum())
                ]
            }

        summary_df = pd.DataFrame(summary_data)
        csv = summary_df.to_csv(index=False)
        st.download_button(
            label="Download Summary CSV",
            data=csv,
            file_name=f"summary_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🏢 <strong>City Furniture Analytics Dashboard</strong> | Powered by Streamlit | Last Updated: October 2025</p>
    <p><em>Advanced Business Intelligence & Customer Satisfaction Analytics</em></p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("*Dashboard last updated: October 2025 | City Furniture Customer Satisfaction Analysis - Ultimate Enhanced Version*")
st.markdown("*Powered by Advanced Analytics & Business Intelligence*")
