const menuToogle = document.querySelector('.menuToogle');
const navigation = document.querySelector('.navigation');

menuToogle.onclick = () => {
    navigation.classList.toggle('open');
}

const list = document.querySelectorAll('.list');



function activeLink() {
    list.forEach((item) => item.classList.remove('active'));
    console.log(this);
    this.classList.add('active');
}

list.forEach((item) => item.addEventListener('click', activeLink));