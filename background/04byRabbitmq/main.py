from datetime import datetime
from core.Job import JobRun
from job.oil import JobOil
from job.step import OilStep


def main():
    print('测试')
    # job= JobRun('123', '123', datetime.now(), 'case_a', '/')
    job = JobOil('123', '123', datetime.now(), 'case_a', '/')
    job.do_job()
    print('作业执行完成')

    # TODO:[*] 19-12-25 测试OilStep
    # oil = OilStep(r'D:\02proj\SearchRescue\SearchRescueSys\background\01byJupyter\data', 'sanjioil.nc')
    oil = OilStep(r'D:\02proj\new_SearchRescueSys\SearchRescueSys\background\01byJupyter\data', 'sanjioil.nc')
    oil.do_job()
    pass


if __name__ == '__main__':
    main()
