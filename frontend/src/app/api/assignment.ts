import CourseEntry, { getFavoriteCoursesIds, getRawCourse } from './course';
import { fetcher } from './fetcher';
import TaskEntry from './task';

// TODO: 型を追加する
export const getRawAllAssignments = async (): Promise<any> => {
  const data = await fetcher.fetch('/direct/assignment/my.json');
  if (data['assignment_collection'] === undefined) {
    return [];
  }
  return data['assignment_collection'];
};

export const getAssignments = async (): Promise<TaskEntry[]> => {
  const rawAssignments = await getRawAllAssignments();
  const favoriteCourses = await getFavoriteCoursesIds();

  const courses = await Promise.all(
    favoriteCourses.map(async (courseId: string) => {
      const course = await getRawCourse(courseId);
      console.log('course', course);
      return new CourseEntry(course['entityId'], course['entityTitle']);
    })
  );

  // TODO: 型を追加する
  const assignments = rawAssignments.map((assignment: any) => {
    let course = courses.find((course) => course.id === assignment['context']);
    if (course === undefined) {
      course = new CourseEntry('unknown', 'unknown');
    }
    const tasks = new TaskEntry(
      assignment['entityId'],
      assignment['entityTitle'],
      // new Date(assignment['openTime']),
      new Date(assignment['dueTime']),
      course.name,
      course.id
    );
    return tasks;
  });
  return assignments;
};
