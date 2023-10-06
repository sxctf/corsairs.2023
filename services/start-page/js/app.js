const sliderMain = new Swiper('.slider_main', {
    freeMode: true,
    centeredSlides: true,
    mousewheel: true,
    parallax: false,
    breakpoints: {
        0: {
            slidesPerView: 2.5,
            spaceBetween: 20
        },    
        680:{
            slidesPerView: 3.5,
            spaceBetween: 40
        }
    }
    
})

const sliderblock = new Swiper('.slider_block', {
    freeMode: true,
    breakpoints: {
        0: {
            slidesPerView: 2.5,
            spaceBetween: 20
        },    
        680:{
            slidesPerView: 3.5,
            spaceBetween: 40
        }
    }
    
})

const sliderBg = new Swiper('.slider_bg', {
    centeredSlides: true,
    parallax: false,
    slidesPerView: 3.5,
    spaceBetween: 40
    
})

// sliderMain.controller.control = sliderBg

document.querySelectorAll('.slider__item').forEach(item => {
    item.addEventListener('click', event => {
        document.querySelector('.slider_main').classList.toggle('opened')
        item.classList.toggle('opened');
        if (item.className.includes("opened")) {
            item.firstElementChild.style.display='block';  
            item.lastElementChild.style.display='block';
        
        } else {
            item.firstElementChild.style.display='none';
            item.lastElementChild.style.display='none';
        }
    })
});

document.querySelectorAll('.slider__item2').forEach(item => {
    item.addEventListener('click', event => {
        item.classList.toggle('opened');
        if (item.className.includes("opened")) {
            
            item.firstElementChild.style.display='block';  
            item.lastElementChild.style.display='block';
        
        } else {
            item.firstElementChild.style.display='none';
            item.lastElementChild.style.display='none';
        }
    })
});



let ports = ['7000', '8000', '9000', '5000', '8080', '4000'];
let target = String(window.location)   

document.getElementById('1').addEventListener('click', event =>{
    window.location.href = target.substring(0, target.length - 1) + ":" + String(ports[0]);
})

document.getElementById('2').addEventListener('click', event =>{
    window.location.href = target.substring(0, target.length - 1) + ":" + String(ports[1]);
})

document.getElementById('3').addEventListener('click', event =>{
    window.location.href = target.substring(0, target.length - 1) + ":" + String(ports[2]);
})

document.getElementById('4').addEventListener('click', event =>{
    window.location.href = target.substring(0, target.length - 1) + ":" + String(ports[3]);
})

document.getElementById('5').addEventListener('click', event =>{
    window.location.href = target.substring(0, target.length - 1) + ":" + String(ports[4]);
})

document.getElementById('6').addEventListener('click', event =>{
    window.location.href = target.substring(0, target.length - 1) + ":" + String(ports[5]);
})

let desc = document.querySelector('.description')
sliderMain.on('slideChange', e => {
    sliderMain.activeIndex > 0 ? desc.classList.add('hidden') : desc.classList.remove('hidden') 
})
