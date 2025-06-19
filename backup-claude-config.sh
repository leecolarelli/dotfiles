#!/bin/bash

# Claude Code Configuration Backup Script
# This script backs up Claude Code settings while sanitizing sensitive data

set -e

SOURCE_FILE="$HOME/.claude.json"
BACKUP_FILE="$(dirname "$0")/claude-code.json"

if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Claude settings file not found at $SOURCE_FILE"
    exit 1
fi

echo "Backing up Claude Code configuration..."
echo "Source: $SOURCE_FILE"
echo "Destination: $BACKUP_FILE"

# Use jq to process the JSON and sanitize sensitive data
jq '
# Remove sensitive data and replace with placeholders
del(.userID) |
del(.oauthAccount.accountUuid) |
del(.oauthAccount.emailAddress) |
del(.oauthAccount.organizationUuid) |
del(.oauthAccount.organizationName) |
if .oauthAccount then .oauthAccount.emailAddress = "###EMAIL###" else . end |
if .oauthAccount then .oauthAccount.organizationName = "###ORGANIZATION###" else . end |

# Remove command history from all projects
.projects = (.projects | to_entries | map({
    key: "###PROJECT_PATH###",
    value: (.value | 
        del(.history) |
        del(.lastSessionId) |
        del(.exampleFiles) |
        del(.exampleFilesGeneratedAt)
    )
}) | from_entries) |

# Sanitize MCP server credentials
.mcpServers = (.mcpServers | to_entries | map({
    key: .key,
    value: (.value |
        if .env then
            .env = (.env | to_entries | map({
                key: .key,
                value: (if (.key | test("TOKEN|PASSWORD|SECRET|KEY"; "i")) then "###" + .key + "###" else .value end)
            }) | from_entries)
        else . end
    )
}) | from_entries) |

# Remove other potentially sensitive or unnecessary data
del(.cachedChangelog) |
del(.changelogLastFetched) |
del(.subscriptionNoticeCount) |
del(.hasAvailableSubscription) |
del(.fallbackAvailableWarningThreshold) |
del(.lastReleaseNotesSeen) |
del(.firstStartTime) |
del(.numStartups)
' "$SOURCE_FILE" > "$BACKUP_FILE"

echo "✅ Backup completed successfully!"
echo "Sensitive data has been sanitized and replaced with placeholders."
echo "Remember to update the placeholders when restoring on a new machine."