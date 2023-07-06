//update the path to the nav img
let navImage = document.querySelector(".the-user-profile-picture");
navImage.setAttribute('src', `${navImage.getAttribute('src').replace('../', '../../')}`);


//update the path to the chat images
let allImagesChats = document.querySelectorAll(".friend-chat-img");
for(let imgChat of allImagesChats){
    imgChat.setAttribute('src', `${imgChat.getAttribute('src').replace('../', '../../')}`);
}



//validate first name form before submission
function validateFirstNameForm(){
    let alertMSG = "";
    //check first name
    let firstNameTest = document.querySelector(".first_name").value.search(/^[A-Z][a-z]{1,10}/g);
    if (firstNameTest === -1){
        alertMSG += "<p>First name needs to be Up to 20 letters and The first letter needs to be capital letter!</p>";
    }
    return checkMsg(alertMSG);
}


//validate last name form before submission
function validateLastNameForm(){
    let alertMSG = "";
    //check last name
    let lastNameTest = document.querySelector(".last_name").value.search(/^[A-Z][a-z]{1,10}/g);
    if (lastNameTest === -1){
        alertMSG += "<p>Last name needs to be Up to 20 letters and The first letter needs to be capital letter!</p>";
    }
    return checkMsg(alertMSG);
}


//validate email form before submission
function validateEmailForm(){
    let alertMSG = "";
    //check email
    let emailInputValue = document.querySelector(".email").value;
    if(emailInputValue == ""){
        alertMSG += "<p>You can register only with gmail!</p>";
    }
    return checkMsg(alertMSG);
}


//validate password form before submission
function validatePasswordForm(){
    let alertMSG = "";
    //check password
    let passwordTest = document.querySelector(".password").value.search(/.{6,}/g);
    if (passwordTest === -1){
        alertMSG += "<p>Password must have six or more characters!</p>";
    }
    return checkMsg(alertMSG);
}


// chack msg
function checkMsg(msg){
    let divAlert = document.querySelector(".alert_mistake");
    if (msg != ""){
        divAlert.innerHTML = `<div class="alert alert-danger" role="alert">${msg}</div>`;
        return false;
    }
}


// picture
//display the picture and add remove button
let divRemove = document.querySelector(".remove");
let divImage = document.querySelector(".image");
const inputFile = document.querySelector("#formFile");
var uploadedFile = "";
inputFile.addEventListener("change", function(){
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        uploadedFile = reader.result;
        divImage.innerHTML = `<img id="image" src="${uploadedFile}" alt="" srcset="">`;
    });
    reader.readAsDataURL(this.files[0]);
    divRemove.innerHTML = `<button type="button" class="btn btn-outline-danger" onclick="clickRemove()">Remove</button>`;
})


//remove file and remove button remove
function clickRemove() {
    uploadedFile = ""
    inputFile.value = "";
    divImage.innerHTML = "";
    divRemove.innerHTML = "";
}

//validate picture form before submission
function validatePictureForm(){
    let alertMSG = "";
    //check password
    if ( inputFile.value === "" ){
        alertMSG += "<p>You have to upload image!</p>";
    }
    return checkMsg(alertMSG);
}

