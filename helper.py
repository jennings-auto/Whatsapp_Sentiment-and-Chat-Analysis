from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji 
import seaborn as sns

extract = URLExtract()

def fetch_stats(selected_user,df):
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    # if selected_user == "Overall":
    #1. Num of messages!
    num_messages = df.shape[0]
        
    #2. Num of Words    
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)
    
    #3. Num of media
    num_media = df[df['message'] == "<Media omitted>\n"].shape[0]

    #4. Num of links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    num_links = len(links)
    return num_messages, num_words, num_media, num_links

def fetch_busy_users(df):
    x = df['user'].value_counts().head(3)
    # df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
    #     columns={'index': 'name', 'user': 'percent'})
    y = df['user'].value_counts().tail(3)
    return x,y

# def create_wordcloud(selected_user,df):
#     if selected_user != "Overall":
#         df = df[df['user'] == selected_user]
#         wc = WordCloud(width=500,height=500,min_font_size=10,background_color='black')
#         # df_wc = wc.generate()
#         df_wc = wc.generate(df['message'].str.cat(sep=" "))
#         return df_wc

def create_wordcloud(selected_user, df):
    
    f = open("stop_hinglish.txt" , 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='black')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc.to_array()

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
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

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

