//validate form before submission(search)
function validateFormSearch(){
    searchValue = document.querySelector(".search-input").value;
    if(searchValue.length === 0){
        return false
    }
}