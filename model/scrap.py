import praw 
import pandas as pd 

# to get those information you should follow this article here https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
client_id = ''
client_secret = '' 
user_agent  = ''

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret ,  user_agent=user_agent) 
hot_questions  = reddit.subreddit('askreddit').hot()
data = [] 

# looping through the questions 
for id , question  in enumerate(hot_questions):
    if question.num_comments != 0 : 
        submission = reddit.submission(id=question.id)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments : 
            data.append([question.title , question.id , question.subreddit , question.num_comments  , question.url , comment.body ])


df = pd.DataFrame(data ,columns=['title', 'id', 'subreddit','num_comments' , 'url', 'comment'])

df.to_csv('reddit_questions.csv')