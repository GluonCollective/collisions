#include "config.h"

#include "yaml-cpp/yaml.h"

namespace po = boost::program_options;
namespace cfg = collisions::config;

cfg::Configuration::Configuration(std::string config_file) {
  YAML::Node config_yaml = YAML::LoadFile(config_file);

  for (auto node_it = config_yaml.begin(); node_it != config_yaml.end();
       node_it++) {
    const std::string name = (*node_it).first.as<std::string>();
    const auto config_strings = (*node_it).second.as<std::vector<std::string>>();
    process_options_[name] = config_strings;
  }

  valid_process_.reserve(process_options_.size());

  for (auto &&x : process_options_) valid_process_.push_back(x.first);
}

std::string cfg::Configuration::GetAvailableOptionsForDocs() const {
  std::string docs;
  for (auto &&p : GetValidProcesses()) docs += p + ", ";

  if (docs.size() < 2)
    throw std::runtime_error("There are no options available.");

  return docs.substr(0, docs.size() - 2);
}

bool cfg::Configuration::IsValidOption(const std::string &option) const {
  const std::vector<std::string> &valid_processes = GetValidProcesses();
  return std::find(valid_processes.begin(), valid_processes.end(), option) !=
         valid_processes.end();
}

bool cfg::ConfigureProgram(std::string &process, int &seed, int &n_events,
                          int argc, char **argv) {
  const cfg::Configuration config;

  po::options_description options("Program options");
  options.add_options()("help", "Produce help message.")(
      "available-processes", "Lists the available processes.")(
      "process", po::value<std::string>(&process)->default_value("SoftQCD"),
      ("Set generation process. Available processes: " +
       config.GetAvailableOptionsForDocs() + ".")
          .c_str())
      //  +
      ("seed", po::value<int>(&seed)->default_value(13),
       "Set seed to generate the events.")(
          "events", po::value<int>(&n_events)->default_value(1),
          "Set how many events should be generated.");

  po::variables_map variables_map;
  po::store(po::parse_command_line(argc, argv, options), variables_map);
  po::notify(variables_map);

  if (variables_map.count("help")) {
    std::cout << options << "\n";
    return false;
  }

  if (variables_map.count("available-processes")) {
    std::cout << config.GetAvailableOptionsForDocs() << std::endl;
    return false;
  }

  if (!cfg::Configuration().IsValidOption(process)) {
    throw po::validation_error(po::validation_error::invalid_option_value);
  }

  std::cout << "Process: " << process << "\n";
  std::cout << "Seed: " << seed << "\n";
  std::cout << "Number of events: " << n_events << "\n";
  
  return true;
}

void cfg::ConfigurePythia(Pythia8::Pythia &pythia,
                          const std::vector<std::string> &processes, int seed) {
  pythia.readString("Beams:eCM = 13000.");

  for (auto &&proc : processes) {
    pythia.readString(proc + "= on");
  }

  pythia.readString("Random:setSeed = on");
  pythia.readString("Random:seed = " + std::to_string(seed));
  pythia.init();
}