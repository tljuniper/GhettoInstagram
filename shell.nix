with import <nixpkgs> {};

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    flask
    jupyter
    numpy
    pillow
  ]);

in pkgs.mkShell {
  buildInputs = [ pythonEnv ];
}
