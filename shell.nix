{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
    python311Packages.beautifulsoup4
    python311Packages.customtkinter
    python311Packages.requests
    python311Packages.tkinter
  ];
}