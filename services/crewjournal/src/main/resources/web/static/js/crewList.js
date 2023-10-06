//	Verify the same password_field1 and password_field2
function passwordControl(){
    let passwordFieldList = document.getElementsByClassName("password_field");
    if(passwordFieldList[0].value == passwordFieldList[1].value){
        alert("Confirmation sent to your e-mail. Please, check it.");
        return true;
    } else {
        alert("Password missmatches!");
        return false;
    }
}
