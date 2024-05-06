import TaskEntry from '../api/task';
import { AssignmentEntryManager } from '../EntryManager/assignment';
import { storage } from '../storageManager';
import AssignmentEntry from './assignment';

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

  async regist() {
    if (!this.initialized) {
      await this.init();
    }

    const assignments = this.tasks.map(
      (task) => new AssignmentEntry(task, this.settings.defaultTime)
    );
    const resps = await Promise.all(
      assignments.map(async (assignment) => {
        const response = await fetch('https://jack.hbenpitsu.net/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ assignment: assignment.toJson() }),
        });
        return response.ok;
      })
    );
    return resps.every((resp) => resp);
  }
}
