let
  pkgs = import ../../nix/nixpkgs.nix {};
  rustTools = import ../../nix/rust-tools.nix {};
in rustTools.buildCachedRustPackage rec {
  stdenv = pkgs.stdenvNoCC;
  name = "ddc";
  workspace = {
    root = ../../.;
    cargoToml = "trusted/dcr-compiler/ddc/Cargo.toml";
    cargoLock = "trusted/dcr-compiler/ddc/Cargo.lock";
    members = [
      "trusted/dcr-compiler/ddc"
      "trusted/delta-data-room-api"
      "trusted/delta-attestation-api"
      "trusted/delta-gcg-driver-api"
      "trusted/delta-sql-worker-api"
      "trusted/delta-container-worker-api"
      "trusted/delta-synth-data-worker-api"
      "trusted/delta-s3-sink-worker-api"
      "trusted/delta-identity-endorsement-api"
    ];
    exclude = [
    ];
  };
  extraSourceDirectoryNames = ["build" "vendor"];
  cargoOptions = (orig: orig ++ [ "-Zavoid-dev-deps" ]);
  cargoBuildOptions = (orig: orig ++ [ "--target=x86_64-unknown-linux-gnu" ]);
  RUSTFLAGS="-C link-arg=-s";

  doCheck = false;

  PROTOC="${pkgs.protobuf}/bin/protoc";
  PROTOC_INCLUDE="${pkgs.protobuf}/include";

  buildInputs = with pkgs; [
    cacert
    protobuf
    openssl
    cmake
    zlib
    clang
    gcc
    pkgconfig
  ];
  LIBCLANG_PATH="${pkgs.llvmPackages.libclang.lib}/lib";
  # FORTIFY requires __memcpy_chk which we don't have access to
  hardeningDisable = [ "fortify" ];
}
