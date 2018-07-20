{ pkgs ?  import ./nixpkgs {}
, stdenv ? pkgs.stdenv
} :

import ./tvm.nix {
  inherit pkgs stdenv;
  tvmCmakeFlagsEx = "-DUSE_LLVM=ON";
  tvmDepsEx = with pkgs; [ llvm_5 clang_5 openblas ];
  tvmCmakeConfig = ''
    set(USE_CUDA OFF)
    set(USE_ROCM OFF)
    set(USE_OPENCL OFF)
    set(USE_METAL OFF)
    set(USE_VULKAN OFF)
    set(USE_OPENGL OFF)
    set(USE_RPC ON)
    set(USE_GRAPH_RUNTIME ON)
    set(USE_GRAPH_RUNTIME_DEBUG ON)
    set(USE_LLVM ON)
    set(USE_BLAS openblas)
    set(USE_RANDOM OFF)
    set(USE_NNPACK OFF)
    set(USE_CUDNN OFF)
    set(USE_CUBLAS OFF)
    set(USE_MIOPEN OFF)
    set(USE_MPS OFF)
    set(USE_ROCBLAS OFF)
    set(USE_SORT ON)
  '';
}

