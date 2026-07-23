#!/bin/bash
# organizer.sh
# Archives the current grades.csv with a timestamp, resets the workspace
# with a fresh empty grades.csv, and logs the action to organizer.log.

ARCHIVE_DIR="archive"
SOURCE_FILE="grades.csv"
LOG_FILE="organizer.log"

# 1. Check if the archive directory exists; create it if it does not
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created archive directory: $ARCHIVE_DIR"
fi

# 2. Make sure there is actually a grades.csv to archive
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' not found. Nothing to archive."
    exit 1
fi

# 3. Generate a timestamp string
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# 4. Build the new archived filename (e.g., grades_20251105-170000.csv)
NEW_FILENAME="grades_${TIMESTAMP}.csv"

# 5. Move the original file into the archive directory with its new name
mv "$SOURCE_FILE" "$ARCHIVE_DIR/$NEW_FILENAME"

# 6. Reset the workspace: create a fresh, empty grades.csv
touch "$SOURCE_FILE"

# 7. Log the archiving details (appended, so the log accumulates over time)
echo "$TIMESTAMP | Original: $SOURCE_FILE | Archived as: $ARCHIVE_DIR/$NEW_FILENAME" >> "$LOG_FILE"

echo "Archived '$SOURCE_FILE' as '$ARCHIVE_DIR/$NEW_FILENAME'."
echo "A fresh, empty '$SOURCE_FILE' has been created."
echo "Logged to '$LOG_FILE'."
