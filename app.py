import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# Load your API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Page setup
st.set_page_config(page_title="BI Assistant", page_icon="📊", layout="wide")
st.title("📊 AI-Powered Business Intelligence Assistant")
st.write("Upload a CSV file and ask questions about your data in plain English.")

# File upload section
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
df=None

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
    st.write("### Preview of your data")
    st.dataframe(df.head(10))
    st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

    ############################## API #####################################
    from langchain_groq import ChatGroq
    from langchain_experimental.agents import create_pandas_dataframe_agent

    # Question input section
    st.write("---")
    st.write("### Ask a question about your data")
    user_question = st.text_input("Type your question here:", placeholder="e.g. What is the average total revenue?")

    if user_question:
        with st.spinner("Thinking..."):
            try:
                # Create the AI model connection
                groq_api_key = os.getenv("GROQ_API_KEY")
                llm = ChatGroq(
                    temperature=0,
                    model="llama-3.3-70b-versatile",
                    api_key=groq_api_key
                )

                # Create the agent that connects AI to your dataframe
                agent = create_pandas_dataframe_agent(
                    llm,
                    df,
                    verbose=False,
                    allow_dangerous_code=True
                )

                # Get the answer
                response = agent.invoke(user_question)

                st.success("Answer:")
                st.write(response["output"])

            except Exception as e:
                st.error(f"Error: {str(e)}")

    ################ CHARTS #####################################
    # Chart generation section
    st.write("---")
    st.write("### Auto Chart Generator")
    st.write("Select columns to visualise your data instantly.")

    col1, col2 = st.columns(2)

    with col1:
        chart_type = st.selectbox(
            "Chart type",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"]
        )

    with col2:
        x_axis = st.selectbox("X axis", df.columns.tolist())

    y_axis = st.selectbox("Y axis", df.columns.tolist())

    if st.button("Generate Chart"):
        with st.spinner("Generating chart..."):
            try:
                if chart_type == "Bar Chart":
                    fig = px.bar(
                        df, x=x_axis, y=y_axis,
                        title=f"{y_axis} by {x_axis}"
                    )
                elif chart_type == "Line Chart":
                    fig = px.line(
                        df, x=x_axis, y=y_axis,
                        title=f"{y_axis} over {x_axis}"
                    )
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(
                        df, x=x_axis, y=y_axis,
                        title=f"{x_axis} vs {y_axis}"
                    )
                elif chart_type == "Histogram":
                    fig = px.histogram(
                        df, x=x_axis,
                        title=f"Distribution of {x_axis}"
                    )

                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Chart error: {str(e)}")

    # AI Chart Suggestion section
    st.write("---")
    st.write("### AI Chart Suggestion")
    st.write("Describe what you want to see and the AI will build the chart.")

    chart_question = st.text_input(
        "Describe your chart:", placeholder="e.g. Show me revenue distribution by churn label"
    )

    if chart_question:
        with st.spinner("Building your chart..."):
            try:
                columns_info = ", ".join(df.columns.tolist())

                prompt = f"""
                I have a dataframe with these columns: {columns_info}

                The user wants to see: {chart_question}

                Reply with ONLY a JSON object in this exact format, nothing else:
                {{"chart_type": "bar", "x": "column_name", "y": "column_name", "title": "chart title"}}

                chart_type must be one of: bar, line, scatter, histogram
                x and y must be exact column names from the list above.
                For histogram, set y to the same as x.
                """

                llm_simple = ChatGroq(
                    temperature=0,
                    model="llama-3.3-70b-versatile",
                    api_key=groq_api_key,
                )

                result = llm_simple.invoke(prompt)
                response_text = result.content.strip()

                import json
                import re

                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    chart_config = json.loads(json_match.group())

                    x_col = chart_config["x"]
                    y_col = chart_config["y"]
                    title = chart_config["title"]
                    ctype = chart_config["chart_type"]

                    if ctype == "bar":
                        fig = px.bar(df, x=x_col, y=y_col, title=title)
                    elif ctype == "line":
                        fig = px.line(df, x=x_col, y=y_col, title=title)
                    elif ctype == "scatter":
                        fig = px.scatter(df, x=x_col, y=y_col, title=title)
                    elif ctype == "histogram":
                        fig = px.histogram(df, x=x_col, title=title)

                    st.plotly_chart(fig, use_container_width=True)
                    st.caption(f"Chart type: {ctype} | X: {x_col} | Y: {y_col}")

            except Exception as e:
                st.error(f"Chart error: {str(e)}")



# Data Summary Section
st.write("---")
st.write("### Automatic Data Summary")

if df is None:
    st.info("Upload a CSV file to see automatic insights.")
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", df.shape[0])
    with col2:
        st.metric("Total Columns", df.shape[1])
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    st.write("#### Column Statistics")
    st.dataframe(df.describe().round(2))

    st.write("#### Data Types")
    dtype_df = pd.DataFrame({
        "Column": df.dtypes.index,
        "Type": df.dtypes.values.astype(str),
        "Null Count": df.isnull().sum().values,
        "Null %": (df.isnull().sum().values / len(df) * 100).round(2)
    })
    st.dataframe(dtype_df)