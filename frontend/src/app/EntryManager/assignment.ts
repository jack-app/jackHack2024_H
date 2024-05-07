import { storage } from '../storageManager';
import { getAssignments } from '../api/assignment';
import TaskEntry from '../api/task';

export class AssignmentEntryManager {
  private _assignments: TaskEntry[];
  constructor() {
    this._assignments = [];
  }

  async init() {
    const assignmentsExists = await this._loadAssignments();
    if (!assignmentsExists) {
      this._fetchAssignments();
    }
  }

  async getAssignments() {
    const assignmentsExists = await this._loadAssignments();
    if (this._assignments.length || assignmentsExists) {
      return this._assignments;
    } else {
      this._fetchAssignments();
      return this._assignments;
    }
  }

  private async _fetchAssignments() {
    const assignments = await getAssignments();
    this._assignments = assignments;
    this._saveAssignments();
  }

  private async _saveAssignments() {
    // storageはpopup/storageManager.jsで定義されている
    await storage.save('assignments', JSON.stringify(this._assignments.map((a) => a.toJson())));
  }

  private async _loadAssignments() {
    const rawAssignments = (await storage.get('assignments')) as string | undefined;
    if (rawAssignments) {
      const assignments = JSON.parse(rawAssignments) as TaskEntryJSONType[];
      const parsed = assignments.map(
        (a) =>
          new TaskEntry(
            a.id,
            a.title,
            new Date(a.openTime),
            new Date(a.dueDate),
            a.courseName,
            a.courseId
          )
      );
      this._assignments = parsed;
      return true;
    } else {
      this._assignments = [];
      return false;
    }
  }
}

type TaskEntryJSONType = {
  id: string;
  title: string;
  openTime: string;
  dueDate: string;
  courseName: string;
  courseId: string;
};
