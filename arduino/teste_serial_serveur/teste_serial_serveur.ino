
void setup() {
  // put your setup ode here, to run one:
  Serial.begin(9600);
  
}

void loop() {
  // put your main ode here, to run repeatedly:
  char recu [10] = "";
  int i=0; 
  while(Serial.available()){
    recu [i] = Serial.read();
    i++;
  }

  //Serial.println(recu);
  if(strcmp(recu, "10") == 0){ //eteindre les lampes
    Serial.println("OK10");
    
    
  }else if(strcmp(recu, "11") == 0){ //allumer les lampes
    
    Serial.println("OK11");
  }else if(strcmp(recu, "12") == 0){ //etat des lampes
    Serial.println("OK12");
  }else if(strcmp(recu, "20") == 0){ //fermer les portes
    Serial.println("OK20");
  }else if(strcmp(recu, "21") == 0){ //ouvrir les portes
    Serial.println("OK21");
  }else if(strcmp(recu, "22") == 0){ //statut des portes
    Serial.println("OK22");
  }else{
    //Serial.println("rien");
  }

  
  delay(1000);
}
