String[] zeilen;
int n = 0;

                //dead, recovered, vaccinated, gesund, infected
color[] colors = {0, #008200, #781AFF, #00FF00, #FF0307, #E80206, #CE0205, #B70407,
                  #C6600C, #EA8D00, #FF9A03, #FEFF03, #FFEB08, #FEFF03, #FEFF03, #FEFF03, #FEFF03, #FEFF03};

void setup(){
  background(0,0,255);
  //noStroke();
  stroke(0);
  
  frameRate(30);
  
  zeilen = loadStrings("2018-11-17_00-36-07.txt");
  
  while(true){
    int[] num = int(split(zeilen[n],'*'));
    n++;
    if(num.length == 4) break;
  }
  
  size(1020,1020);
}

void draw(){
  
  if(n < zeilen.length-1){
    
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
    
    n++;
  }
  
  
}
