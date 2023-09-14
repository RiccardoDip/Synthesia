import oscP5.*;
import netP5.*;
  
OscP5 oscP5;

NetAddress receiver;

void setup() {

  /* start oscP5, listening for incoming messages at port 12000 */
  
  oscP5 = new OscP5( this , 32000 );
}



/* by default incoming osc message are forwarded to the oscEvent method. */

void oscEvent(OscMessage theOscMessage) {
  print("Message received");
  if(theOscMessage.checkAddrPattern("/change") == true) {
    if(theOscMessage.checkTypetag("f")) {
      float OSCvalue = theOscMessage.get(0).floatValue();
      println("value: " + OSCvalue);
    }
  }
}
