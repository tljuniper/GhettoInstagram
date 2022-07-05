{ system ? builtins.currentSystem }:
let
  nixpkgs = import <nixpkgs> { };
  pkgs = import <nixpkgs> {
    config = { allowUnfree = true; };
    overlays = [ (import ./overlay.nix) ];
    inherit system;
  };
in rec {
  inherit (pkgs) vinstagram;

  dev-shell = pkgs.mkShell {
    buildInputs =
      with pkgs; [
        python3Packages.black
        python3Packages.flask
        python3Packages.pillow
      ];
    };
}
