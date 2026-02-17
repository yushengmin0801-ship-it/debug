const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const overlay = document.getElementById('start-overlay');

let width, height;
let platforms = [];
let player = { x: 0, y: 0, scaleY: 1, jumpForce: 0 };
let gameActive = false;
let score = 0;
let isPressing = false;
let pressTime = 0;

function init() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    
    platforms = [
        { x: width/4, y: height * 0.7, w: 80, h: 40, color: '#FF9A9E' },
        { x: width/4 + 150, y: height * 0.7, w: 80, h: 40, color: '#A18CD1' }
    ];
    
    player.x = platforms[0].x;
    player.y = platforms[0].y - 20;
    score = 0;
    scoreEl.innerText = score;
    draw();
}

function draw() {
    ctx.clearRect(0,0,width,height);
    
    // Draw platforms
    platforms.forEach(p => {
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x - p.w/2, p.y, p.w, p.h);
        // Fake 3D
        ctx.fillStyle = 'rgba(0,0,0,0.1)';
        ctx.fillRect(p.x - p.w/2, p.y + p.h, p.w, 10);
    });
    
    // Draw player
    ctx.fillStyle = '#667eea';
    ctx.save();
    ctx.translate(player.x, player.y);
    ctx.scale(1, player.scaleY);
    ctx.fillRect(-15, -30, 30, 30);
    ctx.restore();
}

function jump() {
    const force = Math.min(pressTime / 10, 15);
    const targetX = player.x + force * 20;
    
    let t = 0;
    const startX = player.x;
    const startY = player.y;
    
    const jumpAnim = setInterval(() => {
        t += 0.05;
        player.x = startX + force * 20 * t;
        player.y = startY - (force * 20 * t - 5 * t * t * 50); // Simple parabola
        
        if (player.y >= startY) {
            player.y = startY;
            clearInterval(jumpAnim);
            checkLand();
        }
        draw();
    }, 20);
}

function checkLand() {
    const target = platforms[1];
    if (Math.abs(player.x - target.x) < target.w / 2) {
        score++;
        scoreEl.innerText = score;
        generateNext();
    } else {
        alert('游戏结束！得分: ' + score);
        init();
    }
}

function generateNext() {
    const last = platforms[1];
    platforms.shift();
    const nextX = last.x + 100 + Math.random() * 150;
    platforms.push({
        x: nextX,
        y: height * 0.7,
        w: 60 + Math.random() * 40,
        h: 40,
        color: '#' + Math.floor(Math.random()*16777215).toString(16)
    });
    
    // Smooth camera move (simple)
    const offset = last.x - width/4;
    platforms.forEach(p => p.x -= offset);
    player.x -= offset;
    draw();
}

overlay.addEventListener('mousedown', () => { isPressing = true; pressTime = 0; });
overlay.addEventListener('mouseup', () => { 
    if(isPressing) { 
        isPressing = false; 
        overlay.classList.add('hidden');
        jump(); 
    } 
});

// Touch support
overlay.addEventListener('touchstart', (e) => { e.preventDefault(); isPressing = true; pressTime = 0; });
overlay.addEventListener('touchend', (e) => { 
    if(isPressing) { 
        isPressing = false; 
        overlay.classList.add('hidden');
        jump(); 
    } 
});

setInterval(() => { if(isPressing) { pressTime += 10; player.scaleY = Math.max(0.6, 1 - pressTime/2000); draw(); } }, 10);

init();
