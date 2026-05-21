import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(

    page_title="ConversaLens",
    page_icon="◉",
    layout="wide"
)

st.markdown(
    """
        
    <h1 style='text-align: center;'>◉ ConversaLens</h1>
    
    <h4 style='text-align: center; color: #6c757d;'>
    AI-Powered Chat Intelligence System
    </h4>

    <p style='text-align: center; color: #808080; font-size:17px;'>
    Analyze communication patterns, engagement trends, sentiment, and conversational behavior from WhatsApp chats.
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("ConversaLens")
st.sidebar.caption("Upload and analyze exported WhatsApp conversations")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        tab1, tab2, tab3, tab4 = st.tabs([
            "Overview",
            "Personality",
            "Insights",
            "Analytics"
        ])

        with tab1:

            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

            st.title("Top Statistics")

            col1, col2, col3, col4 =  st.columns(4)

            with col1:
                st.subheader("Total Messages")
                st.title(num_messages)

            with col2:
                st.subheader("Total Words")
                st.title(words)

            with col3:
                st.subheader("Media Shared")
                st.title(num_media_messages)

            with col4:
                st.subheader("Link Shared")
                st.title(num_links)

            # monthly timeline
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color = 'green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # daily timeline
            st.title("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # Activity Map
            st.title('Activity Map')
            col1, col2 = st.columns(2)
            with col1:
                st.header("Most Busy day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most Busy Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color = 'orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)

            # finding the busiest users in the group(group level)
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values, color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.dataframe(new_df)

        with tab2:

            st.title("Chat Personality Report")

            report = helper.chat_personality(selected_user, df)

            st.metric("Total Messages", report["total_messages"])
            st.metric("Avg Words", report["avg_words"])

            st.info(f"Most Active User: {report['most_active_user']}")
            st.success(f"Busy Day: {report['busy_day']}")

        with tab3:

            st.title("Smart Insights")

            insights = helper.smart_insights(selected_user, df)

            for i in insights:
                st.info(i)

            st.subheader("Conversation Sentiment Analysis")

            mood, score = helper.chat_sentiment(selected_user, df)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Overall Sentiment", mood)

            with col2:
                st.metric("Sentiment Score", score)

            if mood == "Positive":
                st.success("Conversations reflect a generally positive interaction pattern.")

            elif mood == "Negative":
                st.warning("Conversations show signs of negative interaction patterns.")

            else:
                st.info("Conversations appear balanced and neutral.")

        with tab4:

            # wordcloud
            st.title("WordCloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # Most common words
            most_common_df = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots()

            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')

            st.title('Most commmon words')
            st.pyplot(fig)

            # Emoji Analysis
            if selected_user == 'Overall':
                emoji_df = helper.emoji_helper(selected_user, df)
                st.title("Emoji Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    fig, ax = plt.subplots()
                    plt.rcParams['font.family'] = 'Segoe UI Emoji'
                    ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct="%0.2f")
                    st.pyplot(fig)












