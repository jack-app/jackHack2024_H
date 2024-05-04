document.getElementById("tataku").addEventListener("click", async () => {
    getAssignments().then((data) => {
        document.getElementById("results").innerText = "";
        for (let i = 0; i < data.length; i++) {
            document.getElementById("results").innerText += data[i].title + "\n";
        }
    })
});
