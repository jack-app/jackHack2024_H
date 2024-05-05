document.getElementById("tataku").addEventListener("click", async () => {
    const assignmentManager = new AssignmentEntryManager();
    await assignmentManager.init();
    const assignments = await assignmentManager.getAssignments();
    console.log(assignments);
});
