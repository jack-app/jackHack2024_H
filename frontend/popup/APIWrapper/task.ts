class TaskEntry {
  readonly id: string;
  readonly title: string;
  readonly dueDate: Date;
  readonly courseName: string;
  readonly courseId: string;
  constructor(
    id: string,
    title: string,
    dueDate: Date,
    courseName: string,
    courseId: string
  ) {
    this.id = id;
    this.title = title;
    this.courseName = courseName;
    this.courseId = courseId;
    this.dueDate = dueDate;
  }
}
