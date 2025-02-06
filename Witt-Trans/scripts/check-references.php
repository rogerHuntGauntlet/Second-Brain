<?php

/**
 * Script to validate cross-references between sections
 */

$sections = glob("sections/*.md");
$references = [];
$errors = [];

// First pass: collect all section headers
foreach ($sections as $section) {
    $content = file_get_contents($section);
    preg_match_all('/^#{1,6} (.+)$/m', $content, $matches);
    $references[basename($section)] = $matches[1];
}

// Second pass: check references
foreach ($sections as $section) {
    $content = file_get_contents($section);
    preg_match_all('/\[([^\]]+)\]\(([^\)]+)\)/', $content, $matches);
    
    foreach ($matches[2] as $reference) {
        if (strpos($reference, '.md') !== false) {
            $refFile = basename($reference);
            if (!file_exists("sections/$refFile")) {
                $errors[] = "$section: Invalid reference to $refFile";
            }
        }
    }
}

if ($errors) {
    echo "Reference validation errors:\n";
    foreach ($errors as $error) {
        echo "- $error\n";
    }
    exit(1);
}

echo "Reference validation passed\n"; 