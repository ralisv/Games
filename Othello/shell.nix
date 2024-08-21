{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3Packages.unicurses
  ];
  shellHook = ''
    python3.12 -m xonsh
    exit
  '';
}
