#ifndef COLLISIONS_CONFIG_H_
#define COLLISIONS_CONFIG_H_
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "Pythia8/Pythia.h"
#include "boost/program_options.hpp"

namespace collisions {
namespace config {
/* Given the variables to save the process, the seed and the number of events;
 * and the main program number of arguments and argument values, configures the
 * generation of the events. */
bool ConfigureProgram(std::string &process, int &seed, int &n_events, int argc,
                     char **argvm);

/* Configuration for the physics processes */
class Configuration {
 public:
  /* Loads the possible configurations from the yaml file. The file should be
   * located in the /event_api folder, so the user can change it easily. */
  explicit Configuration(std::string config_file = "/pythia_config/processes.yml");

  /* Returns a list with the valid physics processes. */
  const std::vector<std::string> &GetValidProcesses() const {
    return valid_process_;
  };

  /* Given an option, returns the corresponding configuration on pythia */
  const std::vector<std::string> &GetOptionConfig(
      const std::string &option) const {
    return process_options_.at(option);
  }

  /* Returns the list of possible configurations that can be used, formatted in
   * a single string to be displayed in the documentation. */
  std::string GetAvailableOptionsForDocs() const;

  /* Given an option for the physics process, returns if it valid. */
  bool IsValidOption(const std::string &option) const;

 private:
  /* Map with the name of the option in the program and the corresponding
   * option on pythia */
  std::map<std::string, std::vector<std::string>> process_options_;

  /* List of the valid options */
  std::vector<std::string> valid_process_;
};

/* Sets the configuration of a pythia instance, using the vector with the list
 * of the strings to be turned on and the seed. */
void ConfigurePythia(Pythia8::Pythia &pythia,
                     const std::vector<std::string> &processes, int seed);

}  // namespace config
}  // namespace collisions

#endif