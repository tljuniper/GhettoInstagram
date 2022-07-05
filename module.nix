{ config, lib, pkgs, ... }:

with lib;

let
  cfg = config.services.vinstagram;
in {
  options.services.vinstagram = {
    enable = mkOption {
      type = types.bool;
      default = false;
      description = ''
        If enabled, it runs.
      '';
    };
    storageDir = mkOption {
      type = types.str;
      description = ''
        This is the path to store images in.
      ''
    }
  };

  config = (mkIf cfg.enable {
    nixpkgs.overlays = [
      (import ./overlay.nix)
    ];
    users.extraGroups.vinstagram = { };
    users.extraUsers.vinstagram= {
      isSystemUser = true;
      description = "Vinstagram user";
      createHome = true;
      home = "/var/lib/vinstagram";
      group = "vinstagram";
    };

    systemd.services.vinstagram = {
      description = "Vinstagram Service";
      wantedBy = [ "multi-user.target" ];
      after = [ "network.target" ];

      serviceConfig.Restart = "always";
      serviceConfig.User = "vinstagram";
      path = with pkgs; [ python3Packages.flask python3Packages.pillow ];

      script = ''
        export STORAGE_DIR=${cfg.storageDir}
        exec ${pkgs.vinstagram}/bin/run
      '';
    };
  });
}
