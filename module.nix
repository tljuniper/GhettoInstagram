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
  };

  config = (mkIf cfg.enable {
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

        script = ''
          FLASK_APP=app.py FLASK_ENV=DEBUG flask run
        '';
      };
    })
}