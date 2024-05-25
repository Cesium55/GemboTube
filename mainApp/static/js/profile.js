
let uploading = 0


function editAvatar(event){

    fr = document.getElementById("avatarForm")

    if (uploading == 0){
        fr.style.display = "block"
        uploading = 1
    }
    else if(uploading == 1){
        fr.style.display = "none"
        uploading = 0
    }
    else {

    }
}