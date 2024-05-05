from calender_api_wrapper import CalenderAPIWrapper
from datetime import datetime, timedelta, timezone
from AssignmentEntry import AssignmentEntry

class CalenderEventGenerator:
    """
    必要な関数
    1. 課題の情報を1つ受け取って、締め切りの最大時間を取得する
    2. CalenderAPIWrapperを叩いて(0で取得した最大時間を関数の引数にする)
       空いている時間帯を取得する
    3. 空いている時間帯に課題を押し込むことを考える(最初の時間から5分ごとにごり押し)
    4. CalenderAPIWrapperを叩いて、課題をカレンダーに登録する
    """
    def __init__(self, creds):
        self.calendar = CalenderAPIWrapper(creds)
        self.start_time = datetime.now()

    def _get_max_due_date(self, event):
        """
        課題の一覧を受け取り、締め切り時間を取得する
        """
        original_datetime_str = event.dueDate
        original_datetime = datetime.strptime(original_datetime_str, "%Y-%m-%d %H:%M:%S")
        jst = timezone(timedelta(hours=9))
        original_datetime_jst = original_datetime.replace(tzinfo=jst)
        converted_datetime_str = original_datetime_jst.strftime("%Y-%m-%dT%H:%M:%S%z")
        return converted_datetime_str
    
    def _get_free_time(self, time_max):
        """
        空いている時間帯を取得する
        """
        time_dict = {}#空いている->0, 予定がある->1以上
        if time_max == None:
            schedule = self.calendar.read_calendar()
        else:
            schedule = self.calendar.read_calendar(time_max)

        # start と end を datetime オブジェクトに変換
        starttime_dt = datetime(*schedule["start_time"])
        self.start_time = starttime_dt
        endtime_dt = datetime(*schedule["end_time"]) + timedelta(days=1)

        # start から end までのすべての日付を取得し、for ループで処理
        current_date = starttime_dt
        while current_date <= endtime_dt:
            time_dict[current_date.strftime("%Y-%m-%d %H:%M:%S")] = 0
            current_date += timedelta(minutes=1)  # 1 分進める

        for event in schedule["events"]:
            # start と end を datetime オブジェクトに変換
            start_dt = datetime(*event["start"])
            start_dt = max(start_dt, starttime_dt)
            end_dt = datetime(*event["end"]) + timedelta(minutes=1)
            end_dt = min(end_dt, endtime_dt)
            if start_dt >= end_dt:
                continue
            time_dict[start_dt.strftime("%Y-%m-%d %H:%M:%S")] += 1
            time_dict[end_dt.strftime("%Y-%m-%d %H:%M:%S")] -= 1
        
        # start から end までのすべての日付を取得し、for ループで処理
        current_date = starttime_dt
        pre = 0
        while current_date <= endtime_dt:
            time_dict[current_date.strftime("%Y-%m-%d %H:%M:%S")] += pre
            pre = time_dict[current_date.strftime("%Y-%m-%d %H:%M:%S")]
            current_date += timedelta(minutes=1)  # 1 分進める
        return time_dict

    def _scheduling_event(self, event, time_dict):
        """
        課題を空いている時間帯に押し込む
        """
        calendar_event = {}
        calendar_event['summary'] = event.title
        calendar_event['description'] = f"{event.courseName}, {event.courseId}, {event.dueDate}"
        time_duration = event.duration  # Minで与えられる
        current_time = self.start_time
        while time_duration > 0:
            while time_dict[current_time.strftime("%Y-%m-%d %H:%M:%S")] != 0:
                current_time += timedelta(minutes=1)
            start = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")

            time_temp = 0
            while time_temp < time_duration and time_dict.get(current_time.strftime("%Y-%m-%d %H:%M:%S")) != None and time_dict[current_time.strftime("%Y-%m-%d %H:%M:%S")] == 0:
                time_temp += 1
                current_time += timedelta(minutes=1)

            if time_dict.get(current_time.strftime("%Y-%m-%d %H:%M:%S")) == None:
                return
            end = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")

            if time_temp >= 5 and (time_duration == time_temp or time_duration - time_temp >= 5):
                time_duration -= time_temp
                calendar_event['start'] = {}
                calendar_event['start']['dateTime'] = self.__convert_datetime(start)
                calendar_event['end'] = {}
                calendar_event['end']['dateTime'] = self.__convert_datetime(end)
                self.__write_event(calendar_event)

    def __write_event(self, event):
        """
        課題をカレンダーに登録する
        """
        print(event)
        self.calendar.write_calendar(event)

    def __convert_datetime(self, datetime_str):
        original_datetime_str = datetime_str
        original_datetime = datetime.strptime(original_datetime_str, "%Y-%m-%dT%H:%M:%S")
        original_datetime = original_datetime + timedelta(hours=9)
        jst = timezone(timedelta(hours=0))
        new_datetime = original_datetime.astimezone(jst)
        new_datetime_str = new_datetime.strftime("%Y-%m-%dT%H:%M:%S%z")
        return new_datetime_str

    def write_event_to_calendar(self, event):
        """
        課題をカレンダーに登録する
        """
        time_max = self._get_max_due_date(event)
        time_dict = self._get_free_time(time_max)
        self._scheduling_event(event, time_dict)


if __name__ == "__main__":
    calendar = CalenderEventGenerator(creds)
    event = AssignmentEntry(
        id="1",
        title="課題1",
        courseName="Google Classroom",
        courseId="1",
        dueDate="2024-05-20 23:59:59",
        duration=600,
    )
    calendar.write_event_to_calendar(event)
