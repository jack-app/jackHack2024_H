const getRawAllAssignments = async () => {
    const response = await fetch("/direct/assignment/my.json");
    if (response.data["assignment_collection"] === undefined) {
        return [];
    }
    return response.data["assignment_collection"]
}

const getAssignments = async () => {
    const rawAssignments = await getRawAllAssignments()
    const courses = await getAllCourses()
    const assignments = rawAssignments.map((assignment) => {
        const course = courses.find((course) => course.id === assignment["context"])
        const assignmentEntry = new AssignmentEntry(assignment["entityId"], assignment["entityTitle"],
            new Date(assignment["dueTime"]), course.name, course.id)
        return assignmentEntry
    })
    return assignments
}

class AssignmentEntry extends TaskEntry {
    constructor(id, title, dueDate, courseName, courseId) {
        super(id, title, dueDate, courseName, courseId)
    }
}
