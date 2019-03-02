#!/bin/bash

iso_file="${1}"
mount_directory="/mnt/iso"

if [[ ! -f "${iso_file}" ]]; then
  echo "File ${iso_file} doesnt exist"
  exit 1; fi

if [[ ! -d "${mount_directory}" ]]; then
  echo "Creating ${mount_directory}"
  mkdir -p "${mount_directory}"; fi

if cat /proc/mounts | grep "${mount_directory}"; then
  echo "Umounting previous iso from ${mount_directory}"
  umount "${mount_directory}"; fi

mount -o loop "${iso_file}" "${mount_directory}"
