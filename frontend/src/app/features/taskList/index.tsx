import { useState, useEffect } from 'react';
import { TaskTable, TaskRowProps } from './TaskTable';
import TaskEntry from '../../api/task';
import { AssignmentEntryManager } from '../../EntryManager/assignment';
import AssignmentEntry from '../../AssignmentEntryRegister/assignment';
import { storage } from '../../storageManager';
import AssignmentEntryRegister from '../../AssignmentEntryRegister';
import { authenticate } from '../../tokenHandler';

export const TaskList = () => {
  const [assignments, setAssignments] = useState<TaskEntry[]>([]);

  const assignmentEntryManager = new AssignmentEntryManager();
  useEffect(() => {
    // Tips: useEffect内でasync関数を直接呼ぶことはできないため、関数を定義して呼び出す
    // https://zenn.dev/syu/articles/b97fb155137d1f
    (async () => {
      assignmentEntryManager.init();
      const loaded = await assignmentEntryManager.getAssignments();
      setAssignments(loaded);
    })();
  }, []);

  // TODO: TACTからのデータを取得する
  const taskList: TaskRowProps[] = assignments.map((assignment) => {
    return {
      task: assignment,
      onClickRegister: async (task) => {
        let duration = 60;
        const defalutTime = await storage.get('defaultTime');
        if (defalutTime) {
          duration = parseInt(String(defalutTime));
        }
        const assignmentEntry = new AssignmentEntry(task, duration);
        const status = await AssignmentEntryRegister.register(assignmentEntry);
        if (status == 200) {
          alert('登録しました');
        } else if (status == 401) {
          alert('登録に失敗しました。認証が完了しているか確認してください。');
          authenticate();
        } else {
          alert('登録に失敗しました。');
        }
      },
    };
  });

  //   const exampleTasks: TaskRowProps[] = [
  //     {
  //       task: new TaskEntry('1', '課題1', new Date(), '講義1', '1'),
  //       onClickRegister: (task) => {
  //         // TODO: APIに登録する処理を書く
  //         console.log(task);
  //       },
  //     },
  //     {
  //       task: new TaskEntry('2', '課題2', new Date(), '講義2', '2'),
  //       onClickRegister: (task) => {
  //         // TODO: APIに登録する処理を書く
  //         console.log(task);
  //       },
  //     },
  //   ];
  return (
    <>{assignments.length === 0 ? <p>課題がありません</p> : <TaskTable taskList={taskList} />}</>
  );
};
