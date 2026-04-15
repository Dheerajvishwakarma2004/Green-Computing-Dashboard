import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Carbon Footprint Reduction Dashboard",
    layout="wide",
    page_icon="🌱",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for Dark Mode compatibility
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global Font */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header - Works in both modes */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 1rem 0;
    }
    
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    
    /* Metric Cards Enhancement */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        color: #667eea;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        font-size: 0.95rem;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Button Styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border: 2px solid #667eea;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.05rem;
        background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Info/Success/Warning boxes */
    .element-container div[data-testid="stMarkdownContainer"] > div[data-testid="stMarkdownContainer"] {
        border-radius: 8px;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        border-radius: 8px;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        border-radius: 8px;
    }
    
    /* Custom Cards */
    .custom-card {
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 1rem 0;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Plotly chart container */
    .js-plotly-plot {
        border-radius: 8px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    </style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('carbon_measures_data.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Error: 'carbon_measures_data.csv' file not found. Please ensure the file is in the same directory as this script.")
        st.stop()

# Load data
df = load_data()

# Calculate average values
df['Avg_Reduction'] = (df['Carbon_Reduction_Min'] + df['Carbon_Reduction_Max']) / 2
df['Avg_Cost'] = (df['Cost_Min'] + df['Cost_Max']) / 2
df['Avg_ROI'] = (df['ROI_Years_Min'] + df['ROI_Years_Max']) / 2

# Title
st.markdown('<h1 class="main-header">🌱 Carbon Footprint Reduction Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Evidence-Based Measures for Tech Companies | Powered by Real-World Data</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Filter Controls")
    st.markdown("---")
    
    # Company size filter
    st.markdown("### 🏢 Company Size")
    company_size_options = list(df['Company_Size'].unique())
    company_size_filter = st.multiselect(
        "Select applicable sizes",
        options=company_size_options,
        default=company_size_options,
        label_visibility="collapsed"
    )
    
    st.markdown("")
    
    # Category filter
    st.markdown("### 📂 Category")
    category_options = list(df['Category'].unique())
    category_filter = st.multiselect(
        "Select categories",
        options=category_options,
        default=category_options,
        label_visibility="collapsed"
    )
    
    st.markdown("")
    
    # Success rate filter
    st.markdown("### ✅ Success Rate Threshold")
    min_success_rate = st.slider(
        "Minimum success rate",
        min_value=0,
        max_value=100,
        value=70,
        step=5,
        label_visibility="collapsed"
    )
    st.caption(f"Showing measures with ≥{min_success_rate}% success rate")
    
    st.markdown("")
    
    # ROI filter
    st.markdown("### 💰 ROI Period")
    max_roi = st.slider(
        "Maximum ROI period",
        min_value=0,
        max_value=10,
        value=10,
        step=1,
        label_visibility="collapsed"
    )
    st.caption(f"Showing measures with ≤{max_roi} year ROI")
    
    st.markdown("")
    
    # Difficulty filter
    st.markdown("### ⚙️ Implementation Difficulty")
    difficulty_options = list(df['Difficulty_Level'].unique())
    difficulty_filter = st.multiselect(
        "Select difficulty levels",
        options=difficulty_options,
        default=difficulty_options,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Reset button
    if st.button("🔄 Reset All Filters"):
        st.rerun()
    
    st.markdown("---")
    
    # Info box
    st.info("💡 **Pro Tip:** Start with Quick Wins (ROI ≤1 year) to build momentum and demonstrate value to stakeholders.")

# Apply filters
df_filtered = df.copy()

if company_size_filter:
    df_filtered = df_filtered[df_filtered['Company_Size'].isin(company_size_filter)]

if category_filter:
    df_filtered = df_filtered[df_filtered['Category'].isin(category_filter)]

if difficulty_filter:
    df_filtered = df_filtered[df_filtered['Difficulty_Level'].isin(difficulty_filter)]

df_filtered = df_filtered[df_filtered['Success_Rate'] >= min_success_rate]
df_filtered = df_filtered[df_filtered['ROI_Years_Max'] <= max_roi]

# Check if filters result in empty dataset
if len(df_filtered) == 0:
    st.warning("⚠️ No measures match your current filter criteria. Please adjust the filters in the sidebar.")
    st.stop()

# Main metrics
st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="📊 AVAILABLE MEASURES",
        value=len(df_filtered),
        delta=f"{len(df_filtered)} of {len(df)} total",
        help="Number of measures matching your filter criteria"
    )

with col2:
    avg_reduction = df_filtered['Avg_Reduction'].mean()
    st.metric(
        label="🌍 AVG CARBON REDUCTION",
        value=f"{avg_reduction:.1f}%",
        delta="Potential savings",
        help="Average carbon reduction across all filtered measures"
    )

with col3:
    avg_success = df_filtered['Success_Rate'].mean()
    st.metric(
        label="✅ AVG SUCCESS RATE",
        value=f"{avg_success:.0f}%",
        delta="Proven effectiveness",
        help="Average success rate based on real implementations"
    )

with col4:
    quick_wins = len(df_filtered[df_filtered['ROI_Years_Max'] <= 1])
    st.metric(
        label="⚡ QUICK WINS",
        value=quick_wins,
        delta="Fast ROI",
        help="Measures with ROI period of 1 year or less"
    )

with col5:
    high_impact = len(df_filtered[df_filtered['Avg_Reduction'] >= 50])
    st.metric(
        label="🎯 HIGH IMPACT",
        value=high_impact,
        delta="Major reduction",
        help="Measures achieving ≥50% carbon reduction"
    )

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🔍 Detailed Analysis",
    "💰 Cost vs Impact",
    "📚 Case Studies",
    "🎯 Recommendations"
])

# ========================================
# TAB 1: OVERVIEW
# ========================================
with tab1:
    st.markdown("### 📊 Comprehensive Overview")
    
    # Summary table
    st.markdown("#### All Measures Summary")
    
    summary_df = df_filtered[[
        'Measure_Name',
        'Category',
        'Company_Size',
        'Carbon_Reduction_Min',
        'Carbon_Reduction_Max',
        'Success_Rate',
        'Difficulty_Level',
        'Implementation_Time_Months'
    ]].copy()
    
    summary_df['Carbon Reduction'] = summary_df['Carbon_Reduction_Min'].astype(str) + '-' + \
                                      summary_df['Carbon_Reduction_Max'].astype(str) + '%'
    summary_df['Timeline'] = summary_df['Implementation_Time_Months'].astype(str) + ' months'
    
    display_df = summary_df[[
        'Measure_Name',
        'Category',
        'Company_Size',
        'Carbon Reduction',
        'Success_Rate',
        'Difficulty_Level',
        'Timeline'
    ]].rename(columns={
        'Measure_Name': 'Measure',
        'Company_Size': 'Applicable To',
        'Success_Rate': 'Success Rate (%)',
        'Difficulty_Level': 'Difficulty'
    })
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    st.markdown("")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌿 Carbon Reduction Potential")
        sorted_data = df_filtered.sort_values('Avg_Reduction', ascending=True)
        
        fig_reduction = go.Figure()
        fig_reduction.add_trace(go.Bar(
            y=sorted_data['Measure_Name'],
            x=sorted_data['Avg_Reduction'],
            orientation='h',
            marker=dict(
                color=sorted_data['Avg_Reduction'],
                colorscale='Greens',
                showscale=True,
                colorbar=dict(title="Reduction %")
            ),
            text=sorted_data['Avg_Reduction'].round(1),
            texttemplate='%{text}%',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Reduction: %{x:.1f}%<extra></extra>'
        ))
        
        fig_reduction.update_layout(
            title='Average Carbon Reduction by Measure',
            xaxis_title='Carbon Reduction (%)',
            yaxis_title='',
            height=500,
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=11)
        )
        
        st.plotly_chart(fig_reduction, use_container_width=True)
    
    with col2:
        st.markdown("#### ✅ Success Rate Distribution")
        sorted_success = df_filtered.sort_values('Success_Rate', ascending=True)
        
        fig_success = go.Figure()
        fig_success.add_trace(go.Bar(
            y=sorted_success['Measure_Name'],
            x=sorted_success['Success_Rate'],
            orientation='h',
            marker=dict(
                color=sorted_success['Success_Rate'],
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="Success %")
            ),
            text=sorted_success['Success_Rate'].round(0),
            texttemplate='%{text}%',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Success Rate: %{x}%<extra></extra>'
        ))
        
        fig_success.update_layout(
            title='Success Rate by Measure',
            xaxis_title='Success Rate (%)',
            yaxis_title='',
            height=500,
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(range=[0, 100]),
            font=dict(size=11)
        )
        
        st.plotly_chart(fig_success, use_container_width=True)
    
    st.markdown("")
    
    # Category breakdown
    st.markdown("#### 📂 Distribution Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        category_counts = df_filtered['Category'].value_counts()
        
        fig_category = go.Figure(data=[go.Pie(
            labels=category_counts.index,
            values=category_counts.values,
            hole=0.4,
            marker=dict(colors=px.colors.qualitative.Set3),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig_category.update_layout(
            title='Measures by Category',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        difficulty_counts = df_filtered['Difficulty_Level'].value_counts()
        
        colors = {'Low': '#4CAF50', 'Medium': '#FFC107', 'High': '#F44336'}
        color_list = [colors.get(x, '#999') for x in difficulty_counts.index]
        
        fig_difficulty = go.Figure(data=[go.Pie(
            labels=difficulty_counts.index,
            values=difficulty_counts.values,
            hole=0.4,
            marker=dict(colors=color_list),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig_difficulty.update_layout(
            title='Measures by Difficulty',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig_difficulty, use_container_width=True)

# ========================================
# TAB 2: DETAILED ANALYSIS
# ========================================
with tab2:
    st.markdown("### 🔍 Deep Dive Analysis")
    
    # Measure selection
    selected_measure = st.selectbox(
        "Select a measure to explore in detail:",
        df_filtered['Measure_Name'].tolist(),
        help="Choose any measure to see comprehensive information"
    )
    
    # Get selected measure data
    measure_data = df_filtered[df_filtered['Measure_Name'] == selected_measure].iloc[0]
    
    # Display measure details
    st.markdown(f"## {measure_data['Measure_Name']}")
    
    # Badges
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📂 Category", measure_data['Category'])
    with col2:
        st.metric("🏢 Applicable To", measure_data['Company_Size'])
    with col3:
        difficulty_emoji = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}
        st.metric("⚙️ Difficulty", f"{difficulty_emoji.get(measure_data['Difficulty_Level'], '⚪')} {measure_data['Difficulty_Level']}")
    with col4:
        st.metric("⏱️ Timeline", f"{measure_data['Implementation_Time_Months']} months")
    
    st.markdown("---")
    
    # Description
    st.markdown("#### 📝 What is this measure?")
    st.markdown(f"<div class='custom-card'>{measure_data['Description']}</div>", unsafe_allow_html=True)
    
    st.markdown("")
    
    # Key metrics
    st.markdown("#### 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🌍 Carbon Reduction",
            f"{measure_data['Carbon_Reduction_Min']}-{measure_data['Carbon_Reduction_Max']}%",
            delta=f"Avg: {measure_data['Avg_Reduction']:.1f}%",
            help="Range of carbon reduction achieved"
        )
    
    with col2:
        st.metric(
            "✅ Success Rate",
            f"{measure_data['Success_Rate']}%",
            delta="Industry proven",
            help="Percentage of successful implementations"
        )
    
    with col3:
        roi_display = f"{measure_data['ROI_Years_Min']:.1f}-{measure_data['ROI_Years_Max']:.1f} yrs"
        if measure_data['ROI_Years_Max'] == 0:
            roi_display = "Immediate"
        st.metric(
            "💰 ROI Period",
            roi_display,
            help="Time to return on investment"
        )
    
    with col4:
        cost_display = f"${measure_data['Cost_Min']:,.0f} - ${measure_data['Cost_Max']:,.0f}"
        st.metric(
            "💵 Investment",
            cost_display,
            help="Implementation cost range"
        )
    
    st.markdown("")
    
    # Cost analysis
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 💰 Investment Analysis")
        
        if measure_data['Cost_Max'] < 10000:
            st.success("✅ **Low Investment** - Minimal financial barrier to implementation")
        elif measure_data['Cost_Max'] < 500000:
            st.info("ℹ️ **Moderate Investment** - Manageable for most organizations")
        else:
            st.warning("⚠️ **Significant Investment** - Strategic planning required")
        
        st.caption(f"**Cost Range:** ${measure_data['Cost_Min']:,.0f} - ${measure_data['Cost_Max']:,.0f}")
        st.caption(f"**Average Cost:** ${measure_data['Avg_Cost']:,.0f}")
    
    with col2:
        st.markdown("#### ⏱️ ROI Timeline")
        
        roi_data = pd.DataFrame({
            'Period': ['Minimum ROI', 'Maximum ROI'],
            'Years': [measure_data['ROI_Years_Min'], measure_data['ROI_Years_Max']]
        })
        
        fig_roi = go.Figure()
        fig_roi.add_trace(go.Bar(
            x=roi_data['Period'],
            y=roi_data['Years'],
            marker=dict(
                color=['#4CAF50', '#FFC107'],
                line=dict(color='rgba(255,255,255,0.3)', width=2)
            ),
            text=roi_data['Years'].round(1),
            texttemplate='%{text} yrs',
            textposition='outside'
        ))
        
        fig_roi.update_layout(
            height=300,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title='Years',
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        
        st.plotly_chart(fig_roi, use_container_width=True)
    
    st.markdown("---")
    
    # Proof of effectiveness
    st.markdown("#### ✅ Real-World Validation")
    
    st.markdown(f"""
    <div class='custom-card'>
        <h4 style='margin-top: 0;'>🏢 {measure_data['Case_Study_Company']}</h4>
        <p style='font-size: 1.05rem; line-height: 1.7;'>{measure_data['Case_Study_Result']}</p>
        <p style='margin-bottom: 0; opacity: 0.8;'><strong>📚 Source:</strong> {measure_data['Case_Study_Source']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Impact visualization
    impact_data = pd.DataFrame({
        'Metric': ['Min Reduction', 'Max Reduction', 'Success Rate'],
        'Value': [
            measure_data['Carbon_Reduction_Min'],
            measure_data['Carbon_Reduction_Max'],
            measure_data['Success_Rate']
        ]
    })
    
    fig_impact = go.Figure()
    fig_impact.add_trace(go.Bar(
        x=impact_data['Metric'],
        y=impact_data['Value'],
        marker=dict(
            color=['#66BB6A', '#4CAF50', '#2E7D32'],
            line=dict(color='rgba(255,255,255,0.3)', width=2)
        ),
        text=impact_data['Value'].round(1),
        texttemplate='%{text}%',
        textposition='outside'
    ))
    
    fig_impact.update_layout(
        title='Impact Metrics Overview',
        yaxis_title='Percentage (%)',
        height=400,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    st.plotly_chart(fig_impact, use_container_width=True)

# ========================================
# TAB 3: COST VS IMPACT
# ========================================
with tab3:
    st.markdown("### 💰 Value Analysis")
    
    st.markdown("#### Cost vs Carbon Reduction Impact")
    
    st.info("💡 **Reading Guide:** Larger bubbles indicate higher success rates. Look for measures in the top-left area (high impact, lower cost) for best value.")
    
    # Scatter plot
    fig_scatter = go.Figure()
    
    for category in df_filtered['Category'].unique():
        cat_data = df_filtered[df_filtered['Category'] == category]
        
        fig_scatter.add_trace(go.Scatter(
            x=cat_data['Avg_Cost'],
            y=cat_data['Avg_Reduction'],
            mode='markers',
            name=category,
            marker=dict(
                size=cat_data['Success_Rate'] / 3,
                opacity=0.7,
                line=dict(width=2, color='white')
            ),
            text=cat_data['Measure_Name'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Cost: $%{x:,.0f}<br>' +
                         'Reduction: %{y:.1f}%<br>' +
                         '<extra></extra>'
        ))
    
    fig_scatter.update_layout(
        title='Investment Cost vs Carbon Reduction Potential',
        xaxis=dict(
            title='Average Cost ($ - Log Scale)',
            type='log',
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            title='Average Carbon Reduction (%)',
            gridcolor='rgba(128,128,128,0.2)'
        ),
        height=600,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='closest'
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # ROI and Timeline comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⏱️ ROI Timeline Comparison")
        
        sorted_roi = df_filtered.sort_values('Avg_ROI')
        
        colors_roi = sorted_roi['Difficulty_Level'].map({
            'Low': '#4CAF50',
            'Medium': '#FFC107',
            'High': '#F44336'
        })
        
        fig_roi_compare = go.Figure()
        fig_roi_compare.add_trace(go.Bar(
            x=sorted_roi['Measure_Name'],
            y=sorted_roi['Avg_ROI'],
            marker=dict(color=colors_roi, line=dict(color='rgba(255,255,255,0.3)', width=1)),
            text=sorted_roi['Avg_ROI'].round(1),
            texttemplate='%{text}y',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>ROI: %{y:.1f} years<extra></extra>'
        ))
        
        fig_roi_compare.update_layout(
            yaxis_title='Years to ROI',
            height=450,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45,
            showlegend=False,
            margin=dict(b=100)
        )
        
        st.plotly_chart(fig_roi_compare, use_container_width=True)
    
    with col2:
        st.markdown("#### 📅 Implementation Timeline")
        
        sorted_time = df_filtered.sort_values('Implementation_Time_Months')
        
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Bar(
            x=sorted_time['Measure_Name'],
            y=sorted_time['Implementation_Time_Months'],
            marker=dict(
                color=sorted_time['Implementation_Time_Months'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Months"),
                line=dict(color='rgba(255,255,255,0.3)', width=1)
            ),
            text=sorted_time['Implementation_Time_Months'],
            texttemplate='%{text}m',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Timeline: %{y} months<extra></extra>'
        ))
        
        fig_timeline.update_layout(
            yaxis_title='Months to Implement',
            height=450,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45,
            showlegend=False,
            margin=dict(b=100)
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.markdown("---")
    
    # Quick wins
    st.markdown("#### 🎯 Quick Wins (ROI ≤ 1 Year)")
    
    quick_wins_df = df_filtered[df_filtered['ROI_Years_Max'] <= 1]
    
    if not quick_wins_df.empty:
        quick_display = quick_wins_df[[
            'Measure_Name',
            'Avg_Reduction',
            'Avg_Cost',
            'Success_Rate',
            'Implementation_Time_Months'
        ]].copy()
        
        quick_display.columns = ['Measure', 'Avg Reduction (%)', 'Avg Cost ($)', 'Success Rate (%)', 'Timeline (months)']
        quick_display = quick_display.sort_values('Avg Reduction (%)', ascending=False)
        
        st.dataframe(
            quick_display.style.format({
                'Avg Reduction (%)': '{:.1f}',
                'Avg Cost ($)': '${:,.0f}',
                'Success Rate (%)': '{:.0f}'
            }).background_gradient(subset=['Avg Reduction (%)'], cmap='Greens'),
            use_container_width=True
        )
        
        st.success(f"✅ **{len(quick_wins_df)} Quick Win(s) Available** - These measures offer immediate to 1-year ROI, perfect for building momentum!")
    else:
        st.info("No quick win measures match your current filters. Try adjusting the ROI period filter.")
    
    st.markdown("")
    
    # Best value
    st.markdown("#### 💎 Best Value Propositions")
    
    best_value_df = df_filtered[
        (df_filtered['Avg_Reduction'] >= 40) & 
        (df_filtered['ROI_Years_Max'] <= 3)
    ]
    
    if not best_value_df.empty:
        best_value_display = best_value_df[[
            'Measure_Name',
            'Avg_Reduction',
            'Avg_ROI',
            'Success_Rate'
        ]].copy()
        
        best_value_display.columns = ['Measure', 'Avg Reduction (%)', 'Avg ROI (years)', 'Success Rate (%)']
        best_value_display = best_value_display.sort_values('Avg Reduction (%)', ascending=False)
        
        st.dataframe(
            best_value_display.style.format({
                'Avg Reduction (%)': '{:.1f}',
                'Avg ROI (years)': '{:.1f}',
                'Success Rate (%)': '{:.0f}'
            }).background_gradient(subset=['Avg Reduction (%)'], cmap='RdYlGn'),
            use_container_width=True
        )
        
        st.success(f"💎 **{len(best_value_df)} High-Value Measure(s)** - Combining significant impact (≥40% reduction) with reasonable ROI (≤3 years)")
    else:
        st.info("No best value measures with current filters. Adjust criteria to see more options.")

# ========================================
# TAB 4: CASE STUDIES
# ========================================
with tab4:
    st.markdown("### 📚 Real-World Success Stories")
    
    st.info("🔍 **Evidence-Based Approach:** Every measure is backed by verified case studies from leading tech companies. All data sourced from official sustainability reports and public disclosures.")
    
    st.markdown("---")
    
    # Group by category
    for category in sorted(df_filtered['Category'].unique()):
        st.markdown(f"### 📁 {category}")
        
        category_measures = df_filtered[df_filtered['Category'] == category]
        
        for idx, row in category_measures.iterrows():
            with st.expander(f"**{row['Measure_Name']}** — Case Study: {row['Case_Study_Company']}", expanded=False):
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"#### 🏢 {row['Case_Study_Company']}")
                    
                    st.markdown("**📊 Results Achieved**")
                    st.success(row['Case_Study_Result'])
                    
                    st.markdown("**📚 Verified Source**")
                    st.caption(row['Case_Study_Source'])
                    
                    st.markdown("---")
                    
                    st.markdown("**📝 About This Measure**")
                    st.write(row['Description'])
                
                with col2:
                    st.markdown("**Key Metrics**")
                    
                    # Carbon reduction
                    st.metric(
                        "🌍 Carbon Reduction",
                        f"{row['Carbon_Reduction_Min']}-{row['Carbon_Reduction_Max']}%"
                    )
                    
                    # Success rate with progress
                    st.metric("✅ Success Rate", f"{row['Success_Rate']}%")
                    st.progress(row['Success_Rate'] / 100)
                    
                    # ROI
                    if row['ROI_Years_Max'] == 0:
                        roi_text = "Immediate"
                    else:
                        roi_text = f"{row['ROI_Years_Min']:.1f}-{row['ROI_Years_Max']:.1f} yrs"
                    st.metric("💰 ROI Period", roi_text)
                    
                    # Timeline
                    st.metric("⏱️ Timeline", f"{row['Implementation_Time_Months']} months")
                    
                    # Difficulty
                    difficulty_colors = {
                        'Low': '🟢',
                        'Medium': '🟡',
                        'High': '🔴'
                    }
                    st.metric("⚙️ Difficulty", f"{difficulty_colors.get(row['Difficulty_Level'], '⚪')} {row['Difficulty_Level']}")
                    
                    # Cost
                    st.metric(
                        "💵 Cost Range",
                        f"${row['Cost_Min']:,.0f}-${row['Cost_Max']:,.0f}"
                    )
        
        st.markdown("---")
    
    # Summary statistics
    st.markdown("### 📈 Evidence Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 Total Case Studies",
            len(df_filtered),
            help="Number of documented real-world implementations"
        )
    
    with col2:
        avg_success = df_filtered['Success_Rate'].mean()
        st.metric(
            "✅ Avg Success Rate",
            f"{avg_success:.0f}%",
            help="Average success rate across all measures"
        )
    
    with col3:
        high_success = len(df_filtered[df_filtered['Success_Rate'] >= 85])
        st.metric(
            "🌟 High Confidence",
            high_success,
            delta="≥85% success",
            help="Measures with very high success rates"
        )
    
    with col4:
        companies_count = len(df_filtered['Case_Study_Company'].unique())
        st.metric(
            "🏢 Companies",
            companies_count,
            help="Number of unique companies featured"
        )
    
    st.markdown("")
    
    # Companies list
    st.markdown("#### 🏢 Featured Companies")
    companies = sorted(df_filtered['Case_Study_Company'].unique())
    st.write(", ".join(companies))

# ========================================
# TAB 5: RECOMMENDATIONS
# ========================================
with tab5:
    st.markdown("### 🎯 Personalized Recommendations")
    
    if len(df_filtered) == 0:
        st.warning("⚠️ No measures match your current filters. Please adjust filter criteria in the sidebar.")
    else:
        # Top recommendations
        st.markdown("#### 🏆 Top 3 Recommended Measures")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            best_impact = df_filtered.loc[df_filtered['Avg_Reduction'].idxmax()]
            st.markdown(f"""
            <div class='custom-card'>
                <h4 class='gradient-text'>🥇 Highest Impact</h4>
                <h3>{best_impact['Measure_Name']}</h3>
                <p><strong>Carbon Reduction:</strong> {best_impact['Avg_Reduction']:.1f}%</p>
                <p><strong>Success Rate:</strong> {best_impact['Success_Rate']}%</p>
                <p><strong>Category:</strong> {best_impact['Category']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            best_roi = df_filtered.loc[df_filtered['Avg_ROI'].idxmin()]
            roi_text = "Immediate" if best_roi['Avg_ROI'] == 0 else f"{best_roi['Avg_ROI']:.1f} years"
            st.markdown(f"""
            <div class='custom-card'>
                <h4 class='gradient-text'>🥈 Fastest ROI</h4>
                <h3>{best_roi['Measure_Name']}</h3>
                <p><strong>ROI Period:</strong> {roi_text}</p>
                <p><strong>Reduction:</strong> {best_roi['Avg_Reduction']:.1f}%</p>
                <p><strong>Category:</strong> {best_roi['Category']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            most_proven = df_filtered.loc[df_filtered['Success_Rate'].idxmax()]
            st.markdown(f"""
            <div class='custom-card'>
                <h4 class='gradient-text'>🥉 Most Proven</h4>
                <h3>{most_proven['Measure_Name']}</h3>
                <p><strong>Success Rate:</strong> {most_proven['Success_Rate']}%</p>
                <p><strong>Reduction:</strong> {most_proven['Avg_Reduction']:.1f}%</p>
                <p><strong>Category:</strong> {most_proven['Category']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Implementation roadmap
        st.markdown("#### 🗺️ Suggested Implementation Roadmap")
        
        # Phase 1
        phase1 = df_filtered[df_filtered['ROI_Years_Max'] <= 1].sort_values('Avg_Reduction', ascending=False)
        if not phase1.empty:
            st.success("**Phase 1: Quick Wins (0-6 months)** - Build momentum with fast ROI")
            for idx, row in phase1.iterrows():
                st.write(f"✅ **{row['Measure_Name']}** → {row['Avg_Reduction']:.1f}% reduction, {row['Implementation_Time_Months']} months")
            st.markdown("")
        
        # Phase 2
        phase2 = df_filtered[
            (df_filtered['ROI_Years_Max'] > 1) & 
            (df_filtered['ROI_Years_Max'] <= 3)
        ].sort_values('Avg_Reduction', ascending=False)
        if not phase2.empty:
            st.info("**Phase 2: Medium-Term (6-18 months)** - Scale impact with proven strategies")
            for idx, row in phase2.iterrows():
                st.write(f"⚙️ **{row['Measure_Name']}** → {row['Avg_Reduction']:.1f}% reduction, {row['Avg_ROI']:.1f}y ROI")
            st.markdown("")
        
        # Phase 3
        phase3 = df_filtered[df_filtered['ROI_Years_Max'] > 3].sort_values('Avg_Reduction', ascending=False)
        if not phase3.empty:
            st.warning("**Phase 3: Strategic (18+ months)** - Transform with major initiatives")
            for idx, row in phase3.iterrows():
                st.write(f"🎯 **{row['Measure_Name']}** → {row['Avg_Reduction']:.1f}% reduction, {row['Avg_ROI']:.1f}y ROI")
        
        st.markdown("---")
        
        # Budget-based recommendations
        st.markdown("#### 💰 Budget-Based Recommendations")
        
        budget_option = st.selectbox(
            "Select your available budget:",
            ["Under $50,000", "$50,000 - $500,000", "$500,000 - $5,000,000", "Over $5,000,000"]
        )
        
        if budget_option == "Under $50,000":
            budget_measures = df_filtered[df_filtered['Cost_Max'] <= 50000]
        elif budget_option == "$50,000 - $500,000":
            budget_measures = df_filtered[(df_filtered['Cost_Min'] >= 50000) & (df_filtered['Cost_Max'] <= 500000)]
        elif budget_option == "$500,000 - $5,000,000":
            budget_measures = df_filtered[(df_filtered['Cost_Min'] >= 500000) & (df_filtered['Cost_Max'] <= 5000000)]
        else:
            budget_measures = df_filtered[df_filtered['Cost_Min'] >= 5000000]
        
        if not budget_measures.empty:
            st.write(f"**{len(budget_measures)} measure(s) available within your budget:**")
            
            budget_display = budget_measures[[
                'Measure_Name',
                'Avg_Reduction',
                'Avg_Cost',
                'Avg_ROI',
                'Success_Rate'
            ]].sort_values('Avg_Reduction', ascending=False)
            
            budget_display.columns = ['Measure', 'Reduction (%)', 'Avg Cost ($)', 'ROI (years)', 'Success Rate (%)']
            
            st.dataframe(
                budget_display.style.format({
                    'Reduction (%)': '{:.1f}',
                    'Avg Cost ($)': '${:,.0f}',
                    'ROI (years)': '{:.1f}',
                    'Success Rate (%)': '{:.0f}'
                }).background_gradient(subset=['Reduction (%)'], cmap='Greens'),
                use_container_width=True
            )
            
            total_reduction = budget_measures['Avg_Reduction'].sum()
            st.success(f"💡 **Combined Impact:** {total_reduction:.1f}% total reduction if all measures implemented")
        else:
            st.info("No measures available within selected budget. Try adjusting your budget range or filters.")
        
        st.markdown("---")
        
        # Category focus
        st.markdown("#### 📊 Recommendations by Focus Area")
        
        for category in sorted(df_filtered['Category'].unique()):
            with st.expander(f"**{category}** ({len(df_filtered[df_filtered['Category'] == category])} measures)"):
                cat_measures = df_filtered[df_filtered['Category'] == category].sort_values('Avg_Reduction', ascending=False)
                
                for idx, row in cat_measures.iterrows():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{row['Measure_Name']}**")
                    with col2:
                        st.write(f"🌍 {row['Avg_Reduction']:.1f}%")
                    with col3:
                        st.write(f"✅ {row['Success_Rate']}%")
                    with col4:
                        roi_txt = "Now" if row['Avg_ROI'] == 0 else f"{row['Avg_ROI']:.1f}y"
                        st.write(f"💰 {roi_txt}")
                    
                    st.markdown("---")

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("### 📌 Implementation Guide")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **💡 Best Practices:**
    - Start with 2-3 Quick Wins to demonstrate value
    - Combine complementary measures for synergy
    - Set clear KPIs and track progress monthly
    - Learn from documented case studies
    - Iterate based on real results
    - Engage stakeholders early and often
    """)

with col2:
    st.success("""
    **✅ Critical Success Factors:**
    - Strong executive sponsorship
    - Accurate baseline carbon measurement
    - Realistic implementation timelines
    - Cross-functional team collaboration
    - Regular progress reviews
    - Celebrate and communicate wins
    """)

st.markdown("---")

# Final info
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("📊 **Data Sources**")
    st.caption("Corporate sustainability reports, verified industry studies, peer-reviewed research (2018-2023)")

with col2:
    st.caption("🔄 **Last Updated**")
    st.caption("2024 | Data compiled from publicly available authoritative sources")

with col3:
    st.caption("⚠️ **Disclaimer**")
    st.caption("Results vary by context. Conduct detailed feasibility analysis before implementation.")

st.markdown("---")
st.markdown("<p style='text-align: center; opacity: 0.6;'>Made with 🌱 for a sustainable future</p>", unsafe_allow_html=True)