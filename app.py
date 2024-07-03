import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#Sentiment analysis:
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


st.sidebar.title("Whatsapp Chat Analyser! 📃")
st.sidebar.text("Analyze with us! (●'◡'●)")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis of USER!", user_list)

    if st.sidebar.button("Show Analysis"):
        st.header(selected_user, "Analysis: ")
        
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user,df)


        col1, col2,col3, col4 = st.columns(4)


        with col1:
            st.header("Total Messages: ")
            st.title(num_messages)
        with col2:
            st.header("Total Words: ")
            st.title(num_words)
        
        with col3:
            st.header("Total Media: ")
            st.title(num_media)
        with col4:
            st.header("Total Links: ")
            st.title(num_links)

        #TIMELINE
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity map:
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        st.title("Weekly Activity Heat Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        # if selected_user == 'Overall':
        #     st.title('Most Busy Users')
        #     x,new_df = helper.most_busy_users(df)
        #     fig, ax = plt.subplots()

        #     col1, col2 = st.columns(2)

        #     with col1:
        #         ax.bar(x.index, x.values,color='red')
        #         plt.xticks(rotation='vertical')
        #         st.pyplot(fig)
        #     with col2:
        #         st.dataframe(new_df)


        #SENTIMENT ANALYSIS:
        st.title('OVERALL SENTIMENT ANALYSIS:')
        nltk.download('vader_lexicon')
        sia = SentimentIntensityAnalyzer()

        def analyze_sentiment(message):
            return sia.polarity_scores(message)['compound']
        
        df['sentiment'] = df['message'].apply(analyze_sentiment)
        # Plot sentiment analysis results
        fig, ax = plt.subplots()
        sns.histplot(df['sentiment'], bins=20, kde=True, ax=ax)
        ax.set_title('Sentiment Analysis of Messages')
        ax.set_xlabel('Sentiment Score')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)




        # FInding busiest users:
        if selected_user == 'Overall':
            # st.title("Most Busy Users (TOP 3)")
            new_df = df[df['user'] != 'group_notification'].copy()
            x,y = helper.fetch_busy_users(new_df)

            col1, col2 = st.columns(2)
            

            with col1:
                st.title("Most BUSY users")
                fig,ax = plt.subplots()
                ax.bar(x.index, x.values, color = 'green')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.title("Most LAZY users")
                fig,ax = plt.subplots()
                ax.bar(y.index, y.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
        
        # WORDCLOUD:

        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off')  # Hide axes ticks
        st.pyplot(fig)

        # Most common Words:
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        #EMOJI IDENTIFIER:

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)
