let playButtone = document.querySelector(".play-movie-e")
let videoe = document.querySelector(".video-container-e")
let myvideoe = document.querySelector("#myvideoe")
let closebtne = document.querySelector(".close-video-e")

playButtone.onclick = () => {
    videoe.classList.add("show-videoe")
    // Auto Play When Click On Button
    myvideoe.play();
};

closebtne.onclick = () => {
    videoe.classList.remove("show-videoe")
    // Pause On Close Video
    myvideoe.pause();
};