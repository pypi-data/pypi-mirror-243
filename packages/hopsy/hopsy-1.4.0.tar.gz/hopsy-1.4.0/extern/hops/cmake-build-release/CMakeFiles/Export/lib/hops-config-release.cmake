#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "hops" for configuration "Release"
set_property(TARGET hops APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(hops PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libhops.so"
  IMPORTED_SONAME_RELEASE "libhops.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS hops )
list(APPEND _IMPORT_CHECK_FILES_FOR_hops "${_IMPORT_PREFIX}/lib/libhops.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
