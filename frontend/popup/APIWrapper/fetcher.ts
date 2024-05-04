class apiFetcher {
    constructor(baseUrl = "https://tact.ac.thers.ac.jp") {
        this.baseUrl = baseUrl;
    }
    async fetch(path) {
        if (path[0] !== "/") {
            throw new Error("Path must start with /");
        }
        const response = await fetch(this.baseUrl + path);
        const data = await response.json();
        return data;
    }
}
const fetcher = new apiFetcher();