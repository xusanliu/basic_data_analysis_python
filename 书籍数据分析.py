#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import pyecharts
from pyecharts.charts import WordCloud
from pyecharts.charts import Bar
from pyecharts import options as opts


# In[2]:


data=np.genfromtxt('rating.txt',delimiter=',')
data=data.astype(int)
rating_sum=np.zeros(10000)
rating_people_count=np.zeros(10000)
for rating in data:
	bookid=rating[1]-1
	rating_sum[bookid]+=rating[2]
	rating_people_count[bookid]+=1
rating_dafen=rating_sum/rating_people_count


# In[3]:


to_read=pd.read_csv('to_read.csv')
books=pd.read_csv('books.csv')
tags=pd.read_csv('tags.csv')
book_tags=pd.read_csv('book_tags.csv')


# In[4]:


to_read.head(5)


# In[5]:


books.head(5)


# In[6]:


to_read_counts=to_read['book_id'].value_counts()


# In[7]:


hottest_50_books_id=pd.DataFrame({
    'book_id':to_read_counts.index,
    'book_counts':to_read_counts.values
})[:50]


# In[8]:


books=books[['book_id','goodreads_book_id','title']]
hottest_50_books_with_title=pd.merge(hottest_50_books_id,books,on='book_id')
hottest_50_books_with_title.to_csv('hottest_50_books_with_title.csv')


# In[9]:


hottest_50_books_with_title.head(5)


# In[10]:


book_tags=pd.read_csv('book_tags.csv')
book_tags.head(5)


# In[11]:


tags=pd.read_csv('tags.csv')
tags.head(5)


# In[12]:


book_tags=book_tags[book_tags['_goodreads_book_id_'].isin(hottest_50_books_with_title['goodreads_book_id'])]
book_tags


# In[13]:


hottest_10_book_tag_id=book_tags[:10]
del hottest_10_book_tag_id['_goodreads_book_id_']
hottest_10_book_tag_id


# In[14]:


hottest_10_book_tag_id_name=pd.merge(hottest_10_book_tag_id,tags,on='tag_id')
hottest_10_book_tag_id_name.to_csv('hottest_10_book_tag_id_name.csv')


# In[15]:


wordcloud=WordCloud()
hottest_50_books_with_title=pd.read_csv('hottest_50_books_with_title.csv')
wordcloud.add(
"",
zip(hottest_50_books_with_title['title'].tolist(),hottest_50_books_with_title['book_counts'].tolist())
)
wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="最多人想读的50本书"))
wordcloud.render('./hottest_50_books.html')


# In[16]:


wordcloud=WordCloud()
hottest_10_book_tag_id_name=pd.read_csv('hottest_10_book_tag_id_name.csv')
wordcloud.add(
"",
zip(hottest_10_book_tag_id_name['tag_name'].tolist(),hottest_10_book_tag_id_name['count'].tolist())
)
wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="最热门的10个标签")) 
wordcloud.render('./hottest_10_tags.html')


# In[17]:


bar=Bar()
bar.add_xaxis(hottest_10_book_tag_id_name['tag_name'].tolist())
bar.add_yaxis("tags",hottest_10_book_tag_id_name['count'].tolist())
bar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))
bar.render('./hottest_10_tags_bar.html')

