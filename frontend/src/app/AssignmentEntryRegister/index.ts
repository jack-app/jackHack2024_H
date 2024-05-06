import TaskEntry from '../api/task';
import { AssignmentEntryManager } from '../EntryManager/assignment';
import { storage } from '../storageManager';
import AssignmentEntry from './assignment';

class RequiredAssignmentEntry {
  readonly id: string;
  readonly title: string;
  readonly dueDate: string;
  readonly courseName: string;
  readonly courseId: string;
  readonly duration: number;
  constructor(
    id: string,
    title: string,
    dueDate: Date,
    courseName: string,
    courseId: string,
    duration: number
  ) {
    this.id = id;
    this.title = title;
    this.courseName = courseName;
    this.courseId = courseId;
    // if (dueDate < new Date()){
    //   dueDate = new Date( Date.now() + 1000 * 60 * 60 * 24 );
    // }
    // this.dueDate = `${dueDate.getFullYear()}-${dueDate.getMonth() + 1}-${dueDate.getDate()} ${dueDate.getHours()}:${dueDate.getMinutes()}:${dueDate.getSeconds()}`;
    this.dueDate = dueDate.toJSON();
    this.duration = duration;
  }
  toJson() {
    return {
      id: this.id,
      title: this.title,
      courseName: this.courseName,
      courseId: this.courseId,
      dueDate: this.dueDate,
      duration: this.duration,
    };
  }
}

export default class AssignmentEntryRegister {
  readonly manager = new AssignmentEntryManager();
  tasks: TaskEntry[];
  settings: { defaultTime: number };
  initialized = false;
  constructor() {
    this.tasks = [];
    this.settings = { defaultTime: 0 };
  }

  async init() {
    await this.manager.init();
    this.tasks = await this.manager.getAssignments();
    const defaultTime = (await storage.get('defaultTime')) as string;
    this.settings = {
      defaultTime: defaultTime ? parseInt(defaultTime) : 0,
    };
    this.initialized = true;
  }

  async regist(): Promise<boolean> {
    if (!this.initialized) {
      await this.init();
    }

    const assignments = this.tasks.map(
      (task) => new AssignmentEntry(task, this.settings.defaultTime)
    );
    const lastUpdateDateTime = await this.getLastUpdateDateTime();
    const resps = await Promise.all(
      assignments
        .filter((assignment) => !assignment.isRegistered(lastUpdateDateTime))
        .map(async (assignment) => {
          return await AssignmentEntryRegister.register(assignment);
        })
    );
    await this.setLastUpdateDateTime(new Date());
    return resps.every((resp) => resp);
  }

  async getLastUpdateDateTime(): Promise<Date> {
    const datetimeString = (await storage.get('lastUpdateTime')) as string;
    return new Date(datetimeString);
  }

  async setLastUpdateDateTime(date: Date) {
    await storage.save('lastUpdateTime', date.toISOString());
  }

  static async register(assignment: AssignmentEntry): Promise<number> {
    const json = assignment.toJson();
    const body = new RequiredAssignmentEntry(
      json.id,
      json.title,
      json.dueDate,
      json.courseName,
      json.courseId,
      json.duration ? json.duration : 60 //なぜかnullが入る
    );
    console.log(JSON.stringify(body.toJson()));
    const response = await fetch('https://jack.hbenpitsu.net/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body.toJson()),
    });
    console.log(response);
    console.log(response.status);
    console.log((await response.json()).msg);
    return response.status;
  }
}
