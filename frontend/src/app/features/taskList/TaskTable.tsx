import TaskEntry from '../../api/task';

const TaskHeader = () => {
  return (
    <thead>
      <tr>
        <th>#</th>
        <th>課題名</th>
        <th>講義サイト</th>
        <th>締切日時</th>
        <th>カレンダーに登録</th>
      </tr>
    </thead>
  );
};

export type TaskRowProps = {
  task: TaskEntry;
  onClickRegister: (task: TaskEntry) => void;
};

const TaskRow = ({ task, onClickRegister, index }: TaskRowProps & { index: number }) => {
  const dueString = task.dueDate.toLocaleString();
  return (
    <tr>
      <td>{index}</td>
      <td>{task.title}</td>
      <td>{task.courseName}</td>
      <td>{dueString}</td>
      <td>
        <label className="toggle -withtext">
          <input onClick={() => onClickRegister(task)} type="checkbox" />
          <div></div>
        </label>
      </td>
    </tr>
  );
};

type TaskListProps = {
  taskList: TaskRowProps[];
};
export const TaskTable = ({ taskList }: TaskListProps) => {
  return (
    <>
      <h4 id="table">課題一覧</h4>

      <table className="table table-striped">
        <TaskHeader />
        <tbody>
          {taskList.map((task, idx) => (
            <TaskRow
              key={task.task.id}
              index={idx + 1}
              task={task.task}
              onClickRegister={task.onClickRegister}
            />
          ))}
        </tbody>
      </table>
    </>
  );
};
