with import <nixpkgs> {};

python3Packages.buildPythonApplication rec {
  name = "ghetto_instagram";
  version = "1.0";
  src = ./.;
  propagatedBuildInputs = with python3Packages; [ flask setuptools ];

  doCheck = true;
  checkInputs = with python3Packages; [ black ];
  preCheck = ''
    black --check --diff ./**/*.py
  '';
}
