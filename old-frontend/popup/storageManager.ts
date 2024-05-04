class Storage {

    save(key, value) {
        return new Promise((resolve, reject) => {
            chrome.storage.local.set({ [key]: value }, () => {
                resolve();
            });
        });
    }

    get(key) {
        return new Promise((resolve, reject) => {
            chrome.storage.local.get([key], (result) => {
                resolve(result[key]);
            });
        });
    }

    remove(key) {
        return new Promise((resolve, reject) => {
            chrome.storage.local.remove(key, () => {
                resolve();
            });
        });
    }

    clear() {
        return new Promise((resolve, reject) => {
            chrome.storage.local.clear(() => {
                resolve();
            });
        });
    }

}

const storage = new Storage();
