#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
import jieba
import pyecharts
from pyecharts.charts import WordCloud
from pyecharts import options as opts


# In[2]:


con=sqlite3.connect('douban_comment_data.db')
comment_data=pd.read_sql_query('select * from comment;',con)
comment_data.head(5)


# In[3]:


movie_comment_counts=comment_data['MOVIEID'].value_counts()
movie_comment_counts=pd.DataFrame({
    'movie_id':movie_comment_counts.index,
    'comment_counts':movie_comment_counts.values
})
movie_comment_counts.head(5)


# In[4]:


movie_data=pd.read_excel('douban_movie_data.xlsx')
movie_data.head(5)


# In[5]:


def get_comments(movie_id):
    comments=comment_data[comment_data['MOVIEID']==movie_id]['CONTENT']
    comments_all=''
    for comment in comments:
        comments_all+=comment+'\n'
    return comments_all


# In[6]:


get_comments('1292052')


# In[7]:


FILTER_WORDS = ['知道','影评','影片','小编','没有','一个','\n','good','is','thing','这个','就是','什么','真的','of',
'我们','最后','一部','the','片子','这么','那么','不是','还是','时候','觉得','电影','但是','hope','Hope','best','因为','只是','故事','看过','豆瓣','maybe']


# In[8]:


movie_id='1292052'
keyword_counts=pd.Series(list(jieba.cut(get_comments(movie_id))))
keyword_counts=keyword_counts[keyword_counts.str.len()>1]
keyword_counts=keyword_counts[~keyword_counts.str.contains('|'.join(FILTER_WORDS))]
keyword_counts=keyword_counts.value_counts()[:20]
keyword_counts


# In[9]:


wordcloud=WordCloud()
wordcloud.add(
"",
zip(keyword_counts.index.tolist(),keyword_counts.values.tolist())
)
wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="最热门的20个评论关键词"))
wordcloud.render('./hottest_keywords.html')


# In[10]:


def get_keywords(movie_id):
    keyword_counts=pd.Series(list(jieba.cut(get_comments(movie_id))))
    keyword_counts=keyword_counts[keyword_counts.str.len()>1]
    keyword_counts=keyword_counts[~keyword_counts.str.contains('|'.join(FILTER_WORDS))]
    keyword_counts=keyword_counts[:20]
    return keyword_counts


# In[11]:


def keywords_wordcloud(movie_id):
    keyword_counts=get_keywords(movie_id)
    wordcloud=WordCloud()
    wordcloud.add(
    "",
    zip(keyword_counts.index.tolist(),keyword_counts.values.tolist())
    )
    wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="最热门的20个评论关键词"))
    wordcloud.render('./hottest_keywords.html')

