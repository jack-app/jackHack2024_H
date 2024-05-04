class Storage {

    save(key: string, value: string) {
        return new Promise((resolve, reject) => {
            chrome.storage.local.set({ [key]: value }, () => {
                resolve(null);
            });
        });
    }

    get(key: string) {
        return new Promise((resolve, reject) => {
            chrome.storage.local.get([key], (result) => {
                resolve(result[key]);
            });
        });
    }

    remove(key: string) {
        return new Promise((resolve, reject) => {
            chrome.storage.local.remove(key, () => {
                resolve(null);
            });
        });
    }

    clear() {
        return new Promise((resolve, reject) => {
            chrome.storage.local.clear(() => {
                resolve(null);
            });
        });
    }

}

export const storage = new Storage();
