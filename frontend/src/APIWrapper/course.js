const getFavoriteCoursesId = async () => {
    const response = await fetch('/portal/favorites/list');
    return response.data["favoriteSiteIds"];
}

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


const getAllCourses = async () => {
    const response = await fetch("/direct/site.json");
    if (response.data["site_collection"] === undefined) {
        return [];
    }
    const courseList = response.data["site_collection"].map((course) => {
        return new CourseEntry(course["entityId"], course["entityTitle"]);
    })
    return courseList;
}

class CourseEntry {
    constructor(id, name) {
        this.id = id;
        this.name = name;
    }
}
