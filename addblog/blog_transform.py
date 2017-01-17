# -*- coding: UTF-8 -*- 
'''
Authorized  by vlon Jang
Created on Apr 10, 2016
Email:zhangzhiwei@ict.ac.cn
From Institute of Computing Technology
All Rights Reserved.
'''
import markdown2
import MySQLdb
import datetime, time
import os, sys

user = 'root'
password = '901022'

default_info={
    'author_id':'1',
    'category' : 'True love',
    'title': 'Why I love wangqingbaidu?',
    'en_title': 'untitled',
    'tags': 'Love',
    'summary' : 'RT',
    'content' : 'RT',
    'img': '/static/img/article/default.jpg'
    }


class markdown2blog:
    def __init__(self, filepath = None):
        self.filepath = filepath
        self.blog_info = default_info
    def get_blog_info(self):
        ep_info = False
        start_content = False
        flines = open(self.filepath).readlines()
        for line in flines:
            if not ep_info:
                if '<ep_info>' in line:
                    ep_info = True
                    continue
                key, value = (x for x in line.strip().split('='))
                self.blog_info[key] = value
            elif start_content:
                self.blog_info['content'] += line
            elif line != '\r\n' and line != '\n':
                start_content = True
                self.blog_info['content'] = line
            else:
                pass

    def content2html(self):
        self.blog_info['content'] = markdown2.markdown(self.blog_info['content'], extras=['fenced-code-blocks']).encode('utf8')
        for key in self.blog_info.keys():
            self.blog_info[key] = self.blog_info[key].replace('\\', '\\\\\\\\')
            self.blog_info[key] = self.blog_info[key].replace('\'', '\\\'')
        
    def insert2db(self):
            self.get_blog_info()
            self.content2html()
            latex_math = '<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>\n'
#             print self.blog_info
#         try:            
            conn=MySQLdb.connect(host='localhost',user='root',passwd='901022',db='blog',port=3306, charset='utf8')
            cur=conn.cursor()
            
            get_category_sql = "select id from blog_category where name='%s'" %self.blog_info['category']
#             print get_category_sql
            cur.execute(get_category_sql)
            category_id = cur.fetchone()
            if category_id:
                self.blog_info['category'] = int(category_id[0])
            else:
                insert_category_sql = "insert into blog_category(name, create_time,rank,status) values(\
                    '%s', '%s',0,0)" %(self.blog_info['category'],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#                print insert_category_sql
                cur.execute(insert_category_sql)
                cur.execute(get_category_sql)
                category_id = cur.fetchone()
                self.blog_info['category'] = int(category_id[0])
#             print  self.blog_info['category']   
            self.blog_info['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.blog_info['en_title'] += str(int(time.time()))
            self.blog_info['content'] = latex_math + self.blog_info['content'] 
            insert_blog_sql = "insert into blog_article(title,en_title,img,tags,summary,content,\
                pub_time,create_time,update_time,author_id, category_id,\
                view_times,zan_times,is_top,rank,status) values\
                ('%(title)s','%(en_title)s','%(img)s','%(tags)s','%(summary)s','%(content)s',\
                '%(time)s','%(time)s','%(time)s',%(author_id)s,%(category)s,\
                0,0,0,0,0)" %self.blog_info
                
#             print insert_blog_sql
#             print self.blog_info
            cur.execute(insert_blog_sql)
            conn.commit()
            cur.close()
            conn.close()
#         except MySQLdb.Error,e:
#             print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
if __name__ == '__main__':
    if len(sys.argv) == 2:
        filepath = ''
        if os.path.isfile(os.getcwd() + '/' + sys.argv[1]):
            filepath = os.getcwd() + '/' + sys.argv[1]
        elif os.path.isfile(sys.argv[1]):
            filepath = sys.argv[1]
        if filepath:
            db_query = markdown2blog(filepath=filepath)
            db_query.insert2db()
        else:
            print 'File not exist!'
    else:
        print 'Please input markdown file path!'
        
        
        
        
