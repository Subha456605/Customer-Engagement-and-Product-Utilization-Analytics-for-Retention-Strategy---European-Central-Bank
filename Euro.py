import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
st.set_page_config(layout="wide")
st.markdown("""
<style>
/* 🔹 Main page background */
.stApp {
    background-color: #111827;
}

/* 🔹 Main title (st.title) */
.block-container  {
    padding-top: 80px;
    }
h1 {
    background: linear-gradient(90deg, #ff00cc, #3333ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
        text-align: center;
}

/* 🔹 Section titles (st.subheader) */
h2, h3 {
    color: #60a5fa !important;
}

/* 🔹 Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

/* 🔹 Sidebar title */
section[data-testid="stSidebar"] h1 {
    color: #7fff00 !important;
}

/* 🔹 Sidebar labels */
section[data-testid="stSidebar"] label {
    color: #60a5fa !important;
    font-weight: 500;
}

/* 🔹 Sidebar inputs text */
section[data-testid="stSidebar"] .stSelectbox div,
section[data-testid="stSidebar"] .stDateInput div,
section[data-testid="stSidebar"] .stMultiSelect div {
    color: #60a5fa !important;
}
/* 🔹 General text */
body, p, span {
    color: #e5e7eb;
}

</style>
""", unsafe_allow_html=True)
st.title("Customer Engagement & Product Utilization Analytics for Retention Strategy - European Bank")
df=pd.read_csv("European_Bank PI.csv")
Churned_Customers=((df["Exited"]==1) & (df["NumOfProducts"]>1)).sum()

df["Product Type"]=np.where(df["NumOfProducts"]>1, "Multi Product", "Single Product")
filtered_df=df.copy()
#sidebar filters 

st.sidebar.image("logo_only.svg", width=300)
Customer_Id = st.sidebar.multiselect(
    "Choose Customer ID",
    df["CustomerId"].unique()
)
if Customer_Id:
    filtered_df = filtered_df[
        filtered_df["CustomerId"].isin(Customer_Id)
    ]

Age_Range=st.sidebar.slider("Select Age", 18, 92, (18, 92))
filtered_df=filtered_df[(filtered_df["Age"]>=Age_Range[0]) & (filtered_df["Age"]<=Age_Range[1])]

Gender=st.sidebar.multiselect("Choose Gender", df["Gender"].unique())
if Gender:
    filtered_df = filtered_df[filtered_df["Gender"].isin(Gender)]

location=st.sidebar.multiselect("Choose Geography", df["Geography"].unique())
if location:
    filtered_df = filtered_df[
        filtered_df["Geography"].isin(location)
    ]

Tenure_Range=st.sidebar.slider("Select Tenure", 0, 10, (0, 10))
filtered_df=filtered_df[(filtered_df["Tenure"]>=Tenure_Range[0]) & (filtered_df["Tenure"]<=Tenure_Range[1])]

product_type=st.sidebar.multiselect("Choose Product Type", df["Product Type"].unique())
if product_type:
    filtered_df = filtered_df[
        filtered_df["Product Type"].isin(product_type)
    ]
    
# KPI calculations
Active_Customer=(filtered_df["IsActiveMember"]==1).sum()
Inactive_Customer=(filtered_df["IsActiveMember"]==0).sum()
Active_lowproduct_customers=len(filtered_df[(filtered_df["IsActiveMember"]==1) & (filtered_df["NumOfProducts"]<=2)])
avg_balance=filtered_df["Balance"].mean()
InActive_highbalance_customers=len(filtered_df[(filtered_df["IsActiveMember"]==0) & (filtered_df["Balance"]>avg_balance)])
Churned_Customers=(filtered_df["Exited"]==1).sum()
Retained_Customers=(filtered_df["Exited"]==0).sum()
Retaintion_Rate=Retained_Customers/len(filtered_df)*100
Churn_Rate=Churned_Customers/len(filtered_df)*100
if len(filtered_df) > 0:
    Churn_Rate = Churned_Customers / len(filtered_df) * 100
else:
    Churn_Rate = 0
Credit_Card_Users=(filtered_df["HasCrCard"]==1).sum()
Normal_Customers=(filtered_df["Sticky Customer"]=="Normal Customer").sum()
Normal_Customers_Percentage=Normal_Customers/len(filtered_df)*100
Premium_Customers=(filtered_df["Premium/Regular"]=="Premium").sum()
Regular_Customers=(filtered_df["Premium/Regular"]=="Regular").sum()
Sticky_Customers=(filtered_df["Sticky Customer"]=="Sticky Customer").sum()
Sticky_Customers_Percentage=Sticky_Customers/len(filtered_df)*100
Total_Customers=len(filtered_df)
Zero_Balance_Customers=(filtered_df["Balance"]==0).sum()

# Retention rate by product type
retention_df = (
    filtered_df.groupby("Product Type")
    .agg(
        Total_Customers=("CustomerId", "count"),
        Retained_Customers=("Exited", lambda x: (x == 0).sum())
    )
    .reset_index()
)

retention_df["Retention Rate"] = (
    retention_df["Retained_Customers"]
    / retention_df["Total_Customers"]
) * 100




# KPI card function
def kpi_card(title, value, icon=None, is_positive=True):
    # gradient colors
    if is_positive:
        gradient = "linear-gradient(135deg, #7c3aed, #a78bfa)"
    else:
        gradient = "linear-gradient(135deg, #ef4444, #f87171)"

    arrow = "↑" if is_positive else "↓"

    st.markdown(f"""
     <div style="
        width:100%;
        background:{gradient};
        padding:15px;
        border-radius:12px;
        color:white;
        margin-bottom:20px;
        ">
        <div style="font-size:17px; font-weight:500;margin-bottom:4px;">
            {title}
        </div>

        <div style="font-size:15px; font-weight:bold; margin-top:4px;">
            {value} {arrow}
        </div>
     </div>
     """, unsafe_allow_html=True)
def kpi_card1(title, value, icon=None, is_positive=True):
    # gradient colors
    if is_positive:
        gradient = "linear-gradient(135deg, #7c3aed, #a78bfa)"
    else:
        gradient = "linear-gradient(135deg, #ef4444, #f87171)"

    arrow = "↑" if is_positive else "↓"

    st.markdown(f"""
     <div style="
        width:100%;
        background:{gradient};
        padding:15px;
        border-radius:12px;
        color:white;
        margin-bottom:20px;
        ">
        <div style="font-size:25px; font-weight:500;margin-bottom:4px;">
            {title}
        </div>

        <div style="font-size:22px; font-weight:bold; margin-top:4px;">
            {value} {arrow}
        </div>
     </div>
     """, unsafe_allow_html=True)
    
def kpi_card2(title, value, icon=None):
    st.markdown(f"""
     <div style="
        width:300px;
        height:170px;
        background:white;
        padding:20px;
        border-radius:20px;
        color:white;
        margin-top:5px;
        margin-bottom:20px;
        text-align:center;
        ">
        <div style="font-size:35px; font-weight:bold;color:black; margin-bottom:6px;">
            {title}
        </div>

        <div style="font-size:35px; font-weight:bold;color:green; margin-top:4px;">
            {value}
        </div>
     </div>
     """, unsafe_allow_html=True)
col1,col2,col3,col4=st.columns(4)
with col1:
    kpi_card1("Total Customers",Total_Customers,icon="👥", is_positive=True)

with col2:
    kpi_card1("Active Customers",Active_Customer,icon="📈", is_positive=True)

with col3:
    kpi_card1("Inactive Customers",Inactive_Customer,icon="📉", is_positive=False)

with col4:
    kpi_card1("Churned Customers", Churned_Customers, icon="⚠️", is_positive=False)


tab1,tab2,tab3=st.tabs(["Product Utilization"," Financial Commitment vs Engagement Analysis","Churn Analysis"])
with tab1:
    st.subheader("Product Utilization Analysis")

    col1, col2 = st.columns(2)
    with col1:
        kpi_card(
            "Total Customers",
            Total_Customers,
            icon="👥",
            is_positive=True
        )

    with col2:
        kpi_card(
            "Churn Rate",
            f"{Churn_Rate:.2f}%",
            icon="⚠️",
            is_positive=False
        )
    st.subheader("Analyze Retention Rate by Product Type, Tenure, and Churn Rate by Number of Products")
    col1,col2,col3=st.columns(3)
    with col1:
        fig=px.bar(
            retention_df,
            x="Product Type",
            y="Retention Rate",
            color="Product Type",
            title="Retention Rate",
            text_auto=".2f%",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(showlegend=False, title_font_size=23,title_x=0.2,height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    tenure_products = (
    filtered_df.groupby("Tenure Group")["NumOfProducts"]
    .sum()
    .reset_index()
    )
    
    with col2:
        fig = px.bar(
        tenure_products,
        x="Tenure Group",
        y="NumOfProducts",
        title="No of usage product",
        labels={
        "Tenure Group": "Tenure Group",
        "NumOfProducts": "Total Products Used"
        }
        )
        fig.update_layout(title_font_size=23, title_x=0.2, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
    churn_df = (
    filtered_df.groupby("NumOfProducts").agg(Total_Customers=("Exited", "count"),
    Churned_Customers=("Exited", lambda x: (x == 1).sum())).reset_index())
    churn_df["Churn Rate"] = (churn_df["Churned_Customers"]/ churn_df["Total_Customers"]) * 100
    with col3:
        fig = px.bar(
        churn_df,
        x="NumOfProducts",
        y="Churn Rate",
        text="Churn Rate",
        title="Churn Rate by No ofProducts"
        )
        fig.update_layout(title_font_size=23, title_x=0.1, height=400)
        st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        ### 📌 Notes

        - **Multi-Product Customers:** Customers holding 2 or more banking products.
        - **Long-Term Customers:** Customers with a tenure of 6 years or more with the bank.
        - **Analysis Period:** Based on the 2025 customer dataset.
        - **Churned Customers:** Customers who have exited the bank's services.
        - **Retained Customers:** Customers who remain active with the bank.
        """)
    with col2:
        st.info("""
        ### 💡 Key Insights

        • Single-product customers exhibit a higher churn rate compared to multi-product customers.

        • Long-term customers (6+ years tenure) tend to use more banking products, indicating stronger customer engagement and loyalty.
        """)
   
with tab2:
    col1,col2,col3=st.columns(3)
    with col1:
        kpi_card("Credit Card Users", Credit_Card_Users, icon="💳", is_positive=True)
    with col2:
        kpi_card("Premium Customers", Premium_Customers, icon="🌟", is_positive=True)
    with col3:
        kpi_card("Sticky Customers", Sticky_Customers, icon="🔒", is_positive=True)
    col1,col2,col3=st.columns(3)
    with col1:
        max_score = filtered_df["CreditScore"].max()
        rating = (
        "Excellent" if max_score >= 800 else
        "Very Good" if max_score >= 740 else
        "Good" if max_score >= 670 else
        "Fair" if max_score >= 580 else
        "Poor"
        )
        
        kpi_card2("Credit Score", f"{filtered_df['CreditScore'].max()} ({rating})", icon="📊")
        
    with col2:
        account_df = (
        filtered_df.groupby("Account Status").size().reset_index(name="Customer Count"))
        
        fig=px.pie(
            account_df,
            names="Account Status",
            values="Customer Count",
            title="Salary Balance Mismatch Detection",
            labels={"Customer Count": "Number of Customers", "Account Status": "Account Status"},
            color="Account Status",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            title_x=0.1,title_font_size=18, height=300,width=300, margin=dict(t=60, b=20, l=20, r=20),legend=dict(
            orientation="v",
            y=0.5,
            yanchor="middle",
            x=1.02,
            xanchor="left"
        ))
                           
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        tenure_df=filtered_df.groupby("Tenure 1").size().reset_index(name="Customer Count")
        fig=px.bar(
            tenure_df,
            x="Tenure 1",
            y="Customer Count",
            title="Customer Distribution by Tenure",
            labels={"Tenure 1": "Tenure (Years)", "Customer Count": "Number of Customers"},
            color="Tenure 1",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(title_x=0.1, height=300,width=300, margin=dict(t=60, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)
with tab3:
    corr_matrix = df[
    ["CreditScore","Age","Exited","NumOfProducts","Balance"]].corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale=[
        "#f8fafc",  
        "#566941",   
        "#94af55"    
        ],
        title="Correlation Heatmap"
    )
    fig.update_layout(
    paper_bgcolor="#e0f2fe",   
    plot_bgcolor="#e0f2fe")
    fig.update_traces(
    textfont=dict(
        color="black",
        size=9
    )
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
        tickfont=dict(
            color="black",
            size=15
        )
    ),
    xaxis=dict(
        tickfont=dict(color="black", size=12)
    ),
    yaxis=dict(
        tickfont=dict(color="black", size=12)
    ),
     title={
        "text": "Correlation Heatmap",
        "x": 0.35,
        "font": {
            "size": 25,
            "color": "#1e3a8a"
        }
    }
    )
    st.plotly_chart(fig, width="stretch")
