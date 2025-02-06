<?php

/**
 * Script to create a new book section with proper template and structure
 */

if ($argc < 2) {
    die("Usage: composer create-section <section-name>\n");
}

$sectionName = $argv[1];
$template = <<<EOT
# {TITLE}

## Overview

{OVERVIEW_CONTENT}

## Main Content

{MAIN_CONTENT}

## Key Points

- Point 1
- Point 2
- Point 3

## References

{REFERENCES}
EOT;

$sectionPath = "sections/{$sectionName}.md";

if (file_exists($sectionPath)) {
    die("Error: Section already exists\n");
}

file_put_contents($sectionPath, $template);
echo "Created new section: {$sectionPath}\n"; 