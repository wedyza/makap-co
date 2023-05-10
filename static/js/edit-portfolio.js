let tabs = document.querySelector(".tabs");
let tabHeader = tabs.querySelector(".tab-header");
let tabBody = tabs.querySelector(".tab-body");
let tabHeaders = tabHeader.querySelectorAll("div");

for(let i=0;i<tabHeaders.length;i++){
  tabHeaders[i].addEventListener("click",function(){
    tabHeader.querySelector(".active").classList.remove("active");
    tabHeaders[i].classList.add("active");
    tabBody.style.marginTop = `-${i*100}vh`;
  })
}