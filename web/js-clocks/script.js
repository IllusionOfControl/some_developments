let hr = document.getElementById("hr")
let mn = document.querySelector("#mn");
let sc = document.querySelector("#sc");

const setAnalogClock = () => {
    let day = new Date();
    let hh = day.getHours() * 30;
    let mm = day.getMinutes() * 6;
    let ss = day.getSeconds() * 6;
    
    hr.style.transform = `rotateZ(${hh+(mm/12)}deg)`;
    mn.style.transform = `rotateZ(${mm}deg)`;
    sc.style.transform = `rotateZ(${ss}deg)`;
}

const setDigitalClock = () => {
    let now = new Date();
    let hh = document.getElementById("hours");
    let mm = document.getElementById("minutes");
    let ss = document.getElementById("seconds");
    let ampm = document.getElementById("ampm");

    hh.innerHTML = (now.getHours() > 12 ? now.getHours() - 12 : now.getHours()).toString().padStart(2, '0');
    mm.innerHTML = now.getMinutes().toString().padStart(2, '0');
    ss.innerHTML = now.getSeconds().toString().padStart(2, '0');
    ampm.innerHTML = (now.getHours() > 12 ? 'PM' : 'AM')
}

setInterval(() => {
    setAnalogClock();
    setDigitalClock();
}, 500);
