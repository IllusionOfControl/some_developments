const cnv  = document.querySelector('canvas');
const ctx  = cnv.getContext('2d');

const settings = {
  canvas_w: 0,
  canvas_h: 0,
  center_x: 0,
  center_y: 0,
};

const config = {
  hue         : 0,
  bgFillColor : `rgba(50, 50, 50, .01)`,
  dirsCount   : 3,
  stepToTurn  : 20,
  dotSize     : 2,
  dotsCount   : 300,
  dotVelocity : 2,
  distance    : 200,
  gradientLen : 5,
};

let dirsList = [];
let dotsList = [];

class Dot {
  constructor() {
    this.pos     = {x: settings.center_x, y: settings.center_y};
    this.dir     = config.dirsCount === 6 ? (Math.random() * 3 | 0) * 2
                  : Math.random() * config.dirsCount | 0;
    this.step    = 0;
  }

  redrawDot() {
    let xy       = Math.abs(this.pos.x - settings.center_x) + Math.abs(this.pos.y - settings.center_y);
    let makeHue  = (config.hue + xy / config.gradientLen ) % 360;
    let color    = `hsl(${ makeHue }, 100%, 50%)`;
    let blur     = config.dotSize - Math.sin(xy / 8) * 2;
    let size     = config.dotSize;// - Math.sin(xy / 9) * 2 + Math.sin(xy / 2);
    let x        = this.pos.x - size / 2;
    let y        = this.pos.y - size / 2;

    drawRect(color, x, y, size, size, color, blur, `lighter`);
  }

  moveDot() {
    this.step++;
    this.pos.x += dirsList[this.dir].x * config.dotVelocity;
    this.pos.y += dirsList[this.dir].y * config.dotVelocity;
  }

  changeDir() {
    if (this.step % config.stepToTurn === 0) {
      this.dir     = Math.random() > 0.5 ? (this.dir + 1) % config.dirsCount : (this.dir + config.dirsCount - 1) % config.dirsCount;
    }
  }

  killDot(id) {
    let percent = Math.random() * Math.exp(this.step / config.distance);
    if (percent > 100) {
      dotsList.splice(id, 1);
    }
  }
}

const drawRect = (color, x, y, w, h, shadowColor, shadowBlur, gco) => {
  ctx.globalCompositeOperation = gco;
  ctx.shadowColor = shadowColor || `black`;
  ctx.shadowBlur  = shadowBlur  || 1;
  ctx.fillStyle   = color;
  ctx.fillRect(x, y, w, h);
}


const createDirs = () => {
  for (let i = 0 ; i < 360 ; i+= 360 / config.dirsCount) {
    let x = Math.cos(i * Math.PI / 180);
    let y = Math.sin(i * Math.PI / 180);
    dirsList.push({x: x, y: y});
  }    
}
  

const addDot = () => {
  if (dotsList.length < config.dotsCount && Math.random() > .8) {
    dotsList.push( new Dot() );
    config.hue = (config.hue + 1) % 360 ;
  }
}

const refreshDots = () => {
  dotsList.forEach( (i, id) => { 
    i.redrawDot();
    i.moveDot();
    i.changeDir();
    i.killDot(id)
  } );
}

const resize = () => {
  settings.canvas_w = cnv.width = innerWidth;
  settings.canvas_h = cnv.height = innerHeight;
  settings.center_x = settings.canvas_w * 0.5;
  settings.center_y = settings.canvas_h * 0.5;
};

const loop = () => {
  drawRect(config.bgFillColor, 0, 0, settings.canvas_w, settings.canvas_h, 0, 0, `normal`);
  addDot();
  refreshDots();

  requestAnimationFrame(loop);
}

window.addEventListener(`resize`, resize);

createDirs();
resize();
loop();