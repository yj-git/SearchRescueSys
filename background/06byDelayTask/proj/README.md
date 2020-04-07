# README
定期复制 栅格数据并做标准化处理，将状态及栅格数据快照写入数据库及日志。
定时任务使用 `apscheduler` 或 `celery`
orm 使用 `sqlalchemy`

## 目录结构
```
|__proj
    |__ conf/
        |__ settings.py     所有的配置文件/常量
    |__ core/
        |__ db.py           所有的操作数据库的逻辑放在此处 ,使用sqlalchemy
        |__ file.py         文件处理的相关逻辑，I开头的抽象类，可以有具体的实现类，但必须由子类继承，无法直接实例化抽象类
        |__ ftp.py          所有的ftp操作逻辑，通过ftpFactory调用file中的 IFileBase 的实现类
    |__ model/
        |__ models.py       所有的model，orm使用sqlalchemy
    |__ util/
        |__ tools.py
    main.py
```

所有的抽象类及接口类均使用`I`的前缀声明，抽象类可以定义具体实现方法，但不能直接实例化，可以通过实现的子类实例化。