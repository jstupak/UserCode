#ifndef PARTICLE_H
#define PARTICLE_H

#include <vector>
#include "TLorentzVector.h"

class Particle:TLorentzVector{
public:

  Particle();

  vector<Particle*> daughters;
  Particle* mother;

  int charge;

};

#endif 
