<?php

/**
 * Script to validate document structure against guidelines
 */

$sections = glob("sections/*.md");
$errors = [];

foreach ($sections as $section) {
    $content = file_get_contents($section);
    
    // Check for required sections
    if (!preg_match('/^# /', $content)) {
        $errors[] = "$section: Missing main title";
    }
    
    if (!preg_match('/## Overview/', $content)) {
        $errors[] = "$section: Missing overview section";
    }
    
    // Add more structural checks as needed
}

if ($errors) {
    echo "Structure validation errors:\n";
    foreach ($errors as $error) {
        echo "- $error\n";
    }
    exit(1);
}

echo "Structure validation passed\n"; 