const getRawAllAssignments = async () => {
    const data = await fetcher.fetch("/direct/assignment/my.json");
    if (data["assignment_collection"] === undefined) {
        return [];
    }
    return data["assignment_collection"]
}

const getAssignments = async () => {
    const rawAssignments = await getRawAllAssignments()
    const favoriteCourses = await getFavoriteCoursesIds()

    const courses = favoriteCourses.map(async (courseId) => {
        const course = await getRawCourse(courseId)
        return new CourseEntry(course["entityId"], course["entityTitle"])
    })

    const assignments = rawAssignments.map((assignment) => {
        var course = courses.find((course) => course.id === assignment["context"])
        if (course === undefined) {
            course = new CourseEntry("unknown", "unknown")
        }
        const assignmentEntry = new AssignmentEntry(assignment["entityId"], assignment["entityTitle"], assignment["dueTimeString"], course.name, course.id)
        return assignmentEntry
    })
    return assignments
}

class AssignmentEntry extends TaskEntry {
    constructor(id, title, dueDate, courseName, courseId) {
        super(id, title, dueDate, courseName, courseId)
    }
}
