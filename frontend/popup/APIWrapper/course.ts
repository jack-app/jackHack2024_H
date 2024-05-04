const getFavoriteCoursesIds = async (): Promise<string[]> => {
  // TODO: 型を追加する
  const data = await fetcher.fetch("/portal/favorites/list");
  console.log(data);
  return data["favoriteSiteIds"];
};

// response.data
//  {
//     "favoriteSiteIds": [
//         "n_2024_A_ZZ2404090014",
//         "n_2024_1002250",
//         "n_2024_1002240",
//         "n_2024_1001329",
//         "n_2024_1001209",
//         "n_2024_1001119",
//         "n_2024_1001069",
//         "n_9999_Z_ZZ333333",
//         "n_2023_A_ZZ2304060013",
//         "n_2023_T_102305080003"
//     ],
//     "autoFavoritesEnabled": true
// }

const getRawCourse = async (courseId: string) => {
  // TODO: 型を追加する
  const data = await fetcher.fetch(`/direct/site/${courseId}.json`);
  return data;
};

const getAllCourses = async (): Promise<CourseEntry[]> => {
  // TODO: 型を追加する
  const data = await fetcher.fetch("/direct/site.json");
  if (data["site_collection"] === undefined) {
    return [];
  }

  // TODO: 型を追加する
  const courseList = data["site_collection"].map((course: any) => {
    return new CourseEntry(course["entityId"], course["entityTitle"]);
  });
  return courseList;
};

class CourseEntry {
  readonly id: string;
  readonly name: string;
  constructor(id: string, name: string) {
    this.id = id;
    this.name = name;
  }
}
