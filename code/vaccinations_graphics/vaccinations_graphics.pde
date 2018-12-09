// Press space to start/pause simulation //<>//

String[] zeilen;
int n = 0;

                //dead, recovered, vaccinated, gesund, infected
color[] colors = {0, #008200, #781AFF, #00FF00, #FF0307, #E80206, #CE0205, #B70407,
                  #C6600C, #EA8D00, #FF9A03, #FEFF03, #FFEB08, #FEFF03, #FEFF03, #FEFF03, #FEFF03, #FEFF03};

boolean start = false;
int offset = 0;

void setup(){
  background(0,0,255);
  //noStroke();
  stroke(0);
  
  frameRate(35);
  
  //zeilen = loadStrings("2018-11-17_14-14-51.txt");
  //zeilen = loadStrings("2018-11-19_14-00-24.txt");
  //zeilen = loadStrings("2018-11-19_14-13-45.txt"); //
  zeilen = loadStrings("2018-11-18_21-40-24.txt");
  zeilen = loadStrings("2018-11-23_09-06-27.txt");
  
  while(true){
    int[] num = int(split(zeilen[n],'*'));
    n++;
    if(num.length == 4) break;
  }
  
  offset = n - 1;
  
  size(1220,1220);
}

void draw(){
  
  if(n < zeilen.length-1 && n > offset){
    
    int[] num = int(split(zeilen[n],' '));
    
    int l = int(sqrt(num.length - 0.1 - 1)) + 1;
    int w = (width - 20)/l;
    
    for(int i = 0; i < l; i++){
      for(int j = 0; j < l; j++){
        
        int idx = j*l + i;
        if(idx >= num.length) break;
        
        fill(colors[ num[idx]+4 ]);
        rect(10 + w*i, 10 + w*j, w, w);
        
      }
    }
    
    if(start){
      println("day: " + (n-offset));
      n++;
    }
  }
  
  
}

void keyReleased(){
  if(key == '2') n += 1; //2
  if(key == '1') n -= 1; //1
  
  if(keyCode == 39) n += 10; //Right arrow
  if(keyCode == 37) n -= 10; //Left arrow
  if(keyCode == 32) start = !start; //Space
  
}
