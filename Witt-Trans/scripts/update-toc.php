<?php

/**
 * Script to automatically update table of contents
 */

$sections = glob("sections/*.md");
$toc = "# Table of Contents\n\n";

foreach ($sections as $section) {
    $content = file_get_contents($section);
    preg_match('/^# (.+)$/m', $content, $matches);
    
    if ($matches) {
        $title = $matches[1];
        $link = basename($section);
        $toc .= "- [$title]($link)\n";
    }
}

file_put_contents("sections/0.1_TOC.md", $toc);
echo "Table of contents updated\n"; 