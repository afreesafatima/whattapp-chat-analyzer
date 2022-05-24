import pandas as pd
from urlextract import URLExtract
from collections import Counter

extract=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    num_messages=df.shape[0]
    words = []
    for word in df['messages']:
        words.extend(word.split())
    num_media=df[df['messages']=='<Media omitted>\n'].shape[0]
    links=[]
    for message in df['messages']:
     links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media,len(links)

def most_buzy(df):
     x=df['user'].value_counts().head()
     new_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'Percent'})

     return x,new_df
def most_common_words(selected_user,df):
    f=open('stop_words.txt','r')
    stop_words=f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp=df[df['user']!='group_notifications']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words=[]
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    x=pd.DataFrame(Counter(words).most_common(10))
    return x
def emoji(selected_user,df,y):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis=[]
    for message in df['messages']:
      emojis.extend([c for c in message if c in y['en']])
    x=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return x
def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    df['month_num'] = df['date'].dt.month
    timeline= df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time=[]
    for i in range (timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline["time"]=time
    return timeline
def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby(['only_date']).count()['messages'].reset_index()
    return daily_timeline
def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def monthly_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    x=df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)
    return x