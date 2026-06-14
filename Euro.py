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
    background-color: white;
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
    color: black !important;
}

/*tab titles*/
button[data-baseweb="tab"] {
    background-color: white !important;
    font-weight: bold;
    color: black !important;
    font-size: 20px;
}
/* 🔹 Sidebar background */
section[data-testid="stSidebar"] {
    background-color: white !important;
}

/* 🔹 Sidebar title */
section[data-testid="stSidebar"] h1 {
    color: black !important;
}

/* 🔹 Sidebar labels */
section[data-testid="stSidebar"] label {
    color: black !important;
    font-weight: 500;
}

/* 🔹 Sidebar inputs text */
section[data-testid="stSidebar"] .stSelectbox div,
section[data-testid="stSidebar"] .stDateInput div,
section[data-testid="stSidebar"] .stMultiSelect div {
    color: blacks !important;
}
/* 🔹 General text */
body, p, span {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)
st.title("Customer Engagement & Product Utilization Analytics for Retention Strategy - European Bank")
df=pd.read_csv("European_Bank.csv")
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
Total_Customers_France=(filtered_df["Geography"]=="France").sum()
Total_Customers_Spain=(filtered_df["Geography"]=="Spain").sum()
Total_Customers_Germany=(filtered_df["Geography"]=="Germany").sum()
single_product_customers=(filtered_df["NumOfProducts"]==1).sum()
multi_product_customers=(filtered_df["NumOfProducts"]>1).sum()
Zero_Balance_Customers=(filtered_df["Balance"]==0).sum()
df["AgeGroup"]=pd.cut(df["Age"], bins=[17, 30, 45, 60, 100], labels=["18-30", "31-45", "46-60", "61+"])
filtered_df["AgeGroup"]=pd.cut(filtered_df["Age"], bins=[17, 30, 45, 60, 100], labels=["18-30", "31-45", "46-60", "61+"])
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
retention_df["Retention Rate"] = retention_df["Retention Rate"].round(2)



# KPI card function
def kpi_card(title, value, icon=None, is_positive=True):

    st.markdown(f"""
     <div style="
        width:100%;
        background:blue;
        padding:15px;
        border-radius:12px;
        color:white;
        margin-bottom:20px;
        ">
        <div style="font-size:17px; font-weight:bold;margin-bottom:4px;">
           {icon if icon else ""} {title}
        </div>

        <div style="font-size:20px; font-weight:bold; margin-top:4px;">
            {value} 
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
           {icon if icon else ""} {title}
        </div>

        <div style="font-size:22px; font-weight:bold; margin-top:4px;">
            {value} {arrow}
        </div>
     </div>
     """, unsafe_allow_html=True)
    
def kpi_card2(title, value, icon=None):
    st.markdown(f"""
     <div style="
        width:350px;
        height:200px;
        background:white;
        padding:20px;
        border-radius:20px;
        color:black;
        margin-top:5px;
        margin-bottom:25px;
        text-align:center;
        ">
        <div style="font-size:35px; font-weight:bold;color:black; margin-bottom:6px;background:yellow; padding:10px; border-radius:10px;">
           {icon if icon else ""} {title}
        </div>

        <div style="font-size:40px; font-weight:bold;color:black; margin-top:4px;background:lightgray; padding:10px; border-radius:10px;">
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


tab1,tab2=st.tabs(["Dashboard","Data Description"])
with tab1:
    st.subheader("Retention Analysis")
    col1,col2,col3=st.columns(3,gap="medium")
    with col1:
        kpi_card(
        "Retained Customers",
        Retained_Customers,
        icon="✅"
     )
        kpi_card(
            "Average Retention Rate",
            f"{Retaintion_Rate:.2f}%",
            icon="📊"
        )
    with col2:
        fig=px.bar(
                retention_df,
                x="Product Type",
                y="Retention Rate",
                color="Product Type",
                title="Retention Rate",
                labels={"Product Type": "Product Type", "Retention Rate": "Retention Rate (%)"},
                color_discrete_map={
                    "Multi Product": "#31b86e",
                    "Single Product": "#391dd4"}
                
            )
        fig.update_layout( title_font_size=20,title_x=0.1,height=400
            )
        fig.update_xaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
        fig.update_yaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
            
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        tenure_retention_df = (
        filtered_df.groupby("Tenure Group").agg(
        Total_Customers=("CustomerId", "count"),
        Retained_Customers=("Exited", lambda x: (x == 0).sum())
        ).reset_index()
        )
        tenure_retention_df["Retention Rate"] = (tenure_retention_df["Retained_Customers"] / tenure_retention_df["Total_Customers"]) * 100
        tenure_retention_df["Retention Rate"] = tenure_retention_df["Retention Rate"].round(2)
        
        fig = px.pie(
        tenure_retention_df,
        values="Retention Rate",
        names="Tenure Group",
        hole=0.4,
        title="Retention Rate by Tenure Group",
        labels={"Tenure Group": "Tenure Group", "Retention Rate": "Retention Rate (%)"},
        color="Tenure Group",
        color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(title_font_size=20, title_x=0.1, height=400,legend_title_font_color="black",legend_title_font_size=16)
        fig.update_xaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
        fig.update_yaxes(showgrid=False,title_font_size=16,title_font_color="black",    tickfont_size=14,tickfont_color="black")
        fig.update_traces(textposition="outside", textinfo="value",texttemplate="%{value:.2f}%", textfont_size=14, textfont_color="black")
        st.plotly_chart(fig, use_container_width=True)
        
        
    st.subheader("Product Utilization Analysis")
    col1,col2,col3=st.columns(3,gap="medium")
    with col1:
        kpi_card(
            "Single Product Customers",
            single_product_customers,
            icon="📦",
            is_positive=True
        )
        kpi_card(
            "Multi Product Customers",
            multi_product_customers,
            icon="📦",
            is_positive=True
        )
    
    with col2:
        tenure_products = (
        filtered_df.groupby("Tenure Group")["NumOfProducts"].sum().reset_index())
        fig = px.bar(
        tenure_products,
        x="Tenure Group",
        y="NumOfProducts",
        title="No of usage product",
        labels={
        "Tenure Group": "Tenure Group",
        "NumOfProducts": "Total Products Used"
        },
        color="Tenure Group"
        )
        fig.update_layout(title_font_size=23, title_x=0.2, height=400,legend_title_font_color="black",legend_title_font_size=16)
        fig.update_xaxes(showgrid=False,showticklabels=False,title_font_color="black")
        fig.update_yaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        age_product_df = (
        filtered_df.groupby("AgeGroup")["NumOfProducts"].sum().reset_index())
        fig = px.bar(
        age_product_df,
        x="AgeGroup",
        y="NumOfProducts",
        title="No of usage product by Age Group",
        labels={"AgeGroup": "Age Group", "NumOfProducts": "Total Products Used"},
        color="AgeGroup")
        fig.update_layout(title_font_size=23, title_x=0.2, height=400,legend_title_font_color="black",legend_title_font_size=16)
        fig.update_xaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
        fig.update_yaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Churn Analysis")
    col1, col2,col3 = st.columns(3,gap="medium")
    with col1:
        kpi_card(
            "Churned Customers",
            Churned_Customers,
            icon="⚠️",
            is_positive=False
        )
        kpi_card(
            "Average Churn Rate",
            f"{Churn_Rate:.2f}%",
            icon="📊",
            is_positive=False
        )
    with col2:
        churn_df = (
        filtered_df.groupby("NumOfProducts").agg(Total_Customers=("Exited", "count"),
        Churned_Customers=("Exited", lambda x: (x == 1).sum())).reset_index())
        churn_df["Churn Rate"] = (churn_df["Churned_Customers"]/ churn_df["Total_Customers"]) * 100
        churn_df["Churn Rate"] = churn_df["Churn Rate"].round(2)
        
        fig = px.bar(
        churn_df,
        x="NumOfProducts",
        y="Churn Rate",
        text="Churn Rate",
        title="Churn Rate by No ofProducts",
        labels={"NumOfProducts": "Number of Products", "Churn Rate": "Churn Rate (%)"},
        color="NumOfProducts",
        color_continuous_scale=["#8A4848", "#ff6666", "#cc0000"]
        )
        fig.update_layout(title_font_size=22, title_x=0.1, height=400,coloraxis_showscale=False)
        fig.update_traces(textposition="outside", textfont_size=14, textfont_color="black")
        fig.update_xaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
        fig.update_yaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        age_churn_df = (
         filtered_df.groupby("AgeGroup")["Exited"].sum().reset_index().rename(columns={"Exited": "Total Churned Customers"})
        )
        
        
        fig=px.bar(
        age_churn_df,
        x="AgeGroup",
        y="Total Churned Customers",
        title="Age-wise Customer Churn Analysis",
        labels={"AgeGroup": "Age Group", "Total Churned Customers": "Number of Churned Customers"},
        color="AgeGroup"
        )
        fig.update_layout(title_font_size=22, title_x=0.1, height=400,legend_title_font_color="black",legend_title_font_size=16)
        fig.update_xaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
        fig.update_yaxes(showgrid=False,title_font_size=16,title_font_color="black",    tickfont_size=14,tickfont_color="black")        
        st.plotly_chart(fig, use_container_width=True)
        
    col1, col2 = st.columns(2)
    with col1:
        churn_by_tenure_group=(filtered_df.groupby("Tenure Group")["Exited"].sum()).reset_index().rename(columns={"Exited": "Total Churned Customers"})
        total_customers_tenure=(filtered_df.groupby("Tenure Group")["CustomerId"].count()).reset_index().rename(columns={"CustomerId": "Total Customers"})
        churn_by_tenure = churn_by_tenure_group.merge(total_customers_tenure, on="Tenure Group")
        
        churn_by_tenure["Churn Rate"] = (churn_by_tenure["Total Churned Customers"] / churn_by_tenure["Total Customers"]) * 100
        fig = px.bar(
            churn_by_tenure,
            x="Tenure Group",
            y="Total Churned Customers",
            title="Churn Rate by Tenure Group",
            labels={"Tenure Group": "Tenure Group", "Total Churned Customers": "Total Churned Customers"},
            color="Tenure Group",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(title_x=0.1, title_font_size=18, height=400,legend_title_font_color="black",legend_title_font_size=16)
        fig.update_xaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
        fig.update_yaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=14,tickfont_color="black")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Overview")
        st.markdown(
            """
            <div style="
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            ">
            <p style="font-size:20px; color:#333; font-weight:bold;">
            🔴 Multi Product users have a higher churn rate.
            </p>

            <p style="font-size:20px; color:#333; font-weight:bold;">
            🔵 Age group 31–60 has the highest number of churned customers.
            </p>

            <p style="font-size:20px; color:#333; font-weight:bold;">
            🟣 Long-term customers account for the highest number of churned customers.
            </p>
            
            </div>
            
            """,unsafe_allow_html=True
            
        )
    st.subheader("Financial Commitment vs Engagement Analysis")
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        kpi_card("Credit Card Users", Credit_Card_Users, icon="💳", is_positive=True)
        kpi_card("Premium Customers", Premium_Customers, icon="🌟", is_positive=True)
        kpi_card("Sticky Customers", Sticky_Customers, icon="🔒", is_positive=True)
    
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
        fig.update_layout(title_x=0.1, height=300,width=300, margin=dict(t=60, b=20, l=20, r=20),legend_font_color="black",legend_title_font_color="black")
        fig.update_xaxes(showgrid=False,showticklabels=False,title_font_color="black")
        fig.update_yaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=16,tickfont_color="black")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🌍Geographically Analysis")
    col1,col2=st.columns(2,gap="small")
    with col1:
        kpi_card(
            "Total Customers(France)",
            Total_Customers_France,
            icon="",
            is_positive=True
        )
        kpi_card(
            "Total Customers(Spain)",
            Total_Customers_Spain,
            icon="",
            is_positive=True
        )
        kpi_card(
            "Total Customers(Germany)",
            Total_Customers_Germany,
            icon="",
            is_positive=True
        )
        geo_churn = (
        filtered_df[filtered_df["Exited"] == 1].groupby("Geography").size().reset_index(name="Churned Customers"))
        fig = px.bar(
        geo_churn,
        x="Geography",
        y="Churned Customers",
        orientation="v",
        color="Geography",
        text="Churned Customers",
        title="Churned Customers"
        )

        fig.update_traces(
            textposition="outside",
            textfont=dict(
                color="black",
                size=15
            )
        )
        fig.update_xaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=16,tickfont_color="black")
        fig.update_yaxes(showgrid=False,title_font_size=16,title_font_color="black",tickfont_size=16,tickfont_color="black")
        fig.update_layout(
            title_x=0.2,
            showlegend=False,height=500,width=400,title_font_size=23
        )

        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        retention_geo = (
        filtered_df.groupby("Geography")["Exited"].apply(lambda x: (x == 0).mean() * 100).reset_index(name="Retention Rate"))
        
        fig = px.pie(
        retention_geo,
        names="Geography",
        values="Retention Rate",
        hole=0.5,
        title="Retention Rate by Geography"
        )

        fig.update_traces(
        textposition="inside",
        texttemplate="%{label}<br>%{value:.2f}%"
        )

        fig.update_layout(
        title_x=0.2,showlegend=False,title_font_size=23,height=500,width=400
        )
        st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.subheader("Dataset Table")
    st.dataframe(filtered_df, width="stretch", height=400)
    
