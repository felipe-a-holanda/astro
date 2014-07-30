var N_PLANETS = 10;






var astrodata = [270.19161263919415,
 156.66910596055087,
 258.27841602351646,
 226.15491825893162,
 348.0305671295551,
 346.0961336010487,
 254.28556418232944,
 263.02162450185193,
 275.32194810249837,
 219.204351083496];

load_astrodata();
 
function load_astrodata(){
    $.get( "_calc_planets", function( d ) {
    astrodata = d;
    //$( ".result" ).html( data );
    console.log( astrodata );
    //callback();
    // fully load every image, then call the start function
    loadAllImages(start);
    
});
    
}

var data;



var asc = 180;

function calc_x_pos(){
    var planet_x = [];
    for(i=0;i<N_PLANETS;i++){
        planet_x.push(pos_x(asc,astrodata.result.planets[i].angle));
    }
    return planet_x;
}
function calc_y_pos(){
    var planet_y = [];
    for(i=0;i<N_PLANETS;i++){
        planet_y.push(pos_y(asc,astrodata.result.planets[i].angle));
    }
    return planet_y;
}
 




function a_diff(x,y){
    return Math.min(360 - Math.abs(x - y), Math.abs(x - y));
}


function pos_x(a0,a){
    x = x0 + r*Math.cos(Math.PI*(a0+a)/180.0);
    return x;
}
function pos_y(a0,a){
    y = y0 - r*Math.sin(Math.PI*(a0+a)/180.0);
    return y;
}





var width = 720;
var height = 720;
var glyph_width = 40;
var glyph_height = 40;

var x0 = width/2;
var y0 = height/2;
var r = 350







var planets = { 0: 'sun', 1:'moon', 2:'mercury', 3:'venus', 4:'mars', 5:'jupiter', 6:'saturn', 7:'uranus', 8:'neptune', 9:'pluto'};





var stage = new Kinetic.Stage({
    container: 'container',
    width: width,
    height: height
});
var layer = new Kinetic.Layer();
stage.add(layer);

var bk = new Kinetic.Rect({
    x: 0,
    y: 0,
    width: stage.getWidth(),
    height: stage.getHeight(),
    fill: "white"
});
layer.add(bk);



// put the paths to your images in imageURLs
var imageURLs = [];
for(i=0;i<10;i++){
    imageURLs.push("static/img/planets/"+planets[i]+".svg");
}



var imagesOK = 0;
var imgs = [];



function loadAllImages(callback) {
    for (var i = 0; i < imageURLs.length; i++) {
        var img = new Image();
        imgs.push(img);
        img.onload = function () {
            imagesOK++;
            if (imagesOK >= imageURLs.length) {
                callback();
            }
        };
        img.onerror = function () {
            alert("image load failed");
        }
        img.crossOrigin = "anonymous";
        img.src = imageURLs[i];
    }
}

function draw_planets(){
    for (var i = 0; i < imgs.length; i++) {
        var img = new Kinetic.Image({
            x: planet_x[i] - glyph_width/2,
            y: planet_y[i] - glyph_height/2,
            width: glyph_width,
            height: glyph_height,
            image: imgs[i],
            draggable: false
        });
        layer.add(img);
    }
}

function draw_aspects(){
    for(i=0;i<10;i++){
        for(j=i+1;j<10;j++){
            a = a_diff(astrodata.result.planets[i].angle,astrodata.result.planets[j].angle);
            
            orb = 10;
            harmonic_aspects =  [0,60,120];
            disharmonic_aspects =  [90,180];
            color='blue';
            aspect = false;
            
            for(k=0;k<harmonic_aspects.length;k++){
                if (a>harmonic_aspects[k] - orb && a<harmonic_aspects[k] + orb){
                    aspect = true;
                    color='blue';
                }
            }
            
            for(k=0;k<disharmonic_aspects.length;k++){
                if (a>disharmonic_aspects[k] - orb && a<disharmonic_aspects[k] + orb){
                    aspect = true;
                    color='red';
                }
            }
            
            
            if (aspect){
                var line = new Kinetic.Line({
                    id: i+'_'+j,
                    points: [planet_x[i], planet_y[i], planet_x[j], planet_y[j]],
                    stroke: color,
                    strokeWidth: 2,
                    lineCap: 'round',
                    lineJoin: 'round'
                });
                layer.add(line);
            }
            
            
            
        }
    }
    
}



function start() {
    // the imgs[] array holds fully loaded images
    // the imgs[] are in the same order as imageURLs[]

    // make each image into a draggable Kinetic.Image
    
    var circle = new Kinetic.Circle({
      radius: r,
      x:x0,
      y:y0,
      fill: 'white',
      stroke: 'grey'
    });
    
    layer.add(circle);
    
    
    
    var day = 0;
    
    planet_x = calc_x_pos();
    planet_y = calc_y_pos();
    draw_aspects();
    draw_planets();
    
    
    layer.draw();
    
    //para ir pro futuro ou passado
    //$('#container').bind('mousewheel', function(event) {
        //event.preventDefault();
        //event.stopPropagation();
        //var deltaY=event.deltaY;
        //day += deltaY;
        //console.log(day);
        //layer.draw();
    //});
    
    //salva como imagem
    //stage.toDataURL({
    //            callback: function(dataUrl) {
    //            window.open(dataUrl);
    //            },
    //            mimeType: 'image/png',
    //            quality: 0.9
    //        });
}
