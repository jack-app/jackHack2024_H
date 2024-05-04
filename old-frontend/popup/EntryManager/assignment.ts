import { getAssignments } from "../"
class AssignmentEntryManager {
    private _assignments: AssignmentEntry[];
    constructor() {
        this._assignments = [];
    }

    async init() {
        const assignmentsExists = await this._loadAssignments();
        console.log(assignmentsExists);
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

    async _fetchAssignments() {
        const assignments = await getAssignments();
        console.log(assignments);
        this._assignments = assignments;
        this._saveAssignments();
    }

    async _saveAssignments() {
        // storageはpopup/storageManager.jsで定義されている
        await storage.save("assignments", this._assignments);
    }

    async _loadAssignments() {
        const assignments = await storage.get("assignments");
        if (assignments.length) {
            this._assignments = assignments;
            return true;
        } else {
            this._assignments = [];
            return false;
        }
    }
}