var vid = document.getElementById("bgvid");
var pauseButton = document.querySelector("#polina button");

function vidFade() {
  vid.classList.add("stopfade");
}

vid.addEventListener('ended', function()
{
    vid.pause();
    vidFade();
});

pauseButton.addEventListener("click", function() {
    vid.classList.toggle("stopfade");
    vid.pause();
    pauseButton.innerHTML = "Processing...";
})