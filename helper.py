from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from textblob import TextBlob


extract = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts()/df.shape[0] * 100, 2).reset_index().rename(columns={'index':'name', 'user':'percent'})
    return x, df

def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df =  pd.DataFrame(Counter(words).most_common(21))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

def chat_personality(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    total_messages = df.shape[0]

    words = []
    for msg in df['message']:
        words.extend(msg.split())

    avg_words_per_msg = len(words) / total_messages if total_messages else 0

    # most active user (for Overall only)
    top_user = None
    if selected_user == 'Overall':
        top_user = df['user'].value_counts().idxmax()

    # time activity pattern
    busy_day = df['day_name'].mode()[0]
    busy_month = df['month'].mode()[0]

    return {
        "total_messages": total_messages,
        "avg_words": round(avg_words_per_msg, 2),
        "most_active_user": top_user,
        "busy_day": busy_day,
        "busy_month": busy_month
    }

def smart_insights(selected_user, df):

    insights = []

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    total_msgs = df.shape[0]

    avg_len = df['message'].apply(lambda x: len(x.split())).mean()

    # Insight 1: Engagement level
    if avg_len < 5:
        insights.append("Conversations are mostly short and quick replies.")
    else:
        insights.append("Conversations are detailed and expressive.")

    # Insight 2: Activity imbalance
    user_counts = df['user'].value_counts(normalize=True)

    if len(user_counts) > 1 and user_counts.iloc[0] > 0.6:
        insights.append("⚠ One user dominates most of the conversation.")

    # Insight 3: Activity level
    if total_msgs > 1000:
        insights.append("Highly active chat.")
    elif total_msgs < 100:
        insights.append("Low activity chat.")

    # Insight 4: Night usage
    night_msgs = df[df['hour'] >= 22].shape[0]
    if night_msgs > total_msgs * 0.3:
        insights.append("High late-night activity detected.")

    return insights

def chat_sentiment(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    text = " ".join(df['message'])

    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        mood = "Positive"
        score = polarity

    elif polarity < -0.1:
        mood = "Negative"
        score = polarity

    else:
        mood = "Neutral"
        score = polarity

    return mood, round(score, 2)