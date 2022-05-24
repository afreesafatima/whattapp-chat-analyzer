import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import emoji
import seaborn as sns

st.sidebar.title("Whattapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     data=bytes_data.decode("utf-8")
     df=preprocessor.preprocess(data)


     #fetch users list
     user_list = list(df['user'].unique())
     user_list.sort()
     user_list.insert(0,'Overall')
     user_list.remove('.')
     user_list.remove('group_notification')
     selected_user=st.sidebar.selectbox("Analysis wrt",user_list)
     if st.sidebar.button("Show Analysis"):
          st.title(selected_user)
          total_messages,total_words,num_media,num_links=helper.fetch_stats(selected_user,df)
          st.title("Total Statistics")
          col1,col2,col3,col4 =st.columns(4)

          with col1:
               st.header("Total Messages")
               st.title(total_messages)
          with col2:
               st.header("Total Words")
               st.title(total_words)
          with col3:
               st.header("Total Media")
               st.title(num_media)
          with col4:
               st.header("Total Links")
               st.title(num_links)
          #finding most busiest user
if selected_user=='Overall':
     st.title("Most_buzy_user")
     x,new_df=helper.most_buzy(df)
     fig,ax=plt.subplots()

     col1,col2=st.columns(2)
     with col1:
          st.header("Bar Chart")
          ax.barh(x.index, x.values,color='red')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)
     with col2:
          st.header("Percentage Analysis")
          st.dataframe(new_df)


most_common_df=helper.most_common_words(selected_user,df)
st.title('most_common_words')
fig,ax=plt.subplots()
plt.barh(most_common_df[0],most_common_df[1])
st.pyplot(fig)
plt.xticks(rotation='vertical')
#emoji analysis
x=helper.emoji(selected_user,df,emoji.UNICODE_EMOJI)
st.title("Emoji Analysis")
col1,col2=st.columns(2)
with col1:

  st.dataframe(x)
with col2:
  fig,ax=plt.subplots()
  ax.pie(x[1],labels=x[0],autopct="%.2f")
  st.pyplot(fig)
  plt.show()
  # monthly timeline
st.title("Monthly Timeline")
timeline=helper.monthly_timeline(selected_user,df)
fig,ax=plt.subplots()
ax.plot(timeline['time'],timeline['messages'],c='green')
plt.xticks(rotation='vertical')
st.pyplot(fig)
#daily timeline
st.title("Daily Timeline")
timeline=helper.daily_timeline(selected_user,df)
fig,ax=plt.subplots()
ax.plot(timeline['only_date'],timeline['messages'],c='red')
plt.xticks(rotation='vertical')
st.pyplot(fig)
#activity map
st.title("Activity Map")
col1,col2=st.columns(2)
with col1:
     st.header("Most busy day")
     busy_day=helper.week_activity_map(selected_user,df)
     fig, ax = plt.subplots()
     ax.bar(busy_day.index,busy_day.values)
     st.pyplot(fig)
with col2:
     st.header("Most busy month")
     busy_day=helper.monthly_activity_map(selected_user,df)
     fig, ax = plt.subplots()
     ax.bar(busy_day.index,busy_day.values,color='orange')
     plt.xticks(rotation='vertical')
     st.pyplot(fig)
st.title("Activity Heatmap")
user_heatmap=helper.activity_heatmap(selected_user,df)
fig, ax = plt.subplots()
ax=sns.heatmap(user_heatmap)
st.pyplot(fig)

