{ system ? builtins.currentSystem }:
let
  pkgs = import <nixpkgs> {
    config = { allowUnfree = true; };
    overlays = [ (import ./overlay.nix) ];
    inherit system;
  };
in rec {
  inherit (pkgs) vinstagram;

  dev-shell = pkgs.mkShell {
    inputsFrom = with pkgs; [
        vinstagram
        python3Packages.black
      ];
    };
}
