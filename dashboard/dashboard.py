import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency
from wordcloud import WordCloud

sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Dashboard E-Commerce')


def show_bar_chart(dataframe):
    top_10_cities = dataframe.head(10)

    plt.figure(figsize=(10, 6))
    plt.bar(top_10_cities['seller_city'],
            top_10_cities['Total_Seller'], color='skyblue')
    plt.xlabel('City')
    plt.ylabel('Total Sellers')
    plt.title('Top 10 Cities by Total Sellers')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    st.pyplot()


def show_hist_chart(dataframe):
    plt.figure(figsize=(15, 10))
    dataframe.hist()
    plt.tight_layout()
    st.pyplot()


def show_word_cloud(wordcloud):
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Product Category Word Cloud', pad=20)
    plt.axis('off')
    st.pyplot()


def show_payment_chart(df_payments):
    grouped_data = df_payments.groupby("payment_type")[
        "payment_value"].sum().reset_index()
    grouped_data = grouped_data.sort_values(
        by="payment_value", ascending=False)

    # Membuat colormap
    colors = plt.cm.viridis(np.linspace(0, 1, len(grouped_data)))

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.barh(grouped_data['payment_type'],
                    grouped_data['payment_value'], color=colors)
    plt.xlabel('Total Payment Value')
    plt.ylabel('Payment Type')
    plt.title('Total Payment Value by Payment Type')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    st.pyplot()


# dataframe
df_sellers = pd.read_csv('../data/sellers_dataset.csv')
df_products = pd.read_csv('../data/products_dataset.csv')
df_payments = pd.read_csv('../data/order_payments_dataset.csv')

# 10 Kota teratas
city_sellers_count = df_sellers.groupby(
    ['seller_state', 'seller_city']).size().reset_index(name='Total_Seller')
city_sellers_count_sorted = city_sellers_count.sort_values(
    by='Total_Seller', ascending=False)

# Membuat WordCloud
total_product_category = df_products['product_category_name'].value_counts()
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(
    total_product_category)
# Membagi layout menjadi 2 baris dan 2 kolom
col1, col2 = st.columns(2)

# Menampilkan visualisasi pada layout grid
with col1:
    st.header("Top 10 Cities by Total Seller")
    show_bar_chart(city_sellers_count_sorted)

with col2:
    st.header("Popular Product Category")
    show_word_cloud(wordcloud)

row1, row2 = st.columns(2)
with row1:
    st.header('The Most Payment Method')
    show_payment_chart(df_payments)
with row2:
    st.header('Statistic Description Products')
    show_hist_chart(df_products)
