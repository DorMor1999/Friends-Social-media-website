//update the path to the nav img
let navImage = document.querySelector(".the-user-profile-picture");
navImage.setAttribute('src', `${navImage.getAttribute('src').replace('../', '../../')}`);


//update the path to the chat images
let allImagesChats = document.querySelectorAll(".friend-chat-img");
for(let imgChat of allImagesChats){
    imgChat.setAttribute('src', `${imgChat.getAttribute('src').replace('../', '../../')}`);
}

