//3D Spectrogram with Microphone Input
//Modified by kylejanzen 2011 - https://kylejanzen.wordpress.com
//Based on script wwritten by John Locke 2011 - http://gracefulspoon.com

//Output .DXF file at any time by pressing "r" on the keyboard

import processing.net.*;
import processing.dxf.*;
import ddf.minim.effects.*;
import ddf.minim.analysis.*;
import ddf.minim.*;

import oscP5.*;
OscP5 o;


JPGEncoderV2 jpg_v2;
Client myClient;
FFT fftLin;
FFT fftLog;

Waveform audio3D;

LowPassSP lowPass;
Minim minim;
AudioInput microphone;
AudioOutput out;
AudioListener listener;

boolean record;

PFont font;

float camzoom;
float maxX = 0;
float maxY = 0;
float maxZ = 0;
float minX = 0;
float minY = 0;
float minZ = 0;
int gate = 0;
PImage screen;
float interpolation;
char controlCharF, controlCharI;

void setup()
{
  frameRate(10);
  size(500, 300, P3D); //screen proportions
  o = new OscP5(this, 32000);

  noStroke();

  minim = new Minim(this);
  lowPass = new LowPassSP(200, 44100);
  out = minim.getLineOut();

  jpg_v2 = new JPGEncoderV2();
  microphone = minim.getLineIn(Minim.STEREO, 4096); //repeat the song

  background(255);

  fftLog = new FFT(microphone.bufferSize(), microphone.sampleRate());
  fftLog.logAverages(1, 2);  //adjust numbers to adjust spacing;
  float w = float (width/fftLog.avgSize());
  float x = w;
  float y = 0;
  float z = 50;
  float radius = 10;

  audio3D = new Waveform(x, y, z, radius);

  myClient = new Client(this, "127.0.0.1", 5000);

  screen = get();

  interpolation = 0.0;

  controlCharF = 'f';
  controlCharI = 'i';
}
void draw()
{
  background(0);
  directionalLight(126, 126, 126, sin(radians(frameCount)), cos(radians(frameCount)), 1);
  ambientLight(102, 102, 102);



  if (frameCount>200)
  {
    for (int i = 0; i < fftLog.avgSize(); i++) {
      float zoom = 1;
      float jitter = (fftLog.getAvg(i)*2);
      //println(jitter);
      PVector foc = new PVector(audio3D.x+jitter, audio3D.y+jitter, 0);
      PVector cam = new PVector(zoom, zoom, -zoom);
      camera(foc.x+cam.x+50, foc.y+cam.y+50, foc.z+cam.z, foc.x, foc.y, foc.z, 0, 0, 1);
    }
  }
  //play the song
  fftLog.forward(microphone.mix);

  audio3D.update();
  audio3D.textdraw();
  audio3D.plotTrace();

  screen = get();
  screen.resize(500, 0);
}

void clientEvent(Client someClient) {
  println("Message received");

  char dataIn = char(someClient.readBytes())[0];

  try {
    println("Getting image from frame");

    if (screen != null) {
      // println(screen.width);
      // println(screen.height);
      // println("Encoding");
      byte[] encoded = jpg_v2.encode(screen, 0.5F);
      if (encoded.length > 32768) {
        encoded = subset(encoded, 0, 32768);
      }

      println("encoded length: " + encoded.length);

      println("Writing to server");
      if (dataIn == controlCharF)
        myClient.write(encoded);
      else if (dataIn == controlCharI)
        myClient.write(str(interpolation));
    }
  }
  catch (IOException e) {
    // Ignore failure to encode
    println("IOException");
    e.printStackTrace();
  }
}





void stop()
{
  // always close Minim audio classes when you finish with them
  microphone.close();
  // always stop Minim before exiting
  minim.stop();
  super.stop();
}
class Waveform
{
  float x, y, z;
  float radius;

  PVector[] pts = new PVector[fftLog.avgSize()];

  PVector[] trace = new PVector[0];

  Waveform(float incomingX, float incomingY, float incomingZ, float incomingRadius)
  {
    x = incomingX;
    y = incomingY;
    z = incomingZ;
    radius = incomingRadius;
  }
  void update()
  {
    plot();
  }
  void plot()
  {
    for (int i = 0; i < fftLog.avgSize(); i++)
    {
      int w = int(width/fftLog.avgSize());

      x = i*w;
      y = frameCount*5;
      z = height/4-fftLog.getAvg(i)*4; //change multiplier to reduces height default '10'

      stroke(0);
      point(x, y, z);
      pts[i] = new PVector(x, y, z);
      //increase size of array trace by length+1
      trace = (PVector[]) expand(trace, trace.length+1);
      //always get the next to last
      trace[trace.length-1] = new PVector(pts[i].x, pts[i].y, pts[i].z);
    }
  }
  void textdraw()
  {
    for (int i =0; i<fftLog.avgSize(); i++) {
      pushMatrix();
      translate(pts[i].x, pts[i].y, pts[i].z);
      rotateY(PI/2);
      rotateZ(PI/2);

      fill(255, 200);
      text(round(fftLog.getAvg(i)*100), 0, 0, 0);
      popMatrix();
    }
  }
  void plotTrace()
  {
    stroke(255, 80);
    int inc = fftLog.avgSize();

    for (int i=1; i<trace.length-inc; i++)
    {
      if (i%inc != 0)
      {
        beginShape(TRIANGLE_STRIP);

        float value = (trace[i].z*100);
        float m = map(value, -500, 20000, 0, 255);
        fill(m*2, 125, -m*2, 140);
        vertex(trace[i].x, trace[i].y, trace[i].z);
        vertex(trace[i-1].x, trace[i-1].y, trace[i-1].z);
        vertex(trace[i+inc].x, trace[i+inc].y, trace[i+inc].z);
        vertex(trace[i-1+inc].x, trace[i-1+inc].y, trace[i-1+inc].z);
        endShape(CLOSE);
      }
    }
  }
}

void oscEvent(OscMessage theMsg) {
  if (theMsg.checkAddrPattern("/Interpolation")==true) {
    interpolation = theMsg.get(0).floatValue();
    println("Interpolation: " + interpolation);
  }
}
