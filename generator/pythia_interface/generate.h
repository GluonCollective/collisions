#ifndef COLLISIONS_GENERATE_H_
#define COLLISIONS_GENERATE_H_

#include <iostream>
#include "Pythia8/Pythia.h"

/* Main function */
int main(int argc, char **argv);

namespace collisions{
namespace output {
/* Given an event, an id to identify this event, and three files to save the
 * particle, mothers and daughters; saves the information of event into the
 * corresponding files. */
void save_event(const Pythia8::Event &event,
                int event_id,
                std::ofstream &particles, std::ofstream &mothers,
                std::ofstream &daughters);
}
}

#endif

