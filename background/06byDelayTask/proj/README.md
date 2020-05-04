# README
定期复制 栅格数据并做标准化处理，将状态及栅格数据快照写入数据库及日志。
定时任务使用 `apscheduler` 或 `celery`
orm 使用 `sqlalchemy`

## 目录结构
```
|__proj
	|__ common/
		|__ common.py
		|__ enmu.py			所有枚举
		|__ exceptionLog.py	记录错误日志的装饰器
		|__	log.py			logging的初始化(配置参数)
    |__ conf/
        |__ settings.py     所有的配置文件/常量
    |__ core/
    	|__ data.py			所有的操作nc文件的读取相关操作逻辑，包含数据验证+数据转换(转换为opendrift可识别的文件)
        |__ db.py           所有的操作数据库的逻辑放在此处 ,使用sqlalchemy(by cwb)
        |__ file.py         文件处理的相关逻辑，I开头的抽象类，可以有具体的实现类，但必须由子类继承，无法直接实例化抽象类
        |__ ftp.py          所有的ftp操作逻辑，通过ftpFactory调用file中的 IFileBase 的实现类
        |__ job.py			所有的 作业+工作流 作业通过apscheduler启动，开启定时任务。所有作业相关的均以 xx_xx_job 命名
        					所有继承自 ICoverageWF 的子类，均需要实现 coverage_convert 由于栅格数据需要转换 long_name 与 standard_name 
    |__ model/
        |__ models.py       所有的model，orm使用sqlalchemy
        |__ midmodel.py		中间 middle model 用来各个模块之间传递数据使用
    |__ util/
        |__ tools.py
    main.py
```

所有的抽象类及接口类均使用`I`的前缀声明，抽象类可以定义具体实现方法，但不能直接实例化，可以通过实现的子类实例化。

## 部分业务逻辑

### 下载逻辑

待补充(已经实现)

### 下载之后写入数据库持久化保存

## 注解

### 中心数值预报产品:

![中心数值预报产品](/Users/evaseemefly/Documents/01Proj/SearchRescueSys/document/99img/中心数值预报产品.png)

流场:

|          |                       |      |
| -------- | --------------------- | ---- |
| 渤海     | Bhs_cur_xx.nc         |      |
| 东中国海 | Ecs_new_current_xx.nc |      |
| 印度洋   | Ind_cur_xx.nc         |      |
| 南海     | Scs_cur_xx.nc         |      |
| 西北太   | Nwp_cur_xx.nc         |      |

风场

|        |                 |      |
| ------ | --------------- | ---- |
| 西北太 | nmefc_wrf_xx.nc |      |

注意综上所述判断文件是什么类型时，将名称按照 **_** 进行切分,只用判断 index=1 的字段是否为 **wrf** 即可。

保险起见当 index=1 的字段 不等于 [ wrf , cur]时，判断 index=2 是否等于 **current**

