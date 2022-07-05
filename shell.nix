with import <nixpkgs> {};

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    numpy
    jupyter
  ]);

in pkgs.mkShell {
  buildInputs = [ pythonEnv ];
}
