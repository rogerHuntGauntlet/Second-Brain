<?php

/**
 * Script to help expand outline sections into prose
 */

if ($argc < 2) {
    die("Usage: composer expand <section-file>\n");
}

$sectionFile = $argv[1];
$content = file_get_contents($sectionFile);

// Create a new file for the prose version
$proseFile = str_replace('.md', '_prose.md', $sectionFile);

// Add header indicating this is the prose version
$header = "# Chapter 1: From Language to Transaction – A New Framework\n\n";
$header .= "_Prose version expanded from outline_\n\n";

file_put_contents($proseFile, $header);

echo "Created prose file: $proseFile\n";
echo "Ready to expand sections using /expand command\n"; 