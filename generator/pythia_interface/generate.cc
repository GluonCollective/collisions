#include "generate.h"
#include "config.h"

#include <vector>
#include <string>
#include <stdexcept>

namespace cfg = collisions::config;
namespace opt = collisions::output;

int main(int argc, char **argv) {
  std::string process;
  int seed;
  int n_events;

  bool run = cfg::ConfigureProgram(process, seed, n_events, argc, argv);

  if (!run) {
    return 0;
  }

  std::ofstream particles;
  std::ofstream mothers;
  std::ofstream daughters;

  particles.open("/tmp/particles.csv");
  mothers.open("/tmp/mothers.csv");
  daughters.open("/tmp/daughters.csv");

  particles << "event,id,PdgCode,E,Px,Py,Pz,Vx,Vy,Vz,Vt\n";
  mothers << "event,id,mother_id\n";
  daughters << "event,id,daughter_id\n";

  // Set up Pythia
  Pythia8::Pythia pythia;
  cfg::Configuration config;
  cfg::ConfigurePythia(pythia, config.GetOptionConfig(process), seed);

  for (int i_event(0); i_event < n_events; ++i_event) {
    pythia.next();
    opt::save_event(pythia.event, i_event, particles, mothers, daughters);
  }

  particles.close();
  mothers.close();
  daughters.close();

  return 0;
}

void opt::save_event(const Pythia8::Event &event,
                     int event_id,
                     std::ofstream &particles,
                     std::ofstream &mothers,
                     std::ofstream &daughters) {
  for (int i(0); i < event.size(); i++) {
    const auto &part = event[i];
    particles << event_id << ",";
    particles << i << ",";
    particles << part.id() << ",";
    particles << part.e() << ",";
    particles << part.px() << "," << part.py() << "," << part.pz() << ",";
    particles << part.xProd() << "," << part.yProd() << "," << part.zProd()
              << "," << part.tProd();
    particles << "\n";

    for (auto &&m: part.motherList())
      mothers << event_id << "," << i << "," << m << "\n";

    for (auto &&d: part.daughterList())
      daughters << event_id << "," << i << "," << d << "\n";
  }
}




