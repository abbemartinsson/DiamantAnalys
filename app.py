import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")
st.title("Diamantanalys för Guldfynd")

@st.cache_data
def load_data():
    df = pd.read_csv("diamonds.csv")
    df.dropna(how="any", inplace=True)
    df = df[(df['x'] > 0) & (df['y'] > 0) & (df['z'] > 0)]
    df["depth_calc"] = 2 * (df["z"] / (df["x"] + df["y"])) * 100
    df["depth_diff"] = np.abs(df["depth"] - df["depth_calc"])
    df = df[df["depth_diff"] <= 1]
    return df

df = load_data()
df_filtered = df[(df["carat"] >= 1) & (df["carat"] <= 2)]

carat_tab, corr_tab, clarity_tab, cut_tab = st.tabs([
    "Carat & Pris", "Korrelationsmatris", "Klarhet & Pris", "Slipning & Pris"])

with carat_tab:
    st.subheader("Carat och Pris")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    bins = np.arange(0.5, df['carat'].max() + 0.5, 0.5)
    sns.histplot(df['carat'], bins=bins, kde=False, ax=axes[0])
    axes[0].set_title('Fördelning av carat')
    sns.scatterplot(x='carat', y='price', data=df, ax=axes[1])
    axes[1].set_title('Samband mellan carat och pris')
    st.pyplot(fig)

with corr_tab:
    st.subheader("Korrelationsmatris (1-2 carat)")
    df_corr = df_filtered.copy()
    df_corr["color"] = pd.Categorical(df_corr["color"], categories=["D","E","F","G","H","I","J"], ordered=True)
    df_corr["clarity"] = pd.Categorical(df_corr["clarity"], categories=["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"], ordered=True)
    df_corr["cut"] = pd.Categorical(df_corr["cut"], categories=["Fair", "Good", "Very Good", "Premium", "Ideal"], ordered=True)
    df_corr["color_num"] = df_corr["color"].cat.codes
    df_corr["clarity_num"] = df_corr["clarity"].cat.codes
    df_corr["cut_num"] = df_corr["cut"].cat.codes
    corr = df_corr[["carat", "depth", "price", "color_num", "clarity_num", "cut_num"]].corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

with clarity_tab:
    st.subheader("Pris och antal per klarhet")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(x="clarity", y="price", data=df_filtered,
                order=["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"], ax=axes[0])
    axes[0].set_title("Pris per klarhet i 1–2 carat")
    clarity_counts = df_filtered["clarity"].value_counts().reindex(
        ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"])
    sns.barplot(x=clarity_counts.index, y=clarity_counts.values, ax=axes[1])
    axes[1].set_title("Antal diamanter per klarhet")
    st.pyplot(fig)

with cut_tab:
    st.subheader("Pris och fördelning av slipning")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(data=df_filtered, x="cut", y="price", ax=axes[0])
    axes[0].set_title("Pris per Slipning i 1-2 carat")
    cut_counts = df_filtered["cut"].value_counts()
    axes[1].pie(cut_counts, labels=cut_counts.index, autopct='%1.1f%%', startangle=140)
    axes[1].set_title("Fördelning av Slipning")
    st.pyplot(fig)
