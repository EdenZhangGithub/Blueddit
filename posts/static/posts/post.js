function toggleEdit(pk){
    var edit_form = document.getElementById("comment-" + pk);

    if(edit_form.style.display === "none"){
        edit_form.style.display = "block";
    }
    else{
        edit_form.style.display = "none";
    }
}
