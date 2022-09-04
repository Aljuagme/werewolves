function addPlayerListElement(){
    let listElement = document.createElement("li")

    let textElement = document.createElement("input")
    textElement.setAttribute("type", "text")
    textElement.setAttribute("name", "players")
    textElement.setAttribute("placeholder", "Add player..")

    let buttonElement = document.createElement("input")
    buttonElement.setAttribute("type", "button")
    buttonElement.setAttribute("value", "X")
    buttonElement.setAttribute("onclick", "removePlayerListElement(this)")
    buttonElement.classList.add("remove_player_button")

    listElement.appendChild(textElement)
    listElement.appendChild(buttonElement)

    let parentListTag = document.getElementById("players")
    parentListTag.appendChild(listElement)
}

function removePlayerListElement(element){
    element.parentElement.remove();
}