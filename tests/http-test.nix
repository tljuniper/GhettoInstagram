with import <nixpkgs> {};

pkgs.nixosTest {
  name = "vinstagram-http-test";

  nodes.testhost = {
    imports = [
      ../module.nix
    ];
    nixpkgs.config.allowUnfree = true;
    services.vinstagram = {
      enable = true;
      storageDir = "/var/lib/vinstagram";
    };
    systemd.tmpfiles.rules = [ "d '/var/lib/vinstagram' 0777 - vinstagram" ];
    environment.systemPackages = [ pkgs.httpie pkgs.imagemagick ];
  };

  testScript = ''
    start_all()

    testhost.wait_for_open_port(5000)
    testhost.wait_for_unit("vinstagram.service")

    testhost.succeed(
      "convert -size 1000x1000 xc:white white.png && http --check-status -f POST :5000/users/user1/photos cv@white.png"
    )

    testhost.succeed("http --check-status :5000/feed users==user1")
  '';
}
