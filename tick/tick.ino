volatile boolean state = false;
volatile boolean discard = false;
unsigned long t1 = 0; // newest
unsigned long t2 = 0; // oldest
unsigned long lastMillis = 0;
unsigned long waitUntil = 200;

void setup()
{
  Serial.begin(9600);
  pinMode(2, INPUT);
  digitalWrite(2, HIGH);
  pinMode(3, INPUT);
  digitalWrite(3, HIGH);
  attachInterrupt(0, hit, FALLING);
  attachInterrupt(1, noise, FALLING);
}

void loop()
{
  if (discard) {
    discard = false;
    t1 = 0;
    t2 = 0;
    waitUntil = millis() + 200;
  }
  
  if (state) {
    state = false;
    
    if (millis() < lastMillis) {
      t1 = 0;
      t2 = 0;
      waitUntil = 200;
      lastMillis = millis();
      return;
    } else {
      lastMillis = millis();
    }
    
    if (millis() < waitUntil)
      return;
    
    if (t2 == 0) {
      t2 = millis();
    } else if (t1 == 0) {
      t1 = millis();
    } else {
      unsigned long oldest_time = t1 - t2;
      t2 = t1;
      t1 = millis();
      unsigned long newest_time = t1 - t2;
      if (oldest_time > newest_time)
        Serial.print("0");
      else
        Serial.print("1");
    }
  }
}

void hit()
{
  state = true;
}

void noise()
{
  discard = true;
}
