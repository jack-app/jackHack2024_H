export default class TaskEntry {
  readonly id: string;
  readonly title: string;
  readonly dueDate: Date;
  readonly courseName: string;
  readonly courseId: string;
  constructor(id: string, title: string, dueDate: Date, courseName: string, courseId: string) {
    this.id = id;
    this.title = title;
    this.courseName = courseName;
    this.courseId = courseId;
    this.dueDate = dueDate;
  }
  toJson() {
    return {
      id: this.id,
      title: this.title,
      dueDate: this.dueDate,
      courseName: this.courseName,
      courseId: this.courseId,
    };
  }
}
