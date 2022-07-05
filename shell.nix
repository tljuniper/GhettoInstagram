with import <nixpkgs> {};

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    numpy
    jupyter
    flask
    pillow
  ]);

in pkgs.mkShell {
  buildInputs = [ pythonEnv ];
}
