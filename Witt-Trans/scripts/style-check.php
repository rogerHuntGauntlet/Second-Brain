<?php

/**
 * Script to check content against style guidelines
 */

$styleGuide = file_get_contents("organizing/tone-style-guidelines.md");
$sections = glob("sections/*.md");
$errors = [];

foreach ($sections as $section) {
    $content = file_get_contents($section);
    
    // Check for passive voice (simple example)
    if (preg_match('/\b(is|are|was|were|be|been|being)\s+\w+ed\b/i', $content, $matches)) {
        $errors[] = "$section: Possible passive voice detected: '{$matches[0]}'";
    }
    
    // Check for overly complex sentences (simple example)
    if (preg_match('/[^.!?]+[.!?]\s*(?=[A-Z])/i', $content, $matches)) {
        foreach ($matches as $sentence) {
            if (str_word_count($sentence) > 40) {
                $errors[] = "$section: Overly complex sentence detected (>40 words)";
            }
        }
    }
    
    // Add more style checks as needed
}

if ($errors) {
    echo "Style validation errors:\n";
    foreach ($errors as $error) {
        echo "- $error\n";
    }
    exit(1);
}

echo "Style validation passed\n"; 