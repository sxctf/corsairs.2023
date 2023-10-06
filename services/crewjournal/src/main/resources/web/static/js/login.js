let login_form = document.getElementsByClassName("login_form")[0];
let pirate=null;
let pirates;
let sha256_field = null;
fetch('/api/pirates').then(response => response.json()).then(data => pirates = data);

function authenticatePirate(){
    hash_field = document.createElement("input");
    hash_field.id = "hash_field";
    hash_field.name = "hash_field";
    hash_field.value = "";
    hash_field.hidden = "yes";
    let login_field = login_form.querySelector("#login_field");
    let password_field = login_form.querySelector("#password_field");
    let login = login_field.value;
    let password = password_field.value;
    for(let p of pirates){
        if(p.login == login && p.password == password){
            pirate = p;
            login_form.appendChild(hash_field);
            return true;
        }
    }
    return false;
}

login_form.addEventListener("submit", function (e) {
//    e.preventDefault();
    if(authenticatePirate()){
        const passwordInput = pirate.login + pirate.password;
        hash_field.value = myWeakHash(passwordInput);
//        login_form.submit();
    } else {
        password_field.value = "";
//        return false;
    }
});

function myWeakHash(data)
{
    if (data.length == 0)
        return "";
    let bytes = data.split('').map(s => s.charCodeAt(0));
    let padding_length = (Math.floor(bytes.length/8) + 1) * 8 - bytes.length;
    for(let i = 0; i < padding_length; i++){
        bytes.push(bytes[i]);
    }
    let resultBytes = "CTF!B0dy".split('').map(s => s.charCodeAt(0));
    for (let i = 0; i < bytes.length / 8; i++) {
        for (let j = 0; j < 8; j++) {
            resultBytes[j] ^= bytes[i * 8 + j];
        }
    }
    const hashHex = resultBytes.map((b) => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}