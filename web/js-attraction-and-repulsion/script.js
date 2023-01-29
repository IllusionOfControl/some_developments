const cnv = document.querySelector(`canvas`);
const ctx = cnv.getContext(`2d`);

const config = {
  dotMinRad: 5,
  dotMaxRad: 20,
  sphereRad: 400,
  bigDotRad: 45,
  mouseSize: 160,
  massFactor: 0.002,
  defColor: `rgba(250, 10, 30, 0.9)`,
  smooth: 0.75,
};

const settings = {
  canvas_w: 0,
  canvas_h: 0,
  center_x: 0,
  center_y: 0,
};

const mouse = {
  x: 0,
  y: 0,
  down: false,
};

let dots = []

const double_PI = 2 * Math.PI;

class Dot {
  constructor(r) {
    this.pos = { x: mouse.x, y: mouse.y };
    this.vel = { x: 0, y: 0 };
    this.rad = r || randomBetween(config.dotMinRad, config.dotMaxRad);
    this.mass = this.rad * config.massFactor;
    this.color = config.defColor;
  }

  draw(x, y) {
    this.pos.x = x || this.pos.x + this.vel.x;
    this.pos.y = y || this.pos.y + this.vel.y;
    createCircle(this.pos.x, this.pos.y, this.rad, true, this.color);
    createCircle(this.pos.x, this.pos.y, this.rad, false, config.defColor);
  }
}

const updateDots = () => {
  for (let i = 0; i < dots.length; i++) {
    let acc = { x: 0, y: 0 };

    for (let j = 0; j < dots.length; j++) {
      if (i == j) continue;
      let [a, b] = [dots[i], dots[j]];

      let delta = { x: b.pos.x - a.pos.x, y: b.pos.y - a.pos.y };
      let dist = Math.sqrt(delta.x * delta.x + delta.y * delta.y) || 1;
      let force = ((dist - config.sphereRad) / dist) * b.mass;

      if (j == 0) {
        let alpha = config.mouseSize / dist;
        a.color = `rgba(250, 10, 30, ${alpha})`;

        dist < config.mouseSize
          ? (force = (dist - config.mouseSize) * b.mass)
          : (force = a.mass);
      }

      acc.x += delta.x * force;
      acc.y += delta.y * force;
    }

    dots[i].vel.x = dots[i].vel.x * config.smooth + acc.x * dots[i].mass;
    dots[i].vel.y = dots[i].vel.y * config.smooth + acc.y * dots[i].mass;
  }

  dots.forEach((e, i) => (i == 0 ? e.draw(mouse.x, mouse.y) : e.draw()));
};

const createCircle = (x, y, rad, fill, color) => {
  ctx.fillStyle = ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, rad, 0, double_PI);
  ctx.closePath();
  fill ? ctx.fill() : ctx.stroke();
}

const randomBetween = (min, max) => {
  return Math.random() * (max - min) + min;
}

const init = () => {
  dots.push(new Dot(config.bigDotRad));
}

const resize = () => {
  settings.canvas_w = cnv.width = innerWidth;
  settings.canvas_h = cnv.height = innerHeight;
  settings.center_x = settings.canvas_w * 0.5;
  settings.center_y = settings.canvas_h * 0.5;

  mouse.x = settings.center_x;
  mouse.y = settings.center_y;
};


const registerEventHandlers = () => {
  cnv.addEventListener(`mousemove`, ({ x, y }) => { mouse.x = x; mouse.y = y});
  window.addEventListener(`mousedown`, () => {mouse.down = !mouse.down});
  window.addEventListener(`mouseup`, () => {mouse.down = !mouse.down});
  window.addEventListener(`resize`, resize);
}

const loop = () => {
  ctx.clearRect(0, 0, settings.canvas_w, settings.canvas_h);

  if (mouse.down) {
    dots.push(new Dot());
  }
  updateDots();
  dots.map((e) => (e == dots[0] ? e.draw(mouse.x, mouse.y) : e.draw()));
  window.requestAnimationFrame(loop);
};

registerEventHandlers();
resize();
init();
loop();
