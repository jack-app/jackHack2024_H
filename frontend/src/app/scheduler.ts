import { auto } from '@twind/core';
import { storage } from './storageManager';
import TaskEntry from './api/task';

export async function RegisterAssignmentsOnLoad() {
    let autoSave = await storage.get('autoSave');
    autoSave = autoSave === 'true' ? true : false;

    if (autoSave) {
        // Secsion manager: add all tasks
    }
}

export async function RegisterAssignmentOnButtonClicked(task: TaskEntry) {
    // Secsion manager: add task
}
