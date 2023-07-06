// add pictures
const fileInput = document.getElementById('file-input');
const imageContainer = document.getElementById('image-container');

let images = [];
let allPictures = [];

// Event listener for when a file is selected
fileInput.addEventListener('change', (event) => {
  const files = event.target.files;
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    allPictures.push(file);
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      images.push(reader.result);
      displayImages();
    }
  }
});

// Function to display images
function displayImages() {
  imageContainer.innerHTML = '';
  for (let i = 0; i < images.length; i++) {
    const imgDiv = document.createElement('div');
    imageContainer.appendChild(imgDiv);
    imgDiv.className = "img-box col-lg-2 col-md-3 col-sm-4";
    const image = document.createElement('img');
    image.className = 'post-images-display';
    image.src = images[i];
    imgDiv.appendChild(image);
    imgDiv.appendChild(document.createElement('br'));
    const removeBtn = document.createElement('button');
    removeBtn.innerText = 'Remove';
    removeBtn.className = 'btn btn-danger remove-picture';
    removeBtn.addEventListener('click', () => {
      images.splice(i, 1);
      allPictures.splice(i, 1);
      displayImages();
    });
    imgDiv.appendChild(removeBtn);
  }
  const newFileList = new DataTransfer();
  for(let j = 0; j < allPictures.length; j++){
    newFileList.items.add(allPictures[j]);
  }
  fileInput.files = newFileList.files;
}

// Event listener for remove all button
function removeAllPictures(){
  images = [];
  allPictures = [];
  fileInput.value = "";
  displayImages();
}



//validate form before submission(new post form)
function validateFormPost(){
    newPostTextInputValue = document.querySelector(".new-post-text-input").value;

    if(newPostTextInputValue.length === 0){
        document.querySelector(".alert_mistake_new_post").innerHTML = `<div class="alert alert-danger" role="alert">You must have a text!</div>`;
        return false
    }
}


// show tags tags New post
function addTagsNewPost(){
    let allTagsParagraph = document.querySelector(".all-tags");
    allTagsParagraph.innerHTML = "";
    let allCheckBoxs = document.querySelectorAll(".checkbox-friend");
    for(let k = 0; k < allCheckBoxs.length; k++){
        if (allCheckBoxs[k].checked == true){
            allTagsParagraph.innerHTML += `@${allCheckBoxs[k].value.split(" | ")[0]} `;
        }
    }
}