"""
課題の一覧を受け取り、カレンダーに登録する
summary: 課題のタイトル = title
description: 課題の説明 = (courseName, courseId, dueDate)
start: 課題をやり始める時間 = 空いている時間に押し込む
end: 課題をやり終える = start + duration

受け取るjsonの形式
class TaskEntry {
    constructor(id, title, dueDate, completed, courseName, courseId) {
        this.id = null
        this.title = null
        this.courseName = null
        this.courseId = null
        this.dueDate = null
        duration = (sec)
    }
}
カレンダー登録に必要な形式
event = {
    'summary': 'Google I/O 2019',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': '2024-05-28T00:00:00-07:00',
    },
    'end': {
        'dateTime': '2024-05-28T01:00:00-07:00',
    },
}
"""
from calender_api_wrapper import CalenderAPIWrapper

class CalenderEventGenerator:
    """
    必要な関数
    0. それぞれの課題の情報を受け取って、締め切りの最大時間を取得する
    1. CalenderAPIWrapperを叩いて(0で取得した最大時間を関数の引数にする)
       空いている時間帯を取得する
    2. 空いている時間帯に課題を押し込むことを考える(区間スケジューリング)
    3. CalenderAPIWrapperを叩いて、課題をカレンダーに登録する
    """
    def __init__(self):
        self.calendar = CalenderAPIWrapper()

    def task_execute(self):
        """
        課題の一覧を受け取って、カレンダーに登録する
        """
        tasks = self.get_tasks()
        self.write_tasks(self.schedule_tasks(tasks))

    def get_max_due_date(self, tasks):
        """
        課題の一覧を受け取り、締め切りの最大時間を取得する
        """
        time_max = None
        time_max = max([task.dueDate for task in tasks])
        return time_max
    
    def get_free_time(self, time_max):
        """
        空いている時間帯を取得する
        """
        free_time_list = []
        if time_max == None:
            schedule = self.calendar.read_calendar()
        else:
            schedule = self.calendar.read_calendar(time_max)
        print(schedule)
        
        return free_time_list

    def schedule_tasks(self, tasks, free_time_list):
        """
        課題を空いている時間帯に押し込む
        """
        free_time_list = self.get_free_time(self.get_max_due_date(tasks))
        return free_time_list

    def write_tasks(self, tasks):
        """
        課題をカレンダーに登録する
        """
        for task in tasks:
            event = {
                'summary': task.title,
                'description': f"{task.courseName}, {task.courseId}, {task.dueDate}",
                'start': {
                    'dateTime': task.start,
                },
                'end': {
                    'dateTime': task.end,
                },
            }
            self.calendar.write_calendar(event)


if __name__ == "__main__":
    calendar = CalenderEventGenerator()
    print(calendar.get_free_time(None))