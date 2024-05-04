// TODO: 型を追加する
const getRawAllAssignments = async (): Promise<any> => {
  const data = await fetcher.fetch("/direct/assignment/my.json");
  if (data["assignment_collection"] === undefined) {
    return [];
  }
  return data["assignment_collection"];
};

const getAssignments = async (): Promise<AssignmentEntry> => {
  const rawAssignments = await getRawAllAssignments();
  const favoriteCourses = await getFavoriteCoursesIds();

  const courses = await Promise.all(
    favoriteCourses.map(async (courseId: string) => {
      const course = await getRawCourse(courseId);
      console.log("course", course);
      return new CourseEntry(course["entityId"], course["entityTitle"]);
    })
  );

  // TODO: 型を追加する
  const assignments = rawAssignments.map((assignment: any) => {
    var course = courses.find((course) => course.id === assignment["context"]);
    if (course === undefined) {
      course = new CourseEntry("unknown", "unknown");
    }
    const assignmentEntry = new AssignmentEntry(
      assignment["entityId"],
      assignment["entityTitle"],
      assignment["dueTimeString"],
      course.name,
      course.id
    );
    return assignmentEntry;
  });
  return assignments;
};

class AssignmentEntry extends TaskEntry {
  constructor(
    id: string,
    title: string,
    dueDate: Date,
    courseName: string,
    courseId: string
  ) {
    super(id, title, dueDate, courseName, courseId);
  }
}
