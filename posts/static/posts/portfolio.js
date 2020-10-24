function showEdit(ticker){
    var quantityCell = document.getElementById(ticker + "-q");
    var label = quantityCell.children[0];
    var input = quantityCell.children[1];

    var buttonCell = document.getElementById(ticker + "-b");
    var editButton = buttonCell.children[0];
    var cancelButton = buttonCell.children[1];
    var saveButton = buttonCell.children[2];

    label.style.display = "none";
    input.style.display = "inline";
    editButton.style.display = "none";
    cancelButton.style.display = "inline";
    saveButton.style.display = "inline";
}

function closeEdit(ticker){
    var quantityCell = document.getElementById(ticker + "-q");
    var label = quantityCell.children[0];
    var input = quantityCell.children[1];

    var buttonCell = document.getElementById(ticker + "-b");
    var editButton = buttonCell.children[0];
    var cancelButton = buttonCell.children[1];
    var saveButton = buttonCell.children[2];

    label.style.display = "inline";
    input.style.display = "none";
    editButton.style.display = "inline";
    cancelButton.style.display = "none";
    saveButton.style.display = "none";
}
