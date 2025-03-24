let medioNavbar = document.getElementById("medioNavbar");
let bars = document.getElementById("bars");
let close =document.getElementById("close");
bars.addEventListener("click" , function(){
    medioNavbar.style.top="0";
})
close.addEventListener("click" , function(){
    medioNavbar.style.top="-100%";
})