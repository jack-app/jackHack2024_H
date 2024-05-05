import TaskEntry from '../api/task';

export default class AssignmentEntry {
  task: TaskEntry;
  duration: number;
  constructor(task: TaskEntry, duration: number) {
    this.task = task;
    this.duration = duration;
  }
  toJson() {
    return {
      ...this.task.toJson(),
      duration: this.duration,
    };
  }
}
