function deleteNote(noteId){
    console.log("DELETED")
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({noteId: noteId})
        ,}).then((_res) => {
            window.location.href ="/";
        });
}