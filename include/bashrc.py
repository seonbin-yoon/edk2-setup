bash_func = (
    "# section_edk2\n"
    "export EDK_TOOLS_PATH=!Edk2path/edk2/BaseTools\n"
    "function setup_edk2() {\n"
    "    local current_dir=$(pwd)\n"
    "    cd !Edk2path/edk2\n"
    "    source edksetup.sh BaseTools\n"
    "    cd $current_dir\n"
    "    clear\n"
    "}\n"
    "\n"
    "setup_edk2\n"
    "# section_end\n"
)
