import oscP5.*; //<>//
import netP5.*;

OscP5 oscP5;

NetAddress receiver;

float counter;

void setup() {
  size(400, 400);

  oscP5 = new OscP5( this, 12000 );

  receiver = new NetAddress( "192.168.178.103", 32000 );

  counter = 0.0;
}

void draw() {
  background(0);
}

void mousePressed() {
  /* send a message on mouse pressed */
  OscMessage myMessage = new OscMessage("/Interpolation");
  myMessage.add(counter);
  oscP5.send(myMessage, receiver);
  println("Message sent!");
  println("Cycling");
  counter += 1.0;
  counter %= 9;
}
