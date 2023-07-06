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


//validate form before submission
function validateForm(){
    let divAlert = document.querySelector(".alert_mistake");
    let alertMSG = "";
    //check first name
    let firstNameTest = document.querySelector(".first_name").value.search(/^[A-Z][a-z]{1,10}/g);
    if (firstNameTest === -1){
        alertMSG += "<p>First name needs to be Up to 20 letters and The first letter needs to be capital letter!</p>";
    }
    //check last name
    let lastNameTest = document.querySelector(".last_name").value.search(/^[A-Z][a-z]{1,10}/g);
    if (lastNameTest === -1){
        alertMSG += "<p>Last name needs to be Up to 20 letters and The first letter needs to be capital letter!</p>";
    }
    //check birthday
    let birthdayValue = document.querySelector(".birthday").value.split('-');
    let date = new Date();
    if( ( birthdayValue == "" ) || ( date.getFullYear() - parseInt(birthdayValue[0]) < 18 ) || ( date.getFullYear() - parseInt(birthdayValue[0]) === 18 && parseInt(birthdayValue[1]) > date.getMonth() + 1 ) || ( date.getFullYear() - parseInt(birthdayValue[0]) === 18 && parseInt(birthdayValue[1]) === date.getMonth() + 1 && parseInt(birthdayValue[2]) > date.getDate() ) ){
        alertMSG += "<p>Age eighteen or older!</p>";
    }
    //check gender
    let maleButton = document.querySelector(".male");
    let femaleButton = document.querySelector(".female");
    if(maleButton.checked == false && femaleButton.checked == false){
        alertMSG += "<p>You must select a gender!</p>";
    }
    //check email
    let emailInputValue = document.querySelector(".email").value;
    if(emailInputValue == ""){
        alertMSG += "<p>You can register only with gmail!</p>";
    }
    //check password
    let passwordTest = document.querySelector(".password").value.search(/.{6,}/g);
    if (passwordTest === -1){
        alertMSG += "<p>Password must have six or more characters!</p>";
    }
    if (alertMSG != ""){
        divAlert.innerHTML = `<div class="alert alert-danger" role="alert">${alertMSG}</div>`;
        return false;
    }
}







