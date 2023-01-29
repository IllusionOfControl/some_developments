const cnv = document.querySelector(`canvas`);
const ctx = cnv.getContext(`2d`);

const config = {
  orbsCount   : 400,
  minVelocity : 0.2,
  ringsCount  : 10,
};

const settings = {
  canvas_w: 0,
  canvas_h: 0,
  center_x: 0,
  center_y: 0,
  parallax_h: 0,
  parallax_w: 0,
  background: 2
}

const mouse = {
  x: 0,
  y: 0
}


let orbsList = [];
let backgrounds = [];


class Orb {
  constructor() {
    this.size     = Math.random() * 5 + 2;
    this.angle    = Math.random() * 360;
    this.radius   = (Math.random() * config.ringsCount | 0) * settings.parallax_h / config.ringsCount;
    this.impact   = this.radius / settings.parallax_h;
    this.velocity = config.minVelocity + Math.random() * config.minVelocity + this.impact;
  }

  refresh() {
    let radian    = this.angle * Math.PI  / 180;

    let cos       = Math.cos(radian);
    let sin       = Math.sin(radian);

    let offset_x   = cos * settings.parallax_w * this.impact;
    let offset_y   = sin * settings.parallax_w * this.impact;

    let parallax_x  = mouse.x / settings.canvas_w * 2 - 1;
    let parallax_y  = mouse.mouse_y / settings.canvas_h;

    let x         = settings.center_x + cos * (settings.parallax_h + this.radius) + offset_x;
    let y         = settings.center_y + sin * (settings.parallax_h + this.radius) - offset_y * parallax_y - parallax_x * offset_x;

    let distToCenter   = Math.hypot(x - settings.center_x, y - settings.center_y);
    let distToMouse   = Math.hypot(x - mouse.x, y - mouse.mouse_y);

    let optic     = sin * this.size * this.impact * .7;
    let mEffect   = distToMouse <= 50 ? (1 - distToMouse / 50) * 25 : 0;
    let size      = this.size + optic + mEffect;

    let h         = this.angle;
    let s         = 100;
    let l         = (1 - Math.sin(this.impact * Math.PI)) * 90 + 10;
    let color     = `hsl(${h}, ${s}%, ${l}%)`;

    if (distToCenter > settings.parallax_h - 1 || sin > 0) {
      ctx.strokeStyle = ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, size, 0, 2 * Math.PI);
      distToMouse <= 50 ? ctx.stroke() : ctx.fill();
    }

    this.angle = (this.angle - this.velocity) % 360;
  }
}


const createStardust = () => {
  for (let i = 0 ; i < config.orbsCount ; i++) {
    orbsList.push( new Orb() );
  }
}

const nextBackground = () => {
  settings.background = settings.background + 1 === backgrounds.length ? 0 : settings.background + 1;
  console.log(`Next! ${settings.background}`)
  console.log(settings.background + 1 === backgrounds.length)
}

const registerEventHandlers = () => {
  cnv.addEventListener(`mousemove`, e => {
    mouse.x = e.clientX - cnv.getBoundingClientRect().left;
    mouse.mouse_y = e.clientY - cnv.getBoundingClientRect().top;
  });
  window.addEventListener(`keydown`, e => {
    if (e.key === 's') nextBackground();

  });
  window.addEventListener(`resize`, resize);
}

const createBackgrounds = () => {
  let bg1 = ctx.createRadialGradient(settings.center_x, settings.center_y, 0, settings.center_x, settings.center_y, settings.center_x);
  bg1.addColorStop(0, `rgb(10, 10, 10)`);
  bg1.addColorStop(.5, `rgb(10, 10, 20)`);
  bg1.addColorStop(1, `rgb(30, 10, 40)`);
  backgrounds.push(bg1)
  
  let bg2 = ctx.createRadialGradient(settings.center_x, settings.center_y, 0, settings.center_x, settings.center_y, settings.center_x);
  bg2.addColorStop(0, `rgb(255, 255, 255)`);
  bg2.addColorStop(.15, `rgb(255, 255, 255)`);
  bg2.addColorStop(.16, `rgb(255, 200, 0)`);
  bg2.addColorStop(.23, `rgb(255, 0, 0)`);
  bg2.addColorStop(.45, `rgb(255, 0, 25)`);
  bg2.addColorStop(.85, `rgb(9, 9, 25)`);
  bg2.addColorStop(1, `rgb(0, 0, 20)`);
  backgrounds.push(bg2)

  let bg3 = ctx.createRadialGradient(settings.center_x, settings.center_y, 0, settings.center_x, settings.center_y, settings.center_x);
  bg3.addColorStop(0, `rgb(0, 0, 0)`);
  bg3.addColorStop(0.14, `rgb(0, 0, 20)`);
  bg3.addColorStop(.17, `rgb(220, 100, 100)`);
  bg3.addColorStop(.23, `rgb(140, 0, 0)`);
  bg3.addColorStop(.35, `rgb(100, 0, 25)`);
  bg3.addColorStop(1, `rgb(30, 10, 40)`);
  backgrounds.push(bg3)
}

const resize = () => {
  settings.canvas_w = cnv.width  = innerWidth;
  settings.canvas_h = cnv.height = innerHeight;
  settings.center_x = settings.canvas_w * .5;
  settings.center_y = settings.canvas_h * .5;
  settings.parallax_h = settings.center_y * .4;
  settings.parallax_w = settings.center_x * .4;

  mouse.x = settings.center_x;
  mouse.y = settings.center_y;

  backgrounds.length = 0;
  createBackgrounds();
}

const loop = () => {
  requestAnimationFrame(loop);
  ctx.globalCompositeOperation = `normal`;
  ctx.fillStyle = backgrounds[settings.background];
  ctx.fillRect(0, 0, settings.canvas_w, settings.canvas_h);

  ctx.globalCompositeOperation = `lighter`;
  orbsList.forEach(e => e.refresh());

  ctx.fillStyle = `rgb(100, 100, 100)`;
  ctx.font = '16px Arial';
  ctx.fillText(
    'Press "s" to switch backgound',
    10,
    settings.canvas_w - 50
  );
}


registerEventHandlers();
resize();
createStardust();
loop();