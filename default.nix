{ buildPythonApplication, setuptools, flask, pillow, black }:

buildPythonApplication rec {
  name = "ghetto_instagram";
  version = "1.0";
  src = ./.;
  propagatedBuildInputs = [ flask pillow setuptools ];

  doCheck = true;
  checkInputs = [ black ];
  preCheck = ''
    black --check --diff ./**/*.py
  '';
}
