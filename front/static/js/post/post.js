// show tags tags New comment
function addTagsNewComment(){
    let allTagsSpan= document.querySelector(".all-tags-comment");
    allTagsSpan.innerHTML = "";
    let allCheckBoxs = document.querySelectorAll(".checkbox-friend-comment");
    for(let k = 0; k < allCheckBoxs.length; k++){
        if (allCheckBoxs[k].checked == true){
            allTagsSpan.innerHTML += `@${allCheckBoxs[k].value.split(" | ")[0]} `;
        }
    }
}

//validate form before submission(new comment form)
function validateFormComment(){
    newCommentTextInputValue = document.querySelector(".new-comment-text-input").value;

    if(newCommentTextInputValue.length === 0){
        document.querySelector(".alert_mistake_new_comment").innerHTML = `<div class="alert alert-danger" role="alert">You must have a text!</div>`;
        return false
    }
}

// width of the td with the pic and name in comments
document.querySelector(".td-comment-pic-and-name").style.width = `${50 + (document.querySelector(".h").innerHTML.length * 10) + 5}px`;

