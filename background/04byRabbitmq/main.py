from datetime import datetime
from core.Job import JobRun, JobOil


def main():
    print('测试')
    # job= JobRun('123', '123', datetime.now(), 'case_a', '/')
    job = JobOil('123', '123', datetime.now(), 'case_a', '/')
    job.do_job()
    print('作业执行完成')
    pass


if __name__ == '__main__':
    main()
