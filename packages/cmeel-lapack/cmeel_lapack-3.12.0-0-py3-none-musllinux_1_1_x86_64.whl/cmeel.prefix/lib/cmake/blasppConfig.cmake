cmake_minimum_required( VERSION 3.15 )

set( blaspp_use_openmp "ON" )
set( blaspp_use_cuda   "ON" )

include( CMakeFindDependencyMacro )
if (blaspp_use_openmp)
    find_dependency( OpenMP )
endif()

# Export private variables used in LAPACK++.
set( blaspp_defines         "-DFORTRAN_ADD_" )
set( blaspp_libraries       "-lblas;OpenMP::OpenMP_CXX" )

set( blaspp_cblas_defines   "" )
set( blaspp_cblas_found     "" )
set( blaspp_cblas_include   "" )
set( blaspp_cblas_libraries "" )

include( "${CMAKE_CURRENT_LIST_DIR}/blasppTargets.cmake" )
