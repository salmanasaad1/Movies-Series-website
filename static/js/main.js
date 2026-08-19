
var swiper = new Swiper(".popular-content", {
    slidesPerView: 1,
    spaceBetween: 10,
    autoplay: {
        delay: 5500,
        desableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev"
    },
    breakpoints:{
        280:{
            slidesPerView: 1,
            spaceBetween: 10,
        },
        320:{
            slidesPerView: 2,
            spaceBetween: 10,
        },
        510:{
            slidesPerView: 2,
            spaceBetween: 10,
        },
        758:{
            slidesPerView: 3,
            spaceBetween: 15,
        },
        900:{
            slidesPerView: 4,
            spaceBetween: 20,
        },
    },
});
//---------------------rating------------------------------------->
//---------------------rating------------------------------------->

// Show Video
let playButton = document.querySelector(".play-movie")
let playButtont = document.querySelector(".play-movie-t")


let video = document.querySelector(".video-container")
let videot = document.querySelector(".video-containert")


let myvideo = document.querySelector("#myvideo")
let myvideot = document.querySelector("#myvideot")


let closebtn = document.querySelector(".close-video")
let closebtnt = document.querySelector(".close-video-t")



playButton.onclick = () => {
    video.classList.add("show-video")
    // Auto Play When Click On Button
    myvideo.play();
};
closebtn.onclick = () => {
    video.classList.remove("show-video")
    // Pause On Close Video
    myvideo.pause();
};
playButtont.onclick = () => {
    videot.classList.add("show-video")
    // Auto Play When Click On Button
    myvideot.play();
};
closebtnt.onclick = () => {
    videot.classList.remove("show-video")
    // Pause On Close Video
    myvideot.pause();
};

