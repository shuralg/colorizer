/*
script.js

*/

// Create DOM elements

var canvas = document.createElement("canvas");
const SIZE = 400;
canvas.width = canvas.height = SIZE - 2;
//canvas.style.position = 'fixed';

var submit_button = document.createElement("button");
submit_button.appendChild(document.createTextNode('Colorize'));

var clear_button = document.createElement("button");
clear_button.appendChild(document.createTextNode('Clear'));

var message =  document.createElement('p');

var img = new Image(SIZE, SIZE)
const src = img.src

// Draw on canvas

var ctx = canvas.getContext("2d");

ctx.lineWidth = 2;
ctx.lineJoin="round";
ctx.miterLimit=1;
ctx.lineCap='round';

var scrollX = 0;
var scrollY = 0;
var mouse;

function getX(event) {
    var offsetOfBox = canvas.getBoundingClientRect();
    return event.clientX - offsetOfBox.left;
};

function getY(event) {
    var offsetOfBox = canvas.getBoundingClientRect();
    return event.clientY - offsetOfBox.top;
};

function draw(event) {
    ctx.lineTo(getX(event), getY(event));
    ctx.stroke();
    ctx.moveTo(getX(event), getY(event));
}

function stop() {
    canvas.removeEventListener('mousemove', draw);
    canvas.removeEventListener('mouseout', draw);
    canvas.removeEventListener('mouseup', stop);
}

canvas.addEventListener('mousedown',(event)=>{
    ctx.beginPath();
    ctx.moveTo(getX(event), getY(event));
    ctx.lineTo(getX(event)+.1, getY(event));
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(getX(event)+.1, getY(event));
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseout', draw);
    canvas.addEventListener('mouseup', stop);
});

// Clear canvas

clear_button.addEventListener('click', () => {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    img.style.visibility='hidden';
    message.innerHTML='';
});

// Send request to server

submit_button.addEventListener('click', () => {
    var img_ins = canvas.toDataURL();

    fetch('http://127.0.0.1:5000/image',{
        method:'POST',
        body: JSON.stringify({image:img_ins}),
        headers:{'Content-Type':'application/json'}
    })
    .then(res=>res.blob())
    .then(function(myBlob) {
          var image = URL.createObjectURL(myBlob);
          img.src = image;
          img.style.visibility='visible';

    })
    .catch(err => {
        message.innerHTML = '<span style="color:red">Error</span><br/>'
        console.log(err);
    });
});
//
//function isImageBlank(image) {
//    let blank = document.createElement('canvas');
//    blank.width = blank.height = SIZE;
//    return blank.toDataURL()===image;
//}

// Add all DOM elements to document body

div = document.createElement("div");
div.appendChild(img);
div.appendChild(canvas);
img.style.position = 'absolute';
canvas.style.position = 'relative';
document.body.appendChild(div)

document.body.appendChild(submit_button);
document.body.appendChild(clear_button);
document.body.appendChild(message);
