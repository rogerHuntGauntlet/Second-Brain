<?php

/**
 * Script to prepare content for pull request
 */

// Run all checks first
system('composer check');

// Get current branch name
$branch = trim(shell_exec('git branch --show-current'));

// Get section name from branch
$sectionName = str_replace('content/', '', $branch);

// Create PR template
$prBody = "## Content Change: $sectionName\n\n";
$prBody .= "- [ ] Content maintains academic & professional tone\n";
$prBody .= "- [ ] Writing is direct and clear\n";
$prBody .= "- [ ] Narrative flow is maintained\n";

// Show next steps
echo "\nReady to submit!\n";
echo "1. Review the changes in your section\n";
echo "2. Create a PR on GitHub\n";
echo "3. Copy the following into your PR description:\n\n";
echo $prBody; 