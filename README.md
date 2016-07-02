#介绍
Python写的博客程序，框架用的Flask，前端用Bootstrap，富文本用的CKeditor。<br>
>manage.py主程序<br>
>config.py Flask配置选项<br>
>APP：\__init\__.py<br>
    >>static存放bootstrap jquery<br>
    >>templates存放jinja渲染模板<br>
    >>models.py集中数据库操作<br>
    >>params.py集中jinja渲染变量<br>
    >>views.py基本路由URL处理<br>
    >>Judge.py详细路由URL处理<br>
    >>From_table.py Flask-web表单集合(不包含html表单)<br>
##更新时间2016年7月2日
1.标签功能<br>
2.归档功能<br>
3.代码块<br>
##更新时间2016年5月24日
1.分类编辑<br>
2.推荐文章选项<br>
##更新时间2016年5月22日
1.后台文章编辑功能<br>
2.前后台文章分页管理显示<br>
3.首页文章页和分类前台<br>
##基本功能
1.数据库用SQLAlchemy实现，原先用SQLite，之后改成了Mysql<br>
2.后台管理员登录，session保持<br>
3.文章分类以及文章的添加删除<br>
![image](http://chuantu.biz/t4/15/1463364291x1035372866.png)<br>
![image](http://chuantu.biz/t4/15/1463364471x1035372866.png)<br>
![image](http://chuantu.biz/t4/15/1463364411x1035372866.png)<br>
